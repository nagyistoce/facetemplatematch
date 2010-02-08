'''
Created on 2010. 2. 8.

@author: Seongjoo
'''
from math import pi, cos, sin
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
        n = 3 # number of orientation
        theta = np.array(np.zeros(n))        
        for k in xrange(0, n - 1):
            theta[k] = k * pi / n
        
        # Discrete frequencies
        a = 2 # for octave spacing]
        freq = [1]
        m = 10
        for k in xrange(0, m - 1):
            freq.append(a ** -k * freq[0])
        
        # get x,y coordinate vector from image array
        image_xy = np.array(np.transpose(np.nonzero(self.imageArray)))
        
        # compute the new x,y coordinate
        image_xy_new = np.zeros(image_xy.shape)
                       
        for angle in theta:
            image_xy_new[:, 0] = image_xy[:, 1] * cos(angle) + \
                                image_xy[:, 0] * sin(angle)
            image_xy_new[:, 1] = -1 * image_xy[:, 0] * sin(angle) + \
                                image_xy[:, 1] * cos(angle)
        
        featureParams = []
        for i in xrange(len(image_xy)):
            x, y = image_xy[i, 0], image_xy[i, 1]            
            for f in freq:
                for angle in theta:                
                    featureParams.append([x, y, f, angle])
            self.computeResponse(featureParams[i])                    
        
    def computeResponse(self, params):
        '''
        compute the response given x,y,f,angle
        '''
    
    def computeNormFeatureMatrix(self):
        '''
        Compute normalized feature matrix G'
        '''
        
    def classDetermination(self):
        '''
        Find the best class based on bestConfidence
        '''
        
