#!/usr/bin/env python
# -*- coding: utf-8 -*-
from PIL import Image
from numpy import array
import sift
from matplotlib import *
import os
outputDir = "./offline/sift/"
fileList = os.listdir("./dataset")

for image in fileList:
	outputName =  outputDir + image[7:-4] + '.sift'
	sift.process_image("./dataset/" + image , outputName)
	edge = 150
	peak = 3
	while(os.path.getsize(outputName) <= 500):
		param = "--edge-thresh "+str(edge)+" --peak-thresh "+str(peak)
		sift.process_image("./dataset/" + image, outputName, param)
	print image[7:-4] + " has finished."

