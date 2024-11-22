import random
import string



"""
Register: Function

Registers and creates a new neuron using the Neuron class
"""
def register(name, registry, cglobals, type, bias=None, limit=None):
    iden = ''.join(random.choices(string.ascii_letters + string.digits, k=10))
    if type == "s":
        cglobals[name] = sNeuron(iden)
    elif type == "n":
        cglobals[name] = Neuron(iden, bias)
    elif type == "b":
        cglobals[name] = bNeuron(iden, limit, bias)
    elif type == "e":
        cglobals[name] = eNeuron(iden, bias)
    else:
        raise ValueError("Must be s, n, b or e")
    registry[iden] = name



"""
getByID: Function

Gets the name of a variable neuron using its ID
"""
def getByID(id, registry):
    obj = registry[id]
    return obj



"""
Neuron: Class

Base for the entire library. It makes a neuron.
"""    
class Neuron:
    def __init__(self, iden, bias=None):
        # Set a random bias if none is provided
        self.bias = bias if bias is not None else random.uniform(-5, 5)
        # Generate a random 10-character alphanumeric ID
        self.iden = iden
        # Placeholder for inputs
        self.inputs = []

        self.connections = {}

    def bind(self, neuron, weight):
        self.connections[neuron.iden] = weight

    def input(self, value, registry, cglobals):
        """Accepts an input value (e.g., from another neuron)."""
        value += self.bias
        for i in range(len(self.connections)):
            keys = list(self.connections.keys())
            values = list(self.connections.values())
            outN = getByID(keys[i], registry)
            cglobals[outN].input(float(values[i])*value, registry, cglobals)
        
    def __repr__(self):
        return f"Neuron(ID={self.iden}, Bias={self.bias})"

    def b(self, bias):
        self.bias = bias

    def w(self, weight, iden):
        self.connections[iden] = weight



"""
sNeuron: Class

Based on the main Neuron class, it makes a neuron that is more
adapted for being a start neuron, so where the entire network begins.
"""
class sNeuron:
    def __init__(self, iden):
        # Generate a random 10-character alphanumeric ID
        self.iden = iden
        # Placeholder for inputs
        self.inputs = []

        self.connections = {}

    def bind(self, neuron, weight):
        self.connections[neuron.iden] = weight

    def input(self, value, registry, cglobals):
        """Accepts an input value (e.g., from another neuron)."""
        for i in range(len(self.connections)):
            keys = list(self.connections.keys())
            values = list(self.connections.values())

            outN = getByID(keys[i], registry)
            cglobals[outN].input(float(values[i])*value, registry, cglobals)
            

    def __repr__(self):
        return f"Neuron(ID={self.iden}, Bias=N/A)"

    def w(self, weight, iden):
        self.connections[iden] = weight



"""
bNeuron: Class

Buffer Neurons take multiple inputs until it reaches the limit at which
point it will add them up, add the bias, and input it to the next neurons.
"""
class bNeuron:
    def __init__(self, iden, limit, bias=None):
        # Set a random bias if none is provided
        self.bias = bias if bias is not None else random.uniform(-5, 5)
        # Generate a random 10-character alphanumeric ID
        self.iden = iden
        # Placeholder for inputs
        self.inputs = []

        self.connections = {}

        self.limit = limit

        self.storage = []

    def bind(self, neuron, weight):
        self.connections[neuron.iden] = weight

    def input(self, value, registry, cglobals):
        """Accepts an input value (e.g., from another neuron)."""
        if len(self.storage) == self.limit:
            value = 0
            for i in range(len(storage)):
                value += storage[i]
            value += bias
            self.storage = []
            for i in range(len(self.connections)):
                keys = list(self.connections.keys())
                values = list(self.connections.values())

                outN = getByID(keys[i], registry)
                cglobals[outN].input(float(values[i])*value, registry, cglobals)
        else:
            self.storage += value
            

    def output(self, value):
        print(value)
        

    def __repr__(self):
        return f"Neuron(ID={self.iden}, Bias={self.bias})"

    def b(self, bias):
        self.bias = bias

    def w(self, weight, iden):
        self.connections[iden] = weight





"""
eNeuron: Class

The ends of the network. They take a input, add the bias and just print it.
"""
class eNeuron:
    def __init__(self, iden, bias=None):
        # Set a random bias if none is provided
        self.bias = bias if bias is not None else random.uniform(-5, 5)
        # Generate a random 10-character alphanumeric ID
        self.iden = iden
        # Placeholder for inputs
        self.inputs = []

        self.connections = {}

    def input(self, value, registry, cglobals):
        """Accepts an input value (e.g., from another neuron)."""
        value += self.bias
        print(value)
            

    def __repr__(self):
        return f"Neuron(ID={self.iden}, Bias={self.bias})"

    def b(self, bias):
        self.bias = bias