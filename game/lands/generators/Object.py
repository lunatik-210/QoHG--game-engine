import random

class ObjectGenerator:
    def __init__(self, probability_array):
        self.missed_prob = self.prob(probability_array)
        self.objects = self.extract_object_ids(probability_array)
        self.mean = self.calc_mean(probability_array)
        self.variance = self.calc_variance(self.mean, probability_array)

    def prob(self, probability_array):
        var = 1
        for obj in probability_array:
            var -= obj[0]
        return var

    def calc_mean(self, probability_array):
        mean = 0
        for obj in probability_array:
            mean += obj[1] * obj[0]
        mean += self.missed_prob * 5
        return mean

    def calc_variance(self, mean, probability_array):
        var = 0
        for obj in probability_array:
            var += abs((obj[1]-mean)) * obj[0]
        var += abs((5-mean)) * self.missed_prob
        return var

    def extract_object_ids(self, probability_array):
        objects = []
        for obj in probability_array:
            objects.append(obj[1])
        return objects

    def generate(self):
        val = abs(int(random.gauss(self.mean, self.variance)))
        if val in self.objects:
            return val
        return None

