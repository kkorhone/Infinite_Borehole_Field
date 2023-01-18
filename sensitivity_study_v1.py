import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

plt.rcParams["font.family"] = "serif"
plt.rcParams["font.serif"] = "Times"
plt.rcParams["font.size"] = 16
plt.rcParams["text.usetex"] = True
plt.rcParams["axes.titlesize"] = 16

df = pd.read_excel(r"E:\Work\Budapest\Shallow_Geothermal_Potential\sensitivity_study_database.xlsx")

for i, column in enumerate(df.columns):
    
    x = df[column].values
    
    m, s = np.mean(x), np.std(x)

    if column == "L_borehole":
        continue
    elif column == "borehole_spacing":
        continue
    elif column == "T_surface":
        label = u"Ground surface temperature [\xb0C]"
        title = f"{m:.1f}$\pm${2*s:.1f} \xb0C"
    elif column == "q_geothermal":
        x *= 1000
        m, s = np.mean(x), np.std(x)
        label = u"Geothermal heat flux density [mW/m\xb2]"
        title = f"{m:.3f}$\pm${2*s:.3f} mW/m\xb2"
    elif column == "E_max":
        label = "Maximal annually extractable energy [MWh/a]"
        title = f"{m:.1f}$\pm${2*s:.1f} MWh/a"
    else:
    
        toks = column.split("_")
        unit = " ".join(toks[1:]).capitalize()
        
        if toks[0] == "h":
            label = f"Thickness of {unit} [m]"
            title = f"{m:.1f}$\pm${2*s:.1f} m"
        elif toks[0] == "rho":
            label = f"Density of {unit} [kg/m$^3$]"
            title = f"{m:.0f}$\pm${2*s:.0f} kg/m\xb3"
        elif toks[0] == "Cp":
            label = f"Specific heat capacity of {unit} [J/(kg$\cdot$K)]"
            title = f"{m:.0f}$\pm${2*s:.0f} J/(kg$\cdot$K)"
        elif toks[0] == "k":
            label = f"Thermal conductivity of {unit} [W/(m$\cdot$K)]"
            title = f"{m:.2f}$\pm${2*s:.2f} W/(m$\cdot$K)"
        elif toks[0] == "phi":
            x *= 100
            m, s = np.mean(x), np.std(x)
            label = f"Porosity of {unit} [\%]"
            title = f"{m:.1f}$\pm${2*s:.1f} \%"

    plt.figure()
    plt.hist(x, 21, ec="k", fc=[0.85,0.85,0.85])
    plt.axvline(m-2*s, ls="--", color="r", lw=2)
    plt.axvline(m+2*s, ls="--", color="r", lw=2)
    plt.axvline(m, ls="-", color="r", lw=2)
    
    plt.title(title)
    plt.xlabel(label)
    plt.ylabel("Count")
    
    plt.tight_layout()
    plt.savefig(f"hist_{i:02d}.png", dpi=300)

    print(column,"===>",label)
