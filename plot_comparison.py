from matplotlib import pyplot as plt
import pandas as pd
import numpy as np

df = pd.read_excel("comparison.xlsx")

E_eed = df["E_eed"]
E_gpot = df["E_gpot"]
E_comsol = df["E_comsol"]

bins = np.arange(-2.6, 1.2, 0.2)

print(E_comsol-E_eed)
print(E_comsol-E_gpot)

plt.hist(E_comsol-E_eed, bins, fc="None", ec="b")
#plt.hist(E_comsol-E_gpot, bins, fc="None", ec="r")
#plt.gca().set_xticks(bins)
