from matplotlib import pyplot as plt
import pandas as pd
import numpy as np

plt.rcParams["font.family"] = "serif"
plt.rcParams["font.serif"] = "Times"
plt.rcParams["font.size"] = 13
plt.rcParams["text.usetex"] = True

file = open("results_influence_radius_v2.txt")

borehole_spacing = np.array([int(token) for token in file.readline().split()])

data_frame = pd.DataFrame(columns=["Geology", "L_borehole", "borehole_spacing", "E_annual"])

while True:
    try:
        tokens = file.readline().replace("=", " ").replace(",", "").strip().split(" ")
        geology, L_borehole = tokens[1], int(tokens[3])
        E_annual = [float(tok) for tok in file.readline().strip().split(" ")]
        for i in range(len(borehole_spacing)):
            data_frame.loc[len(data_frame)] = [geology, L_borehole, borehole_spacing[i], E_annual[i]]
    except:
        break

geologies = data_frame["Geology"].unique()

fig = plt.figure(figsize=(6, 4))
ax1 = fig.add_subplot(111)
ax2 = ax1.twinx()

#ax1.axvspan(100, 140, color=[0.85,0.85,0.85])#, alpha=0.5)

for geology in geologies:

    df = data_frame[data_frame["Geology"]==geology]

    for L_borehole in df["L_borehole"].unique():

        _df = df[df["L_borehole"]==L_borehole]

        x, y = _df[["borehole_spacing", "E_annual"]].values.T

        if L_borehole == 100:
            h1, = ax1.plot(x, y, "b-")
        elif L_borehole == 200:
            h2, = ax2.plot(x, y, "r-")
        else:
            raise ValueError(f"Strange borehole length: {L_borehole}.")

h3 = ax1.axvline(100, color="k", ls="--")

plt.legend((h1, h2, h3), ("100-m deep boreholes", "200-m deep boreholes", "Influence radius"), framealpha=1, handlelength=1)

ax1.set_xlabel("$B$ [m]")

ax1.set_ylabel("$E_{ann}$ from 100-m deep boreholes [MWh]")
ax2.set_ylabel("$E_{ann}$ from 200-m deep boreholes [MWh]")

ax1.set_xlim([20, 140])
ax2.set_xlim([20, 140])

plt.tight_layout()

plt.savefig("influence_radii.png", dpi=300)

plt.show()
