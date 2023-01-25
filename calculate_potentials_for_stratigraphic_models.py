from comsol import Parameters, init_model, eval_temp
from geology import Geology, PorousMaterial, PorousLayer
from budapest import make_geologies
from itertools import product
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import os, mph


os.environ["KMP_DUPLICATE_LIB_OK"] = "True" # Gets rid of the annoying OpenMP initialization error.


def calculate_potentials(with_groundwater_flow, plot_fits=False):

    monthly_fractions = [0.194717, 0.17216, 0.128944, 0.075402, 0.024336, 0, 0, 0, 0.025227, 0.076465, 0.129925, 0.172824]

    assert np.abs(np.sum(monthly_fractions) - 1) < 1e-6

    T_min = 0.0

    if with_groundwater_flow:
        file_name = "results_with_groundwater_flow.xlsx"
        geologies = make_geologies(v_groundwater="predefined")
    else:
        file_name = "results_without_groundwater_flow.xlsx"
        geologies = make_geologies(v_groundwater=0)

    data_frame = pd.read_excel(file_name)

    client = mph.start(cores=8)

    for i in range(len(data_frame)):

        row = data_frame.iloc[i]

        if not np.isnan(row["E_max"]):
            print(f"Skipping geology={row['Geology']} L_borehole={row['L_borehole']} m, borehole_spacing={row['borehole_spacing']} m, E_annual={row['E_max']} MWh")
            continue
        else:
            print(f"Calculating geology={row['Geology']} L_borehole={row['L_borehole']} m, borehole_spacing={row['borehole_spacing']} m")

        params = Parameters(L_borehole=row["L_borehole"], D_borehole=0.150, borehole_spacing=row["borehole_spacing"], E_annual=0, num_years=50, monthly_fractions=monthly_fractions)

        geology = list(filter(lambda item: item.name==row["Geology"], geologies))

        assert len(geology) == 1

        geology = geology[0]

        model = init_model(client, params, geology)

        # This is a cheap solution to the minimization problem in Eq. (5).
        # Using, for example, scipy.optimize.fminbound() would require 10-20
        # COMSOL simulations to be run which would be very time consuming.
        # Instead, we can take advantage of the observation that the borehole
        # wall temperature is linear in the maximal annually extractable energy.
        # So, we can calculate just 3 points and fit a regression line to those
        # points: T_wall = p[0] * E_annual + p[1], where p is a regression line
        # fit to the data points using np.polyfit(). Now E_max can be found as:
        # E_max = (T_min - p[1]) / p[0], where T_min is the minimal allowed
        # temperature of the borehole wall.

        x = [10, 30, np.nan]
        y = [np.nan, np.nan, np.nan]

        for j in range(len(x)):
            y[j] = eval_temp(model, x[j])
            if j == 1:
                p = np.polyfit(x[0:2], y[0:2], 1)
                x[2] = -p[1] / p[0]

        p = np.polyfit(x, y, 1)

        SS_res = np.sum((y - np.polyval(p, x))**2)
        SS_tot = np.sum((y - np.mean(y))**2)

        R_squared = 1 - SS_res / SS_tot

        RMSE = np.sqrt(np.mean((y - np.polyval(p, x))**2))

        xi = np.linspace(0.95*np.min(x), 1.05*np.max(x), 1000)
        yi = np.polyval(p, xi)

        E_max = (T_min - p[1]) / p[0]

        if plot_fits:
            plt.figure()
            plt.plot(x, y, "bo")
            plt.plot(xi, yi, "r-")
            plt.axhline(T_min, ls="--", color="r")
            plt.axvline(E_max, ls="--", color="r")
            plt.plot([E_max], [T_min], "ro")
            plt.gca().set_xlim([np.min(xi), np.max(xi)])
            plt.xlabel("E_annual [MWh]")
            plt.ylabel(u"T_ave [\xb0C]")
            plt.tight_layout()
            plt.savefig(f"fit_without_groundwater_flow_{row['Geology'].lower().replace('-','_')}_{row['L_borehole']}_{row['borehole_spacing']}.png")
            plt.close()

        print(f"Result E_max={E_max:.3f} R_squared={R_squared:.6f} RMSE={RMSE:.6f}")

        data_frame.loc[i, ["E_max", "R_squared", "RMSE"]] = [E_max, R_squared, RMSE]
        data_frame.to_excel(file_name, index=False)

if __name__ == "__main__":

    calculate_potentials(with_groundwater_flow=True, plot_fits=True)
    calculate_potentials(with_groundwater_flow=False, plot_fits=True)
