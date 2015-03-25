# -*- coding: utf-8 -*-

import numpy as np

class SOM1d():
    '''1-d self organizing map for 2-dimmential inputs
    '''
    def __init__(self, data):
        assert len(data.shape) == 2
        self.data = data.copy()

        self.x_avg = np.average(data[:, 0], axis=0)
        self.y_avg = np.average(data[:, 1], axis=0)

        self.x_std = np.std(data[:, 0], axis=0)
        self.y_std = np.std(data[:, 1], axis=0)

        ratio = 4.0/3.0     # (Number of SOM unit) / (Number of points)
        self.w = np.zeros((data.shape[0]*ratio, 2))


    @property
    def size(self):
        return self.w.shape[0]

    def normalize(self):
        self.data[:, 0] = (self.data[:, 0] - self.x_avg)/self.x_std
        self.data[:, 1] = (self.data[:, 1] - self.y_avg)/self.y_std


    def denormalyze(self):
        self.data[:, 0] = self.x_std*self.data[:, 0] + self.x_avg
        self.data[:, 1] = self.y_std*self.data[:, 1] + self.y_avg

        self.w[:, 0] = self.x_std*self.w[:, 0] + self.x_avg
        self.w[:, 1] = self.y_std*self.w[:, 1] + self.y_avg

    def distances(self, point):
        '''Return array of Euclidean distances between self.w and point
        '''
        diff = self.w - point
        return np.sqrt(np.sum(diff**2, axis=1))

    def BMU_idx(self, point):
        '''Return index of best matching unit pf the point
        '''
        dists = self.distances(point)
        return np.argmin(dists)

    def gaussian(self, c, sigma, circular=False):
        """ Returns a Gaussian centered in c """
        d = 2*np.pi * sigma**2

        if not circular:
            dists = range(self.size)-c
        else:
            dx = np.abs(np.arange(self.size)-c)
            dx1 = abs(self.size - np.mod(dx, self.size))
            dists = np.min(np.array([dx, dx1]),  axis=0)

        ax = np.exp(-np.power(dists, 2)/d)
        return ax

    def update(self, sigma, circular):
        data = np.random.permutation(self.data)

        for point in data:
            bmu = self.BMU_idx(point)

            delta = (point - self.w[bmu, :])
            bubble = self.gaussian(bmu, sigma, circular=circular)

            dx = delta[0] * bubble
            dy = delta[1] * bubble

            self.w[:, 0] += dx
            self.w[:, 1] += dy

    def train(self,rlen, lrate=0.99, sigma_init=5.0, circular=False):
        sigma = sigma_init
        for t in range(rlen):
            sigma = sigma * lrate
            self.update(sigma, circular)

    def connect(self):
        # train SOM
        self.normalize()
        self.train(self.size*150, lrate=0.99, sigma_init=self.size, circular=False)
        self.train(self.size*500, lrate=0.99, sigma_init=2, circular=False)
        self.denormalyze()

        ordered = {}
        for point in self.data:
            bmu = self.BMU_idx(point)
            try:
                ordered[bmu].append(point)
            except KeyError:
                ordered[bmu] = [point]

        result = []
        for i in range(self.size):
            try:
                pnts = ordered[i]
                if len(pnts) != 1:
                    print 'WARNING: points are not ordered', pnts
                    for point in pnts:
                        result.append(point.tolist())
                else:
                    result.append(pnts[0].tolist())
            except KeyError:
                # It's Ok
                pass

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

    som = SOM1d(data)
    print som.connect()

    import matplotlib.pyplot as plt
    plt.plot(som.w[:, 0], som.w[:, 1], 'r-o', som.data[:,0], som.data[:,1], 'o')
    plt.show()
