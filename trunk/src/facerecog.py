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

from __future__ import division # for the True Division
import os
import sys
import getopt
import numpy as np
import cProfile

# custom modules
from ImageUtils import utils
import templatematch.templatematching as templateMatching

def xp01(test_image, db_path, character_index):
    ''' Experiment on ORL facedatabase
    using template matching on the given image
    '''
    
    linedivide = '=' * 50
    print '\n', linedivide
    print "Test image: ", test_image
    testClass = os.path.dirname(test_image)
    testClass = os.path.split(testClass)[-1]    
    
    print "\nPerforming template matching on ORL facedatabase"    

    matching_error = np.zeros(40)
    for i in range(40): # for 40 templates
        template_class = 's' + str(i + 1) # get template class
        template_image = os.path.join(db_path, template_class, '1.pgm')
##        print "\nTemplate: ", template_image
              
        tm  = templateMatching.templateMatching2()        
        AC = tm.templateMatching(test_image, template_image, \
                                         character_index[i])[0]
##        print "warped feature point coordinate is "
##        print AC
##        ErrorSum[i] = error

##            print "\nComputing coeffs"
        test = utils.im2array(test_image)
        test_index = np.transpose(np.nonzero(test))        
        
        A, B = tm.sinusoidalCoeffs(character_index[i], AC)
##        print "A = ", A
##        print "B = ", B

##            print "\nComputing DX"
        DX = tm.sinusoidalWarping(A, B, test_index)
##        print "DX = ", DX
        
        # compute template matching error
        matching_error[i] = tm.matchingError(test_image, template_image, DX)
##        print "With", template_class, "matching error = ", matching_error[i]

##    print "ErrorSum = ", ErrorSum
##    ErrMin = ErrorSum.min()
    error_min = matching_error.min()
    MinErrorClass = np.nonzero(matching_error == error_min)[0][0] + 1
    MinErrorClass = 's' + str(MinErrorClass)

    verdict = "\tIncorrect match."    

    if MinErrorClass == testClass:
        verdict = "\tCorrect match!"        

    linedivide = '-' * 50
    print "\n", linedivide
    print "Match result:", verdict
    print "\nMin Error = ", error_min    
    print "Min Error Class is", MinErrorClass
    print "True Class: ", testClass

def xp02(db_path, character_index):
    ''' perform experiment on the all images in the ORL face DB
    '''
   
    match_count = 0# correct match count
    total = 0 # total # test images
    for i in xrange(40):
        template_class = 's' + str(i + 1) # get template class name      
        for im in xrange(9):
            im_name = str(im + 2) + '.pgm'
            test_image = os.path.join(db_path, template_class, im_name)
            
            if xp01(test_image, db_path, character_index): # match found
                match_count += 1
                
            total += 1
            performance = match_count / total
            performance *= 100 # percent conversion

            # show matching result
            print ''
            print "Match correctly found:", match_count
            print "Total image evaluated:", total
            print "Matching performance (%%): %.2f" % performance
    

############################################################################
#
# standard main function part
#
############################################################################
class Usage(Exception):
    def _get_message(self, message):
        return self._message
    def _set_message(self, message):
        self._message = message
    message = property(_get_message, _set_message)

def main(argv=None):
    # Import Psyco if available
    try:
        import psyco
        psyco.full()
    except ImportError:
        print 'Psyco not installed, the program will just run slower'
    
    if argv is None:
        argv = sys.argv
    try:
        try:
            opts, args = getopt.getopt(argv[1:], "h", ["help"])
        except getopt.error, msg:
            raise Usage(msg)

        for o, a in opts:
            if o in ("-h", "--help"):
                print __doc__
                return 0
        
        #arg1 = os.path.join(args[0])
        
        # load data from Matlab data file
        from scipy.io import loadmat
        x = loadmat('../data/Coord.mat')
        character_index = x['Coord'].tolist()[0] # matlab index adjustment
        character_index = np.array(character_index, dtype='float') - 1

        # database path
        db_path = '../data/orl_faces/' # orl faces
                
        while 1:        
            print "\nTemplate Matching"
            operation = input("Choose operation (0: exit, 1: Whole DB, 2: individual image): ")
            
            if operation == 0:
                print "Experiment terminated."
                return 0;
              
            elif operation == 1: 
                cProfile.runctx('xp02(db_path, character_index);',\
                                 globals(), locals()) # perform experiment on all images
            
            elif operation == 2:
                # experiment task 01                 
                test_image = input("Specify test image path: ") # get test image path                            
                test_image = os.path.join(db_path, test_image) # make it as full path              
                
                cProfile.runctx('xp01(test_image, db_path, character_index);',\
                                 globals(), locals())
                
        return 0
        
    except Usage, err:
        print >> sys.stderr, err.msg
        print >> sys.stderr, "use --help for help"
        return 2

if __name__ == '__main__':
    sys.exit(main())
