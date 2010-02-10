import numpy as np
from scipy import ndimage
import scipy.cluster.vq as clusters
from scipy import signal
import math

from ImageUtils import utils
import sobels

# fileters

def LAT(img, threshold=None):
    '''Adaptive thresholding'''
    
    imArray = utils.im2array(img)

    # set default threshold if not specified
    if threshold is None:
        T=imArray.mean()
    else:
        T=threshold

    Tdiff=1
    while(Tdiff):        
        # Segment image into object and background
        G1_mask=np.array(imArray>T, dtype='uint8') # object segments mask
        G2_mask=np.array(imArray<=T, dtype='uint8') # background mask

        G1=G1_mask*imArray # object image pixel
        G2=G2_mask*imArray # background image pixel

        # A new threshold is created using the mean values of the two segments
        Tnew= (G1.mean()+G2.mean())/2
        Tdiff=Tnew-T
        T=Tnew # set the new threshold as threshold
        # iterate until new threshold aproximately matches the old threshold
        if Tdiff<0.0002:
            Tdiff=0

    G1=np.array(imArray>T, dtype='uint8')
    G1*=255
    G, imG1 = utils.formatimage(G1)
    return imG1
    
def gaborwavelet(img):
    '''Gabor wavelet (GW) filter '''
    imArray = utils.im2array(img)
    
    row_size, col_size = imArray.shape
    x = np.array(range(1, row_size+1), dtype='float')
    x = x.reshape((row_size,1))
    y = np.array(range(1, col_size+1), dtype='float')
    y = y.reshape((1, col_size))

    orientations = []
    for i in range(8):
        orientations.append(i*math.pi/8)

    w = signal.freqz()# spatial frequency
    G = np.exp( -(x**2 + y**2) / (2*imArray.std()**2))
    GList =[] # image edge container for different directions
    for theta in orientations:
        wave_vector = x*np.cos(theta)+ y*np.sin(theta)
        G *= np.cos( w * wave_vector)+ 1j*np.sin( w * wave_vector)
    
        # Apply Gabor filter to image    
        sigma = ndimage.convolve(imArray, G)
        GList.append(sigma)
        # Get the imaginary part of GW

    # format the output image    
    sigma, output_image = utils.formatimage(sigma)
    return output_image

def EdgeImage(img, threshold=0):
    imArray = utils.im2array(img)
    G_mag, imG_mag = sobels.sobel(img, threshold=threshold)
    row_size, col_size = G_mag.shape
    EdgeMap = np.zeros(imArray.shape)
    
    # thresholding and Edge map
    #EdgeMap = np.array(G_mag > threshold, dtype='uint8')
    for row in xrange(0,row_size-3):
        for col in xrange(0, col_size-3):
            if G_mag[row, col] > threshold:
                EdgeMap[row:row+3, col:col+3] = np.ones((3,3))

    EdgeIntensity = imArray * EdgeMap
    EdgeIntensity, imEdgeIntensity = utils.formatimage(EdgeIntensity)

    return [EdgeIntensity, EdgeMap, imEdgeIntensity]

def EEIM(TemplateImage, EdgeIntensity, EdgeMap):
    '''
    EEIM is a subfunction for elastic edge intensity matching,
    which returns a matching error.
    '''

    # initialization
    imArray = utils.im2array(TemplateImage)
    #row_size, column_size = imArray.shape
    EdgeMapN = EdgeMap.sum()
    elasticity = 4
    NumCluster = 10    

    # K-means Clustering of EdgeIntensity
    EdgeCoord = np.transpose(np.nonzero(EdgeMap > 0))

    [centroid, label] = clusters.kmeans2(EdgeCoord, NumCluster)    
    
    # Partitioning of EdgeIntensity
    Cluster = np.array(np.zeros((label.size, 4)))
    Cluster[:,0] = label
    Cluster[:,1:3] = EdgeCoord
    selEI = []
    for i in label:
        row,col = EdgeCoord[i]
        selEI.append(EdgeIntensity[row,col])
    selEI = np.array(selEI)
    Cluster[:,-1] = selEI
    
    #return MatchingError
    
    
