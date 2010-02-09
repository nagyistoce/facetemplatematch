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
            
    def computeFeatureMatrix(self):
        '''
        Compute feature matrix G at (x,y) 
        '''
        
        '''
        construct a feature matrix G
        at an image location (x,y)
        '''
        # Discrete rotation angles
        n = 4 # number of orientation
        theta = np.arange(n) * pi / n
        
        # Discrete frequencies
        a = 2 # for octave spacing
        fmax = 10
        m = 10
        freq = fmax*a*np.arange(m)        
        
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
        Gxy = []
        for i in xrange(len(image_xy)):
            x, y = image_xy[i, 0], image_xy[i, 1]            
            for f in freq:
                for angle in theta:                
                    featureParams.append([x, y, f, angle])
            
            for m in xrange(len(freq)):
                for n in xrange(len(theta)):            
                    Gxy = self.computeResponse(featureParams[i])
            print Gxy                  
        
    def computeResponse(self, params):
        '''
        compute the response given x,y,f,angle
        '''
        return params
    
    def computeNormFeatureMatrix(self):
        '''
        Compute normalized feature matrix G'
        '''
        
    def classDetermination(self):
        '''
        Find the best class based on bestConfidence
        '''
        
