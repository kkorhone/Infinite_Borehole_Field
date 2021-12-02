from comsol import Parameters, init_model, eval_temp
from geology import Material, Geology, Layer
# from scipy.optimize import minimize_scalar
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import os, mph


os.environ["KMP_DUPLICATE_LIB_OK"] = "True" # Gets rid of the ...


if __name__ == "__main__":

    # The monthly energy consumption fractions.

    monthly_fractions = [0.194717, 0.17216, 0.128944, 0.075402, 0.024336, 0, 0, 0, 0.025227, 0.076465, 0.129925, 0.172824]

    # Creates materials for the geological models.

    quaternary      = Material("Quaternary",      3.0, 1800, 1800)
    miocene         = Material("Miocene",         1.8,  840, 2200)
    upper_oligocene = Material("Upper Oligocene", 1.8,  900, 2500)
    lower_oligocene = Material("Lower Oligocene", 1.5, 2100, 2000)
    eocene          = Material("Eocene",          2.0,  840, 2100)
    triassic        = Material("Triassic",        2.5,  850, 2700)

    # Creates the geological models.

    geology1 = Geology("B-21",  13.2, 0.0938000)
    geology2 = Geology("B-30",  13.2, 0.0905000)
    geology3 = Geology("B-39",  13.2, 0.0980000)
    geology4 = Geology("B-48",  13.2, 0.0867000)
    geology5 = Geology("B-63",  13.2, 0.0928000)
    geology6 = Geology("B-13",  13.2, 0.0835810)
    geology7 = Geology("B-56",  13.2, 0.0836250)
    geology8 = Geology("B-179", 13.2, 0.0828568)
    geology9 = Geology("B-180", 13.2, 0.0827390)

    # Adds layers to the geological models.

    geology1.add_layers([Layer("Quaternary", 0,  -15.30, quaternary, 0.30), Layer("Lower Oligocene",  -15.30, -523.00, lower_oligocene, 0.05), Layer("Eocene",          -523.00,  -633.00, eocene,          0.15), Layer("Triassic",         -633.00,  -766.40, triassic,        0.15)])
    geology2.add_layers([Layer("Quaternary", 0,  -16.50, quaternary, 0.30), Layer("Lower Oligocene",  -16.50, -551.00, lower_oligocene, 0.05), Layer("Eocene",          -551.00,  -695.30, eocene,          0.15), Layer("Triassic",         -695.30,  -800.00, triassic,        0.15)])
    geology3.add_layers([Layer("Quaternary", 0,  -14.40, quaternary, 0.30), Layer("Upper Oligocene",  -14.40, -285.40, upper_oligocene, 0.10), Layer("Lower Oligocene", -285.40,  -482.00, lower_oligocene, 0.05), Layer("Triassic",         -482.00,  -650.00, triassic,        0.15)])
    geology4.add_layers([Layer("Quaternary", 0,   -7.90, quaternary, 0.30), Layer("Miocene",           -7.90, -360.30, miocene,         0.10), Layer("Upper Oligocene", -360.30,  -507.00, upper_oligocene, 0.10), Layer("Lower Oligocene",  -507.00, -1081.70, lower_oligocene, 0.05), Layer("eocene",   -1081.70, -1128.00, eocene,   0.15), Layer("triassic", -1128.00, -1198.00, triassic, 0.15)])
    geology5.add_layers([Layer("Quaternary", 0,  -24.85, quaternary, 0.30), Layer("Miocene",          -24.85, -700.00, miocene,         0.10), Layer("Upper Oligocene", -700.00,  -701.00, upper_oligocene, 0.10)])
    geology6.add_layers([Layer("Quaternary", 0,  -12.00, quaternary, 0.30), Layer("Miocene",          -12.00, -424.82, miocene,         0.10), Layer("Upper Oligocene", -424.82,  -647.42, upper_oligocene, 0.10), Layer("Lower Oligocene",  -647.42, -1194.00, lower_oligocene, 0.05), Layer("eocene",   -1194.00, -1234.82, eocene,   0.15)])
    geology7.add_layers([Layer("Quaternary", 0,  -15.00, quaternary, 0.30), Layer("Miocene",          -15.00, -439.10, miocene,         0.10), Layer("Upper Oligocene", -439.10,  -775.40, upper_oligocene, 0.10), Layer("Lower Oligocene",  -775.40, -1095.00, lower_oligocene, 0.05), Layer("eocene",   -1095.00, -1172.00, eocene,   0.15), Layer("triassic", -1172.00, -1233.00, triassic, 0.15)])
    geology8.add_layers([Layer("Miocene",    0, -351.00,    miocene, 0.10), Layer("Upper Oligocene", -351.00, -600.00, upper_oligocene, 0.10), Layer("Lower Oligocene", -600.00, -1025.00, lower_oligocene, 0.05), Layer("Eocene",          -1025.00, -1240.00, eocene,          0.15), Layer("triassic", -1240.00, -1304.50, triassic, 0.15)])
    geology9.add_layers([Layer("Miocene",    0, -347.30,    miocene, 0.10), Layer("Upper Oligocene", -347.30, -580.00, upper_oligocene, 0.10), Layer("Lower Oligocene", -580.00, -1027.00, lower_oligocene, 0.05), Layer("Eocene",          -1027.00, -1228.40, eocene,          0.15), Layer("triassic", -1228.40, -1270.00, triassic, 0.15)])

    # Evaluates borehole the shallow geothermal potentials.

    data_frame = pd.DataFrame(columns=["Geology", "L_borehole", "borehole_spacing", "E_annual", "cost"])

    geology = [geology1, geology2, geology3, geology4, geology5, geology6, geology7, geology8, geology9]

    L_borehole = [150, 300]
    borehole_spacing = [20, 500]

    # options = {"disp": True} # , "xatol": 0.001}

    client = mph.start(cores=8)

    for i in range(len(borehole_spacing)):
        for j in range(len(L_borehole)):

            params = Parameters(L_borehole=L_borehole[j], D_borehole=0.150, borehole_spacing=borehole_spacing[i], E_annual=30, num_years=50, monthly_fractions=monthly_fractions)

            for k in range(len(geology)):

                model = init_model(client, params, geology[k])

                # Crude estimate of the annually extractable energy.

                if borehole_spacing[i] == 20:
                    x = [0, 10, 20, 30]
                else:
                    x = [20, 40, 60]
                y = [eval_temp(model,x[n]) for n in range(len(x))]

                p = np.polyfit(x, y, 1)

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

                # bounds = [0.95*crude_estimate, 1.05*crude_estimate]

                # print(f"geology={geology[k].name}, L_borehole={params.L_borehole} m, borehole_spacing={params.borehole_spacing} m, crude_estimate={crude_estimate:.6f} MWh, bounds=[{bounds[0]:.6f} MWh, {bounds[1]:.6f} MWh]")

                # result = minimize_scalar(lambda x: np.abs(min_ave_temp(model,x)), method="bounded", bounds=bounds, options=options)

                # print(f"geology={geology[k].name}, L_borehole={params.L_borehole} m, borehole_spacing={params.borehole_spacing} m, result.x={result.x:.6f} MWh, result.fun={result.fun:.9f} K")

                # data_frame.loc[len(data_frame)] = [geology[k].name, L_borehole[j], borehole_spacing[i], result.x, result.fun]

                data_frame.loc[len(data_frame)] = [geology[k].name, L_borehole[j], borehole_spacing[i], crude_estimate, 0]

                data_frame.to_excel("results_v4.xlsx")
