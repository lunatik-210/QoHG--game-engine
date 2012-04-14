import random

class ObjectGenerator:
    def __init__(self, probability_array):
        self.objects = self.extract_object_ids(probability_array)
        self.mean = self.calc_mean(probability_array)
        self.variance = self.calc_variance(self.mean, probability_array)

    def calc_mean(self, probability_array):
        mean = 0
        for obj in probability_array:
            array = probability_array[obj]
            mean += array[0] * array[1]
        return mean

    def calc_variance(self, mean, probability_array):
        var = 0
        for obj in probability_array:
            array = probability_array[obj]
            var += abs((array[0]-mean)) * array[1]
        return var

    def extract_object_ids(self, probability_array):
        objects = []
        for obj in probability_array:
            objects.append(probability_array[obj][0])
        return objects

    def generate(self):
        val = abs(int(random.gauss(self.mean, self.variance)))
        if val in self.objects:
            return val
        return None