'''
Created on 2010. 2. 8.

@author: Seongjoo
'''
from math import pow

class FaceFeature(object):
    '''
    Implementation of invariant search of object class
    location (x,y) in a 2D image space
    
    Kyrki et al 2004
    '''


    def __init__(self):
        '''
        Constructor
        '''
        
    # TODO
    def computeFeatureMatrix(self, imageArray):
        '''
        Compute feature matrix G at (x,y) 
        '''
        
        row, col = imageArray.shape
        
        G = []
        
        # f0 to fm
        a = 2 # for octave spacing]
        m=10
        f = [1,]
        
        '''
        construct a feature matrix G
        at an image location (x,y)
        '''       
        for k in xrange(0, m-1):
            f.append(pow(a,-k)*f[0])
            
            
        
    def computeNormFeatureMatrix(self):
        '''
        Compute normalized feature matrix G'
        '''
        
    def classDetermination(self):
        '''
        Find the best class based on bestConfidence
        '''
        