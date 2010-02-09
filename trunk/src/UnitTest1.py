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

import unittest
import utils
from FeatureExtract.facefeature import FaceFeature

class Test(unittest.TestCase):
     
    def testFaceFeature(self):
        img = '../data/orl_faces/s1/2.pgm'
        imageArray = utils.im2array(img)
        gFeature = FaceFeature(imageArray)        
        
    def testComputeFeatureMatrix(self):
        img = '../data/orl_faces/s1/2.pgm'
        imageArray = utils.im2array(img) 
        gFeature = FaceFeature(imageArray)
        gFeature.computeFeatureMatrix()


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()