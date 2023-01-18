import statsmodels.api as sm
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

variables = ["T_surface",                   # x1
             "q_geothermal",                # x2
             "k_quaternary_deposits",       # x3
             "k_upper_oligocene_rocks",     # x4
             "k_lower_oligocene_rocks",     # x5
             "k_triassic_rocks",            # x6
             # "Cp_quaternary_deposits",      # x7
             # "Cp_upper_oligocene_rocks",    # x8
             # "Cp_lower_oligocene_rocks",    # x9
             # "Cp_triassic_rocks",           # x10
             # "rho_quaternary_deposits",     # x11
             # "rho_upper_oligocene_rocks",   # x12
             # "rho_lower_oligocene_rocks",   # x13
             # "rho_triassic_rocks",          # x14
             "phi_quaternary_deposits",     # x7
             "phi_upper_oligocene_rocks",   # x8
             "phi_lower_oligocene_rocks",   # x9
             "phi_triassic_rocks",          # x10
             "h_quaternary_deposits",       # x5
             "h_upper_oligocene_rocks",     # x6
             "h_lower_oligocene_rocks",     # x7
             "C_quaternary_deposits",      # x8
             "C_upper_oligocene_rocks",    # x9
             "C_lower_oligocene_rocks",    # x10
             "C_triassic_rocks",           # x11
]

df = pd.read_excel("sensitivity_study_database.xlsx")

df["C_quaternary_deposits"] = df["rho_quaternary_deposits"] * df["Cp_quaternary_deposits"]
df["C_upper_oligocene_rocks"] = df["rho_upper_oligocene_rocks"] * df["Cp_upper_oligocene_rocks"]
df["C_lower_oligocene_rocks"] = df["rho_lower_oligocene_rocks"] * df["Cp_lower_oligocene_rocks"]
df["C_triassic_rocks"] = df["rho_triassic_rocks"] * df["Cp_triassic_rocks"]

_df = df[variables]

X = _df.values
Y = df["E_max"].values

corr = _df[variables].corr()

print(np.amin(corr), np.amax(corr))

plt.matshow(corr, vmin=-.25, vmax=+.25, cmap="inferno")
ticks = np.arange(0,len(_df.columns),1)
plt.gca().set_xticks(ticks)
plt.xticks(rotation=90)
plt.gca().set_yticks(ticks)
plt.gca().set_xticklabels(_df.columns)
plt.gca().set_yticklabels(_df.columns)


raise SystemExit

model = sm.OLS(Y, sm.add_constant(X))

results = model.fit()

print(results.summary())

for i in range(len(variables)):
    x, y = X[:,i], Y
    p = np.polyfit(x, y, 1)
    plt.figure()
    plt.plot(x, y, "ro")
    plt.plot(x, np.polyval(p,x), "r-")
    plt.title(variables[i]+"\n"+f"{results.params[i]}"+"\n"+f"{p[0]}")

m, s = np.mean(Y), np.std(Y)

plt.figure()
plt.hist(Y)
plt.axvline(m, color="r", ls="--")
plt.axvline(m-2*s, color="b", ls="--")
plt.axvline(m+2*s, color="b", ls="--")

print(f"E_max = {m:.1f}\xb1{2*s:.1f} ({m-2*s:.1f}-{m+2*s:.1f})")
