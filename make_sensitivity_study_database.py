import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

num_samples = 100
L_borehole = 200
borehole_spacing = 100

while True:

    T_surface = 1.0 * np.random.randn(num_samples) + 13.2
    q_geothermal = 11.3 * np.random.randn(num_samples) + 92.2

    k_quaternary_deposits = 0.53 * np.random.randn(num_samples) + 3.0
    k_upper_oligocene_rocks = 0.53 * np.random.randn(num_samples) + 1.8
    k_lower_oligocene_rocks = 0.53 * np.random.randn(num_samples) + 1.5
    k_triassic_rocks = 0.53 * np.random.randn(num_samples) + 2.5

    Cp_quaternary_deposits = 30 * np.random.randn(num_samples) + 1800
    Cp_upper_oligocene_rocks = 30 * np.random.randn(num_samples) + 900
    Cp_lower_oligocene_rocks = 30 * np.random.randn(num_samples) + 2100
    Cp_triassic_rocks = 30 * np.random.randn(num_samples) + 850

    rho_quaternary_deposits = 64 * np.random.randn(num_samples) + 1800
    rho_upper_oligocene_rocks = 64 * np.random.randn(num_samples) + 2500
    rho_lower_oligocene_rocks = 64 * np.random.randn(num_samples) + 2000
    rho_triassic_rocks = 64 * np.random.randn(num_samples) + 2700

    phi_quaternary_deposits = 0.01 * np.random.randn(num_samples) + 0.3
    phi_upper_oligocene_rocks = 0.01 * np.random.randn(num_samples) + 0.1
    phi_lower_oligocene_rocks = 0.01 * np.random.randn(num_samples) + 0.05
    phi_triassic_rocks = 0.01 * np.random.randn(num_samples) + 0.15

    h_quaternary_deposits = 5 * np.random.randn(num_samples) + 15
    h_upper_oligocene_rocks = 20 * np.random.randn(num_samples) + 270
    h_lower_oligocene_rocks = 20 * np.random.randn(num_samples) + 200

    try:

        assert all(k_quaternary_deposits>0.5)
        assert all(k_upper_oligocene_rocks>0.5)
        assert all(k_lower_oligocene_rocks>0.5)
        assert all(k_triassic_rocks>0.5)

        assert all(Cp_quaternary_deposits>0)
        assert all(Cp_upper_oligocene_rocks>0)
        assert all(Cp_lower_oligocene_rocks>0)
        assert all(Cp_triassic_rocks>0)

        assert all(rho_quaternary_deposits>0)
        assert all(rho_upper_oligocene_rocks>0)
        assert all(rho_lower_oligocene_rocks>0)
        assert all(rho_triassic_rocks>0)

        assert all(phi_quaternary_deposits>0.01)
        assert all(phi_upper_oligocene_rocks>0.01)
        assert all(phi_lower_oligocene_rocks>0.01)
        assert all(phi_triassic_rocks>0.01)

        assert all(h_quaternary_deposits>5)
        assert all(h_upper_oligocene_rocks>10)
        assert all(h_lower_oligocene_rocks>10)

        assert all(q_geothermal>50)

        break

    except:

        pass

bins = np.arange(0, 5, 0.1)
plt.figure()
plt.hist(k_quaternary_deposits, bins, alpha=0.5)
plt.hist(k_upper_oligocene_rocks, bins, alpha=0.5)
plt.hist(k_lower_oligocene_rocks, bins, alpha=0.5)
plt.hist(k_triassic_rocks , bins, alpha=0.5)

bins = np.arange(740, 2260, 20)
plt.figure()
plt.hist(Cp_quaternary_deposits, bins, alpha=0.5)
plt.hist(Cp_upper_oligocene_rocks, bins, alpha=0.5)
plt.hist(Cp_lower_oligocene_rocks, bins, alpha=0.5)
plt.hist(Cp_triassic_rocks , bins, alpha=0.5)

bins = np.arange(1500, 3000, 20)
plt.figure()
plt.hist(rho_quaternary_deposits, bins, alpha=0.5)
plt.hist(rho_upper_oligocene_rocks, bins, alpha=0.5)
plt.hist(rho_lower_oligocene_rocks, bins, alpha=0.5)
plt.hist(rho_triassic_rocks , bins, alpha=0.5)

bins = np.arange(0, 350, 5)
plt.figure()
plt.hist(h_quaternary_deposits, bins, alpha=0.5)
plt.hist(h_upper_oligocene_rocks, bins, alpha=0.5)
plt.hist(h_lower_oligocene_rocks, bins, alpha=0.5)

bins = np.arange(50, 140, 5)
plt.figure()
plt.hist(q_geothermal, bins, alpha=0.5)

bins = np.arange(9, 18, 0.5)
plt.figure()
plt.hist(T_surface, bins, alpha=0.5)

plt.figure()

for i in range(num_samples):

    z1 = -h_quaternary_deposits[i]
    z2 = -h_quaternary_deposits[i]-h_upper_oligocene_rocks[i]
    z3 = -h_quaternary_deposits[i]-h_upper_oligocene_rocks[i]-h_lower_oligocene_rocks[i]

    plt.plot([i,i],[0,z1],"r-")
    plt.plot([i,i],[z1,z2], "g-")
    plt.plot([i,i],[z2,z3], "b-")
    plt.plot([i,i],[z3,-650], "c")

df = pd.DataFrame(columns=["L_borehole", "borehole_spacing", "T_surface", "q_geothermal", "k_quaternary_deposits", "k_upper_oligocene_rocks", "k_lower_oligocene_rocks", "k_triassic_rocks", "Cp_quaternary_deposits", "Cp_upper_oligocene_rocks", "Cp_lower_oligocene_rocks", "Cp_triassic_rocks", "rho_quaternary_deposits", "rho_upper_oligocene_rocks", "rho_lower_oligocene_rocks", "rho_triassic_rocks", "phi_quaternary_deposits", "phi_upper_oligocene_rocks", "phi_lower_oligocene_rocks", "phi_triassic_rocks", "h_quaternary_deposits", "h_upper_oligocene_rocks", "h_lower_oligocene_rocks", "E_max"])

df["L_borehole"] = L_borehole * np.ones(num_samples)
df["borehole_spacing"] = borehole_spacing * np.ones(num_samples)

df["k_quaternary_deposits"] = k_quaternary_deposits
df["k_upper_oligocene_rocks"] = k_upper_oligocene_rocks
df["k_lower_oligocene_rocks"] = k_lower_oligocene_rocks
df["k_triassic_rocks"] = k_triassic_rocks

df["Cp_quaternary_deposits"] = Cp_quaternary_deposits
df["Cp_upper_oligocene_rocks"] = Cp_upper_oligocene_rocks
df["Cp_lower_oligocene_rocks"] = Cp_lower_oligocene_rocks
df["Cp_triassic_rocks"] = Cp_triassic_rocks

df["rho_quaternary_deposits"] = rho_quaternary_deposits
df["rho_upper_oligocene_rocks"] = rho_upper_oligocene_rocks
df["rho_lower_oligocene_rocks"] = rho_lower_oligocene_rocks
df["rho_triassic_rocks"] = rho_triassic_rocks

df["phi_quaternary_deposits"] = phi_quaternary_deposits
df["phi_upper_oligocene_rocks"] = phi_upper_oligocene_rocks
df["phi_lower_oligocene_rocks"] = phi_lower_oligocene_rocks
df["phi_triassic_rocks"] = phi_triassic_rocks

df["h_quaternary_deposits"] = h_quaternary_deposits
df["h_upper_oligocene_rocks"] = h_upper_oligocene_rocks
df["h_lower_oligocene_rocks"] = h_lower_oligocene_rocks

df["T_surface"] = T_surface
df["q_geothermal"] = q_geothermal * 1e-3

df.to_excel("sensitivity_study_database.xlsx", index=False)
