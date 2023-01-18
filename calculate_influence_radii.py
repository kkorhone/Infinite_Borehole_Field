from comsol import Parameters, init_model, eval_temp
from budapest import make_geologies
from itertools import product
import matplotlib.pyplot as plt
import numpy as np
import os, mph


os.environ["KMP_DUPLICATE_LIB_OK"] = "True" # Gets rid of the annoying OpenMP initialization error.


if __name__ == "__main__":

    file_name = "results_influence_radius.txt"

    monthly_fractions = [0.194717, 0.17216, 0.128944, 0.075402, 0.024336, 0, 0, 0, 0.025227, 0.076465, 0.129925, 0.172824]

    geologies = make_geologies(v_groundwater=0)

    cases = list(product(*[map(lambda geology: geology.name, geologies), [100, 200]]))

    #client = mph.start(cores=6)

    X = [20, 30, 40, 50, 60, 70, 80, 90, 100, 110, 120, 130, 140]

    file = open(file_name, "w")
    file.write(" ".join(str(_X) for _X in X) + "\n")
    file.close()

    for i in range(12): case = cases.pop(); print(case)

    print(cases)

    while len(cases) > 0:

        geology_name, L_borehole = cases.pop()

        geology = next(filter(lambda geology: geology.name==geology_name, geologies))

        Y = []

        file = open(file_name, "a")
        file.write(f"geology={geology.name}, L_borehole={L_borehole} m\n")
        file.close()

        for borehole_spacing in X:

            print(f"Calculating geology={geology.name}, L_borehole={L_borehole} m, borehole_spacing={borehole_spacing} m")

            params = Parameters(L_borehole=L_borehole, D_borehole=0.150, borehole_spacing=borehole_spacing, E_annual=0, num_years=50, monthly_fractions=monthly_fractions)

            #model = init_model(client, params, geology)

            x = [10, 20, 40]
            #y = [eval_temp(model, x[i]) for i in range(len(x))]
            y = [1, 2, 3]

            p = np.polyfit(x, y, 1)

            SS_res = np.sum((y - np.polyval(p, x))**2)
            SS_tot = np.sum((y - np.mean(y))**2)

            R_squared = 1 - SS_res / SS_tot

            RMSE = np.sqrt(np.mean((y - np.polyval(p, x))**2))

            xi = np.linspace(x[0], x[-1], 1000)
            yi = np.polyval(p, xi)

            crude_estimate = -p[1] / p[0]

            Y.append(crude_estimate)

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

        file = open(file_name, "a")
        file.write(" ".join(str(_Y) for _Y in Y) + "\n")
        file.close()
