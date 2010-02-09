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

import numpy as np
from numpy.linalg import norm, inv
from ImageUtils import utils

class templateMatching(object):
    def templateMatching(self, test_image, template_image, \
                         charac_index, elasticity=16):
        test = utils.im2array(test_image)
        template = utils.im2array(template_image)
        Coord = np.array(charac_index)
    
    
        width = 5
        # creating K from the template image
        A = Coord[:, 0] - width
        B = Coord[:, 0] + width
        C = Coord[:, 1] - width
        D = Coord[:, 1] + width
        
    ##    r, c = Coord.shape
        row, col = test.shape  
        ONE = np.ones(Coord.shape[0])
        ZERO = np.zeros(Coord.shape[0]) 
    
        A = np.maximum(A, ZERO)
        B = np.minimum(B, row * ONE - 1)    
        C = np.maximum(C, ZERO)
        D = np.minimum(D, col * ONE - 1)
    
        NumCharac = Coord.shape[0]
        ABCD = np.array(np.zeros((NumCharac, 4)))
        ABCD[:, 0] = A
        ABCD[:, 1] = B
        ABCD[:, 2] = C
        ABCD[:, 3] = D   
    
        errors = np.zeros(NumCharac) 
        for i in xrange(NumCharac):        
            a, b, c, d = ABCD[i, :]        
            K = template[a:b + 1, c:d + 1]        
            pre_error = 10 ** 6
    
            increment = 2
            for j in xrange(-elasticity, elasticity + increment, increment):
                for k in xrange(-elasticity, elasticity + increment, increment):
    ##                print "i, j, k", i, j, k
                    if a + j >= 0 and b + j + 1 <= row and \
                       c + k >= 0 and d + k + 1 <= col:                    
    ##                    print "i, j, k", i, j
                        test_sample = test[a + j:b + j + 1, \
                                      c + k:d + k + 1]                    
                        errors[i] = norm(test_sample - K, 2)                    
    
                        if pre_error > errors[i]:
                            pre_error = errors[i]
                            newX_index = np.ceil((a + b) / 2 + j)
                            newY_index = np.ceil((c + d) / 2 + k)                        
                            Coord[i, :] = [newX_index, newY_index]
    
            errors[i] = pre_error # for debugging
    
    ##    print "modification toggle"
    ##    print "Errors = ", errors
        error = errors.sum()
    ##    print "Error Sum: ", error
    
        return Coord, error
    
    def sinusoidalCoeffs(self, original_coord, warped_coord):
        X = np.array(original_coord, dtype='double')
        Y = np.array(warped_coord, dtype='double')
        row = X.shape[0]
        m = int(np.sqrt(row))
    
        sinvalues = np.zeros((row, row))
        XDisplacement = np.zeros((1, row))
        YDisplacement = np.zeros((1, row))
    
        for i in xrange(m):
            for j in xrange(m):
                for k in xrange(row):
                    rs = int(np.sqrt(row + 1) * i + j)
                    sinvalues[rs, k] = np.sin(np.pi * (i + 1) * X[k, 0]) * \
                                        np.sin(np.pi * (j + 1) * X[k, 1])                    
                    XDisplacement[:, k] = Y[k, 0] - X[k, 0]
                    YDisplacement[:, k] = Y[k, 1] - X[k, 1]                
        
        A = np.dot(XDisplacement, inv(sinvalues + np.eye(row) / 10))
        B = np.dot(YDisplacement , inv(sinvalues + np.eye(row) / 10))
        A = np.array(A)
        B = np.array(B)
    
        return A, B
    
    def sinusoidalWarping(self, coeff_A, coeff_B, original_coord):
        X = np.array(original_coord, dtype='double')
        A = coeff_A
        B = coeff_B
    
        row, cow = X.shape
        rr = A.shape[1]
        m = int(np.sqrt(rr))
        DX = np.zeros((row, 2))
        sinvalues = np.zeros((rr, row))
    
        for i in xrange(m):
            for j in xrange(m):
                for k in xrange(row):
                    rs = int(np.sqrt(rr + 1) * i + j)
    ##                print i,j,k, rs
                    sinvalues[rs, k] = \
                       np.sin(np.pi * (i + 1) * X[k, 0]) * np.sin(np.pi * (j + 1) * X[k, 1])
       
        DX_A = np.dot(A, sinvalues).conj().T
        DX_A = np.ceil(DX_A)  
        DX_B = np.dot(B, sinvalues).conj().T
        DX_B = np.ceil(DX_B)
        DX[:, 0] = DX_A[:, 0]
        DX[:, 1] = DX_B[:, 0]
        DX = np.array(DX, dtype='uint32')
        return DX
    
    def matchingError(self, test_image, template_image, warped_index):
        test = utils.im2array(test_image)
        template = utils.im2array(template_image)
        
        ti = np.transpose(np.nonzero(test)) 
        wi = warped_index
    
        NumPixel = ti.shape[0]
    
        ERROR = np.zeros((NumPixel, 1))
        for i in xrange(NumPixel):
            error = test[ti[i][0], ti[i][1]] - template[wi[i][0], wi[i][1]]
            ERROR[i] = error
    
        ERROR **= 2
        Error_matching = np.sqrt(ERROR.sum())
        return Error_matching    
    
class templateMatching2(object):
    
    def templateMatching(self, test_image, template_image, \
                         charac_index, elasticity=16):
        test = utils.im2array(test_image)
        template = utils.im2array(template_image)
        Coord = np.array(charac_index)
    
        width = 5
        # creating K from the template image
        A = Coord[:, 0] - width
        B = Coord[:, 0] + width
        C = Coord[:, 1] - width
        D = Coord[:, 1] + width
        
    ##    r, c = Coord.shape
        row, col = test.shape  
        ONE = np.ones(Coord.shape[0])
        ZERO = np.zeros(Coord.shape[0]) 
    
        A = np.maximum(A, ZERO)
        B = np.minimum(B, row * ONE - 1)    
        C = np.maximum(C, ZERO)
        D = np.minimum(D, col * ONE - 1)
    
        NumCharac = Coord.shape[0]
        ABCD = np.array(np.zeros((NumCharac, 4)))
        ABCD[:, 0] = A
        ABCD[:, 1] = B
        ABCD[:, 2] = C
        ABCD[:, 3] = D   
    
        errors = np.zeros(NumCharac) 
        for i in xrange(NumCharac):        
            a, b, c, d = ABCD[i, :]        
            K = template[a:b + 1, c:d + 1]        
            pre_error = 10 ** 6
    
            increment = 2
            for j in xrange(-elasticity, elasticity + increment, increment):
                for k in xrange(-elasticity, elasticity + increment, increment):
    ##                print "i, j, k", i, j, k
                    if a + j >= 0 and b + j + 1 <= row \
                        and c + k >= 0 and d + k + 1 <= col:                                                
                        test_sample = test[a + j:b + j + 1, c + k:d + k + 1]                        
                        errors[i] = norm(test_sample - K, 2)                    
    
                        if pre_error > errors[i]:
                            pre_error = errors[i]
                            newX_index = np.ceil((a + b) / 2 + j)
                            newY_index = np.ceil((c + d) / 2 + k)                        
                            Coord[i, :] = [newX_index, newY_index]
    
            errors[i] = pre_error # for debugging
    
    ##    print "modification toggle"
    ##    print "Errors = ", errors
        error = errors.sum()
    ##    print "Error Sum: ", error
    
        return Coord, error
    
    def sinusoidalCoeffs(self, original_coord, warped_coord):
        X = np.array(original_coord, dtype='double')
        Y = np.array(warped_coord, dtype='double')
        row = X.shape[0]
        m = int(np.sqrt(row))
    
        sinvalues = np.zeros((row, row))
        XDisplacement = np.zeros((1, row))
        YDisplacement = np.zeros((1, row))
    
        for i in xrange(m):
            for j in xrange(m):            
                sinvalues[:, :] = np.sin(np.pi * (i + 1) * X[:, 0]) * \
                                    np.sin(np.pi * (j + 1) * X[:, 1])                
                XDisplacement[:, :] = Y[:, 0] - X[:, 0]
                YDisplacement[:, :] = Y[:, 1] - X[:, 1]                
        
        A = np.dot(XDisplacement, inv(sinvalues + np.eye(row) / 10))
        B = np.dot(YDisplacement , inv(sinvalues + np.eye(row) / 10))
        A = np.array(A)
        B = np.array(B)
    
        return A, B
    
    def sinusoidalWarping(self, coeff_A, coeff_B, original_coord):
        X = np.array(original_coord, dtype='double')
        A = coeff_A
        B = coeff_B
    
        row = X.shape[0]
        rr = A.shape[1]
        m = int(np.sqrt(rr))
        DX = np.zeros((row, 2))
        sinvalues = np.zeros((rr, row))
    
        pi = np.pi   
        
        for i in xrange(m):
            for j in xrange(m):
                X_term = np.sin(pi * (i + 1) * X[:, 0])
                Y_term = np.sin(pi * (j + 1) * X[:, 1])
                sinvalues[:, :] = X_term * Y_term
    
    ##    print sinvalues[0:9,0]
    
        DX_A = np.dot(A, sinvalues).conj().T
        DX_A = np.ceil(DX_A).transpose()    
        DX_B = np.dot(B, sinvalues).conj().T
        DX_B = np.ceil(DX_B).transpose()
        DX[:, 0] = DX_A[:, 0]
        DX[:, 1] = DX_B[:, 0]
        DX = np.array(DX, dtype='uint32')
        return DX
    
    def matchingError(self, test_image, template_image, warped_index):
        test = utils.im2array(test_image)
        template = utils.im2array(template_image)
        
        ti = np.transpose(np.nonzero(test)) 
        wi = warped_index
    
        NumPixel = ti.shape[0]
    
        ERROR = np.zeros((NumPixel, 1)) 
        ERROR[:, 0] = test[ti[:, 0], ti[:, 1]] - template[wi[:, 0], wi[:, 1]]
        ERROR **= 2
        Error_matching = np.sqrt(ERROR.sum())
    
        return Error_matching
    

                    
