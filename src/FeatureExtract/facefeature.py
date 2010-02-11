'''
Copyright (c) 2010 Lee Seongjoo

Permission is hereby granted, free of charge, to any person
obtaining a copy of this software and associated documentation
files (the "Software"), to deal in the Software without
restriction, including without limitation the rights to use,
copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the
Software is furnished to do so, subject to the following
conditions:

The above copyright notice and this permission notice shall be
included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES
OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
OTHER DEALINGS IN THE SOFTWARE.
'''

from math import pi, cos, sin
import numpy as np
import scipy.stsci.convolve as convolve
#from psyco.classes import __metaclass__

class GaborFeatureSpace(object):
    '''
    Implementation of invariant search of object class
    location (x,y) in a 2D image space using Gabor feature space
    
    Kyrki et al 2004
    '''


    def __init__(self, imageArray):
        '''
        Constructor
        '''
        self.imageArray = imageArray
            
    def featureSpace(self):
        '''
        Compute feature matrix G at (x,y) 
        '''
        
        # Compute Gabor filter parameters
        
        # Compute Gabor filter Response
        
        # Construct Gabor Feature Space        
    
    def filterResponse(self, params):
        '''
        compute the response given x,y,f,angle
        '''        
        return convolve.convolve2d(params, self.imageArray)   
    
    
    def filterParams(self):
        
        m, n = 5 , 4 # number of frequency and orientation
        
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
            featureParams[i] = [[f, angle] for f in freq for angle in theta]
                    
        
        
    def getDiscreteFreq(self, pixelIntensity , a=2, m=10):
        '''
        Get discrete frequencies at (x,y)
        '''
        fmax = 10        
        freq = fmax * a * np.arange(m)   
        return freq 
    
    def getDiscreteRotation(self, pixelIntensity, orientation=4):
        '''
        Discrete rotation angles
        '''
        n = orientation
        theta = np.arange(n) * pi / n
        return theta        
        
    def computeNormFeatureMatrix(self):
        '''
        Compute normalized feature matrix G'
        '''        
        
