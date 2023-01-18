from geology import Geology, PorousLayer, PorousMaterial
from comsol import Parameters, init_model, eval_temp
from utils import time_elapsed

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

import os, mph, time

os.environ["KMP_DUPLICATE_LIB_OK"] = "True" # Gets rid of the annoying OpenMP initialization error.

xlsx_name = "sensitivity_study_database.xlsx"

data_frame = pd.read_excel(xlsx_name)

monthly_fractions = [0.194717, 0.17216, 0.128944, 0.075402, 0.024336, 0, 0, 0, 0.025227, 0.076465, 0.129925, 0.172824]

client = mph.start(cores=8)

start_tic = time.time()

for i in range(len(data_frame)):

    df = data_frame.iloc[i]

    if not np.isnan(df["E_max"]):
        print(f"*** Skipping row={i+1}")
        continue
    else:
        print(f"*** Calculating row={i+1}")

    tic = time.time()

    params = Parameters(L_borehole=df["L_borehole"], D_borehole=0.150, borehole_spacing=df["borehole_spacing"], E_annual=0, num_years=50, monthly_fractions=monthly_fractions)

    quaternary_deposits   = PorousMaterial("Quaternary Deposits",   k_matrix=df["k_quaternary_deposits"],   Cp_matrix=df["Cp_quaternary_deposits"],   rho_matrix=df["rho_quaternary_deposits"],   porosity=df["phi_quaternary_deposits"])
    upper_oligocene_rocks = PorousMaterial("Upper Oligocene Rocks", k_matrix=df["k_upper_oligocene_rocks"], Cp_matrix=df["Cp_upper_oligocene_rocks"], rho_matrix=df["rho_upper_oligocene_rocks"], porosity=df["phi_upper_oligocene_rocks"])
    lower_oligocene_rocks = PorousMaterial("Lower Oligocene Rocks", k_matrix=df["k_lower_oligocene_rocks"], Cp_matrix=df["Cp_lower_oligocene_rocks"], rho_matrix=df["rho_lower_oligocene_rocks"], porosity=df["phi_lower_oligocene_rocks"])
    triassic_rocks        = PorousMaterial("Triassic Rocks",        k_matrix=df["k_triassic_rocks"],        Cp_matrix=df["Cp_triassic_rocks"],        rho_matrix=df["rho_triassic_rocks"],        porosity=df["phi_triassic_rocks"])

    geology = Geology("B-39",  T_surface=df["T_surface"], q_geothermal=df["q_geothermal"])

    z1 = -df["h_quaternary_deposits"]
    z2 = -df["h_quaternary_deposits"]-df["h_upper_oligocene_rocks"]
    z3 = -df["h_quaternary_deposits"]-df["h_upper_oligocene_rocks"]-df["h_lower_oligocene_rocks"]

    geology.add_layer(PorousLayer("Quaternary Layer",      z_from=0,  z_to=z1,   material=quaternary_deposits))
    geology.add_layer(PorousLayer("Upper Oligocene Layer", z_from=z1, z_to=z2,   material=upper_oligocene_rocks))
    geology.add_layer(PorousLayer("Lower Oligocene Layer", z_from=z2, z_to=z3,   material=lower_oligocene_rocks))
    geology.add_layer(PorousLayer("Triassic Layer",        z_from=z3, z_to=-650, material=triassic_rocks))

    model = init_model(client, params, geology)

    if df["borehole_spacing"] == 20:
        x = [5, 10, 15]
    elif df["borehole_spacing"] == 100:
        x = [10, 22.5, 35]
    else:
        raise ValueError(f"Bad borehole_spacing: {df['borehole_spacing']} m.")

    x = [10, 20, 40]
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
    
    end_toc = time.time()

    print(f"*** total_elapsed={time_elapsed(end_toc-start_tic)}")
