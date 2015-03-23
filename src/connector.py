# -*- coding: utf-8 -*-

import numpy as np

class SOM1d():
    '''1-d self organizing map for 2-dimmential inputs
    '''
    def __init__(self, data):
        assert len(data.shape) == 2
        self.data = data
        
        x_avg = np.average(data[:, 0], axis=0)
        y_avg = np.average(data[:, 1], axis=0)
        self.w = np.ones((data.shape[0]*2, 2))
        self.w[:, 0] *= x_avg
        self.w[:, 1] *= y_avg
        
#        idx = np.random.choice(range(self.data.shape[0]), self.data.shape[0])
#        self.w = data[idx, :]
#        self.w = data + np.random.normal(size=data.shape)
        
        
    @property
    def size(self):
        return self.w.shape[0]

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
        
    def gaussian(self, c, sigma):
        """ Returns a Gaussian centered in c """
        d = 2*np.pi * sigma**2
        ax = np.exp(-np.power(range(self.size)-c, 2)/d)
        return ax               
        
    def train(self,rlen, lrate_init=0.5, lrate_final=0.01, sigma_init=5.0, sigma_final=1):      
#        import ipdb
#        ipdb.set_trace()
        for t in range(rlen):
            
            sigma = (sigma_final-sigma_init)*t/rlen + sigma_init
            lrate = (lrate_final-lrate_init)*t/rlen + lrate_init
        
            point_id = np.random.choice(range(self.data.shape[0]), 1)
            point = self.data[point_id, :]
            bmu = self.BMU_idx(point)
        
            delta = (point - self.w[bmu, :])
            bubble = self.gaussian(bmu, sigma)*lrate
            
            dx = delta[:, 0] * bubble
            dy = delta[:, 1] * bubble
            
            self.w[:, 0] += dx
            self.w[:, 1] += dy
            
    def connect(self):
        # train SOM
        self.train(self.size*50, lrate_init=0.9, sigma_init=self.size, sigma_final=2)
        self.train(self.size*500, lrate_init=0.9, sigma_init=2, sigma_final=0.1)
        
        ordered = {}
        for point in self.data:
            bmu = self.BMU_idx(point)
            try:
                ordered[bmu].append(point)
            except KeyError:
                ordered[bmu] = [point]
        
        result = []
        print ordered
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
