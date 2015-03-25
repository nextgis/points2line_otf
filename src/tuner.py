# -*- coding: utf-8 -*-

import numpy as np


class Tuner():
    def __init__(self, data):
        self.data = data

    @property
    def size(self):
        return len(self.data)

    def penalty(self, order):
        '''Return sum of distances between units
        '''
        x1 = np.take(self.data, order)
        x2 = np.roll(x1, 1)
        d = np.sum(abs(x1 - x2)[1:])  # (x1 - x2)[0] is the distance between the first and the last points
        return d

    def roll_to_max_distance(self, order):
        # Roll the order that,
        # so the first and the last points are the most distance
        x1 = np.take(self.data, order)
        x2 = np.roll(x1, 1)
        d = abs(x1 - x2)
        idx = np.argmax(d)
        return np.roll(order, -idx)


    def permute(self, index, order):
        tests = np.empty((self.size, self.size), dtype=np.int)
        num = order[index]
        base = np.delete(order, index)

        for i in range(self.size):
            tests[i, :] = np.insert(base, i, num)

        return tests

    def reorder(self, init_order):
        global_best_penalty = self.penalty(init_order)
        global_best_order = init_order

        # List of candidates of good start point to optimize:
        # eliminate the biggest distance from
        candidates = [init_order, self.roll_to_max_distance(init_order)]

        for best_order in candidates:
            best_penalty = self.penalty(best_order)

            final = False
            while not final:
                final = True
                for idx in range(self.size):
                    for order in self.permute(idx, best_order):
                        if self.penalty(order) < best_penalty:
                            best_order = order
                            best_penalty = self.penalty(order)
                            final = False
                            break
            if best_penalty < global_best_penalty:
                global_best_penalty = best_penalty
                global_best_order = best_order

        return global_best_order
