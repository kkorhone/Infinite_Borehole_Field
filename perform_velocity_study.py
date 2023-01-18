from comsol import Parameters, init_model, eval_temp
from budapest import make_geologies
from utils import time_elapsed

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

import os, mph, time

os.environ["KMP_DUPLICATE_LIB_OK"] = "True" # Gets rid of the annoying OpenMP initialization error.

xlsx_name = r"Velocity_Study\velocity_study_v2.xlsx"

data_frame = pd.read_excel(xlsx_name)

monthly_fractions = [0.194717, 0.17216, 0.128944, 0.075402, 0.024336, 0, 0, 0, 0.025227, 0.076465, 0.129925, 0.172824]

client = mph.start(cores=8)

for i in range(len(data_frame)):

    df = data_frame.iloc[i]

    if not np.isnan(df["E_max"]):
        print(f"*** Skipping row={i+1}")
        continue
    else:
        print(f"*** Calculating row={i+1}")

    tic = time.time()

    params = Parameters(L_borehole=df["L_borehole"], D_borehole=0.150, borehole_spacing=df["borehole_spacing"], E_annual=0, num_years=50, monthly_fractions=monthly_fractions)

    geologies = make_geologies(darcy_flux=df["darcy_flux"])

    model = init_model(client, params, geologies[2])

    if df["borehole_spacing"] == 20 and df["L_borehole"] == 100:
        x = [5, 7.5, 10]
    elif df["borehole_spacing"] > 20 and df["L_borehole"] == 100:
        x = [12.5, 15, 17.5]
    elif df["borehole_spacing"] == 20 and df["L_borehole"] == 200:
        x = [10, 15, 20]
    elif df["borehole_spacing"] > 20 and df["L_borehole"] == 200:
        x = [30, 35, 40]
    else:
        raise ValueError(f"Bad borehole_spacing: {df['borehole_spacing']} m.")

    y = [eval_temp(model, x[i]) for i in range(len(x))]

    p = np.polyfit(x, y, 1)

    E_max = -p[1] / p[0]

    SS_res = np.sum((y - np.polyval(p, x))**2)
    SS_tot = np.sum((y - np.mean(y))**2)

    R_squared = 1 - SS_res / SS_tot

    RMSE = np.sqrt(np.mean((y - np.polyval(p, x))**2))

    xi = np.linspace(x[0], x[-1], 1000)
    yi = np.polyval(p, xi)

    toc = time.time()

    plt.figure()
    plt.plot(x, y, "bo")
    plt.plot(xi, yi, "r-")
    plt.axhline(0, ls="--", color="r")
    plt.axvline(E_max, ls="--", color="r")
    plt.plot([E_max], [0], "rx")
    plt.gca().set_xlim([x[0], x[-1]])
    plt.xlabel("E_max [MWh]")
    plt.ylabel(u"T_avg [\xb0C]")
    plt.title(f"R^2={R_squared:.6f} RMSE={RMSE:.6f}")
    plt.tight_layout()
    plt.savefig(f"model_{i+1:03d}.png")
    plt.show()
    plt.close()

    print(f"*** Solved row={i+1} elapsed={time_elapsed(toc-tic)} L_borehole={df['L_borehole']} m, borehole_spacing={df['borehole_spacing']} m, E_max={E_max:.6f} MWh")

    data_frame.loc[i, "E_max"] = E_max

    data_frame.to_excel(xlsx_name, index=False)
