from geology import Geology, PorousMaterial, PorousLayer
import pandas as pd
import numpy as np
import eed
import os


os.environ["KMP_DUPLICATE_LIB_OK"] = "True" # Gets rid of the annoying OpenMP initialization error.


if __name__ == "__main__":

    # Sets up the monthly energy consumption profile.

    monthly_fractions = [0.194717, 0.17216, 0.128944, 0.075402, 0.024336, 0, 0, 0, 0.025227, 0.076465, 0.129925, 0.172824]

    # Creates materials for the geological models.

    quaternary_deposits   = PorousMaterial("Quaternary Deposits",   k_matrix=3.0, Cp_matrix=1800, rho_matrix=1800, porosity=0.30)
    miocene_rocks         = PorousMaterial("Miocene Rocks",         k_matrix=1.8, Cp_matrix=840,  rho_matrix=2200, porosity=0.10)
    upper_oligocene_rocks = PorousMaterial("Upper Oligocene Rocks", k_matrix=1.8, Cp_matrix=900,  rho_matrix=2500, porosity=0.10)
    lower_oligocene_rocks = PorousMaterial("Lower Oligocene Rocks", k_matrix=1.5, Cp_matrix=2100, rho_matrix=2000, porosity=0.05)
    eocene_rocks          = PorousMaterial("Eocene Rocks",          k_matrix=2.0, Cp_matrix=840,  rho_matrix=2100, porosity=0.15)
    triassic_rocks        = PorousMaterial("Triassic Rocks",        k_matrix=2.5, Cp_matrix=850,  rho_matrix=2700, porosity=0.15)

    # Sets up the groundwater flow velocities.

    v_quaternary      = 1.0e-08
    v_miocene         = 1.0e-09
    v_upper_oligocene = 0.5e-09
    v_lower_oligocene = 1.0e-10
    v_eocene          = 1.0e-09
    v_triassic        = 1.0e-08

    # Creates the geologies.

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
    geology9.add_layer(PorousLayer("triassic Layer",        z_from=-1228.4, z_to=-1270.00, material=triassic_rocks,        velocity=v_triassic))

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

    geology = [geology1, geology2, geology3, geology4, geology5, geology6, geology7, geology8, geology9, geology10, geology11, geology12]

    # Estimates the shallow geothermal potentials.

    data_frame = pd.DataFrame(columns=["Geology", "L_borehole", "borehole_spacing", "E_annual", "T_fluid"])

    L_borehole = [100, 200]
    borehole_spacing = [20, 500]

    for i in range(len(L_borehole)):
        for j in range(len(borehole_spacing)):
            for k in range(len(geology)):

                avg = geology[k].calc_averages()

                if borehole_spacing[j] == 20:
                    rec_num = 761
                elif borehole_spacing[j] == 500:
                    rec_num = 0
                else:
                    raise ValueError("rec_num")

                params = {
                    "k_ground": avg["k"],
                    "C_ground": avg["C"],
                    "T_surface": geology[k].T_surface,
                    "q_geothermal": geology[k].q_geothermal,
                    "rec_num": rec_num,
                    "L_borehole": L_borehole[i],
                    "D_borehole": 0.150,
                    "borehole_spacing": borehole_spacing[j],
                    "R_borehole": 0.0,
                    "E_annual": 100,
                    "SPF": 99999,
                    "num_years": 50,
                    "monthly_fractions": monthly_fractions
                }

                if borehole_spacing[j] == 20:
                    if L_borehole[i] == 100:
                        E_max, T_fluid = eed.optimize_energy(params, [5000, 20000], 0)
                    elif L_borehole[i] == 200:
                        E_max, T_fluid = eed.optimize_energy(params, [5000, 40000], 0)
                    else:
                        raise ValueError("L_borehole")
                    E_annual = E_max / 1156
                elif borehole_spacing[j] == 500:
                    if L_borehole[i] == 100:
                        E_annual, T_fluid = eed.optimize_energy(params, [1, 50], 0)
                    elif L_borehole[i] == 200:
                        E_annual, T_fluid = eed.optimize_energy(params, [1, 50], 0)
                    else:
                        raise ValueError("L_borehole")
                else:
                    raise ValueError("borehole_spacing")

                print(f"geology={geology[k].name}, L_borehole={params['L_borehole']} m, borehole_spacing={params['borehole_spacing']} m, E_annual={E_annual:.6f} MWh, T_fluid={T_fluid:.6f} \xb0C")

                data_frame.loc[len(data_frame)] = [geology[k].name, L_borehole[i], borehole_spacing[j], E_annual, T_fluid]

                data_frame.to_excel("results_eed.xlsx")
