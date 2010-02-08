'''
Created on 2010. 2. 8.

@author: Seongjoo
'''
from math import pi, pow, cos, sin
import numpy as np

class FaceFeature(object):
    '''
    Implementation of invariant search of object class
    location (x,y) in a 2D image space using Gabor filter
    
    Kyrki et al 2004
    '''


    def __init__(self, imageArray):
        '''
        Constructor
        '''
        self.imageArray = imageArray
            
    def computeFeatureMatrix(self):
        '''
        Compute feature matrix G at (x,y) 
        '''
        
        '''
        construct a feature matrix G
        at an image location (x,y)
        '''
        # Discrete rotation angles
        theta = []
        n = 3 # number of orientation
        for k in xrange(0, n-1):
            theta.append(k*pi/n)
        
        # Discrete frequencies
        a = 2 # for octave spacing]
        f = [1]
        m=10
        for k in xrange(1, m-1):
            f.append(pow(a,-k)*f[0])
        
        # get x,y coordinate vector from image array
        image_xy = np.transpose(np.nonzero(self.imageArray))
        
        # compute the new x,y coordinate
        image_xy_new = image_xy[:]
        image_xy_new[0,:] = image_xy[0,:]*cos(theta) + image_xy[1,:]*sin(theta)
            
        
    def computeNormFeatureMatrix(self):
        '''
        Compute normalized feature matrix G'
        '''
        
    def classDetermination(self):
        '''
        Find the best class based on bestConfidence
        '''
        