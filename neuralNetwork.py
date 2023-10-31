import random

def lerp(a, b, t):
    return a + (b - a) * t

class Level:
    def __init__(self, input_count, output_count):
        self.inputs = [0] * input_count
        self.outputs = [0] * output_count
        self.biases = [0] * output_count
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
        for i in range(len(level.inputs)):
            level.inputs[i] = given_inputs[i]

        for i in range(len(level.outputs)):
            sum = 0
            for j in range(len(level.inputs)):
                sum += level.inputs[j] * level.weights[j][i]
                #print("sum: ",sum)

            level.outputs[i] = 1 if sum > level.biases[i] else 0

        return level.outputs


class NeuralNetwork:
    def __init__(self, neuron_counts):
        self.levels = []
        for i in range(len(neuron_counts) - 1):
            self.levels.append(Level(neuron_counts[i], neuron_counts[i + 1]))

    @staticmethod
    def feed_forward(given_inputs, network):
        outputs = Level.feed_forward(given_inputs, network.levels[0])
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
