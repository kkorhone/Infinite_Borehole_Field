from matplotlib import pyplot as plt
from scipy.io import loadmat
import numpy as np

plt.rcParams["font.family"] = "serif"
plt.rcParams["font.serif"] = "Times"
plt.rcParams["font.size"] = 13
plt.rcParams["text.usetex"] = True

data = loadmat("results_influence_radius_v3.mat")

borehole_spacing = data["borehole_spacing"].reshape(-1)

X = data["X"]

fig = plt.figure(figsize=(6, 4))

ax1 = fig.add_subplot(111)
ax2 = ax1.twinx()

for i in range(24):
    if i % 2 == 0:
        h1, = ax1.plot(borehole_spacing, X[i,:], "r-")
    else:
        h2, = ax2.plot(borehole_spacing, X[i,:], "b-")

h3 = ax1.axvline(100, color="k", ls="--")

plt.legend((h1, h2, h3), ("100-m deep boreholes", "200-m deep boreholes", "Influence radius ($B_\infty$)"), framealpha=1, handlelength=1)

ax1.set_xlabel("$B$ [m]")

ax1.set_ylabel("$E_\mathrm{max}$ from 100-m deep boreholes [MWh/a]", color="r")
ax2.set_ylabel("$E_\mathrm{max}$ from 200-m deep boreholes [MWh/a]", color="b")

dy1 = 2
dy2 = 4
dx = 20

xlim = [20, 140]
ylim1 = ax1.get_ylim()
ylim2 = ax2.get_ylim()

ax1.set_xlim(xlim)
ax2.set_xlim(xlim)

xlim = [np.ceil(xlim[0]/dy2)*dy2, np.floor(xlim[1]/dy2)*dy2]
ylim1 = [np.ceil(ylim1[0]/dy1)*dy1, np.floor(ylim1[1]/dy1)*dy1]
ylim2 = [np.ceil(ylim2[0]/dy2)*dy2, np.floor(ylim2[1]/dy2)*dy2]

yticks1 = np.arange(ylim1[0], ylim1[1]+dy1, dy1)
yticks2 = np.arange(ylim2[0], ylim2[1]+dy2, dy2)

ax1.tick_params(axis="y", colors="r")
ax2.tick_params(axis="y", colors="b")

#ax1.set_xticks(np.arange(20, 150, 10))
#ax1.set_yticks(yticks1)
#ax2.set_yticks(yticks2)

ax2.spines["left"].set_color("r")
ax2.spines["right"].set_color("b")

plt.tight_layout()

plt.savefig("influence_radii.png", dpi=300)

plt.show()
