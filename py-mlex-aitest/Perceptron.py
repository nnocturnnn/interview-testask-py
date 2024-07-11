import math as m
import random
import matplotlib.pyplot as plt
import numpy as np
import statistics

down_limit = -5
up_limit = 5
p1 = 8
p2 = 0
train_data_size = 4000
test_data_size = 100
neuron_number = 40
number = 1
train_iterations = 10
learn_coeff = 0.01

def x_gen(down_limit, up_limit): 
    return random.uniform(down_limit, up_limit)

def function(x):
    return m.sin(x * (m.sqrt(p1 + 1))) + m.cos(x * (m.sqrt(p2 + 1)))

def test_generate(down_limit, up_limit, size):
    x_set, y_set = [], []
    for _ in range(size):
        x = x_gen(down_limit, up_limit)
        y = function(x)
        x_set.append(x)
        y_set.append(y)
    return x_set, y_set

def function_activ(x):
    return np.tanh(x)

def function_der_activation(x):
    return (((np.cosh(x)) ** 2) - ((np.sinh(x)) ** 2)) / ((np.cosh(x)) ** 2)

class Neuron: 
    def __init__(self, number):
        weights = []
        for _ in range(number):
            weights.append(np.random.normal(0, 1))
        self.weights = np.array(weights)
        self.total, self.result = None, None
        self.offset = np.random.normal(0, 1)
    def predict(self, input_values):
        self.total = np.dot(self.weights, input_values) + self.offset
        self.result = function_activ(self.total)
        return self.result

class Linear_neuron(Neuron): 
    def __init__(self, number):
        super().__init__(number)
    def predict(self, input_values):
        super().predict(input_values)
        return self.total

class Perceptron:
    def __init__(self, hideaway_neur_number, number):
        self.hideaway_neur = []
        for _ in range(hideaway_neur_number):
            self.hideaway_neur.append(Neuron(number))
        self.output_neuron = Linear_neuron(hideaway_neur_number)
        
    def predict(self, x):
        hidden_layer_results = []
        for neuron in self.hideaway_neur:
            hidden_layer_results.append(neuron.predict(x))
        return self.output_neuron.predict(hidden_layer_results)

    def train(self, data, y_all_true, epochs, learn_coeff):
        e = []
        for epoch in range(epochs):
            for x, y_tr in zip(data, y_all_true):
                y_pred = self.predict(x)
                deriv_1 = -2 * (y_tr - y_pred)             
                e.append(abs((y_tr - y_pred) / y_tr))
                deriv_2 = []
                deriv_3 = []
                for i in range(len(self.hideaway_neur)):
                    deriv_2.append(self.hideaway_neur[i].result)
                for i in range(len(self.output_neuron.weights)):
                    deriv_3.append(self.output_neuron.weights[i] * function_der_activation(self.output_neuron.total))
                deriv_4 = []
                deriv_5 = []
                for i in range(len(self.hideaway_neur)):
                    w = []
                    deriv_4.append(function_der_activation(self.hideaway_neur[i].total))
                    for j in range(len(self.hideaway_neur[0].weights)):
                        w.append(x * function_der_activation(self.hideaway_neur[i].result))
                    deriv_5.append(w)
                for i in range(len(self.hideaway_neur)):
                    self.hideaway_neur[i].offset -= learn_coeff * deriv_1 * deriv_3[i] * deriv_4[i]
                    for j in range(len(self.hideaway_neur[0].weights)):
                        self.hideaway_neur[i].weights[j] -= learn_coeff * deriv_1 * deriv_5[i] * deriv_5[i][j]
                for i in range(len(self.output_neuron.weights)):
                    self.output_neuron.weights[i] -= learn_coeff * deriv_1 * deriv_2[i]
                self.output_neuron.offset -= learn_coeff * deriv_1
            print(e[-1], epoch)
        print("Approximation error: ", sum(e)/len(e))
        return y_tr, y_pred   

    def verify(self, test_x, test_y):
        network_results = []
        e = []
        for element in test_x:
            network_results.append(self.predict(element))
        for i in range(len(test_x)):
            e.append(abs((test_y[i] - network_results[i][0]) / test_y[i]))
        print("малейшая ошибка: ", min(e))
        print("самая большая ошибка: ", max(e))
        print("средняя ошибка аппроксимации: ", sum(e)/len(e))
        print("стандартное отклонение ошибки:", statistics.stdev(e))
        plt.plot(test_x, test_y, 'o', color='red')
        plt.plot(test_x, network_results, 'o', color='blue')
        plt.show()

train_data = test_generate(down_limit, up_limit, train_data_size)
test_data = test_generate(down_limit, up_limit, test_data_size)
chain = Perceptron(neuron_number, number)
chain.train(train_data[0], train_data[1], train_iterations, learn_coeff)
chain.verify(test_data[0], test_data[1])