import random
import copy

def lerp(a, b, t):
    return a + (b - a) * t

class Level:
    def __init__(self, input_count, output_count):
        self.inputs = [0] * input_count # equals the number of neurons in this layer
        self.outputs = [0] * output_count   # equals the number of neurons in the next layer
        self.biases = [0] * output_count    # one bias for each neuron in the next layer

        # weights:  list of lists, each neuron gets as many weights as it is connected to neurons
        # e.g. layer 0: 1 neuron, layer 1: 3 neurons --> the neuron in layer 0 has 3 weights
        # the weights basically sit on the connections between neurons
        self.weights = [[0] * output_count for _ in range(input_count)]

        self.randomize()

    def randomize(self):
        for i in range(len(self.inputs)):
            for j in range(len(self.outputs)):
                self.weights[i][j] = random.uniform(-1, 1)
        
        for i in range(len(self.biases)):
            self.biases[i] = random.uniform(-1, 1)

    @staticmethod
    def feed_forward(given_inputs, level):
        #print("inputs: ",given_inputs)
        # each neuron in one layer gets an input, this comes from the previous layer
        for i in range(len(level.inputs)):
            level.inputs[i] = given_inputs[i]


        for i in range(len(level.outputs)):
            sum = 0
            for j in range(len(level.inputs)):
                sum += level.inputs[j] * level.weights[j][i]
                #print("sum: ",sum)

            level.outputs[i] = 1 if sum > level.biases[i] else 0 # usually done with a sigmodial function instead of binary

        return level.outputs


class NeuralNetwork:
    def __init__(self, neurons_per_level):
        self.levels = []
        # a neural network is a list of layers/levels
        for i in range(len(neurons_per_level) - 1): # we iterate over all levels, except the last --> last level doesnt need to feed information forward
            # the amount of inputs equal the number of neurons for this layer
            # the amout of outputs equals the number of neurons for the NEXT layer
            self.levels.append(Level(neurons_per_level[i], neurons_per_level[i + 1]))

    @staticmethod
    def feed_forward( network, given_inputs):
        # the 0th layer gets the input values (sensor values)
        outputs = Level.feed_forward(given_inputs, network.levels[0])
        # from the 1st layer on we can iterate over the layers and just always feed the values forward
        # to the next layer
        for i in range(1, len(network.levels)):
            outputs = Level.feed_forward(outputs, network.levels[i])
        return outputs

    @staticmethod
    def mutate(network, amount=1):

        for level in network.levels:
            for i in range(len(level.biases)):
                level.biases[i] = lerp(level.biases[i], random.uniform(-1, 1), amount)
            
            for i in range(len(level.weights)):
                for j in range(len(level.weights[i])):
                    level.weights[i][j] = lerp(level.weights[i][j], random.uniform(-1, 1), amount)

    def get_brain_data(self):
        brain_data = {}
        for i,level in enumerate(self.levels):
            brain_data[f"Level {i}"] = {"weights": level.weights,
                                        "biases": level.biases,
                                        } 
        return brain_data
    
    def set_brain_data(self,brain_data):
        for i,level in enumerate(self.levels):
            level.weights = copy.deepcopy(brain_data[f"Level {i}"]["weights"])
            level.biases = copy.deepcopy(brain_data[f"Level {i}"]["biases"])

    def randomize(self):
        for level in self.levels:
            level.randomize()


