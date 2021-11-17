import numpy as np


class Material:
    """This class is used to store physical properties of materials."""

    def __init__(self, name, k, Cp, rho):
        self.name = " ".join([token.capitalize() for token in name.split()])
        self.k = k # Thermal conductivity
        self.Cp = Cp # Specific heat capacity
        self.rho = rho # Density
        self.C = rho * Cp # Volumetric heat capacity
        
    def __str__(self):
        return f"Material(name={self.name}, k={self.k} W/(m*K), Cp={self.Cp} J/(kg*K), rho={self.rho} kg/m^3, C={self.C/1000000} MJ/(m^3*K))"


class Geology:
    """This class represents a geological model that stores both environmental variables and geological layers."""
    
    def __init__(self, name, T_surface, q_geothermal, layers=[]):
        self.name = " ".join([token.capitalize() for token in name.split()])
        self.T_surface = T_surface # Ground surface temperature
        self.q_geothermal = q_geothermal # Geothermal heat flux density
        self.thickness = 0 # Thickness of the model
        self.layers = [] # Geological layers
        if len(layers) > 0:
            self.add_layers(layers)
        
    def add_layer(self, layer):
        """Adds a single layer to the geology."""
        if len(self.layers) == 0:
            # Adds the top layer.
            if layer.z_from == 0:
                self.layers.append(layer)
            else:
                raise ValueError("The first layer must begin from the ground level.")
        else:
            # Adds a layer to the bottom of the geology.
            if layer.z_from == self.layers[-1].z_to:
                self.layers.append(layer)
            else:
                raise ValueError("Layers can be added only to the bottom of the geology.")
        self.thickness = -layer.z_to
                
    def add_layers(self, layers):
        """Adds a list of layers to the geology."""
        for layer in layers:
            self.add_layer(layer)
            
    def split(self, z):
        split_layers = []
        for layer in self.layers:
            split_layers.extend(layer.split(z))
        return Geology(self.name, self.T_surface, self.q_geothermal, split_layers)

    def __str__(self):
        layers = ", ".join([f"{layer.name} ({str(np.round(layer.thickness,3))} m)" for layer in self.layers])
        return f"Geology(name={self.name}, T_surface={self.T_surface} degC, q_geothermal={1000*self.q_geothermal} mW/m^2, thickness={self.thickness} m, layers=[{layers}])"
        

class Layer:
    """This class represents a geological layer with a material and vertical extent."""
    
    def __init__(self, name, z_from, z_to, matrix_material, fluid_material=None, porosity=0):
        if z_to > z_from:
            raise ValueError("The top of the layer must be located above its bottom.")
        if porosity < 0 or porosity >= 1:
            raise ValueError("The porosity of the layer must be >= 0 and < 1.")
        self.name = " ".join([token.capitalize() for token in name.split()])
        self.tag = name.lower().replace(" ", "_")
        self.z_from = z_from
        self.z_to = z_to
        self.thickness = z_from - z_to
        if porosity > 0:
            k_effective = (1.0 - porosity) * matrix_material.k + porosity * fluid_material.k
            rho_effective = (1.0 - porosity) * matrix_material.rho + porosity * fluid_material.rho
            Cp_effective = (1.0 - porosity) * (matrix_material.C + porosity * fluid_material.C) / rho_effective
            name = f"Porous {matrix_material.name}"
            self.material = Material(name, k_effective, rho_effective, Cp_effective)
        else:
            self.material = matrix_material
            
    def split(self, z):
        """Splits this layer into two parts that are located above and below the specified depth."""
        if self.z_to < z and z < self.z_from:
            above = Layer(f"{self.name} (Upper Half)", self.z_from, z, self.material)
            below = Layer(f"{self.name} (Lower Half)", z, self.z_to, self.material)
            return [above, below]
        else:
            return [self]

    def __str__(self):
        return f"Layer(name={self.name} material={self.material}, z_from={self.z_from} m, z_to={self.z_to} m, thickness={self.thickness} m)"


if __name__ == "__main__":
    water = Material("Water", 0.6, 4186, 1000)
    sand = Material("Sand", 1, 1000, 1800)
    granite = Material("Granite", 3, 730, 2700)
    geology = Geology("Simple", 12.3, 0.04567)
    geology.add_layers([Layer("Soil", 0, -50, sand, water, 0.3), Layer("Bedrock", -50, -200, granite)])
    print("----------")
    print("Materials:")
    print("----------")
    print(water)
    print(sand)
    print(granite)
    print("-------")
    print("Layers:")
    print("-------")
    for layer in geology.layers:
        print(layer)
    print("--------")
    print("Geology:")
    print("--------")
    print(geology)
