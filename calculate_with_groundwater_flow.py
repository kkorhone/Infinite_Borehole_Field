from comsol import Parameters, init_model, eval_temp, save_model
from geology import Material, Geology, Layer
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import os, mph


os.environ["KMP_DUPLICATE_LIB_OK"] = "True" # Gets rid of the annoying OpenMP initialization error.


if __name__ == "__main__":

    file_name = "results_v7w.xlsx"

    # Sets up the monthly energy consumption profile.

    monthly_fractions = [0.194717, 0.17216, 0.128944, 0.075402, 0.024336, 0, 0, 0, 0.025227, 0.076465, 0.129925, 0.172824]

    # Creates materials for the geological models.

    quaternary      = Material("Quaternary",      3.0, 1800, 1800)
    miocene         = Material("Miocene",         1.8,  840, 2200)
    upper_oligocene = Material("Upper Oligocene", 1.8,  900, 2500)
    lower_oligocene = Material("Lower Oligocene", 1.5, 2100, 2000)
    eocene          = Material("Eocene",          2.0,  840, 2100)
    triassic        = Material("Triassic",        2.5,  850, 2700)

    # Sets up the groundwater flow velocities.

    v_quaternary      = 1.0e-08
    v_miocene         = 1.0e-09
    v_upper_oligocene = 0.5e-09
    v_lower_oligocene = 1.0e-10
    v_eocene          = 1.0e-09
    v_triassic        = 1.0e-08

    # Sets up the porosities.

    eps_quaternary      = 0.30
    eps_miocene         = 0.10
    eps_upper_oligocene = 0.10
    eps_lower_oligocene = 0.05
    eps_eocene          = 0.15
    eps_triassic        = 0.15

    # Creates the geologies.

    geology1  = Geology("B-21",  13.2, 0.0938000)
    geology2  = Geology("B-30",  13.2, 0.0905000)
    geology3  = Geology("B-39",  13.2, 0.0980000)
    geology4  = Geology("B-48",  13.2, 0.0867000)
    geology5  = Geology("B-63",  13.2, 0.0928000)
    geology6  = Geology("B-13",  13.2, 0.0835810)
    geology7  = Geology("B-56",  13.2, 0.0836250)
    geology8  = Geology("B-179", 13.2, 0.0828568)
    geology9  = Geology("B-180", 13.2, 0.0827390)
    geology10 = Geology("Pm_1",  13.2, 0.0714500)
    geology11 = Geology("B-64",  13.2, 0.0911600)
    geology12 = Geology("B-38",  13.2, 0.1016000)

    # Adds the layers to the geologies.

    geology1.add_layers([ Layer("Quaternary", 0,  -15.30, quaternary, eps_quaternary, v_quaternary), Layer("Lower Oligocene",  -15.30, -523.00, lower_oligocene, eps_lower_oligocene, v_lower_oligocene), Layer("Eocene",          -523.00,  -633.00, eocene,          eps_eocene,          v_eocene),          Layer("Triassic",         -633.00,  -766.40, triassic,        eps_triassic,        v_triassic)])
    geology2.add_layers([ Layer("Quaternary", 0,  -16.50, quaternary, eps_quaternary, v_quaternary), Layer("Lower Oligocene",  -16.50, -551.00, lower_oligocene, eps_lower_oligocene, v_lower_oligocene), Layer("Eocene",          -551.00,  -695.30, eocene,          eps_eocene,          v_eocene),          Layer("Triassic",         -695.30,  -800.00, triassic,        eps_triassic,        v_triassic)])
    geology3.add_layers([ Layer("Quaternary", 0,  -14.40, quaternary, eps_quaternary, v_quaternary), Layer("Upper Oligocene",  -14.40, -285.40, upper_oligocene, eps_upper_oligocene, v_upper_oligocene), Layer("Lower Oligocene", -285.40,  -482.00, lower_oligocene, eps_lower_oligocene, v_lower_oligocene), Layer("Triassic",         -482.00,  -650.00, triassic,        eps_triassic,        v_triassic)])
    geology4.add_layers([ Layer("Quaternary", 0,   -7.90, quaternary, eps_quaternary, v_quaternary), Layer("Miocene",           -7.90, -360.30, miocene,         eps_miocene,         v_miocene),         Layer("Upper Oligocene", -360.30,  -507.00, upper_oligocene, eps_upper_oligocene, v_upper_oligocene), Layer("Lower Oligocene",  -507.00, -1081.70, lower_oligocene, eps_lower_oligocene, v_lower_oligocene), Layer("eocene",   -1081.70, -1128.00, eocene,   eps_eocene,   v_eocene), Layer("triassic", -1128.00, -1198.00, triassic, eps_triassic, v_triassic)])
    geology5.add_layers([ Layer("Quaternary", 0,  -24.85, quaternary, eps_quaternary, v_quaternary), Layer("Miocene",          -24.85, -700.00, miocene,         eps_miocene,         v_miocene),         Layer("Upper Oligocene", -700.00,  -701.00, upper_oligocene, eps_upper_oligocene, v_upper_oligocene)])
    geology6.add_layers([ Layer("Quaternary", 0,  -12.00, quaternary, eps_quaternary, v_quaternary), Layer("Miocene",          -12.00, -424.82, miocene,         eps_miocene,         v_miocene),         Layer("Upper Oligocene", -424.82,  -647.42, upper_oligocene, eps_upper_oligocene, v_upper_oligocene), Layer("Lower Oligocene",  -647.42, -1194.00, lower_oligocene, eps_lower_oligocene, v_lower_oligocene), Layer("eocene",   -1194.00, -1234.82, eocene,   eps_eocene,   v_eocene)])
    geology7.add_layers([ Layer("Quaternary", 0,  -15.00, quaternary, eps_quaternary, v_quaternary), Layer("Miocene",          -15.00, -439.10, miocene,         eps_miocene,         v_miocene),         Layer("Upper Oligocene", -439.10,  -775.40, upper_oligocene, eps_upper_oligocene, v_upper_oligocene), Layer("Lower Oligocene",  -775.40, -1095.00, lower_oligocene, eps_lower_oligocene, v_lower_oligocene), Layer("eocene",   -1095.00, -1172.00, eocene,   eps_eocene,   v_eocene), Layer("triassic", -1172.00, -1233.00, triassic, eps_triassic, v_triassic)])
    geology8.add_layers([ Layer("Miocene",    0, -351.00, miocene,    eps_miocene,    v_miocene),    Layer("Upper Oligocene", -351.00, -600.00, upper_oligocene, eps_upper_oligocene, v_upper_oligocene), Layer("Lower Oligocene", -600.00, -1025.00, lower_oligocene, eps_lower_oligocene, v_lower_oligocene), Layer("Eocene",          -1025.00, -1240.00, eocene,          eps_eocene,          v_eocene),          Layer("triassic", -1240.00, -1304.50, triassic, eps_triassic, v_triassic)])
    geology9.add_layers([ Layer("Miocene",    0, -347.30, miocene,    eps_miocene,    v_miocene),    Layer("Upper Oligocene", -347.30, -580.00, upper_oligocene, eps_upper_oligocene, v_upper_oligocene), Layer("Lower Oligocene", -580.00, -1027.00, lower_oligocene, eps_lower_oligocene, v_lower_oligocene), Layer("Eocene",          -1027.00, -1228.40, eocene,          eps_eocene,          v_eocene),          Layer("triassic", -1228.40, -1270.00, triassic, eps_triassic, v_triassic)])
    geology10.add_layers([Layer("Quaternary", 0,  -10.00, quaternary, eps_quaternary, v_quaternary), Layer("Miocene",          -10.00, -180.00, miocene,         eps_miocene,         v_miocene),         Layer("Upper Oligocene", -180.00,  -280.00, upper_oligocene, eps_upper_oligocene, v_upper_oligocene), Layer("Lower Oligocene",  -280.00, -1070.00, lower_oligocene, eps_lower_oligocene, v_lower_oligocene), Layer("Eocene",   -1070.00, -1340.00, eocene,   eps_eocene,   v_eocene), Layer("triassic", -1340.00, -1735.00, triassic, eps_triassic, v_triassic)])
    geology11.add_layers([Layer("Quaternary", 0,  -13.40, quaternary, eps_quaternary, v_quaternary), Layer("Miocene",          -13.40, -319.00, miocene,         eps_miocene,         v_miocene),         Layer("Upper Oligocene", -319.00,  -600.00, upper_oligocene, eps_upper_oligocene, v_upper_oligocene)])
    geology12.add_layers([Layer("Quaternary", 0,  -21.00, quaternary, eps_quaternary, v_quaternary), Layer("Lower Oligocene",  -21.00, -175.00, lower_oligocene, eps_lower_oligocene, v_lower_oligocene), Layer("Eocene",          -175.00,  -320.00, eocene,          eps_eocene,          v_eocene),          Layer("Triassic",         -320.00,  -559.50, triassic,        eps_triassic,        v_triassic)])

    # Estimates the shallow geothermal potentials.

    if os.path.exists(file_name):
        data_frame = pd.read_excel(file_name)
        print(data_frame)
    else:
        data_frame = pd.DataFrame(columns=["Geology", "L_borehole", "borehole_spacing", "E_annual", "R_squared", "RMSE"])

    geology = [geology1, geology2, geology3, geology4, geology5, geology6, geology7, geology8, geology9, geology10, geology11, geology12]

    L_borehole = [100, 150, 200]
    borehole_spacing = [20, 500]

    client = mph.start(cores=8)

    for i in range(len(L_borehole)):
        for j in range(len(borehole_spacing)):
            for k in range(len(geology)):

                df = data_frame[(data_frame["L_borehole"]==L_borehole[i]) & (data_frame["borehole_spacing"]==borehole_spacing[j]) & (data_frame["Geology"]==geology[k].name)]

                if len(df) > 0:
                    print(f"Skipping geology={geology[k].name}, L_borehole={L_borehole[i]} m, borehole_spacing={borehole_spacing[j]} m")
                    continue
                else:
                    print(f"Calculating geology={geology[k].name}, L_borehole={L_borehole[i]} m, borehole_spacing={borehole_spacing[j]} m")

                params = Parameters(L_borehole=L_borehole[i], D_borehole=0.150, borehole_spacing=borehole_spacing[j], E_annual=0, num_years=50, monthly_fractions=monthly_fractions)

                model = init_model(client, params, geology[k])

                x = [0, 20, 40]
                y = [eval_temp(model, _x) for _x in x]

                p = np.polyfit(x, y, 1)

                SS_res = np.sum((y - np.polyval(p, x))**2)
                SS_tot = np.sum((y - np.mean(y))**2)

                R_squared = 1 - SS_res / SS_tot

                rmse = np.sqrt(np.mean((y - np.polyval(p, x))**2))

                xi = np.linspace(x[0], x[-1], 1000)
                yi = np.polyval(p, xi)

                crude_estimate = p[1] / -p[0]

                plt.figure()
                plt.plot(x, y, "bo")
                plt.plot(xi, yi, "r-")
                plt.axhline(0, ls="--", color="r")
                plt.axvline(crude_estimate, ls="--", color="r")
                plt.plot([crude_estimate], [0], "rx")
                plt.gca().set_xlim([x[0], x[-1]])
                plt.xlabel("E_annual [MWh]")
                plt.ylabel(u"temp [\xb0C]")
                plt.tight_layout()
                plt.show()

                print(f"geology={geology[k].name}, L_borehole={params.L_borehole} m, borehole_spacing={params.borehole_spacing} m, crude_estimate={crude_estimate:.6f} MWh")

                data_frame.loc[len(data_frame)] = [geology[k].name, L_borehole[i], borehole_spacing[j], crude_estimate, R_squared, rmse]

                data_frame.to_excel(file_name)
