num_samples = 100;

k_quaternary_deposits = 0.53 * np.random.randn(num_samples) + 3.0;
k_upper_oligocene_rocks = 0.53 * np.random.randn(num_samples) + 1.8;
k_lower_oligocene_rocks = 0.53 * np.random.randn(num_samples) + 1.5;
k_triassic_rocks = 0.53 * np.random.randn(num_samples) + 2.5;

Cp_quaternary_deposits = 30 * np.random.randn(num_samples) + 1800;
Cp_upper_oligocene_rocks = 30 * np.random.randn(num_samples) + 900;
Cp_lower_oligocene_rocks = 30 * np.random.randn(num_samples) + 2100;
Cp_triassic_rocks = 30 * np.random.randn(num_samples) + 850;

rho_quaternary_deposits = 64 * np.random.randn(num_samples) + 1800;
rho_upper_oligocene_rocks = 64 * np.random.randn(num_samples) + 2500;
rho_lower_oligocene_rocks = 64 * np.random.randn(num_samples) + 2000;
rho_triassic_rocks = 64 * np.random.randn(num_samples) + 2700;

porosity_quaternary_deposits = 0.01 * np.random.randn(num_samples) + 0.3;
porosity_upper_oligocene_rocks = 0.01 * np.random.randn(num_samples) + 0.1;
porosity_lower_oligocene_rocks = 0.01 * np.random.randn(num_samples) + 0.05;
porosity_triassic_rocks = 0.01 * np.random.randn(num_samples) + 0.15;

assert(all(porosity_quaternary_deposits>0));
assert(all(porosity_upper_oligocene_rocks>0));
assert(all(porosity_lower_oligocene_rocks>0));
assert(all(porosity_triassic_rocks>0));

h_quaternary_deposits = 0.01 * np.random.randn(num_samples) + 0.3
h_upper_oligocene_rocks = 0.01 * np.random.randn(num_samples) + 0.1
h_lower_oligocene_rocks = 0.01 * np.random.randn(num_samples) + 0.05
h_triassic_rocks = 0.01 * np.random.randn(num_samples) + 0.15

figure()
hist(k_quaternary_deposits, 11)
hold on
hist(k_upper_oligocene_rocks, 11)
hist(k_lower_oligocene_rocks, 11)
hist(k_triassic_rocks, 11)
hold off

figure()
hist(Cp_quaternary_deposits, 11)
hold on
hist(Cp_upper_oligocene_rocks, 11)
hist(Cp_lower_oligocene_rocks, 11)
hist(Cp_triassic_rocks, 11)
hold off

figure()
hist(rho_quaternary_deposits, 11)
hold on
hist(rho_upper_oligocene_rocks, 11)
hist(rho_lower_oligocene_rocks, 11)
hist(rho_triassic_rocks, 11)
hold off

figure()
hist(porosity_quaternary_deposits, 11)
hold on
hist(porosity_upper_oligocene_rocks, 11)
hist(porosity_lower_oligocene_rocks, 11)
hist(porosity_triassic_rocks, 11)
hold off

show()

raise SystemExit

for i in range(100):

    quaternary_deposits   = PorousMaterial("Quaternary Deposits",   k_matrix=k_quaternary_deposits[i], Cp_matrix=Cp_quaternary_deposits[i], rho_matrix=rho_quaternary_deposits[i], porosity=porosity_quaternary_deposits[i])
    upper_oligocene_rocks = PorousMaterial("Upper Oligocene Rocks", k_matrix=1.8, Cp_matrix=900,  rho_matrix=2500, porosity=0.10)
    lower_oligocene_rocks = PorousMaterial("Lower Oligocene Rocks", k_matrix=1.5, Cp_matrix=2100, rho_matrix=2000, porosity=0.05)
    triassic_rocks        = PorousMaterial("Triassic Rocks",        k_matrix=2.5, Cp_matrix=850,  rho_matrix=2700, porosity=0.15)

    geology3 = Geology("B-39",  T_surface=13.2, q_geothermal=0.0980000)

    geology3.add_layer(PorousLayer("Quaternary Layer",      z_from=0.0,    z_to=-14.4,  material=quaternary_deposits))
    geology3.add_layer(PorousLayer("Upper Oligocene Layer", z_from=-14.4,  z_to=-285.4, material=upper_oligocene_rocks))
    geology3.add_layer(PorousLayer("Lower Oligocene Layer", z_from=-285.4, z_to=-482.0, material=lower_oligocene_rocks))
    geology3.add_layer(PorousLayer("Triassic Layer",        z_from=-482.0, z_to=-650.0, material=triassic_rocks))
