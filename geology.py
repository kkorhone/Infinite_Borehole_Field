import numpy as np


class Material:
    """This class is used to store physical properties of materials."""

    def __init__(self, name, k, Cp, rho):
        self.name = " ".join([token.capitalize() for token in name.replace("_", " ").split()])
        self.tag = self.name.replace(" ", "_").lower()
        self.k = k # Thermal conductivity [W/(m*K)]
        self.Cp = Cp # Specific heat capacity [J/(kg*K)]
        self.rho = rho # Density [kg/m^3]
        self.C = self.rho * self.Cp # Volumetric heat capacity [J/(m^3*K)]

    def __str__(self):
        return f"Material(name={self.name}, tag={self.tag}, k={self.k} W/(m\xb7K), Cp={self.Cp} J/(kg\xb7K), rho={self.rho} kg/m\xb3, C={self.C/1000000} MJ/(m\xb3\xb7K))"


class Geology:
    """This class represents a geological model including both environmental variables and geological layers."""

    def __init__(self, name, T_surface, q_geothermal, layers=[]):
        self.name = " ".join([token.capitalize() for token in name.replace("_", " ").split()])
        self.T_surface = T_surface # Ground surface temperature [degC]
        self.q_geothermal = q_geothermal # Geothermal heat flux density [W/m^2]
        self.thickness = 0 # Thickness of the model [m]
        self.has_porous_layers = False # True if the model has at least one porous layer
        self.has_groundwater_flow = False # True if the model has at least one layer with groundwater flow
        self.layers = [] # The layers in the model
        if len(layers) > 0:
            self.add_layers(layers)

    def add_layer(self, layer):
        """Adds a single layer to the geology."""
        if len(self.layers) == 0:
            # Adds a top layer.
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
        if layer.porosity > 0:
            self.has_porous_layers = True
        if layer.velocity > 0:
            self.has_groundwater_flow = True
        self.thickness = -layer.z_to

    def add_layers(self, layers):
        """Adds a list of layers to the geology."""
        for layer in layers:
            self.add_layer(layer)

    def split(self, z):
        """Adds a layer interface at the depth z."""
        split_layers = []
        for layer in self.layers:
            split_layers.extend(layer.split(z))
        return Geology(self.name, self.T_surface, self.q_geothermal, split_layers)

    def __str__(self):
        layers = ", ".join([f"{layer.name} ({str(np.round(layer.thickness,3))} m)" for layer in self.layers])
        return f"Geology(name={self.name}, T_surface={self.T_surface} \xb0C, q_geothermal={1000*self.q_geothermal} mW/m\xb2, thickness={self.thickness} m, has_porous_layers={self.has_porous_layers}, layers=[{layers}])"


class Layer:
    """This class represents a geological layer with a vertical extent, material, and porosity."""

    def __init__(self, name, z_from, z_to, material, porosity=0, velocity=0):
        if z_from > 0:
            raise ValueError("The layer must be located below the zero level.")
        if z_to > z_from:
            raise ValueError("The top of the layer must be located above its bottom.")
        if porosity < 0 or porosity >= 1:
            raise ValueError("Porosity must be greater than or equal to zero and less than one.")
        if velocity < 0:
            raise ValueError("Velocity must be greater than or equal to zero.")
        if velocity > 0 and porosity == 0:
            raise ValueError("Layer can not have groundwater flow if it has zero porosity.")
        self.name = " ".join([token.capitalize() for token in name.replace("_", " ").split()])
        self.tag = self.name.replace(" ", "_").lower()
        self.z_from = z_from
        self.z_to = z_to
        self.thickness = z_from - z_to
        self.material = material
        self.porosity = porosity
        self.velocity = velocity

    def split(self, z):
        """Splits this layer to two parts. One part is above the depth z and the other is below the depth z."""
        if self.z_to < z and z < self.z_from:
            above = Layer(f"Upper Part of {self.name}", self.z_from, z, self.material, self.porosity, self.velocity)
            below = Layer(f"Lower Part of {self.name}", z, self.z_to, self.material, self.porosity, self.velocity)
            return [above, below]
        else:
            return [self]

    def __str__(self):
        return f"Layer(name={self.name}, tag={self.tag}, z_from={self.z_from} m, z_to={self.z_to} m, thickness={self.thickness} m, material={self.material}, porosity={self.porosity}, velocity={self.velocity} m/s)"


if __name__ == "__main__":
    # Creates materials
    water = Material("Water", 0.6, 4186, 1000)
    sand = Material("Sand", 1, 1000, 1800)
    granite = Material("Granite", 3, 730, 2700)
    # Prints materials
    print(water)
    print(sand)
    print(granite)
    # Creates geologies
    geology1 = Geology("bedrock with overburden", 12.3, 0.04567)
    geology1.add_layers([Layer("overburden", 0, -50, sand, 0.3), Layer("bedrock", -50, -200, granite)])
    geology2 = Geology("granitic geology", 12.3, 0.04567)
    geology2.add_layers([Layer("granite", 0, -200, granite)])
    # Prints layers
    for layer in geology1.layers:
        print(layer)
    for layer in geology2.layers:
        print(layer)
    # Prints geologies
    print(geology1)
    print(geology2)
