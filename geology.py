from utils import num_to_str


class Material:
    """This class is used to store physical properties of materials."""

    def __init__(self, name, k, Cp, rho):
        self.name, self.tag = name, name.replace(" ", "_").lower()
        self.k, self.Cp, self.rho = k, Cp, rho

    def __str__(self):
        return f"Material(name={self.name}, tag={self.tag}, k={num_to_str(self.k)} W/(m\xb7K), Cp={num_to_str(self.Cp)} J/(kg\xb7K), rho={num_to_str(self.rho)} kg/m\xb3)"


class PorousMaterial(Material):
    """This class represents a material with voids."""

    def __init__(self, name, k_matrix, Cp_matrix, rho_matrix, porosity=0, k_fluid=0.6, Cp_fluid=4186, rho_fluid=1000):
        if porosity < 0 or porosity >= 1:
            raise ValueError("Porosity must be greater than or equal to zero and less than one.")
        self.porosity = porosity
        self.k_matrix, self.Cp_matrix, self.rho_matrix = k_matrix, Cp_matrix, rho_matrix
        self.k_fluid, self.Cp_fluid, self.rho_fluid = k_fluid, Cp_fluid, rho_fluid
        k_effective = (1 - porosity) * k_matrix + porosity * k_fluid
        rho_effective = (1 - porosity) * rho_matrix + porosity * rho_fluid
        C_effective = (1 - porosity) * rho_matrix * Cp_matrix + porosity * rho_fluid * Cp_fluid
        super().__init__(name, k_effective, C_effective/rho_effective, rho_effective)

    def __str__(self):
        return f"PorousMaterial(name={self.name}, tag={self.tag}, k_matrix={num_to_str(self.k_matrix)} W/(m\xb7K), Cp_matrix={num_to_str(self.Cp_matrix)} J/(kg\xb7K), rho_matrix={num_to_str(self.rho_matrix)} kg/m\xb3, k_fluid={num_to_str(self.k_fluid)} W/(m\xb7K), Cp_fluid={num_to_str(self.Cp_fluid)} J/(kg\xb7K), rho_fluid={num_to_str(self.rho_fluid)} kg/m\xb3, k={num_to_str(self.k)} W/(m\xb7K), Cp={num_to_str(self.Cp)} J/(kg\xb7K), rho={num_to_str(self.rho)} kg/m\xb3, porosity={num_to_str(100*self.porosity)} %)"


class Layer:
    """This class represents a subsurface layer in a geological model."""

    def __init__(self, name, material, z_from, z_to):
        if z_from > 0:
            raise ValueError("The layer must be located completely below the ground surface.")
        if z_to > z_from:
            raise ValueError("The top of the layer must be located above its bottom.")
        if z_to == z_from:
            raise ValueError("The layer must have a positive thickness.")
        self.name, self.tag = name, name.replace(" ", "_").lower()
        self.z_from, self.z_to, self.thickness = z_from, z_to, z_from-z_to
        self.material = material

    def split(self, z):
        """Splits this layer to two parts. One part is above the specified depth and the other part is below it."""
        if self.z_to < z and z < self.z_from:
            above = Layer(f"Upper Part of {self.name}", self.material, self.z_from, z)
            below = Layer(f"Lower Part of {self.name}", self.material, z, self.z_to)
            return [above, below]
        else:
            return [self]

    def __str__(self):
        return f"Layer(name={self.name}, tag={self.tag}, material={self.material}, z_from={num_to_str(self.z_from)} m, z_to={num_to_str(self.z_to)} m, thickness={num_to_str(self.thickness)} m)"


class PorousLayer(Layer):
    """This class represents a subsurface layer with a porous material that may include groundwater flow."""

    def __init__(self, name, material, z_from, z_to, velocity=0):
        if type(material) is not PorousMaterial:
            raise TypeError("Expected a porous material.")
        if velocity < 0:
            raise ValueError("Velocity must be greater than or equal to zero.")
        if velocity > 0 and material.porosity == 0:
            raise ValueError("Layer can not have groundwater flow if its material has zero porosity.")
        super().__init__(name, material, z_from, z_to)
        self.velocity = velocity

    def split(self, z):
        if self.z_to < z and z < self.z_from:
            above = PorousLayer(f"Upper Part of {self.name}", self.material, self.z_from, z, self.velocity)
            below = PorousLayer(f"Lower Part of {self.name}", self.material, z, self.z_to, self.velocity)
            return [above, below]
        else:
            return [self]

    def __str__(self):
        return f"PorousLayer(name={self.name}, tag={self.tag}, material={self.material}, z_from={num_to_str(self.z_from)} m, z_to={num_to_str(self.z_to)} m, thickness={num_to_str(self.thickness)} m, velocity={num_to_str(self.velocity)} m/s)"


class Geology:
    """This class represents a geological model with environmental variables and subsurface layers."""

    def __init__(self, name, T_surface, q_geothermal, layers=[]):
        self.name, self.tag = name, name.replace(" ", "_").lower()
        self.T_surface, self.q_geothermal = T_surface, q_geothermal
        self.thickness = 0
        self.has_groundwater_flow = False
        self.layers = []
        if len(layers) > 0:
            self.add_layers(layers)

    def add_layer(self, layer):
        """Adds a single layer to this geology."""
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
        self.thickness = -layer.z_to
        if type(layer) is PorousLayer and layer.velocity > 0:
            self.has_groundwater_flow = True

    def add_layers(self, layers):
        """Adds a list of layers to this geology."""
        for layer in layers:
            self.add_layer(layer)

    def split(self, z):
        """Adds a layer interface at the specified depth."""
        split_layers = []
        for layer in self.layers:
            split_layers.extend(layer.split(z))
        return Geology(self.name, self.T_surface, self.q_geothermal, split_layers)

    def __str__(self):
        layers = ", ".join([f"{layer.name} ({num_to_str(layer.thickness)} m)" for layer in self.layers])
        return f"Geology(name={self.name}, T_surface={num_to_str(self.T_surface)} \xb0C, q_geothermal={num_to_str(self.q_geothermal)} W/m\xb2, thickness={num_to_str(self.thickness)} m, layers=[{layers}])"


if __name__ == "__main__":
    # Creates materials
    sand = PorousMaterial("Sand", 1, 1000, 1800, 0.333)
    granite = Material("Granite", 3, 730, 2700)
    # Prints materials
    print("Materials", 50*"=")
    print(sand)
    print(granite)
    # Creates layers
    sandy_layer = PorousLayer("Sandy layer", sand, 0, -100, 0.123e-2)
    granitic_layer = Layer("Granitic layer", granite, -100, -200)
    # Prints layers
    print("Layers", 50*"=")
    print(sandy_layer)
    print(granitic_layer)
    # Creates geologies
    geology1 = Geology("Bedrock with overburden", 12.3, 0.04567)
    geology1.add_layer(sandy_layer)
    geology1.add_layer(granitic_layer)
    geology2 = Geology("Another geology", -12.3, 0.04567, layers=[sandy_layer, granitic_layer])
    # Prints geologies
    print("Geologies", 50*"=")
    print(geology1)
    print(geology2)
