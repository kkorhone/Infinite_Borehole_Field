from comsol import Parameters, init_model, eval_temp
from geology import Geology, PorousMaterial, PorousLayer
from itertools import product
import matplotlib.pyplot as plt
from utils import save_model
import pandas as pd
import numpy as np
import os, mph


os.environ["KMP_DUPLICATE_LIB_OK"] = "True" # Gets rid of the annoying OpenMP initialization error.


if __name__ == "__main__":

    file_name = "results_v9_without_groundwater_flow.xlsx"

    # Sets up the monthly energy consumption profile.

    monthly_fractions = [0.194717, 0.17216, 0.128944, 0.075402, 0.024336, 0, 0, 0, 0.025227, 0.076465, 0.129925, 0.172824]

    # Creates materials for the geological models.

    quaternary_deposits   = PorousMaterial("Quaternary Deposits",   k_matrix=3.0, Cp_matrix=1800, rho_matrix=1800, porosity=0.30)
    miocene_rocks         = PorousMaterial("Miocene Rocks",         k_matrix=1.8, Cp_matrix=840,  rho_matrix=2200, porosity=0.10)
    upper_oligocene_rocks = PorousMaterial("Upper Oligocene Rocks", k_matrix=1.8, Cp_matrix=900,  rho_matrix=2500, porosity=0.10)
    lower_oligocene_rocks = PorousMaterial("Lower Oligocene Rocks", k_matrix=1.5, Cp_matrix=2100, rho_matrix=2000, porosity=0.05)
    eocene_rocks          = PorousMaterial("Eocene Rocks",          k_matrix=2.0, Cp_matrix=840,  rho_matrix=2100, porosity=0.15)
    triassic_rocks        = PorousMaterial("Triassic Rocks",        k_matrix=2.5, Cp_matrix=850,  rho_matrix=2700, porosity=0.15)

    # Creates the geologies.

    geology1 = Geology("B-21",  T_surface=13.2, q_geothermal=0.0938000)

    geology1.add_layer(PorousLayer("Quaternary Layer",      z_from=0.0,    z_to=-15.3,  material=quaternary_deposits))
    geology1.add_layer(PorousLayer("Lower Oligocene Layer", z_from=-15.3,  z_to=-523.0, material=lower_oligocene_rocks))
    geology1.add_layer(PorousLayer("Eocene Layer",          z_from=-523.0, z_to=-633.0, material=eocene_rocks))
    geology1.add_layer(PorousLayer("Triassic Layer",        z_from=-633.0, z_to=-766.4, material=triassic_rocks))

    geology2 = Geology("B-30",  T_surface=13.2, q_geothermal=0.0905000)

    geology2.add_layer(PorousLayer("Quaternary Layer",      z_from=0.0,    z_to=-16.5,  material=quaternary_deposits))
    geology2.add_layer(PorousLayer("Lower Oligocene Layer", z_from=-16.5,  z_to=-551.0, material=lower_oligocene_rocks))
    geology2.add_layer(PorousLayer("Eocene Layer",          z_from=-551.0, z_to=-695.3, material=eocene_rocks))
    geology2.add_layer(PorousLayer("Triassic Layer",        z_from=-695.3, z_to=-800.0, material=triassic_rocks))

    geology3 = Geology("B-39",  T_surface=13.2, q_geothermal=0.0980000)

    geology3.add_layer(PorousLayer("Quaternary Layer",      z_from=0.0,    z_to=-14.4,  material=quaternary_deposits))
    geology3.add_layer(PorousLayer("Upper Oligocene Layer", z_from=-14.4,  z_to=-285.4, material=upper_oligocene_rocks))
    geology3.add_layer(PorousLayer("Lower Oligocene Layer", z_from=-285.4, z_to=-482.0, material=lower_oligocene_rocks))
    geology3.add_layer(PorousLayer("Triassic Layer",        z_from=-482.0, z_to=-650.0, material=triassic_rocks))

    geology4 = Geology("B-48",  T_surface=13.2, q_geothermal=0.0867000)

    geology4.add_layer(PorousLayer("Quaternary Layer",      z_from=0.0,     z_to=-7.9,    material=quaternary_deposits))
    geology4.add_layer(PorousLayer("Miocene Layer",         z_from=-7.9,    z_to=-360.3,  material=miocene_rocks))
    geology4.add_layer(PorousLayer("Upper Oligocene Layer", z_from=-360.3,  z_to=-507.0,  material=upper_oligocene_rocks))
    geology4.add_layer(PorousLayer("Lower Oligocene Layer", z_from= -507.0, z_to=-1081.7, material=lower_oligocene_rocks))
    geology4.add_layer(PorousLayer("Eocene Layer",          z_from=-1081.7, z_to=-1128.0, material=eocene_rocks))
    geology4.add_layer(PorousLayer("Triassic Layer",        z_from=-1128.0, z_to=-1198.0, material=triassic_rocks))

    geology5 = Geology("B-63",  T_surface=13.2, q_geothermal=0.0928000)

    geology5.add_layer(PorousLayer("Quaternary Layer",      z_from=0.00,    z_to=-24.85,  material=quaternary_deposits))
    geology5.add_layer(PorousLayer("Miocene Layer",         z_from=-24.85,  z_to=-700.00, material=miocene_rocks))
    geology5.add_layer(PorousLayer("Upper Oligocene Layer", z_from=-700.00, z_to=-701.00, material=upper_oligocene_rocks))

    geology6 = Geology("B-13",  T_surface=13.2, q_geothermal=0.0835810)

    geology6.add_layer(PorousLayer("Quaternary Layer",      z_from=0.00,     z_to=-12.00,   material=quaternary_deposits))
    geology6.add_layer(PorousLayer("Miocene Layer",         z_from=-12.00,   z_to=-424.82,  material=miocene_rocks))
    geology6.add_layer(PorousLayer("Upper Oligocene Layer", z_from=-424.82,  z_to=-647.42,  material=upper_oligocene_rocks))
    geology6.add_layer(PorousLayer("Lower Oligocene Layer", z_from= -647.42, z_to=-1194.00, material=lower_oligocene_rocks))
    geology6.add_layer(PorousLayer("Eocene Layer",          z_from=-1194.00, z_to=-1234.82, material=eocene_rocks))

    geology7 = Geology("B-56",  T_surface=13.2, q_geothermal=0.0836250)

    geology7.add_layer(PorousLayer("Quaternary Layer",      z_from=0.0,     z_to=-15.0,   material=quaternary_deposits))
    geology7.add_layer(PorousLayer("Miocene Layer",         z_from=-15.0,   z_to=-439.1,  material=miocene_rocks))
    geology7.add_layer(PorousLayer("Upper Oligocene Layer", z_from=-439.1,  z_to=-775.4,  material=upper_oligocene_rocks))
    geology7.add_layer(PorousLayer("Lower Oligocene Layer", z_from=-775.4,  z_to=-1095.0, material=lower_oligocene_rocks))
    geology7.add_layer(PorousLayer("Eocene Layer",          z_from=-1095.0, z_to=-1172.0, material=eocene_rocks))
    geology7.add_layer(PorousLayer("Triassic Layer",        z_from=-1172.0, z_to=-1233.0, material=triassic_rocks))

    geology8 = Geology("B-179", T_surface=13.2, q_geothermal=0.0828568)

    geology8.add_layer(PorousLayer("Miocene Layer",         z_from=0.0,     z_to=-351.0,  material=miocene_rocks))
    geology8.add_layer(PorousLayer("Upper Oligocene Layer", z_from=-351.0,  z_to=-600.0,  material=upper_oligocene_rocks))
    geology8.add_layer(PorousLayer("Lower Oligocene Layer", z_from=-600.0,  z_to=-1025.0, material=lower_oligocene_rocks))
    geology8.add_layer(PorousLayer("Eocene Layer",          z_from=-1025.0, z_to=-1240.0, material=eocene_rocks))
    geology8.add_layer(PorousLayer("Triassic Layer",        z_from=-1240.0, z_to=-1304.5, material=triassic_rocks))

    geology9 = Geology("B-180", T_surface=13.2, q_geothermal=0.0827390)

    geology9.add_layer(PorousLayer("Miocene Layer",         z_from=0.0,     z_to=-347.30,  material=miocene_rocks))
    geology9.add_layer(PorousLayer("Upper Oligocene Layer", z_from=-347.3,  z_to=-580.00,  material=upper_oligocene_rocks))
    geology9.add_layer(PorousLayer("Lower Oligocene Layer", z_from=-580.0,  z_to=-1027.00, material=lower_oligocene_rocks))
    geology9.add_layer(PorousLayer("Eocene Layer",          z_from=-1027.0, z_to=-1228.40, material=eocene_rocks))
    geology9.add_layer(PorousLayer("triassic Layer",        z_from=-1228.4, z_to=-1270.00, material=triassic_rocks))

    geology10 = Geology("Pm_1", T_surface=13.2, q_geothermal=0.0714500)

    geology10.add_layer(PorousLayer("Quaternary Layer",      z_from=0.0,     z_to=-10.0,   material=quaternary_deposits))
    geology10.add_layer(PorousLayer("Miocene Layer",         z_from=-10.0,   z_to=-180.0,  material=miocene_rocks))
    geology10.add_layer(PorousLayer("Upper Oligocene Layer", z_from=-180.0,  z_to=-280.0,  material=upper_oligocene_rocks))
    geology10.add_layer(PorousLayer("Lower Oligocene Layer", z_from=-280.0,  z_to=-1070.0, material=lower_oligocene_rocks))
    geology10.add_layer(PorousLayer("Eocene Layer",          z_from=-1070.0, z_to=-1340.0, material=eocene_rocks))
    geology10.add_layer(PorousLayer("Triassic Layer",        z_from=-1340.0, z_to=-1735.0, material=triassic_rocks))

    geology11 = Geology("B-64",  T_surface=13.2, q_geothermal=0.0911600)

    geology11.add_layer(PorousLayer("Quaternary Layer",      z_from=0,      z_to=-13.4,  material=quaternary_deposits))
    geology11.add_layer(PorousLayer("Miocene Layer",         z_from=-13.4,  z_to=-319.0, material=miocene_rocks))
    geology11.add_layer(PorousLayer("Upper Oligocene Layer", z_from=-319.0, z_to=-600.0, material=upper_oligocene_rocks))

    geology12 = Geology("B-38",  T_surface=13.2, q_geothermal=0.1016000)

    geology12.add_layer(PorousLayer("Quaternary Layer",      z_from=0,      z_to=-21.0,  material=quaternary_deposits))
    geology12.add_layer(PorousLayer("Lower Oligocene Layer", z_from=-21.0,  z_to=-175.0, material=lower_oligocene_rocks))
    geology12.add_layer(PorousLayer("Eocene Layer",          z_from=-175.0, z_to=-320.0, material=eocene_rocks))
    geology12.add_layer(PorousLayer("Triassic Layer",        z_from=-320.0, z_to=-559.5, material=triassic_rocks))

    geologies = [geology1, geology2, geology3, geology4, geology5, geology6, geology7, geology8, geology9, geology10, geology11, geology12]

    # Estimates the shallow geothermal potentials.

    if os.path.exists(file_name):
        data_frame = pd.read_excel(file_name, index_col=False)
        calculated = list(zip(data_frame["Geology"], data_frame["L_borehole"], data_frame["borehole_spacing"]))
    else:
        data_frame = pd.DataFrame(columns=["Geology", "L_borehole", "borehole_spacing", "E_annual", "R_squared", "RMSE"])

    uncalculated = list(product(*[map(lambda geology: geology.name, geologies), [100, 200], [20, 500]]))

    while len(calculated) > 0:
        geology_name, L_borehole, borehole_spacing = calculated.pop()
        print(f"Skipping geology={geology_name}, L_borehole={L_borehole} m, borehole_spacing={borehole_spacing} m")
        uncalculated.remove((geology_name, L_borehole, borehole_spacing))

    client = mph.start(cores=8)

    while len(uncalculated) > 0:

        geology_name, L_borehole, borehole_spacing = uncalculated.pop()

        print(f"Calculating geology={geology_name}, L_borehole={L_borehole} m, borehole_spacing={borehole_spacing} m")

        params = Parameters(L_borehole=L_borehole, D_borehole=0.150, borehole_spacing=borehole_spacing, E_annual=0, num_years=50, monthly_fractions=monthly_fractions)

        geology = next(filter(lambda geology: geology.name==geology_name, geologies))

        model = init_model(client, params, geology)

        if borehole_spacing == 20:
            x = [5, 10, 20]
        elif borehole_spacing == 500:
            x = [10, 30, 40]
        else:
            raise ValueError("borehole_spacing")

        y = [eval_temp(model, x[i]) for i in range(len(x))]

        p = np.polyfit(x, y, 1)

        SS_res = np.sum((y - np.polyval(p, x))**2)
        SS_tot = np.sum((y - np.mean(y))**2)

        R_squared = 1 - SS_res / SS_tot

        RMSE = np.sqrt(np.mean((y - np.polyval(p, x))**2))

        xi = np.linspace(x[0], x[-1], 1000)
        yi = np.polyval(p, xi)

        crude_estimate = -p[1] / p[0]

        plt.figure()
        plt.plot(x, y, "bo")
        plt.plot(xi, yi, "r-")
        plt.axhline(0, ls="--", color="r")
        plt.axvline(crude_estimate, ls="--", color="r")
        plt.plot([crude_estimate], [0], "rx")
        plt.gca().set_xlim([x[0], x[-1]])
        plt.xlabel("E_annual [MWh]")
        plt.ylabel(u"T_wall [\xb0C]")
        plt.tight_layout()
        plt.show()

        print(f"geology={geology.name}, L_borehole={params.L_borehole} m, borehole_spacing={params.borehole_spacing} m, crude_estimate={crude_estimate:.6f} MWh")

        data_frame.loc[len(data_frame)] = [geology.name, L_borehole, borehole_spacing, crude_estimate, R_squared, RMSE]

        data_frame.to_excel(file_name, index=False)
