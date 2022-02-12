import matplotlib.pyplot as plt
import numpy as np

Tg = 16.0
q = 0.090

h = np.array([10, 50, 100, 500])
k = np.array([1, 3, 0.5, 4])
I = np.array([0, 1, 2, 3])

def T(l, z):
    return Tg + sum(q/k[:l]*h[:l]) - sum(q/k[l]*h[:l]) - q/k[l]*z

z1 = 0
for l in range(len(h)):
    z2 = z1 - h[l]
    z = np.linspace(z1, z2, 100)
    plt.plot(T(l,z),z)
    plt.axhline(z1, ls=":")
    plt.axhline(z2, ls=":")
    z1 = z2

plt.show()
