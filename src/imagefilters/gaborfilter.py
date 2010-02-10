'''
Created on 2010. 2. 10.

@author: Seongjoo
'''
import numpy as np
from numpy import cos, sin, pi
import scipy.stsci.convolve as convolve
from scipy import signal
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
    
    def response(self, frequency, rotation):
        gb = self.gabor2DFunction(4, 3)
        
        response = convolve.convolve2d(gb, self.image)
        
        return response
        
    def gaborwavelet(self, img):
        '''
        Gabor wavelet (GW) filter
        (Is this working?) 
        '''
        imArray = utils.im2array(img)
        
        row_size, col_size = imArray.shape
        x = np.array(range(1, row_size+1), dtype='float')
        x = x.reshape((row_size,1))
        y = np.array(range(1, col_size+1), dtype='float')
        y = y.reshape((1, col_size))
    
        orientations = []
        for i in range(8):
            orientations.append(i*pi/8)
    
        w = signal.freqz()# spatial frequency
        G = np.exp( -(x**2 + y**2) / (2*imArray.std()**2))
        GList =[] # image edge container for different directions
        for theta in orientations:
            wave_vector = x*np.cos(theta)+ y*np.sin(theta)
            G *= np.cos( w * wave_vector)+ 1j*np.sin( w * wave_vector)
        
            # Apply Gabor filter to image    
            sigma = convolve.convolve2d(imArray, G)
            GList.append(sigma)
            # Get the imaginary part of GW
    
        # format the output image    
        sigma, output_image = utils.formatimage(sigma)
        return output_image
        
