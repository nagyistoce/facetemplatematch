'''
Created on 2010. 2. 11.

@author: Seongjoo
'''

import numpy as np
from numpy.random import random

class ParticleFilter(object):
    '''
    ParticleFilter
    
    Reference:
    
    '''


    def __init__(self):
        '''
        Constructor
        '''
    
    def particlefilter(self, sequence, pos, stepsize, n):
        seq = iter(sequence)
        x = np.ones((n, 2), int) * pos #Initial position
        f0 = seq.next()[tuple(pos)] * np.ones(n)   # Target color model
        yield pos, x, np.ones(n) / n 
        for im in seq:
            x += random.uniform(-stepsize, stepsize, x.shape) # Particle motion model: uniform step
            x = x.clip(np.zeros(2), np.array(im.shape) - 1).astype(int) # Clip out-of-bounds particles
            f = im[tuple(x.T)]  # Measure particle colors
            w = 1. / (1. + (f0 - f) ** 2) # Weigght~ inverse quadratic color distance
            w /= sum(w)   # Normalize w
            yield sum(x.T * w, axis=1), x, w   # Return expected position, particles and weights
            if 1. / sum(w ** 2) < n / 2.:
                x = x[self.resample(w), :]  
    
    def resample(self, weights):
        n = len(weights)
        indices = []
        C = [0.] + [sum(weights[:i + 1]) for i in range(n)]
        u0, j = random(), 0
        for u in [(u0 + i) / n for i in range(n)]:
            while u > C[j]:
                j += 1
            indices.append(j - 1)
        return indices
            
            
