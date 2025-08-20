class Weighting(object):
    def __init__(self, values = None, weights = None):
        self.values = values
        self.weights = weights
        self.index = 0
        if self.values is not None:
            self.validate()
            self.calculate()

    def validate(self):
        if len(self.values) != len(self.weights):
            raise ValueError("Length of values and weights do not match")
        if sum(self.weights) == 0:
            raise ValueError("All weights are zero")
        return True

    def calculate(self):
        values = self.values
        weights = self.weights
        weighted_sum = sum(value * weight for value, weight in zip(values, weights))
        total_weight = sum(weights)
        weighted_average = weighted_sum / total_weight
        normalized_weighted_average_percentage = (weighted_average / sum(values)) * 100
        decimals = 2
        factor = 10 ** decimals
        self.index = int(normalized_weighted_average_percentage * factor + 0.5) / factor

    def get_values(self):
        return self.values

    def get_weights(self):
        return self.weights

    def get_index(self):
        if self.validate():
            self.calculate()
            return self.index
        else:
            return False

    def set_values(self, values):
        self.values = values

    def set_weights(self, weights):
        self.weights = weights

    def main(self):
        self.set_values([4, 4, 4, 4])
        self.set_weights([2, 2, 2, 2])
        print(self.get_values())
        print(self.get_weights())
        return self.get_index()


if __name__ == '__main__':
    x = Weighting()
    print(x.main())