import pandas as pd

df = pd.read_excel("results_shallow_geothermal_potentials.xlsx")

for geology_name in df["Geology"].unique():
    _df = df[df["Geology"]==geology_name]
    