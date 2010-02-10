'''
Created on 2010. 2. 10.

@author: Seongjoo
'''
import numpy as np
from numpy import cos, sin, pi
from ImageUtils import utils 

class GaborFilter(object):
    '''
    classdocs
    '''


    def __init__(self, image):
        '''
        Constructor
        '''
        self.image = utils.im2array(image) 
        
    def gabor2DFunction(self, frequency, rotation, gamma=1, etha=1):
        '''
        Implementation of normalized 2-D Gabor filter function
        defined by Kyrki V, 2002
        '''
        f = frequency
        theta = rotation
        
        xy_index = np.transpose(np.nonzero(self.image))
        
        x = xy_index[:, 0]
        y = xy_index[:, 1]
        
        x_new = x * cos(theta) + y * sin(theta)
        y_new = -1 * x * sin(theta) + y * cos(theta)
        
        N = f**2/(pi*gamma*etha)
        term2d = -1*f**2*(x_new**2/gamma**2+y_new**2/etha**2)
        gb = N*np.exp(term2d)*np.exp((2 * pi * f * x_new)*1j)
        
        return gb
        
    def filterParams(self, fn=4, orientation=4, gamma=1, etha=1):
        
        m, n = fn , orientation # number of frequency and orientation
        
        # Discrete frequencies
        freq = self.getDiscreteFreq(self.imageArray)
        theta = self.getDiscreteRotation(self.imageArray)
        
        # get x,y coordinate vector from image array
        image_xy = np.transpose(np.nonzero(self.imageArray))
        
        image_xy_new = np.zeros(image_xy.shape)
        for angle in theta:
            image_xy_new[:, 0] = image_xy[:, 1] * cos(angle) + \
                                    image_xy[:, 0] * sin(angle)
            image_xy_new[:, 1] = -1 * image_xy[:, 0] * sin(angle) + \
                                image_xy[:, 1] * cos(angle)        
        
        row, col = self.imageArray.shape
        pixels = row * col
        sizeResponse = m * n
        featureParams = np.zeros((pixels, sizeResponse, 2))
        for i in xrange(len(image_xy)):                        
            param_xy = [[f, angle] for f in freq for angle in theta]
            featureParams[i] = param_xy
        
