# -*- coding: utf-8 -*-

import numpy as np

class Connector():
    def __init__(self, data):
        assert len(data.shape) == 2
        # self.data = data.copy()

        # Computation of distance matrix:
        self.z = np.array([complex(p[0], p[1]) for p in data])
        # mesh this array so that you will have all combinations
        m, n = np.meshgrid(self.z, self.z)
        # get the distance via the norm
        self.dists = abs(m-n)

    @property
    def size(self):
        return self.z.shape[0]

    def find_ends(self):
        # Try to find indexes of the first and the latest points.
        # The euristic is:
        #   * if a point is a middle point, then the direction to the two
        #   closest points are different.
        #   * if a point is a end point, then the direction to the two
        #   closest points are similar.

        # find directions to two closest points
        d = np.zeros(self.size)
        for i in range(self.size):
            x = np.argsort(self.dists[i, :])[1:3]
            # vectors from i-th point to the closest points
            vects = np.array([self.z[x[0]], self.z[x[1]]]) - self.z[i]
            # similarity (the angle)
            d[i] = abs(np.angle(vects[0]) - np.angle(vects[1]))

        init, last = np.argsort(d)[:2]
        return (init, last)

    def get_closest(self, index, pull):
        x = pull[0]
        d = self.dists[index, x]
        for c in pull[1: ]:
            if self.dists[index, c] < d:
                d = self.dists[index, c]
                x = c

        pull.remove(x)
        return x, pull

    def connect(self):
        pull = range(self.size)

        x = self.find_ends()[0]
        order = [x]
        pull.remove(x)
        while len(pull) > 0:
            x, pull = self.get_closest(x, pull)
            order.append(x)

        result = np.take(self.z, order, axis=0)
        result = np.array([[z.real, z.imag] for z in result])

        return result


if __name__ == "__main__":
    data = np.array([
        [-0.1, 0],
        [0, 1.1],
        [0, 2.03],
        [0, 3.2],
        [0, 4.1],
        [0, 5.2],
        [0, 6.02],
        [1, 5.1],
        [1, 4.03],
        [3, 1.5],
        [2, 2.01],
        [1, 2],
        [1, 3]
    ])

    con = Connector(data)
    result = con.connect()
    print result

    import matplotlib.pyplot as plt
    plt.plot(result[:, 0], result[:, 1], 'r-o', con.z.real, con.z.imag, 'o')
    plt.show()
