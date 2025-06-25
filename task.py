# task.py

class Task:
    def __init__(self, orders, num_couriers, max_weight):
        self.orders = orders
        self.num_couriers = num_couriers
        self.max_weight = max_weight

    def to_dict(self):
        return {
            'orders': self.orders,
            'num_couriers': self.num_couriers,
            'max_weight': self.max_weight
        }

    @staticmethod
    def from_dict(d):
        return Task(d['orders'], d['num_couriers'], d['max_weight'])
