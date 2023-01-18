import statsmodels.api as sm
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

variables = ["T_surface",                   # 1
             "q_geothermal",                # 2
             #"k_quaternary_deposits",       # 3
             "k_upper_oligocene_rocks",     # 4
             #"k_lower_oligocene_rocks",     # 5
             #"k_triassic_rocks",            # 6
             #"phi_quaternary_deposits",     # 7
             #"phi_upper_oligocene_rocks",   # 8
             #"phi_lower_oligocene_rocks",   # 9
             #"phi_triassic_rocks",          # 10
             #"h_quaternary_deposits",       # 11
             #"h_upper_oligocene_rocks",     # 12
             #"h_lower_oligocene_rocks",     # 13
             #"C_quaternary_deposits",       # 14
             #"C_upper_oligocene_rocks",     # 15
             #"C_lower_oligocene_rocks",     # 16
             #"C_triassic_rocks",            # 17
]

df = pd.read_excel(r"E:\Work\Budapest\Shallow_Geothermal_Potential\Sensitivity_Study_v1\sensitivity_study_database.xlsx")

df["C_quaternary_deposits"] = df["rho_quaternary_deposits"] * df["Cp_quaternary_deposits"] * 1e-6
df["C_upper_oligocene_rocks"] = df["rho_upper_oligocene_rocks"] * df["Cp_upper_oligocene_rocks"] * 1e-6
df["C_lower_oligocene_rocks"] = df["rho_lower_oligocene_rocks"] * df["Cp_lower_oligocene_rocks"] * 1e-6
df["C_triassic_rocks"] = df["rho_triassic_rocks"] * df["Cp_triassic_rocks"] * 1e-6

_df = df[variables]

X = _df.values
Y = df["E_max"].values

corr = _df[variables].corr()

print(np.amin(corr), np.amax(corr))

#plt.matshow(corr, vmin=-.25, vmax=+.25, cmap="inferno")
#ticks = np.arange(0,len(_df.columns),1)
#plt.gca().set_xticks(ticks)
#plt.xticks(rotation=90)
#plt.gca().set_yticks(ticks)
#plt.gca().set_xticklabels(_df.columns)
#plt.gca().set_yticklabels(_df.columns)
#raise SystemExit

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
plt.hist(Y, density=True)
plt.axvline(m, color="r", ls="--")
plt.axvline(m-2*s, color="b", ls="--")
plt.axvline(m+2*s, color="b", ls="--")

print(f"E_max = {m:.1f}\xb1{2*s:.1f} ({m-2*s:.1f}-{m+2*s:.1f})")
