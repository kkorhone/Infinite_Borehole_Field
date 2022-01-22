from utils import num_to_str, time_elapsed
from geology import PorousMaterial, PorousLayer
import numpy as np
import time


class Parameters:
    """This class is used to store model parameters regarding the borehole and heat extraction from it."""

    def __init__(self, L_borehole, D_borehole, borehole_spacing, num_years, E_annual, monthly_fractions=None):
        if monthly_fractions is not None:
            if len(monthly_fractions) != 12:
                raise ValueError("There must be 12 monthly fractions.")
            if np.abs(np.sum(monthly_fractions)-1) > 1e-6:
                raise ValueError("The sum of monthly fractions must be one.")
        self.L_borehole = L_borehole
        self.D_borehole = D_borehole
        self.borehole_spacing = borehole_spacing
        self.num_years = num_years
        self.E_annual = E_annual
        self.monthly_fractions = monthly_fractions

    def __str__(self):
        descr = f"L_borehole={num_to_str(self.L_borehole)} m, D_borehole={num_to_str(self.D_borehole)} m, borehole_spacing={num_to_str(self.borehole_spacing)} m, num_years={num_to_str(self.num_years)}, E_annual={num_to_str(self.E_annual)} MWh"
        if self.monthly_fractions is not None:
            monthly_fractions = ", ".join([num_to_str(fraction) for fraction in self.monthly_fractions])
            descr += f", monthly_fractions=[{monthly_fractions}]"
        return f"Parameters({descr})"


def eval_temp(model, E_annual):
    """Evaluates the coldest mean borehole wall temperature during a simulation using the specified heat extraction."""
    tic = time.time()
    model.parameter("E_annual", f"{num_to_str(E_annual)}[MWh]")
    model.solve()
    T_ave = model.evaluate("T_ave", "degC")
    temp = np.min(T_ave)
    toc = time.time()
    print(f"time_elapsed={time_elapsed(toc-tic)}, E_annual={num_to_str(E_annual)} MWh, temp={num_to_str(temp)} K")
    return temp



def init_model(client, params, geology):
    """Constructs a new COMSOL model using the specified client having the specified parameters for simulating heat extraction from the specified geology."""

    # -------------------------------------------------------------------------
    # Creates a new COMSOL model.
    # -------------------------------------------------------------------------

    print("Creating a new COMSOL model...", end=" ")

    tic = time.time()

    model = client.create(f"Model of {geology.name}")

    model.java.component().create("comp1", True)
    model.java.component("comp1").geom().create("geom1", 3)
    model.java.component("comp1").mesh().create("mesh1")

    toc = time.time()

    print(f"Done in {time_elapsed(toc-tic)}.")

    # -------------------------------------------------------------------------
    # Sets up model parameters.
    # -------------------------------------------------------------------------

    print("Setting up model parameters...", end=" ")

    tic = time.time()

    model.java.param().set("H_model", f"{num_to_str(geology.thickness)}[m]")

    model.java.param().set("D_borehole", f"{num_to_str(params.D_borehole)}[m]")
    model.java.param().set("L_borehole", f"{num_to_str(params.L_borehole)}[m]")
    model.java.param().set("borehole_spacing", f"{num_to_str(params.borehole_spacing)}[m]")

    model.java.param().set("T_surface", f"{num_to_str(geology.T_surface)}[degC]")
    model.java.param().set("q_geothermal", f"{num_to_str(geology.q_geothermal)}[W/m^2]")

    model.java.param().set("E_annual", f"{num_to_str(params.E_annual)}[MWh]")
    model.java.param().set("A_wall", "pi*D_borehole*L_borehole")

    for layer in geology.layers:
        model.java.param().set(f"h_{layer.tag}", f"{num_to_str(layer.thickness)}[m]")
        model.java.param().set(f"k_eff_{layer.tag}", f"{num_to_str(layer.material.k)}[W/(m*K)]")
        model.java.param().set(f"Cp_eff_{layer.tag}", f"{num_to_str(layer.material.Cp)}[J/(kg*K)]")
        model.java.param().set(f"rho_eff_{layer.tag}", f"{num_to_str(layer.material.rho)}[kg/m^3]")
        if type(layer) is PorousLayer:
            model.java.param().set(f"k_fluid_{layer.tag}", f"{num_to_str(layer.material.k_fluid)}[W/(m*K)]")
            model.java.param().set(f"Cp_fluid_{layer.tag}", f"{num_to_str(layer.material.Cp_fluid)}[J/(kg*K)]")
            model.java.param().set(f"rho_fluid_{layer.tag}", f"{num_to_str(layer.material.rho_fluid)}[kg/m^3]")
            model.java.param().set(f"k_solid_{layer.tag}", f"{num_to_str(layer.material.k_matrix)}[W/(m*K)]")
            model.java.param().set(f"Cp_solid_{layer.tag}", f"{num_to_str(layer.material.Cp_matrix)}[J/(kg*K)]")
            model.java.param().set(f"rho_solid_{layer.tag}", f"{num_to_str(layer.material.rho_matrix)}[kg/m^3]")
            model.java.param().set(f"eps_{layer.tag}", f"{num_to_str(layer.material.porosity)}[1]")
            if layer.velocity > 0:
                model.java.param().set(f"v_{layer.tag}", f"{num_to_str(layer.velocity)}[m/s]")

    toc = time.time()

    print(f"Done in {time_elapsed(toc-tic)}.")

    # -------------------------------------------------------------------------
    # Creates initial temperature function.
    # -------------------------------------------------------------------------

    print("Creating functions...", end=" ")

    tic = time.time()

    pieces = []

    start = "0"
    for i in range(len(geology.layers)):
        start += f"-h_{geology.layers[i].tag}"
        if i == 0:
            end = "0"
            T_offset = "T_surface"
            expr = f"{T_offset}-q_geothermal/k_eff_{geology.layers[i].tag}*z"
        else:
            if i - 1 == 0:
                h_offset = f"h_{geology.layers[i-1].tag}"
            else:
                h_offset += f"+h_{geology.layers[i-1].tag}"
            T_offset += f"+q_geothermal/k_eff_{geology.layers[i-1].tag}*h_{geology.layers[i-1].tag}"
            end += f"-h_{geology.layers[i-1].tag}"
            expr = f"{T_offset}-q_geothermal/k_eff_{geology.layers[i].tag}*(z+{h_offset})"
        pieces.append([start, end, expr])

    model.java.func().create("pw1", "Piecewise")
    model.java.func("pw1").set("funcname", "T_initial")
    model.java.func("pw1").set("arg", "z")
    model.java.func("pw1").set("extrap", "interior")
    model.java.func("pw1").set("pieces", pieces)
    model.java.func("pw1").set("argunit", "m")
    model.java.func("pw1").set("fununit", "K")

    # -------------------------------------------------------------------------
    # Creates monthly profile function if monthly fractions have been defined.
    # -------------------------------------------------------------------------

    if params.monthly_fractions is not None:

        pieces = []

        for i in range(12):
            pieces.append([f"{i}/12", f"{i+1}/12", f"{params.monthly_fractions[i]}"])

        model.java.func().create("pw2", "Piecewise")
        model.java.func("pw2").set("funcname", "monthly_fractions")
        model.java.func("pw2").set("arg", "t")
        model.java.func("pw2").set("extrap", "periodic")
        model.java.func("pw2").set("pieces", pieces)
        model.java.func("pw2").set("argunit", "a")
        model.java.func("pw2").set("fununit", "1")

    toc = time.time()

    print(f"Done in {time_elapsed(toc-tic)}.")

    # -------------------------------------------------------------------------
    # Creates model geometry.
    # -------------------------------------------------------------------------

    print("Creating model geometry...", end=" ")

    tic = time.time()

    split_geology = geology.split(-params.L_borehole)

    tags = []

    for layer in split_geology.layers:
        tags.append(f"layer{len(tags)+1}")
        model.java.component("comp1").geom("geom1").create(tags[-1], "Block")
        model.java.component("comp1").geom("geom1").feature(tags[-1]).label(f"{layer.name}")
        model.java.component("comp1").geom("geom1").feature(tags[-1]).set("pos", ["-0.5*borehole_spacing", "-0.5*borehole_spacing", f"{layer.z_to}"])
        if geology.has_groundwater_flow:
            model.java.component("comp1").geom("geom1").feature(tags[-1]).set("size", ["borehole_spacing", "0.5*borehole_spacing", f"{layer.thickness}"])
        else:
            model.java.component("comp1").geom("geom1").feature(tags[-1]).set("size", ["0.5*borehole_spacing", "0.5*borehole_spacing", f"{layer.thickness}"])

    model.java.component("comp1").geom("geom1").create("borehole_cylinder", "Cylinder")
    model.java.component("comp1").geom("geom1").feature("borehole_cylinder").label("Borehole Cylinder")
    model.java.component("comp1").geom("geom1").feature("borehole_cylinder").set("pos", ["0", "0", "-L_borehole"])
    model.java.component("comp1").geom("geom1").feature("borehole_cylinder").set("r", "0.5*D_borehole")
    model.java.component("comp1").geom("geom1").feature("borehole_cylinder").set("h", "L_borehole")

    model.java.component("comp1").geom("geom1").create("dif1", "Difference")
    model.java.component("comp1").geom("geom1").feature("dif1").selection("input").set(tags)
    model.java.component("comp1").geom("geom1").feature("dif1").selection("input2").set("borehole_cylinder")

    model.java.component("comp1").geom("geom1").run()

    toc = time.time()

    print(f"Done in {time_elapsed(toc-tic)}.")

    # -------------------------------------------------------------------------
    # Creates selections.
    # -------------------------------------------------------------------------

    print("Creating selections...", end=" ")

    tic = time.time()

    model.java.component("comp1").selection().create("ground_surface_selection", "Box")
    model.java.component("comp1").selection("ground_surface_selection").label("Ground Surface Selection")
    model.java.component("comp1").selection("ground_surface_selection").set("entitydim", "2")
    model.java.component("comp1").selection("ground_surface_selection").set("zmin", "0")
    model.java.component("comp1").selection("ground_surface_selection").set("zmax", "0")
    model.java.component("comp1").selection("ground_surface_selection").set("condition", "allvertices")

    model.java.component("comp1").selection().create("geothermal_boundary_selection", "Box")
    model.java.component("comp1").selection("geothermal_boundary_selection").label("Bottom Boundary Selection")
    model.java.component("comp1").selection("geothermal_boundary_selection").set("entitydim", "2")
    model.java.component("comp1").selection("geothermal_boundary_selection").set("zmin", f"{-geology.thickness}")
    model.java.component("comp1").selection("geothermal_boundary_selection").set("zmax", f"{-geology.thickness}")
    model.java.component("comp1").selection("geothermal_boundary_selection").set("condition", "allvertices")

    model.java.component("comp1").selection().create("sweep_domains_selection", "Box")
    model.java.component("comp1").selection("sweep_domains_selection").label("Sweep Domains Selection")
    model.java.component("comp1").selection("sweep_domains_selection").set("entitydim", "3")
    model.java.component("comp1").selection("sweep_domains_selection").set("zmin", "-L_borehole")
    model.java.component("comp1").selection("sweep_domains_selection").set("zmax", "0")
    model.java.component("comp1").selection("sweep_domains_selection").set("condition", "allvertices")

    model.java.component("comp1").selection().create("borehole_wall_selection", "Cylinder")
    model.java.component("comp1").selection("borehole_wall_selection").label("Borehole Wall Selection")
    model.java.component("comp1").selection("borehole_wall_selection").set("top", "0")
    model.java.component("comp1").selection("borehole_wall_selection").set("bottom", "-L_borehole")
    model.java.component("comp1").selection("borehole_wall_selection").set("r", "0.5*D_borehole")
    model.java.component("comp1").selection("borehole_wall_selection").set("condition", "allvertices")
    model.java.component("comp1").selection("borehole_wall_selection").set("entitydim", "2")

    model.java.component("comp1").selection().create("borehole_edge_selection", "Cylinder")
    model.java.component("comp1").selection("borehole_edge_selection").label("Borehole Edge Selection")
    model.java.component("comp1").selection("borehole_edge_selection").set("entitydim", "1")
    model.java.component("comp1").selection("borehole_edge_selection").set("top", "0")
    model.java.component("comp1").selection("borehole_edge_selection").set("bottom", "-L_borehole")
    model.java.component("comp1").selection("borehole_edge_selection").set("r", "1[mm]")
    model.java.component("comp1").selection("borehole_edge_selection").set("condition", "allvertices")
    model.java.component("comp1").selection("borehole_edge_selection").set("pos", ["0", "-0.5*D_borehole", "0"])

    model.java.component("comp1").selection().create("collar_edge_selection", "Cylinder")
    model.java.component("comp1").selection("collar_edge_selection").label("Collar Edge Selection")
    model.java.component("comp1").selection("collar_edge_selection").set("entitydim", "1")
    model.java.component("comp1").selection("collar_edge_selection").set("r", "0.5*D_borehole")
    model.java.component("comp1").selection("collar_edge_selection").set("top", "0")
    model.java.component("comp1").selection("collar_edge_selection").set("bottom", "0")
    model.java.component("comp1").selection("collar_edge_selection").set("condition", "allvertices")

    for layer in geology.layers:
        tag = f"{layer.tag}_selection"
        model.java.component("comp1").selection().create(tag, "Box")
        model.java.component("comp1").selection(tag).label(f"{layer.name} Selection")
        model.java.component("comp1").selection(tag).set("entitydim", "3")
        model.java.component("comp1").selection(tag).set("zmin", f"{layer.z_to}")
        model.java.component("comp1").selection(tag).set("zmax", f"{layer.z_from}")
        model.java.component("comp1").selection(tag).set("condition", "allvertices")

    model.java.component("comp1").selection().create("left_boundary_selection", "Box")
    model.java.component("comp1").selection("left_boundary_selection").label("Left Boundary Selection")
    model.java.component("comp1").selection("left_boundary_selection").set("entitydim", "2")
    model.java.component("comp1").selection("left_boundary_selection").set("xmin", "-0.5*borehole_spacing")
    model.java.component("comp1").selection("left_boundary_selection").set("xmax", "-0.5*borehole_spacing")
    model.java.component("comp1").selection("left_boundary_selection").set("condition", "allvertices")

    model.java.component("comp1").selection().create("right_boundary_selection", "Box")
    model.java.component("comp1").selection("right_boundary_selection").label("Right Boundary Selection")
    model.java.component("comp1").selection("right_boundary_selection").set("entitydim", "2")
    if geology.has_groundwater_flow:
        model.java.component("comp1").selection("right_boundary_selection").set("xmin", "0.5*borehole_spacing")
        model.java.component("comp1").selection("right_boundary_selection").set("xmax", "0.5*borehole_spacing")
    else:
        model.java.component("comp1").selection("right_boundary_selection").set("xmin", "0")
        model.java.component("comp1").selection("right_boundary_selection").set("xmax", "0")
    model.java.component("comp1").selection("right_boundary_selection").set("condition", "allvertices")

    model.java.component("comp1").selection().create("left_and_right_boundaries_selection", "Union")
    model.java.component("comp1").selection("left_and_right_boundaries_selection").label("Left and Right Bondaries Selection")
    model.java.component("comp1").selection("left_and_right_boundaries_selection").set("entitydim", "2")
    model.java.component("comp1").selection("left_and_right_boundaries_selection").set("input", ["left_boundary_selection", "right_boundary_selection"])

    toc = time.time()

    print(f"Done in {time_elapsed(toc-tic)}.")

    # -------------------------------------------------------------------------
    # Creates mesh.
    # -------------------------------------------------------------------------

    print("Creating mesh...", end=" ")

    tic = time.time()

    model.java.component("comp1").mesh("mesh1").create("collar_edge", "Edge")
    model.java.component("comp1").mesh("mesh1").feature("collar_edge").selection().named("collar_edge_selection")
    model.java.component("comp1").mesh("mesh1").feature("collar_edge").label("Collar Edge Mesh")

    model.java.component("comp1").mesh("mesh1").feature("collar_edge").create("dis1", "Distribution")
    model.java.component("comp1").mesh("mesh1").feature("collar_edge").feature("dis1").set("numelem", "10")

    model.java.component("comp1").mesh("mesh1").create("ground_surface_mesh", "FreeTri")
    model.java.component("comp1").mesh("mesh1").feature("ground_surface_mesh").selection().named("ground_surface_selection")
    model.java.component("comp1").mesh("mesh1").feature("ground_surface_mesh").label("Ground Surface Mesh")
    model.java.component("comp1").mesh("mesh1").feature("ground_surface_mesh").set("method", "del")

    model.java.component("comp1").mesh("mesh1").feature("ground_surface_mesh").create("size1", "Size")
    model.java.component("comp1").mesh("mesh1").feature("ground_surface_mesh").feature("size1").set("custom", "on")
    model.java.component("comp1").mesh("mesh1").feature("ground_surface_mesh").feature("size1").set("hgradactive", "on")
    model.java.component("comp1").mesh("mesh1").feature("ground_surface_mesh").feature("size1").set("hgrad", "1.2")

    model.java.component("comp1").mesh("mesh1").create("swept_mesh", "Sweep")
    model.java.component("comp1").mesh("mesh1").feature("swept_mesh").selection().named("sweep_domains_selection")
    model.java.component("comp1").mesh("mesh1").feature("swept_mesh").label("Swept Mesh")

    #model.java.component("comp1").mesh("mesh1").feature("swept_mesh").create("dis1", "Distribution")
    #model.java.component("comp1").mesh("mesh1").feature("swept_mesh").feature("dis1").set("numelem", "10")

    for i, layer in enumerate(geology.layers):

        if layer.z_from <= -params.L_borehole:
            break

        num_elem = int(np.max([20, np.ceil(layer.thickness/5)]))

        model.java.component("comp1").mesh("mesh1").feature("swept_mesh").create(f"dis{i+1}", "Distribution")
        model.java.component("comp1").mesh("mesh1").feature("swept_mesh").feature(f"dis{i+1}").set("type", "predefined")
        model.java.component("comp1").mesh("mesh1").feature("swept_mesh").feature(f"dis{i+1}").set("growthrate", "exponential")
        model.java.component("comp1").mesh("mesh1").feature("swept_mesh").feature(f"dis{i+1}").set("elemcount", str(num_elem))
        model.java.component("comp1").mesh("mesh1").feature("swept_mesh").feature(f"dis{i+1}").set("elemratio", "10")
        model.java.component("comp1").mesh("mesh1").feature("swept_mesh").feature(f"dis{i+1}").set("symmetric", "on")
        model.java.component("comp1").mesh("mesh1").feature("swept_mesh").feature(f"dis{i+1}").selection().named(f"{layer.tag}_selection")

    model.java.component("comp1").mesh("mesh1").create("tetrahedral_mesh", "FreeTet")

    model.java.component("comp1").mesh("mesh1").feature("tetrahedral_mesh").create("size1", "Size")
    model.java.component("comp1").mesh("mesh1").feature("tetrahedral_mesh").feature("size1").set("hauto", "1")
    model.java.component("comp1").mesh("mesh1").feature("tetrahedral_mesh").feature("size1").set("custom", "on")
    model.java.component("comp1").mesh("mesh1").feature("tetrahedral_mesh").feature("size1").set("hgrad", "1.1")
    model.java.component("comp1").mesh("mesh1").feature("tetrahedral_mesh").feature("size1").set("hgradactive", "on")

    model.java.component("comp1").mesh("mesh1").run()

    toc = time.time()

    print(f"Done in {time_elapsed(toc-tic)}.")

    num_elems = model.java.component("comp1").mesh("mesh1").stat().getNumElem()

    print(f"Number of elements: {num_elems:,}")

    # -------------------------------------------------------------------------
    # Creates physics.
    # -------------------------------------------------------------------------

    print("Creating physics...", end=" ")

    tic = time.time()

    model.java.component("comp1").physics().create("ht", "PorousMediaHeatTransfer", "geom1")

    model.java.component("comp1").physics("ht").prop("ShapeProperty").set("order_temperature", "1")

    model.java.component("comp1").physics("ht").feature("init1").set("Tinit", "T_initial(z)")

    for i, layer in enumerate(geology.layers):

        if type(layer) is PorousLayer:

            model.java.component("comp1").physics("ht").create(f"porous{i+2}", "PorousMediumHeatTransferModel", 3)
            model.java.component("comp1").physics("ht").feature(f"porous{i+2}").selection().named(f"{layer.tag}_selection")
            model.java.component("comp1").physics("ht").feature(f"porous{i+2}").label(layer.name)

            model.java.component("comp1").physics("ht").feature(f"porous{i+2}").feature("fluid1").label("Water")
            model.java.component("comp1").physics("ht").feature(f"porous{i+2}").feature("fluid1").set("k_mat", "userdef")
            model.java.component("comp1").physics("ht").feature(f"porous{i+2}").feature("fluid1").set("k", [[f"k_fluid_{layer.tag}"], ["0"], ["0"], ["0"], [f"k_fluid_{layer.tag}"], ["0"], ["0"], ["0"], [f"k_fluid_{layer.tag}"]])
            model.java.component("comp1").physics("ht").feature(f"porous{i+2}").feature("fluid1").set("rho_mat", "userdef")
            model.java.component("comp1").physics("ht").feature(f"porous{i+2}").feature("fluid1").set("rho", f"rho_fluid_{layer.tag}")
            model.java.component("comp1").physics("ht").feature(f"porous{i+2}").feature("fluid1").set("Cp_mat", "userdef")
            model.java.component("comp1").physics("ht").feature(f"porous{i+2}").feature("fluid1").set("Cp", f"Cp_fluid_{layer.tag}")
            model.java.component("comp1").physics("ht").feature(f"porous{i+2}").feature("fluid1").set("gamma_mat", "userdef")
            model.java.component("comp1").physics("ht").feature(f"porous{i+2}").feature("fluid1").set("gamma", "1")

            model.java.component("comp1").physics("ht").feature(f"porous{i+2}").feature("pm1").set("porousMatrixPropertiesType", "solidPhaseProperties")
            model.java.component("comp1").physics("ht").feature(f"porous{i+2}").feature("pm1").label(layer.name)
            model.java.component("comp1").physics("ht").feature(f"porous{i+2}").feature("pm1").set("poro_mat", "userdef")
            model.java.component("comp1").physics("ht").feature(f"porous{i+2}").feature("pm1").set("poro", f"eps_{layer.tag}")
            model.java.component("comp1").physics("ht").feature(f"porous{i+2}").feature("pm1").set("k_sp_mat", "userdef")
            model.java.component("comp1").physics("ht").feature(f"porous{i+2}").feature("pm1").set("k_sp", [[f"k_solid_{layer.tag}"], ["0"], ["0"], ["0"], [f"k_solid_{layer.tag}"], ["0"], ["0"], ["0"], [f"k_solid_{layer.tag}"]])
            model.java.component("comp1").physics("ht").feature(f"porous{i+2}").feature("pm1").set("rho_sp_mat", "userdef")
            model.java.component("comp1").physics("ht").feature(f"porous{i+2}").feature("pm1").set("rho_sp", f"rho_solid_{layer.tag}")
            model.java.component("comp1").physics("ht").feature(f"porous{i+2}").feature("pm1").set("Cp_sp_mat", "userdef")
            model.java.component("comp1").physics("ht").feature(f"porous{i+2}").feature("pm1").set("Cp_sp", f"Cp_solid_{layer.tag}")

            if layer.velocity > 0:
                model.java.component("comp1").physics("ht").feature(f"porous{i+2}").feature("fluid1").set("u_src", "userdef");
                model.java.component("comp1").physics("ht").feature(f"porous{i+2}").feature("fluid1").set("u", [f"v_{layer.tag}", "0", "0"])

        else:

            model.java.component("comp1").physics("ht").create(f"solid{i+1}", "SolidHeatTransferModel", 3)
            model.java.component("comp1").physics("ht").feature(f"solid{i+1}").selection().named(f"{layer.tag}_selection")
            model.java.component("comp1").physics("ht").feature(f"solid{i+1}").label(f"{layer.name} Solid")
            model.java.component("comp1").physics("ht").feature(f"solid{i+1}").set("k_mat", "userdef")
            model.java.component("comp1").physics("ht").feature(f"solid{i+1}").set("k", [[f"k_eff_{layer.tag}"], ["0"], ["0"], ["0"], [f"k_eff_{layer.tag}"], ["0"], ["0"], ["0"], [f"k_eff_{layer.tag}"]])
            model.java.component("comp1").physics("ht").feature(f"solid{i+1}").set("rho_mat", "userdef")
            model.java.component("comp1").physics("ht").feature(f"solid{i+1}").set("rho", f"rho_eff_{layer.tag}")
            model.java.component("comp1").physics("ht").feature(f"solid{i+1}").set("Cp_mat", "userdef")
            model.java.component("comp1").physics("ht").feature(f"solid{i+1}").set("Cp", f"Cp_eff_{layer.tag}")

    model.java.component("comp1").physics("ht").create("ground_surface_temperature", "TemperatureBoundary", 2)
    model.java.component("comp1").physics("ht").feature("ground_surface_temperature").label("Ground Surface Temperature")
    model.java.component("comp1").physics("ht").feature("ground_surface_temperature").selection().named("ground_surface_selection")
    model.java.component("comp1").physics("ht").feature("ground_surface_temperature").set("T0", "T_surface")

    model.java.component("comp1").physics("ht").create("geothermal_heat_flux", "HeatFluxBoundary", 2)
    model.java.component("comp1").physics("ht").feature("geothermal_heat_flux").label("Geothermal Heat Flux")
    model.java.component("comp1").physics("ht").feature("geothermal_heat_flux").selection().named("geothermal_boundary_selection")
    model.java.component("comp1").physics("ht").feature("geothermal_heat_flux").set("q0", "q_geothermal")
    model.java.component("comp1").physics("ht").feature("geothermal_heat_flux").set("materialType", "solid")

    model.java.component("comp1").physics("ht").create("borehole_wall_heat_flux", "HeatFluxBoundary", 2)
    model.java.component("comp1").physics("ht").feature("borehole_wall_heat_flux").label("Borehole Wall Heat Flux")
    model.java.component("comp1").physics("ht").feature("borehole_wall_heat_flux").selection().named("borehole_wall_selection")
    model.java.component("comp1").physics("ht").feature("borehole_wall_heat_flux").set("q0", "-Q_extraction/A_wall")

    if geology.has_groundwater_flow:
        model.java.component("comp1").physics("ht").create("pc1", "PeriodicHeat", 2)
        model.java.component("comp1").physics("ht").feature("pc1").selection().named("left_and_right_boundaries_selection")
        model.java.component("comp1").physics("ht").feature("pc1").create("dd1", "DestinationDomains", 2)
        model.java.component("comp1").physics("ht").feature("pc1").feature("dd1").selection().named("left_boundary_selection")

    toc = time.time()

    print(f"Done in {time_elapsed(toc-tic)}.")

    # -------------------------------------------------------------------------
    # Creates operators and variables.
    # -------------------------------------------------------------------------

    print("Creating operators and variables...", end=" ")

    tic = time.time()

    model.java.component("comp1").cpl().create("borehole_wall_integration", "Integration")
    model.java.component("comp1").cpl("borehole_wall_integration").label("Borehole Wall Integration")
    model.java.component("comp1").cpl("borehole_wall_integration").set("axisym", "on")
    model.java.component("comp1").cpl("borehole_wall_integration").selection().geom("geom1", 2)
    model.java.component("comp1").cpl("borehole_wall_integration").selection().named("borehole_wall_selection")

    model.java.component("comp1").cpl().create("borehole_wall_minimum", "Minimum")
    model.java.component("comp1").cpl("borehole_wall_minimum").label("Borehole Wall Minimum")
    model.java.component("comp1").cpl("borehole_wall_minimum").selection().geom("geom1", 2)
    model.java.component("comp1").cpl("borehole_wall_minimum").selection().named("borehole_wall_selection")

    model.java.component("comp1").cpl().create("borehole_wall_average", "Average")
    model.java.component("comp1").cpl("borehole_wall_average").label("Borehole Wall Average")
    model.java.component("comp1").cpl("borehole_wall_average").selection().geom("geom1", 2)
    model.java.component("comp1").cpl("borehole_wall_average").selection().named("borehole_wall_selection")

    model.java.component("comp1").variable().create("var1")
    model.java.component("comp1").variable("var1").set("T_min", "borehole_wall_minimum(T)")
    model.java.component("comp1").variable("var1").set("T_ave", "borehole_wall_average(T)")
    ### *** model.java.component("comp1").variable("var1").set("Q_wall", "4*borehole_wall_integration(ht.ndflux)")

    if params.monthly_fractions is not None:
        model.java.component("comp1").variable("var1").set("Q_extraction", "(E_annual*monthly_fractions(t))/(1[a]/12)")
    else:
        model.java.component("comp1").variable("var1").set("Q_extraction", "E_annual/1[a]")

    toc = time.time()

    print(f"Done in {time_elapsed(toc-tic)}.")

    # -------------------------------------------------------------------------
    # Creates solution and solver.
    # -------------------------------------------------------------------------

    print("Creating solution and solver...", end=" ")

    tic = time.time()

    tlist = f"range(0,1/12,{params.num_years})"

    model.java.study().create("std1")

    model.java.study("std1").setGenPlots(False)
    model.java.study("std1").setGenConv(False)

    model.java.study("std1").create("time", "Transient")
    model.java.study("std1").feature("time").set("tunit", "a")
    model.java.study("std1").feature("time").set("tlist", tlist)

    if params.monthly_fractions is None:
        model.java.study("std1").feature("time").set("usertol", "on")
        model.java.study("std1").feature("time").set("rtol", "1e-3")

    model.java.sol().create("sol1")
    model.java.sol("sol1").study("std1")
    model.java.sol("sol1").attach("std1")

    model.java.sol("sol1").create("st1", "StudyStep")

    model.java.sol("sol1").create("v1", "Variables")

    model.java.sol("sol1").create("t1", "Time")
    model.java.sol("sol1").feature("t1").create("d1", "Direct")
    model.java.sol("sol1").feature("t1").feature("d1").set("linsolver", "pardiso")
    model.java.sol("sol1").feature("t1").feature().remove("dDef")
    model.java.sol("sol1").feature("t1").feature().remove("fcDef")
    model.java.sol("sol1").feature("t1").set("tunit", "a")
    model.java.sol("sol1").feature("t1").set("tlist", tlist)
    model.java.sol("sol1").feature("t1").set("maxorder", "2")
    model.java.sol("sol1").feature("t1").set("estrat", "exclude")
    model.java.sol("sol1").feature("t1").set("control", "time")

    if params.monthly_fractions is None:
        model.java.sol("sol1").feature("t1").set("tstepsbdf", "free")
        model.java.sol("sol1").feature("t1").set("initialstepbdfactive", "on")
        model.java.sol("sol1").feature("t1").set("initialstepbdf", "1e-6")
    else:
        model.java.sol("sol1").feature("t1").set("tstepsbdf", "strict")

    toc = time.time()

    print(f"Done in {time_elapsed(toc-tic)}.")

    xmi = model.java.sol("sol1").feature("st1").xmeshInfo()

    num_dofs = xmi.nDofs()

    print(f"Number of degrees of freedom: {num_dofs:,}")

    return model

if __name__ == "__main__":
    from geology import Geology, Layer, Material
    from utils import save_model
    import mph
    # Creates and prints parameters.
    print("Parameters", 50*"=")
    params = Parameters(L_borehole=300, D_borehole=0.115, borehole_spacing=20, E_annual=30, num_years=20)
    print(params)
    # Creates and prints materials.
    sand = PorousMaterial("Sand", 1, 1000, 1500, porosity=0.30)
    granite = Material("Granite", 3, 700, 2700)
    sandstone = PorousMaterial("Sandstone", 2.5, 700, 2500, porosity=0.15)
    gneiss = Material("Gneiss", 4, 800, 2900)
    print("Materials", 50*"=")
    print(sand)
    print(granite)
    print(sandstone)
    print(gneiss)
    # Creates and prints layers.
    sand_layer = PorousLayer("Sand Layer", sand, 0, -100, velocity=1e-4)
    granite_layer = Layer("Granite Layer", granite, -100, -200)
    sandstone_layer = PorousLayer("Sandstone Layer", sandstone, -200, -300, velocity=1e-5)
    gneiss_layer = Layer("Gneiss Layer", gneiss, -300, -1000)
    print(sand_layer)
    print(granite_layer)
    print(sandstone_layer)
    print(gneiss_layer)
    # Creates and prints geology.
    geology = Geology("Test Geology", 6.5, 0.065, layers=[sand_layer, granite_layer, sandstone_layer, gneiss_layer])
    print(geology)
    # Creates and saves model.
    client = mph.start(cores=8)
    model = init_model(client, params, geology)
    save_model(model)
