'''
Created on 2010. 2. 8.

@author: Seongjoo
'''
import unittest
import utils
from FeatureExtract.facefeature import FaceFeature

class Test(unittest.TestCase):


    def testFaceFeature(self):
        gFeature = FaceFeature()        
        
    def testComputeFeatureMatrix(self):
        img = '../data/orl_faces/s1/2.pgm'
        imageArray = utils.im2array(img) 
        gFeature = FaceFeature()
        gFeature.computeFeatureMatrix(imageArray)


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()