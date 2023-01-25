# ================================================================================
# This script is used to estimate the influence of groundwater flow on the results
# ================================================================================

from comsol import Parameters, init_model, eval_temp
from budapest import make_geologies
from itertools import product
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import os, mph


os.environ["KMP_DUPLICATE_LIB_OK"] = "True" # Gets rid of the annoying OpenMP initialization error.


if __name__ == "__main__":

    file_name = "groundwater_threshold.xlsx"

    monthly_fractions = [0.194717, 0.17216, 0.128944, 0.075402, 0.024336, 0, 0, 0, 0.025227, 0.076465, 0.129925, 0.172824]

    v_groundwater = np.logspace(-9, -5, 9)

    L_borehole = 200
    borehole_spacing = 20

    client = mph.start(cores=16)

    for i in range(len(v_groundwater)):

        geologies = make_geologies(v_groundwater=v_groundwater[i])

        geology_name, L_borehole, borehole_spacing, v_groundwater = uncalculated.pop()

        print(f"Calculating geology={geology_name}, L_borehole={L_borehole} m, borehole_spacing={borehole_spacing} m, v_groundwater={v_groundwater} m")

        params = Parameters(L_borehole=L_borehole, D_borehole=0.150, borehole_spacing=borehole_spacing, E_annual=0, num_years=50, monthly_fractions=monthly_fractions)

        geology = next(filter(lambda geology: geology.name==geology_name, geologies))

        for layer in geology.layers:
            layer.velocity = v_groundwater

        model = init_model(client, params, geology)

        client.clear()
        #client.save(f"model_{L_borehole}_{borehole_spacing}_{}

        if borehole_spacing == 100:
            x = [50, 100, 150]
        else:
            x = [5, 10, 20]
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

        print(f"geology={geology.name}, L_borehole={params.L_borehole} m, borehole_spacing={borehole_spacing} m, v_groundwater={v_groundwater} m/s, crude_estimate={crude_estimate:.6f} MWh")

        data_frame.loc[len(data_frame)] = [geology.name, L_borehole, borehole_spacing, v_groundwater, crude_estimate, R_squared, RMSE]

        data_frame.to_excel(file_name, index=False)
