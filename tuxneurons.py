import random
import string
import math

####################################################################################################
########## SECTION 1 ###############################################################################
####### PUBLIC FUNCTIONS ###########################################################################
####################################################################################################





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
Network: Function

Creates a new network using the Neuron class.
I suck at loops so some (most) of the code is generated by Tabnine Autocomplete.
Thank god that autocompletion is a thing.
I've tested this and it works.
"""
def network(registry, cglobals, sn, hl, hn, en):
    """
    Network: Function

    Creates a new network using the Neuron class

    sn: start neurons
    hl: hidden layers
    hn: hidden neurons
    en: end neurons
    registry: the registry of the network
    cglobals: the global variables of the network
    """
    
    # Creates the network
    tn = sn + (hl*hn) + en
    for i in range(sn):
        register(f"s{i}", registry, cglobals, "s", 0)
    for i in range(hl):
        for j in range(hn):
            register(f"n{i}_{j}", registry, cglobals, "n", 0)
    for i in range(en):
        register(f"e{i}", registry, cglobals, "e", 0)
    
    # Binds the neurons
    for i in range(sn):
        for j in range(hn):
            cglobals[f"s{i}"].bind(cglobals[f"n0{j}"], 1)
    for i in range(hl-1):
        for j in range(hn):
            for k in range(en):
                cglobals[f"n{i}_{j}"].bind(cglobals[f"n{i+1}_{k}"], 1)
    # Bind the neurons from the second to last layer to the end neurons
    for i in range(hn):
        for j in range(en):
            cglobals[f"n{hl-1}_{i}"].bind(cglobals[f"e{j}"], 1)
        


"""
getByID: Function

Gets the name of a variable neuron using its ID
"""
def getByID(id, registry):
    obj = registry[id]
    return obj










####################################################################################################
########## SECTION 2 ###############################################################################
######## Neuron Classes ############################################################################
####################################################################################################





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
        
        self.parents = 0

    def bind(self, neuron, weight):
        self.connections[neuron.iden] = weight
        neuron.parents += 1
        

    def input(self, value, registry, cglobals):
        """Accepts an input value (e.g., from another neuron)."""
        self.inputs.append(value)
        if len(self.inputs) == self.parents:
            value = relu(sum(self.inputs) + self.bias)

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
        neuron.parents += 1

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

This feature has been implemented into the default neuron, but it is here just 
in case anyone needs it. 
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
        self.storage.append(value)

        """Accepts an input value (e.g., from another neuron)."""
        if len(self.storage) >= self.limit:
            value = 0
            for i in range(len(self.storage)):
                value += self.storage[i]
            value += self.bias
            self.storage = []
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
eNeuron: Class

The ends of the network. They take a input, add the bias and just print it.
"""
class eNeuron:
    def __init__(self, iden, bias=None):
        # Set a random bias if none is provided
        self.bias = bias if bias is not None else random.uniform(-5, 5)
        # Generate a random 10-character alphanumeric ID
        self.iden = iden
        
        self.inputs = []

        self.result = 0
        
        self.parents = 0

    def input(self, value, registry, cglobals):
        """Accepts an input value (e.g., from another neuron)."""
        self.inputs.append(value)
        if len(self.inputs) == self.parents:
            value = sig(sum(self.inputs) + self.bias)
            self.result = value

    def __repr__(self):
        return f"Neuron(ID={self.iden}, Bias={self.bias})"

    def b(self, bias):
        self.bias = bias










####################################################################################################
########## SECTION 3 ###############################################################################
########## Training ################################################################################
####################################################################################################





'''
The format for the dataset is a list of tupples, wich each tupple containing
2 lists. Example:

dataset = [
    ([0, 0], [0]),
    ([0, 1], [1]),
    ([1, 0], [1])
]

Which means each tupple is a entry of training data.
And the first list in a tupple is the list of inputs, while the second list
is a list of the expected, correct outputs.
'''





def sig(x):
    """
    The sigmoid function.

    Maps any real-valued number to a value between 0 and 1.

    The sigmoid function is defined as 1 / (1 + e^(-x)).

    Parameters:
    x (float): The input to the function.

    Returns:
    float: The output of the function.
    """
    return 1/(1 + (math.e**(-x)))





def tanh(x):
    """
    The Hyperbolic Tangent function.

    Maps any real-valued number to a value between -1 and 1.

    The hyperbolic tangent function is defined as (e^x - e^(-x)) / (e^x + e^(-x)).

    Parameters:
    x (float): The input to the function.

    Returns:
    float: The output of the function.
    """
    return (math.e**x - math.e**(-x)) / (math.e**x + math.e**(-x))





def relu(x):
    """
    The ReLU (Rectified Linear Unit) function.

    Maps any real-valued number to its positive part.

    The ReLU function is defined as max(0, x).

    Parameters:
    x (float): The input to the function.

    Returns:
    float: The output of the function.
    """
    if x > 0:
        return x
    else:
        return 0
    
    
    
    
    
"""
# For those who can implement the derivative of Softmax
# (I don't have the patience to do this anymore)

def sm(x: list, ind: None):
    s = 0
    for i in range(len(x)):
        s += math.e**float(x[i])
    if ind == None:
        r = []
        for i in range(len(x)):
            r.append((math.e**float(x[i]))/s)
        return r
    else:
        return math.e**float(x[ind])/s
"""





def desig(x):
    """
    The derivative of the Sigmoid function.
    
    Returns sig(x) * (1 - sig(x))
    """
    return sig(x) * (1-sign(x))





def detanh(x):
    """
    The derivative of the Hyperbolic Tangent function.
    
    Returns 1 - tanh(x)^2
    """
    
    return 1 - tanh(x)**2





def derelu(x):
    """
    The derivative of the Relu function.
    Returns 1 if x is greater than 0, and 0 if not.
    """
    
    if x > 0:
        return 1
    else:
        return 0





def av(l: list):
    """
    Returns the average of the elements in the list l.

    Parameters
    ----------
    l : list
        The list of numbers to average.

    Returns
    -------
    float
        The average of the elements in l.
    """
    return sum(l) / len(l)
    




def error(target: list, actual: list) -> float:
    """
    Calculate the Mean Squared Error (MSE) between target and actual outputs.

    :param target: List of lists containing the correct outputs (ground truth).
    :param actual: List of lists containing the predicted outputs.
    :return: Mean Squared Error (float).
    """
    squared_errors = []

    for i in range(len(target)):
        for j in range(len(target[i])):
            squared_errors.append((target[i][j] - actual[i][j]) ** 2)

    return av(squared_errors)




# Function to calculate the number of parameters for any given network
def n_params(nInput, hidden, nhidden, nOutput):
    params = (nInput * nhidden + nhidden * nhidden * (hidden - 1) + nhidden * nOutput) + (nhidden * hidden + nOutput)
    return params





# Training Functions





def feed_and_get_error(cglobals, registry, inputs, outputs, dataset):
    err_list = []
    
    for i in range(len(dataset)):
        
        # Input the dataset into the input layer
        for j in range(len(inputs)):
            cglobals[inputs[j]].input(dataset[i][0][j], registry, cglobals)
        # Output & Error
        for j in range(len(outputs)):
            cglobals[outputs[j]].input(dataset[i][1][j], registry, cglobals)
        
        # Calculate error
        outputs = []
        for j in range(len(outputs)):
            outputs.append(cglobals[outputs[j]].result)
        err_list.append(error(dataset[i][1]), outputs)
    err = av(err_list)
    return err




def basicTraining(cglobals, registry: dict, inputs: int, outputs: int, 
                  rate: float, dataset: list, hlayers: int, hneurons: int):
    # Step 1: Feed each set of inputs from the dataset into each input neuron
    # and calculate error
    
    err = feed_and_get_error(cglobals, registry, inputs, outputs, dataset)
    
    STARTB = []
    
    # Step 2: change every weight in the input layer and calculate the new weights
    for i in range(inputs): # For each input neuron
        INPUTB = {}
        
        # List of IDs for the connections of the neuron
        keyc = list(cglobals[f's{i}'].connections.keys())
        
        # List of weights for the connections of the neuron 
        valuec = list(cglobals[f's{i}'].connections.values()) 
        
        for j in range(len(cglobals[f's{i}'].connections)): # For each connection
            cglobals[f"s{i}"].w(
                                valuec[j] + 0.01,
                                keyc[j]
                                )
            
            # New Error
            nerr = feed_and_get_error(cglobals, registry, inputs, outputs, dataset)
            derr = nerr - err
            
            derr = derr / 0.01
            
            neww = valuec[j] - (rate * derr)
            
            INPUTB[keyc[j]] = neww
            
            # Reset the weight
            cglobals[f"s{i}"].w(
                                valuec[j],
                                keyc[j]
                                )            
            
        STARTB.append(INPUTB)
    
    HIDDENB = []
    
    # Step 3: change every weight in the hidden layer and calculate the new weights
    # + change the bias
    for i in range(hlayers): # For each hidden layer
        LAYERB = []
        for j in range(hneurons): # For each hidden neuron
            NEURONB = [0, {}]
            cglobals[f'n{i}_{j}'].b(cglobals[f'n{i}_{j}'].bias + 0.01)
            nerr = feed_and_get_error(cglobals, registry, inputs, outputs, dataset)
            derr = nerr - err
            derr = derr / 0.01
            newb = (cglobals[f'n{i}_{j}'].bias - 0.01) - (rate * derr)
            NEURONB[0] = newb
            
            for k in range(len(cglobals[f'n{i}_{j}'].connections)): # For each connection
                keyc = list(cglobals[f'n{i}_{j}'].connections.keys())
                
                valuec = list(cglobals[f'n{i}_{j}'].connections.values())
                
                cglobals[f'n{i}_{j}'].w(
                    valuec[k] + 0.01,
                    keyc[k]
                )
                
                nerr = feed_and_get_error(cglobals, registry, inputs, outputs, dataset)
                derr = nerr - err
                derr = derr / 0.01
                neww = valuec[k] - (rate * derr)
                NEURONB[1][keyc[k]] = neww
                
                cglobals[f'n{i}_{j}'].w(
                    valuec[k],
                    keyc[k]
                )
            
            LAYERB.append(NEURONB)
        HIDDENB.append(LAYERB)

    ENDB = []
    
    # Step 4: change every bias in the last layer
    for i in range(outputs):
        cglobals[f'e{i}'].b(cglobals[f'e{i}'].bias + 0.01)
        nerr = feed_and_get_error(cglobals, registry, inputs, outputs, dataset)
        derr = nerr - err
        derr = derr / 0.01
        newb = (cglobals[f'e{i}'].bias - 0.01) - (rate * derr)
        ENDB.append(newb)
        cglobals[f'e{i}'].b(cglobals[f'e{i}'].bias)
        
    # Step 5: apply the changes
    
    
    # Apply the changes to the input layer weights
    for i in range(inputs):
        for j in range(len(cglobals[f's{i}'].connections)):
            keyc = list(cglobals[f's{i}'].connections.keys())
            valuec = list(cglobals[f's{i}'].connections.values())
            keyb = list(STARTB.[i].keys())
            cglobals[f's{i}'].w(
                keyb[j],
                valuec[j]
            )
    for layer in range(hlayers): # I almost forgot that `i` is not the only option
        
        
    

def train(cglobals, registry: dict, inputs: list, outputs: list, 
          rate: float = 0.001, dataset: list):
    # Split the dataset into batches of 20 if it is larger than 40
    if len(dataset) > 40:
        number_of_batches = len(dataset) // 20
        if len(dataset) > (number_of_batches * 20):
            number_of_batches += 1    
        batches = []
        for i in range(number_of_batches):
            batch = []
            for j in range(20):
                if len(dataset) == 0:
                    break
                tmp = random.randint(0, len(dataset) - 1)
                batch.append(dataset[tmp])
                dataset.pop(tmp)
            batches.append(batch)
        dataset = batches

