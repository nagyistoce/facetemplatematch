#!/usr/bin/env python
import numpy as np
from scipy import ndimage

from ImageUtils import utils

def sobel(img, threshold=0, mode=None):
    imArray = utils.im2array(img)    

    Gx=ndimage.sobel(imArray, axis=0) # the horizontal derivative approx.
    Gy=ndimage.sobel(imArray, axis=1) # the vertical derivative approx.
    G_mag = np.sqrt( Gx**2 + Gy**2)    
    G_angle = np.arctan2(Gy, Gx)

    G_mag -= threshold
    
    G_mag, imG_mag = utils.formatimage(G_mag, mode=mode)    
        
    return [G_mag, imG_mag]

def sobel_handson(img):
    imArray = utils.im2array(img)    

    gx = np.array([[1, 0, -1], [2, 0, -2] , [1, 0, -1]], dtype='float')
    gy = gx.transpose()

    Gx = ndimage.convolve(imArray, gx) # the horizontal derivative approx.
    Gy = ndimage.convolve(imArray, gy) # the vertical derivative approx.
    G_mag = np.sqrt(Gx**2 + Gy**2)
    G_angle = np.arctan2(Gy, Gx)

    G_mag, output_image = utils.formatimage(G_mag)
    
    return [output_image]

def sobelLAT(img):
    '''
    Edge extraction of image using 4-directional
    Sobel edge operators with LAT
    '''    
    imArray = utils.im2array(img)
    
    # low pass filtering of input image
    LowPassFilter=np.array([[1., 2., 1.],[2., 4., 2.],[1., 2., 1.]])
    LowPassFilter /= 16
    imArray_lowpass=ndimage.convolve(imArray, LowPassFilter)

    # sobel edge operators
    z0=np.array([[1., 2., 1.], [0., 0., 0.], [-1., -2., -1]])
    z1=np.array([[2., 1., 0.], [1., 0., -1.], [0., -1., -2.]])
    z2=np.array([[1., 0., -1.], [2., 0., -2.], [1., 0., -1.]])
    z3=np.array([[0., -1., -2.], [1., 0., -1.], [2., 1., 0.]])
    SobelEdgeList=[z0, z1, z2, z3]

    G=np.array(np.zeros(imArray.shape))
    for zk in SobelEdgeList:
        Gx = ndimage.convolve(imArray, zk)
        Gy = ndimage.convolve(imArray, zk.transpose())
        Gnew = np.sqrt( Gx**2 + Gy**2 )
        # keeping max values
        left_mask = np.array( Gnew >= G, dtype='uint8')
        right_mask = np.array( left_mask==0, dtype='uint8')
        G = Gnew * left_mask + G * right_mask 

    LAT = G/imArray_lowpass
    
    LAT, imLAT = utils.formatimage(LAT, dtype='uint8')  # format image as uint8
    
    binary_edge_map=np.array(LAT>1, dtype='uint8')    
    binary_edge_map *= 255 # grayscaling
    binary_edge_map, imOutput = utils.formatimage(binary_edge_map)

    return [binary_edge_map, imOutput]

