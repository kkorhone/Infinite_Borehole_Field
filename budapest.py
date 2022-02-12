from geology import PorousMaterial, PorousLayer, Geology

def make_geologies(v_groundwater=0):

    quaternary_deposits   = PorousMaterial("Quaternary Deposits",   k_matrix=3.0, Cp_matrix=1800, rho_matrix=1800, porosity=0.30)
    miocene_rocks         = PorousMaterial("Miocene Rocks",         k_matrix=1.8, Cp_matrix=840,  rho_matrix=2200, porosity=0.10)
    upper_oligocene_rocks = PorousMaterial("Upper Oligocene Rocks", k_matrix=1.8, Cp_matrix=900,  rho_matrix=2500, porosity=0.10)
    lower_oligocene_rocks = PorousMaterial("Lower Oligocene Rocks", k_matrix=1.5, Cp_matrix=2100, rho_matrix=2000, porosity=0.05)
    eocene_rocks          = PorousMaterial("Eocene Rocks",          k_matrix=2.0, Cp_matrix=840,  rho_matrix=2100, porosity=0.15)
    triassic_rocks        = PorousMaterial("Triassic Rocks",        k_matrix=2.5, Cp_matrix=850,  rho_matrix=2700, porosity=0.15)

    if v_groundwater == "predefined":
        print("*** Using predefined groundwater flow velocities.")
        v_quaternary      = 1.0e-08
        v_miocene         = 1.0e-09
        v_upper_oligocene = 0.5e-09
        v_lower_oligocene = 1.0e-10
        v_eocene          = 1.0e-09
        v_triassic        = 1.0e-08
    else:
        print(f"*** Using uniform groundwater flow velocity of {v_groundwater} m/s.")
        v_quaternary      = v_groundwater
        v_miocene         = v_groundwater
        v_upper_oligocene = v_groundwater
        v_lower_oligocene = v_groundwater
        v_eocene          = v_groundwater
        v_triassic        = v_groundwater

    geology1 = Geology("B-21",  T_surface=13.2, q_geothermal=0.0938000)

    geology1.add_layer(PorousLayer("Quaternary Layer",      z_from=0.0,    z_to=-15.3,  material=quaternary_deposits,   velocity=v_quaternary))
    geology1.add_layer(PorousLayer("Lower Oligocene Layer", z_from=-15.3,  z_to=-523.0, material=lower_oligocene_rocks, velocity=v_lower_oligocene))
    geology1.add_layer(PorousLayer("Eocene Layer",          z_from=-523.0, z_to=-633.0, material=eocene_rocks,          velocity=v_eocene))
    geology1.add_layer(PorousLayer("Triassic Layer",        z_from=-633.0, z_to=-766.4, material=triassic_rocks,        velocity=v_triassic))

    geology2 = Geology("B-30",  T_surface=13.2, q_geothermal=0.0905000)

    geology2.add_layer(PorousLayer("Quaternary Layer",      z_from=0.0,    z_to=-16.5,  material=quaternary_deposits,   velocity=v_quaternary))
    geology2.add_layer(PorousLayer("Lower Oligocene Layer", z_from=-16.5,  z_to=-551.0, material=lower_oligocene_rocks, velocity=v_lower_oligocene))
    geology2.add_layer(PorousLayer("Eocene Layer",          z_from=-551.0, z_to=-695.3, material=eocene_rocks,          velocity=v_eocene))
    geology2.add_layer(PorousLayer("Triassic Layer",        z_from=-695.3, z_to=-800.0, material=triassic_rocks,        velocity=v_triassic))

    geology3 = Geology("B-39",  T_surface=13.2, q_geothermal=0.0980000)

    geology3.add_layer(PorousLayer("Quaternary Layer",      z_from=0.0,    z_to=-14.4,  material=quaternary_deposits,   velocity=v_quaternary))
    geology3.add_layer(PorousLayer("Upper Oligocene Layer", z_from=-14.4,  z_to=-285.4, material=upper_oligocene_rocks, velocity=v_upper_oligocene))
    geology3.add_layer(PorousLayer("Lower Oligocene Layer", z_from=-285.4, z_to=-482.0, material=lower_oligocene_rocks, velocity=v_lower_oligocene))
    geology3.add_layer(PorousLayer("Triassic Layer",        z_from=-482.0, z_to=-650.0, material=triassic_rocks,        velocity=v_triassic))

    geology4 = Geology("B-48",  T_surface=13.2, q_geothermal=0.0867000)

    geology4.add_layer(PorousLayer("Quaternary Layer",      z_from=0.0,     z_to=-7.9,    material=quaternary_deposits,   velocity=v_quaternary))
    geology4.add_layer(PorousLayer("Miocene Layer",         z_from=-7.9,    z_to=-360.3,  material=miocene_rocks,         velocity=v_miocene))
    geology4.add_layer(PorousLayer("Upper Oligocene Layer", z_from=-360.3,  z_to=-507.0,  material=upper_oligocene_rocks, velocity=v_upper_oligocene))
    geology4.add_layer(PorousLayer("Lower Oligocene Layer", z_from= -507.0, z_to=-1081.7, material=lower_oligocene_rocks, velocity=v_lower_oligocene))
    geology4.add_layer(PorousLayer("Eocene Layer",          z_from=-1081.7, z_to=-1128.0, material=eocene_rocks,          velocity=v_eocene))
    geology4.add_layer(PorousLayer("Triassic Layer",        z_from=-1128.0, z_to=-1198.0, material=triassic_rocks,        velocity=v_triassic))

    geology5 = Geology("B-63",  T_surface=13.2, q_geothermal=0.0928000)

    geology5.add_layer(PorousLayer("Quaternary Layer",      z_from=0.00,    z_to=-24.85,  material=quaternary_deposits,   velocity=v_quaternary))
    geology5.add_layer(PorousLayer("Miocene Layer",         z_from=-24.85,  z_to=-700.00, material=miocene_rocks,         velocity=v_miocene))
    geology5.add_layer(PorousLayer("Upper Oligocene Layer", z_from=-700.00, z_to=-701.00, material=upper_oligocene_rocks, velocity=v_upper_oligocene))

    geology6 = Geology("B-13",  T_surface=13.2, q_geothermal=0.0835810)

    geology6.add_layer(PorousLayer("Quaternary Layer",      z_from=0.00,     z_to=-12.00,   material=quaternary_deposits,   velocity=v_quaternary))
    geology6.add_layer(PorousLayer("Miocene Layer",         z_from=-12.00,   z_to=-424.82,  material=miocene_rocks,         velocity=v_miocene))
    geology6.add_layer(PorousLayer("Upper Oligocene Layer", z_from=-424.82,  z_to=-647.42,  material=upper_oligocene_rocks, velocity=v_upper_oligocene))
    geology6.add_layer(PorousLayer("Lower Oligocene Layer", z_from= -647.42, z_to=-1194.00, material=lower_oligocene_rocks, velocity=v_lower_oligocene))
    geology6.add_layer(PorousLayer("Eocene Layer",          z_from=-1194.00, z_to=-1234.82, material=eocene_rocks,          velocity=v_eocene))

    geology7 = Geology("B-56",  T_surface=13.2, q_geothermal=0.0836250)

    geology7.add_layer(PorousLayer("Quaternary Layer",      z_from=0.0,     z_to=-15.0,   material=quaternary_deposits,   velocity=v_quaternary))
    geology7.add_layer(PorousLayer("Miocene Layer",         z_from=-15.0,   z_to=-439.1,  material=miocene_rocks,         velocity=v_miocene))
    geology7.add_layer(PorousLayer("Upper Oligocene Layer", z_from=-439.1,  z_to=-775.4,  material=upper_oligocene_rocks, velocity=v_upper_oligocene))
    geology7.add_layer(PorousLayer("Lower Oligocene Layer", z_from=-775.4,  z_to=-1095.0, material=lower_oligocene_rocks, velocity=v_lower_oligocene))
    geology7.add_layer(PorousLayer("Eocene Layer",          z_from=-1095.0, z_to=-1172.0, material=eocene_rocks,          velocity=v_eocene))
    geology7.add_layer(PorousLayer("Triassic Layer",        z_from=-1172.0, z_to=-1233.0, material=triassic_rocks,        velocity=v_triassic))

    geology8 = Geology("B-179", T_surface=13.2, q_geothermal=0.0828568)

    geology8.add_layer(PorousLayer("Miocene Layer",         z_from=0.0,     z_to=-351.0,  material=miocene_rocks,         velocity=v_miocene))
    geology8.add_layer(PorousLayer("Upper Oligocene Layer", z_from=-351.0,  z_to=-600.0,  material=upper_oligocene_rocks, velocity=v_upper_oligocene))
    geology8.add_layer(PorousLayer("Lower Oligocene Layer", z_from=-600.0,  z_to=-1025.0, material=lower_oligocene_rocks, velocity=v_lower_oligocene))
    geology8.add_layer(PorousLayer("Eocene Layer",          z_from=-1025.0, z_to=-1240.0, material=eocene_rocks,          velocity=v_eocene))
    geology8.add_layer(PorousLayer("Triassic Layer",        z_from=-1240.0, z_to=-1304.5, material=triassic_rocks,        velocity=v_triassic))

    geology9 = Geology("B-180", T_surface=13.2, q_geothermal=0.0827390)

    geology9.add_layer(PorousLayer("Miocene Layer",         z_from=0.0,     z_to=-347.30,  material=miocene_rocks,         velocity=v_miocene))
    geology9.add_layer(PorousLayer("Upper Oligocene Layer", z_from=-347.3,  z_to=-580.00,  material=upper_oligocene_rocks, velocity=v_upper_oligocene))
    geology9.add_layer(PorousLayer("Lower Oligocene Layer", z_from=-580.0,  z_to=-1027.00, material=lower_oligocene_rocks, velocity=v_lower_oligocene))
    geology9.add_layer(PorousLayer("Eocene Layer",          z_from=-1027.0, z_to=-1228.40, material=eocene_rocks,          velocity=v_eocene))
    geology9.add_layer(PorousLayer("Triassic Layer",        z_from=-1228.4, z_to=-1270.00, material=triassic_rocks,        velocity=v_triassic))

    geology10 = Geology("Pm_1", T_surface=13.2, q_geothermal=0.0714500)

    geology10.add_layer(PorousLayer("Quaternary Layer",      z_from=0.0,     z_to=-10.0,   material=quaternary_deposits,   velocity=v_quaternary))
    geology10.add_layer(PorousLayer("Miocene Layer",         z_from=-10.0,   z_to=-180.0,  material=miocene_rocks,         velocity=v_miocene))
    geology10.add_layer(PorousLayer("Upper Oligocene Layer", z_from=-180.0,  z_to=-280.0,  material=upper_oligocene_rocks, velocity=v_upper_oligocene))
    geology10.add_layer(PorousLayer("Lower Oligocene Layer", z_from=-280.0,  z_to=-1070.0, material=lower_oligocene_rocks, velocity=v_lower_oligocene))
    geology10.add_layer(PorousLayer("Eocene Layer",          z_from=-1070.0, z_to=-1340.0, material=eocene_rocks,          velocity=v_eocene))
    geology10.add_layer(PorousLayer("Triassic Layer",        z_from=-1340.0, z_to=-1735.0, material=triassic_rocks,        velocity=v_triassic))

    geology11 = Geology("B-64",  T_surface=13.2, q_geothermal=0.0911600)

    geology11.add_layer(PorousLayer("Quaternary Layer",      z_from=0,      z_to=-13.4,  material=quaternary_deposits,   velocity=v_quaternary))
    geology11.add_layer(PorousLayer("Miocene Layer",         z_from=-13.4,  z_to=-319.0, material=miocene_rocks,         velocity=v_miocene))
    geology11.add_layer(PorousLayer("Upper Oligocene Layer", z_from=-319.0, z_to=-600.0, material=upper_oligocene_rocks, velocity=v_upper_oligocene))

    geology12 = Geology("B-38",  T_surface=13.2, q_geothermal=0.1016000)

    geology12.add_layer(PorousLayer("Quaternary Layer",      z_from=0,      z_to=-21.0,  material=quaternary_deposits,   velocity=v_quaternary))
    geology12.add_layer(PorousLayer("Lower Oligocene Layer", z_from=-21.0,  z_to=-175.0, material=lower_oligocene_rocks, velocity=v_lower_oligocene))
    geology12.add_layer(PorousLayer("Eocene Layer",          z_from=-175.0, z_to=-320.0, material=eocene_rocks,          velocity=v_eocene))
    geology12.add_layer(PorousLayer("Triassic Layer",        z_from=-320.0, z_to=-559.5, material=triassic_rocks,        velocity=v_triassic))

    return [geology1, geology2, geology3, geology4, geology5, geology6, geology7, geology8, geology9, geology10, geology11, geology12]

if __name__ == "__main__":

    import matplotlib.pyplot as plt
    import numpy as np

    plt.rcParams["font.family"] = "serif"
    plt.rcParams["font.serif"] = "Times"
    plt.rcParams["font.size"] = 14
    plt.rcParams["text.usetex"] = True

    geologies = make_geologies()

    plt.figure(figsize=(8, 6))

    colors = {"Quaternary Layer": "r", "Miocene Layer": "g", "Upper Oligocene Layer": "b", "Lower Oligocene Layer": "c", "Eocene Layer": "m", "Triassic Layer": "y"}
    handles = {}

    for i, geology in enumerate(geologies):
        plt.text(i+1, 0, geology.name.replace("_", r"\textunderscore"), ha="center", va="bottom")
        for j, layer in enumerate(geology.layers):
            h, = plt.fill([i+0.7, i+1.3, i+1.3, i+0.7], [layer.z_from, layer.z_from, layer.z_to, layer.z_to], color=colors[layer.name], ec=colors[layer.name], fc=colors[layer.name])
            handles[layer.name] = h

    plt.legend((handles["Quaternary Layer"], handles["Miocene Layer"], handles["Upper Oligocene Layer"], handles["Lower Oligocene Layer"], handles["Eocene Layer"], handles["Triassic Layer"]), ("Quaternary deposits", "Miocene sandstones", "Upper Oligocene layer (clay)", "Lower Oligocene layer (clay marl)", "Eocene marl", "Triassic carbonates"), framealpha=1, labelspacing=0.333)

    plt.gca().spines.top.set_color("none")
    plt.gca().spines.bottom.set_color("none")
    plt.gca().spines.right.set_color("none")

    plt.ylabel("Depth [m]")
    plt.gca().set_xticks([])
    plt.gca().set_xlim([0.5, 12.5])
    plt.gca().set_ylim([-1805, 0])
    plt.gca().set_yticks(np.arange(-1800, 200, 200))
    plt.gca().yaxis.grid(color="k", ls="--")

    plt.tight_layout()

    plt.savefig("geologies.png")

    plt.show()
