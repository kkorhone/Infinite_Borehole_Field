import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

from sklearn.datasets import make_regression
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor

import statsmodels.api as sm

plt.rcParams["font.family"] = "serif"
plt.rcParams["font.serif"] = "Times"
plt.rcParams["font.size"] = 16
plt.rcParams["text.usetex"] = True
plt.rcParams["axes.titlesize"] = 16

fig = plt.figure(figsize=(10.5, 7.5))
ax = fig.subplots(2, 2)

for i, L_borehole in enumerate([100, 200]):
    for j, borehole_spacing in enumerate([20, 100]):
        
        df = pd.read_excel(f"E:\\Work\\Budapest\\Shallow_Geothermal_Potential\\Sensitivity_Study_{L_borehole}m_{borehole_spacing}m\\sensitivity_study_database.xlsx")

        x = df["E_max"].values
        
        m, s = np.mean(x), np.std(x)

        plt.axes(ax[i, j])
        plt.hist(x, 21, ec="k", fc=[0.85,0.85,0.85])
        plt.axvline(m-2*s, ls="--", color="r", lw=2)
        plt.axvline(m+2*s, ls="--", color="r", lw=2)
        plt.axvline(m, ls="-", color="r", lw=2)
        plt.gca().set_ylim([0, 14])
        plt.gca().set_yticks([0, 2, 4, 6, 8, 10, 12, 14])
        plt.title("$H = %d$ m, $B = %d$ m: $E_\mathrm{max} = %.1f\pm%.1f$ MWh/a" % (L_borehole, borehole_spacing, m, 2*s), fontsize=16)
        
        if i == 1:
            plt.xlabel("$E_\mathrm{max}$ [MWh/a]")
        if j == 0:
            plt.ylabel("Frequency")
        else:
            plt.gca().set_yticklabels([])

        if i == 0 and j == 0:
            plt.gca().set_xlim(5.5, 10)
            plt.gca().set_xticks([6, 7, 8, 9, 10])
            plt.text(5.6, 12.5, "(a)")
        elif i == 0 and j == 1:
            plt.gca().set_xlim(7, 23)
            plt.gca().set_xticks([8, 10, 12, 14, 16, 18, 20, 22])
            plt.text(7.3, 12.5, "(b)")
        elif i == 1 and j == 0:
            plt.gca().set_xlim(12, 18.5)
            plt.gca().set_xticks([12, 13, 14, 15, 16, 17, 18])
            plt.text(12.15, 12.5, "(c)")
        elif i == 1 and j == 1:
            plt.gca().set_xlim(16, 48)
            plt.gca().set_xticks([20, 25, 30, 35, 40, 45])
            plt.text(16.8, 12.5, "(d)")
            
        #plt.text(plt.gca().get_xlim()[0], 12, f"{L_borehole} {borehole_spacing}")
        
        plt.tight_layout()
        plt.savefig(f"hist_{L_borehole}m_{borehole_spacing}m.png", dpi=300)
        
        for col in df.columns:
            x = df[col]
            m, s, v = np.mean(x), np.std(x), np.var(x)
            print(f"{col:<30s} {m:.3f} {s:.3f} {v:.3f}")


# L_borehole, borehole_spacing, T_surface, q_geothermal, k_quaternary_deposits, k_upper_oligocene_rocks, k_lower_oligocene_rocks, k_triassic_rocks, Cp_quaternary_deposits, Cp_upper_oligocene_rocks, Cp_lower_oligocene_rocks, Cp_triassic_rocks, rho_quaternary_deposits, rho_upper_oligocene_rocks, rho_lower_oligocene_rocks, rho_triassic_rocks, phi_quaternary_deposits, phi_upper_oligocene_rocks, phi_lower_oligocene_rocks, phi_triassic_rocks, h_quaternary_deposits, h_upper_oligocene_rocks, h_lower_oligocene_rocks, E_max

plt.savefig("sensitivity.png", dpi=300)
