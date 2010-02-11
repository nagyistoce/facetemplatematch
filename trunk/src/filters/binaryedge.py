#!/usr/bin/env python
import numpy as np
import pywt

from ImageUtils import utils # utils for image formatting
import sobels

def wtHighFreq(img, mode='haar', level=1):
    '''
    Apply Wavelet Transform to an image
    Author: Lee Seongjoo seongjoo@csai.yonsei.ac.kr
    2009 (c) Lee Seongjoo
    '''    
    imArray = utils.im2array(img)   
    
    # compute coefficients of multiresolution WT
    coeffs=pywt.wavedec2(imArray, mode, level=level)

    # high frequency coeffs
    coeffs_H=list(coeffs)
    # discarding the low frequency
    # Approximation coeffs are from the low-pass filter
    coeffs_H[0]=np.zeros(coeffs_H[0].shape) 

    # multilevel reconstruction
    imArray_H=pywt.waverec2(coeffs_H, mode)
    
    #Compute binarization of image
    HA=imArray_H.mean() # mean value of high frequency part imArray_H
    SBEI=np.array(imArray_H<HA+5, dtype='uint8') # binarized image
           
    #msg='Multiresolution Wavelet Transform level: '+ str(level)
    #print msg
    #print "execution took", t_end-t0, "seconds"

    # converting resulting ndarray into an image
    imArray_H, image_wavetransformed = utils.formatimage(imArray_H)
    
    SBEI *= 255 # SBEI to grayscale
    SBEI, image_binarized = utils.formatimage(SBEI) 
    
    imgData=[SBEI,image_wavetransformed, image_binarized]
    
    return imgData

def BEI(img, scale=6):
    '''
    Compute sum of SBEIs. Default scale is 6.
    '''
    
    sumSBEI=np.zeros((112,92)) # initialization
    imageList=[] # wavelet transformed images container list
        
    #print "Processing image's BEI"
    for level in range(1, scale):
        SBEI, image_WT, im_SBEI = wtHighFreq(img,level=level)        
        imageList.append(image_WT) # store wave transformed image
        sumSBEI+=SBEI

    #imageList.insert(0, imgData[5]) # insert the original image into the list

    imgSize=imageList[-1].size[-1]*imageList[-1].size[-1]
    NfpList=[]
    TList=[]
    for t in range(1, scale-1):
        threshold=np.array(sumSBEI>=t, dtype='uint8')
        Nfp=threshold.sum()
        T=abs(Nfp/imgSize-0.2)
        NfpList.append(Nfp)
        TList.append(T)

    threshold=min(TList) # set threshold
    BEI = np.array(sumSBEI > threshold, dtype='uint8') # binary image    

    BEI *= 255    
    BEI, imBEI = utils.formatimage(BEI)
        
    return [BEI, imBEI]
    
def BEI2(img, scale=6):
    ''' noise filtered enhanced BEI
    Algorithm based on Song et al 2007
    '''
    arrayBEI, imBEI = BEI(img, scale)
    binary_image_map, imsobelLAT = sobels.sobelLAT(img)
    
    # noise filtering
    BEI2 = arrayBEI * binary_image_map
    
    # clustering
    # finding all eight-connected components from BEI
    # then 
    
    # image formatting
    BEI2 *= 255 # Black-and-White image value
    BEI2, imBEI2 = utils.formatimage(BEI2)

    return [BEI2, imBEI2]

