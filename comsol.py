import numpy as np
import time


class Parameters:
    """This class is used to store parameters regarding the borehole and heat extraction from it."""
    
    def __init__(self, L_borehole, D_borehole, borehole_spacing, num_years, E_annual, monthly_fractions=None):
        if monthly_fractions is not None:
            if not len(monthly_fractions) == 12:
                raise ValueError("There must be 12 monthly fractions.")
            if np.abs(np.sum(monthly_fractions)-1) > 1e-6:
                raise ValueError("The sum of monthly fractions must be 1.")
        self.L_borehole = L_borehole
        self.D_borehole = D_borehole
        self.borehole_spacing = borehole_spacing
        self.num_years = num_years
        self.E_annual = E_annual
        self.monthly_fractions = monthly_fractions

    def __str__(self):
        if self.monthly_fractions is not None:
            monthly_fractions = ", ".join([str(fraction) for fraction in self.monthly_fractions]).replace(".0", "")
            return f"Parameters(L_borehole={self.L_borehole} m, D_borehole={int(1000*self.D_borehole)} mm, borehole_spacing={self.borehole_spacing} m, num_years={self.num_years}, E_annual={str(round(self.E_annual,3))} MWh, monthly_fractions=[{monthly_fractions}])"
        return f"Parameters(L_borehole={self.L_borehole} m, D_borehole={int(1000*self.D_borehole)} mm, borehole_spacing={self.borehole_spacing} m, num_years={self.num_years}, E_annual={str(round(self.E_annual,3))} MWh)"


def init_model(client, params, geology):
    """Constructs a new COMSOL model using the specified client having the specified parameters for simulating heat extraction from the specified geology."""
    
    # Creates a new COMSOL model.
    
    print("Creating a new COMSOL model...", end=" ")
    
    tic = time.time()
    
    python_model = client.create("Model")
    
    model = python_model.java
    
    model.component().create("comp1", True)
    
    model.component("comp1").geom().create("geom1", 3)
    
    model.component("comp1").mesh().create("mesh1")
    
    toc = time.time()
    
    print(f"Done in {str(np.round(toc-tic,3))} seconds.")
    
    # Sets up model parameters.
    
    print("Setting up model parameters...", end=" ")
    
    tic = time.time()
    
    model.param().set("H_model", f"{geology.thickness}[m]")
    
    model.param().set("D_borehole", f"{params.D_borehole}[m]")
    model.param().set("L_borehole", f"{params.L_borehole}[m]")
    model.param().set("borehole_spacing", f"{params.borehole_spacing}[m]")
    
    for layer in geology.layers:
        model.param().set(f"h_{layer.tag}", f"{layer.thickness}[m]")
        model.param().set(f"k_{layer.tag}", f"{layer.material.k}[W/(m*K)]")
        model.param().set(f"Cp_{layer.tag}", f"{layer.material.Cp}[J/(kg*K)]")
        model.param().set(f"rho_{layer.tag}", f"{layer.material.rho}[kg/m^3]")
    
    model.param().set("T_surface", f"{geology.T_surface}[degC]")
    model.param().set("q_geothermal", f"{geology.q_geothermal}[W/m^2]")
    
    model.param().set("E_annual", f"{params.E_annual}[MWh]")
    
    model.param().set("A_wall", "pi*D_borehole*L_borehole")
    
    toc = time.time()
    
    print(f"Done in {str(np.round(toc-tic,3))} seconds.")
    
    # Creates initial temperature function.
    
    print("Creating functions...", end=" ")
    
    tic = time.time()

    pieces = []
    
    start = "0"
    for i in range(len(geology.layers)):
        start += f"-h_{geology.layers[i].tag}"
        if i == 0:
            end = "0"
            T_offset = "T_surface"
            expr = f"{T_offset}-q_geothermal/k_{geology.layers[i].tag}*z"
        else:
            if i - 1 == 0:
                h_offset = f"h_{geology.layers[i-1].tag}"
            else:
                h_offset += f"+h_{geology.layers[i-1].tag}"
            T_offset += f"+q_geothermal/k_{geology.layers[i-1].tag}*h_{geology.layers[i-1].tag}"
            end += f"-h_{geology.layers[i-1].tag}"
            expr = f"{T_offset}-q_geothermal/k_{geology.layers[i].tag}*(z+{h_offset})"
        pieces.append([start, end, expr])
        
    model.func().create("pw1", "Piecewise")
    model.func("pw1").set("funcname", "T_initial")
    model.func("pw1").set("arg", "z")
    model.func("pw1").set("extrap", "interior")
    model.func("pw1").set("pieces", pieces)
    model.func("pw1").set("argunit", "m")
    model.func("pw1").set("fununit", "K")
    
    # Creates a monthly profile function if monthly fractions have been defined.
    
    if params.monthly_fractions is not None:
        
        pieces = []
        
        for i in range(12):
            pieces.append([f"{i}/12", f"{i+1}/12", f"{params.monthly_fractions[i]}"])
            
        model.func().create("pw2", "Piecewise")
        model.func("pw2").set("funcname", "monthly_fractions")
        model.func("pw2").set("arg", "t")
        model.func("pw2").set("extrap", "periodic")
        model.func("pw2").set("pieces", pieces)
        model.func("pw2").set("argunit", "a")
        model.func("pw2").set("fununit", "1")

    toc = time.time()
    
    print(f"Done in {str(np.round(toc-tic,3))} seconds.")
    
    # Creates model geometry.
    
    print("Creating model geometry...", end=" ")

    tic = time.time()

    split_geology = geology.split(-params.L_borehole)
    
    tags = []
    
    for layer in split_geology.layers:
        tags.append(f"layer{len(tags)+1}")
        model.component("comp1").geom("geom1").create(tags[-1], "Block")
        model.component("comp1").geom("geom1").feature(tags[-1]).label(f"{layer.name} Block")
        model.component("comp1").geom("geom1").feature(tags[-1]).set("pos", ["-0.5*borehole_spacing", "-0.5*borehole_spacing", f"{layer.z_to}"])
        model.component("comp1").geom("geom1").feature(tags[-1]).set("size", ["0.5*borehole_spacing", "0.5*borehole_spacing", f"{layer.thickness}"])

    model.component("comp1").geom("geom1").create("borehole_cylinder", "Cylinder")
    model.component("comp1").geom("geom1").feature("borehole_cylinder").label("Borehole Cylinder")
    model.component("comp1").geom("geom1").feature("borehole_cylinder").set("pos", ["0", "0", "-L_borehole"])
    model.component("comp1").geom("geom1").feature("borehole_cylinder").set("r", "0.5*D_borehole")
    model.component("comp1").geom("geom1").feature("borehole_cylinder").set("h", "L_borehole")
    
    model.component("comp1").geom("geom1").create("dif1", "Difference")
    model.component("comp1").geom("geom1").feature("dif1").selection("input").set(tags)
    model.component("comp1").geom("geom1").feature("dif1").selection("input2").set("borehole_cylinder")
    
    model.component("comp1").geom("geom1").run()
    
    toc = time.time()
    
    print(f"Done in {str(np.round(toc-tic,3))} seconds.")
    
    # Creates selections.
    
    print("Creating selections...", end=" ")
    
    tic = time.time()

    model.component("comp1").selection().create("ground_surface_selection", "Box")
    model.component("comp1").selection("ground_surface_selection").label("Ground Surface Selection")
    model.component("comp1").selection("ground_surface_selection").set("entitydim", "2")
    model.component("comp1").selection("ground_surface_selection").set("zmin", "0")
    model.component("comp1").selection("ground_surface_selection").set("zmax", "0")
    model.component("comp1").selection("ground_surface_selection").set("condition", "allvertices")
    
    model.component("comp1").selection().create("bottom_boundary_selection", "Box")
    model.component("comp1").selection("bottom_boundary_selection").label("Bottom Boundary Selection")
    model.component("comp1").selection("bottom_boundary_selection").set("entitydim", "2")
    model.component("comp1").selection("bottom_boundary_selection").set("zmin", f"{-geology.thickness}")
    model.component("comp1").selection("bottom_boundary_selection").set("zmax", f"{-geology.thickness}")
    model.component("comp1").selection("bottom_boundary_selection").set("condition", "allvertices")
    
    model.component("comp1").selection().create("sweep_domains_selection", "Box")
    model.component("comp1").selection("sweep_domains_selection").label("Sweep Domains Selection")
    model.component("comp1").selection("sweep_domains_selection").set("entitydim", "3")
    model.component("comp1").selection("sweep_domains_selection").set("zmin", "-L_borehole")
    model.component("comp1").selection("sweep_domains_selection").set("zmax", "0")
    model.component("comp1").selection("sweep_domains_selection").set("condition", "allvertices")
    
    model.component("comp1").selection().create("borehole_wall_selection", "Cylinder")
    model.component("comp1").selection("borehole_wall_selection").label("Borehole Wall Selection")
    model.component("comp1").selection("borehole_wall_selection").set("top", "0")
    model.component("comp1").selection("borehole_wall_selection").set("bottom", "-L_borehole")
    model.component("comp1").selection("borehole_wall_selection").set("r", "0.5*D_borehole")
    model.component("comp1").selection("borehole_wall_selection").set("condition", "allvertices")
    model.component("comp1").selection("borehole_wall_selection").set("entitydim", "2")
    
    model.component("comp1").selection().create("borehole_edge_selection", "Cylinder")
    model.component("comp1").selection("borehole_edge_selection").label("Borehole Edge Selection")
    model.component("comp1").selection("borehole_edge_selection").set("entitydim", "1")
    model.component("comp1").selection("borehole_edge_selection").set("top", "0")
    model.component("comp1").selection("borehole_edge_selection").set("bottom", "-L_borehole")
    model.component("comp1").selection("borehole_edge_selection").set("r", "1[mm]")
    model.component("comp1").selection("borehole_edge_selection").set("condition", "allvertices")
    model.component("comp1").selection("borehole_edge_selection").set("pos", ["0", "-0.5*D_borehole", "0"])

    model.component("comp1").selection().create("collar_edge_selection", "Cylinder")
    model.component("comp1").selection("collar_edge_selection").label("Collar Edge Selection")
    model.component("comp1").selection("collar_edge_selection").set("entitydim", "1")
    model.component("comp1").selection("collar_edge_selection").set("r", "0.5*D_borehole")
    model.component("comp1").selection("collar_edge_selection").set("top", "0")
    model.component("comp1").selection("collar_edge_selection").set("bottom", "0")
    model.component("comp1").selection("collar_edge_selection").set("condition", "allvertices")
    
    layer_tags = []

    for layer in geology.layers:
        tag = f"layer{len(layer_tags)+1}_selection"
        model.component("comp1").selection().create(tag, "Box")
        model.component("comp1").selection(tag).label(f"{layer.name} Selection")
        model.component("comp1").selection(tag).set("entitydim", "3")
        model.component("comp1").selection(tag).set("zmin", f"{layer.z_to}")
        model.component("comp1").selection(tag).set("zmax", f"{layer.z_from}")
        model.component("comp1").selection(tag).set("condition", "allvertices")
        layer_tags.append(tag)

    toc = time.time()
    
    print(f"Done in {str(np.round(toc-tic,3))} seconds.")

    # Creates mesh.

    print("Creating mesh...", end=" ")
    
    tic = time.time()
    
    model.component("comp1").mesh("mesh1").create("collar_edge", "Edge")
    model.component("comp1").mesh("mesh1").feature("collar_edge").label("Collar Edge Mesh")
    model.component("comp1").mesh("mesh1").feature("collar_edge").selection().named("collar_edge_selection")

    model.component("comp1").mesh("mesh1").feature("collar_edge").create('size1', 'Size');
    model.component("comp1").mesh("mesh1").feature("collar_edge").feature("size1").set('custom', 'on')
    model.component("comp1").mesh("mesh1").feature("collar_edge").feature("size1").set('hmaxactive', "on")
    model.component("comp1").mesh("mesh1").feature("collar_edge").feature("size1").set('hmax', '5[mm]')
    model.component("comp1").mesh("mesh1").feature("collar_edge").feature("size1").set('hminactive', "on")
    model.component("comp1").mesh("mesh1").feature("collar_edge").feature("size1").set('hmin', '5[mm]')
    
    model.component("comp1").mesh("mesh1").create("ground_surface_mesh", "FreeTri")
    model.component("comp1").mesh("mesh1").feature("ground_surface_mesh").label("Ground Surface Mesh")
    model.component("comp1").mesh("mesh1").feature("ground_surface_mesh").selection().named("ground_surface_selection")
    model.component("comp1").mesh("mesh1").feature("ground_surface_mesh").set("method", "del")

    model.component("comp1").mesh("mesh1").feature("ground_surface_mesh").create('size1', 'Size');
    model.component("comp1").mesh("mesh1").feature("ground_surface_mesh").feature("size1").set('hauto', "1")
    model.component("comp1").mesh("mesh1").feature("ground_surface_mesh").feature("size1").set('custom', 'on')
    #model.component("comp1").mesh("mesh1").feature("ground_surface_mesh").feature("size1").set('hminactive', "on")
    #model.component("comp1").mesh("mesh1").feature("ground_surface_mesh").feature("size1").set('hmin', '1[mm]')
    #model.component("comp1").mesh("mesh1").feature("ground_surface_mesh").feature("size1").set('hmaxactive', "on")
    #model.component("comp1").mesh("mesh1").feature("ground_surface_mesh").feature("size1").set('hmax', '5[m]')
    model.component("comp1").mesh("mesh1").feature("ground_surface_mesh").feature("size1").set('hgradactive', "on")
    model.component("comp1").mesh("mesh1").feature("ground_surface_mesh").feature("size1").set('hgrad', "1.1")
    
    model.component("comp1").mesh("mesh1").create("swept_mesh", "Sweep")
    model.component("comp1").mesh("mesh1").feature("swept_mesh").label("Swept Mesh")
    model.component("comp1").mesh("mesh1").feature("swept_mesh").selection().named("sweep_domains_selection")

    model.component("comp1").mesh("mesh1").feature("swept_mesh").create('dis1', 'Distribution')
    model.component("comp1").mesh("mesh1").feature("swept_mesh").feature("dis1").set('type', 'predefined')
    model.component("comp1").mesh("mesh1").feature("swept_mesh").feature("dis1").set('method', 'geometric')
    model.component("comp1").mesh("mesh1").feature("swept_mesh").feature("dis1").set('symmetric', "on")
    model.component("comp1").mesh("mesh1").feature("swept_mesh").feature("dis1").set('elemcount', "30")
    model.component("comp1").mesh("mesh1").feature("swept_mesh").feature("dis1").set('elemratio', "10")
    
    model.component("comp1").mesh("mesh1").create("tetrahedral_mesh", "FreeTet")

    model.component("comp1").mesh("mesh1").feature("tetrahedral_mesh").create('size1', 'Size')
    model.component("comp1").mesh("mesh1").feature("tetrahedral_mesh").feature("size1").set('hauto', "1")
    model.component("comp1").mesh("mesh1").feature("tetrahedral_mesh").feature("size1").set('custom', 'on')
    #model.component("comp1").mesh("mesh1").feature("tetrahedral_mesh").feature("size1").set('hminactive', "on")
    #model.component("comp1").mesh("mesh1").feature("tetrahedral_mesh").feature("size1").set('hmin', '1[mm]')
    #model.component("comp1").mesh("mesh1").feature("tetrahedral_mesh").feature("size1").set('hmaxactive', "on")
    #model.component("comp1").mesh("mesh1").feature("tetrahedral_mesh").feature("size1").set('hmax', '10[m]')
    model.component("comp1").mesh("mesh1").feature("tetrahedral_mesh").feature("size1").set('hgradactive', "on")
    model.component("comp1").mesh("mesh1").feature("tetrahedral_mesh").feature("size1").set('hgrad', "1.1")
    
    model.component("comp1").mesh("mesh1").run()
    
    toc = time.time()
    
    print(f"Done in {str(np.round(toc-tic,3))} seconds.")

    num_elems = model.component("comp1").mesh("mesh1").stat().getNumElem()
    
    print(f"Number of elements: {num_elems:,}")

    # Creates physics.
    
    print("Creating physics...", end=" ")

    tic = time.time()

    model.component("comp1").physics().create("ht", "HeatTransfer", "geom1")
    model.component("comp1").physics("ht").prop("ShapeProperty").set("order_temperature", "1")
    
    model.component("comp1").physics("ht").feature("init1").set("Tinit", "T_initial(z)")
    
    for i, layer in enumerate(geology.layers):
        tag = f"solid{i+1}"
        if i > 0:
            model.component("comp1").physics("ht").create(tag, "SolidHeatTransferModel", 3)
            model.component("comp1").physics("ht").feature(tag).selection().named(layer_tags[i])
        model.component("comp1").physics("ht").feature(tag).label(f"{layer.name} Solid")
        model.component("comp1").physics("ht").feature(tag).set("k_mat", "userdef")
        model.component("comp1").physics("ht").feature(tag).set("k", [[f"k_{layer.tag}"], ["0"], ["0"], ["0"], [f"k_{layer.tag}"], ["0"], ["0"], ["0"], [f"k_{layer.tag}"]])
        model.component("comp1").physics("ht").feature(tag).set("rho_mat", "userdef")
        model.component("comp1").physics("ht").feature(tag).set("rho", f"rho_{layer.tag}")
        model.component("comp1").physics("ht").feature(tag).set("Cp_mat", "userdef")
        model.component("comp1").physics("ht").feature(tag).set("Cp", f"Cp_{layer.tag}")
    
    model.component("comp1").physics("ht").create("ground_surface_temperature", "TemperatureBoundary", 2)
    model.component("comp1").physics("ht").feature("ground_surface_temperature").label("Ground Surface Temperature")
    model.component("comp1").physics("ht").feature("ground_surface_temperature").selection().named("ground_surface_selection")
    model.component("comp1").physics("ht").feature("ground_surface_temperature").set("T0", "T_surface")
    
    model.component("comp1").physics("ht").create("geothermal_heat_flux", "HeatFluxBoundary", 2)
    model.component("comp1").physics("ht").feature("geothermal_heat_flux").label("Geothermal Heat Flux")
    model.component("comp1").physics("ht").feature("geothermal_heat_flux").selection().named("bottom_boundary_selection")
    model.component("comp1").physics("ht").feature("geothermal_heat_flux").set("q0", "q_geothermal")
    model.component("comp1").physics("ht").feature("geothermal_heat_flux").set("materialType", "solid")
    
    model.component("comp1").physics("ht").create("borehole_wall_heat_flux", "HeatFluxBoundary", 2)
    model.component("comp1").physics("ht").feature("borehole_wall_heat_flux").label("Borehole Wall Heat Flux")
    model.component("comp1").physics("ht").feature("borehole_wall_heat_flux").selection().named("borehole_wall_selection")
    model.component("comp1").physics("ht").feature("borehole_wall_heat_flux").set("q0", "-Q_extraction/A_wall")
    
    toc = time.time()
    
    print(f"Done in {str(np.round(toc-tic,3))} seconds.")
    
    # Creates operators and variables.
    
    print("Creating operators and variables...", end=" ")

    tic = time.time()

    model.component("comp1").cpl().create("borehole_wall_integration", "Integration")
    model.component("comp1").cpl("borehole_wall_integration").label("Borehole Wall Integration")
    model.component("comp1").cpl("borehole_wall_integration").set("axisym", "on")
    model.component("comp1").cpl("borehole_wall_integration").selection().geom("geom1", 2)
    model.component("comp1").cpl("borehole_wall_integration").selection().named("borehole_wall_selection")
    
    model.component("comp1").cpl().create("borehole_wall_minimum", "Minimum")
    model.component("comp1").cpl("borehole_wall_minimum").label("Borehole Wall Minimum")
    model.component("comp1").cpl("borehole_wall_minimum").selection().geom("geom1", 2)
    model.component("comp1").cpl("borehole_wall_minimum").selection().named("borehole_wall_selection")
    
    model.component("comp1").cpl().create("borehole_wall_average", "Average")
    model.component("comp1").cpl("borehole_wall_average").label("Borehole Wall Average")
    model.component("comp1").cpl("borehole_wall_average").selection().geom("geom1", 2)
    model.component("comp1").cpl("borehole_wall_average").selection().named("borehole_wall_selection")

    model.component("comp1").variable().create("var1")
    model.component("comp1").variable("var1").set("T_min", "borehole_wall_minimum(T)")
    model.component("comp1").variable("var1").set("T_ave", "borehole_wall_average(T)")
    model.component("comp1").variable("var1").set("Q_wall", "4*borehole_wall_integration(ht.ndflux)")
    
    if params.monthly_fractions is not None:
        model.component("comp1").variable("var1").set("Q_extraction", "(E_annual*monthly_fractions(t))/(1[a]/12)")
    else:
        model.component("comp1").variable("var1").set("Q_extraction", "E_annual/1[a]")
    
    toc = time.time()
    
    print(f"Done in {str(np.round(toc-tic,3))} seconds.")
    
    # Creates solution and solver.
    
    print("Creating solution and solver...", end=" ")

    tic = time.time()
    
    tlist = f"range(0,1/12,{params.num_years})"

    model.study().create("std1")

    model.study("std1").setGenPlots(False)
    model.study("std1").setGenConv(False)

    model.study("std1").create("time", "Transient")
    model.study("std1").feature("time").set("tunit", "a")
    model.study("std1").feature("time").set("tlist", tlist)

    if params.monthly_fractions is not None:
        model.study("std1").feature("time").set("usertol", "on");
        model.study("std1").feature("time").set("rtol", "1e-3");
    
    model.sol().create("sol1")
    model.sol("sol1").study("std1")
    model.sol("sol1").attach("std1")

    model.sol("sol1").create("st1", "StudyStep")

    model.sol("sol1").create("v1", "Variables")

    model.sol("sol1").create("t1", "Time")
    model.sol("sol1").feature("t1").create("d1", "Direct")
    model.sol("sol1").feature("t1").feature("d1").set("linsolver", "pardiso")
    model.sol("sol1").feature("t1").feature().remove("dDef")
    model.sol("sol1").feature("t1").feature().remove("fcDef")
    model.sol("sol1").feature("t1").set("tunit", "a")
    model.sol("sol1").feature("t1").set("tlist", tlist)
    model.sol("sol1").feature("t1").set("maxorder", "2")
    model.sol("sol1").feature("t1").set("estrat", "exclude")
    model.sol("sol1").feature("t1").set("control", "time")

    if params.monthly_fractions is not None:
        model.sol("sol1").feature("t1").set("tstepsbdf", "free")
        model.sol("sol1").feature("t1").set("initialstepbdfactive", "on")
        model.sol("sol1").feature("t1").set("initialstepbdf", "1e-6")
    else:
        model.sol("sol1").feature("t1").set("tstepsbdf", "strict")
    
    toc = time.time()
    
    print(f"Done in {str(np.round(toc-tic,3))} seconds.")

    # Evaluates the first time step.
    
    # print("Evaluating the first time step...", end=" ")

    # tic = time.time()

    # model.sol("sol1").runFromTo("st1", "v1")

    # toc = time.time()
    
    # print(f"Done in {str(np.round(toc-tic,3))} seconds.")
    
    # Adds a plot.
    
    # print("Adding a plot...", end=" ")

    # tic = time.time()

    # model.java.result().create("pg1", "PlotGroup1D")
    # model.java.result("pg1").run()
    # model.java.result("pg1").create("lngr1", "LineGraph")
    # model.java.result("pg1").feature("lngr1").selection().named("borehole_edge_selection")
    # model.java.result("pg1").feature("lngr1").set("expr", "z")
    # model.java.result("pg1").feature("lngr1").set("xdata", "expr")
    # model.java.result("pg1").feature("lngr1").set("xdataunit", "degC")
    # model.java.result("pg1").feature().duplicate("lngr2", "lngr1")
    # model.java.result("pg1").run()
    # model.java.result("pg1").feature("lngr2").set("xdataexpr", f"13.2[degC]-{gradient}[K/km]*z")
    # model.java.result("pg1").run()

    # toc = time.time()
    
    # print(f"Done in {str(np.round(toc-tic,3))} seconds.")
    
    xmi = model.sol("sol1").feature("st1").xmeshInfo()
    
    num_dofs = xmi.nDofs()
    
    print(f"Number of degrees of freedom: {num_dofs:,}")
    
    return python_model
