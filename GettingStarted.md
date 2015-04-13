# Introduction #

This program performs face recognition using template matching on ORL face database. Many features are required for face recognition including but not limited to:

  1. An algorithm extracting unique feature of a face
  1. Another algorithm sophisticate enough to correctly categorize the same face using the extracted unique feature from the face

For now, feature extraction was assumed done correctly. Features were extracted by mouse click using Matlab and the information is avaiable in Matlab's mat file format. The program currently uses the information from the mat file.

Template matching algorithm was implemented but its performance is only a proof-of-concept and not complete.

### Assumptions ###

For now, feature extraction was assumed done correctly. Features were extracted by mouse click using Matlab and the information is available in Matlab's mat file format. The program currently uses the information from the mat file.

Template matching algorithm was implemented but its performance is only a proof-of-concept and not complete.

### Requirements ###
Python Interpreter version: Python 2.5, 2.6

Required Python Extensions
  * numpy
  * scipy
  * PIL
  * [PyWavelets](http://wavelets.scipy.org/moin/)

## Quick Start ##

In command console, type the following command in /src directory:

>python facerecog.py

Then, you can choose an operation as either 1) perform face recognition using entire face databse, 2) perform face recognition for a specific image. ('0' for termination.)

For the second option, specify image among the orl face database. The image path is joined with orl face database path. So specify only the folder name and image file name as below.

> Specify test image path: 's2/2.pgm'


profiling is activated for performance measure.

## Descriptioin of Packages ##

This project is a combination of python packages. Each package is being implemented. See detailed description of packages in [Packages](Packages.md) page.