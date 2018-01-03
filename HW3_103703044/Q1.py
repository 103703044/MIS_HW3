import numpy as np
import math
from PIL import Image
def Q1_run(input,fileList):
	rank = []
	distance = []
	i = 0
	inputRGB = input.histogram()
	distance = [[1.0,""]for j in xrange(len(fileList))]
	for comparedFile in fileList:
		comparedImage = Image.open("./dataset/" + comparedFile)
		comparedRGB = comparedImage.histogram()
		EuclideanDistance = CountEuclideanDistance(inputRGB,comparedRGB)
		distance[i][0] = EuclideanDistance
		distance[i][1] = comparedFile
		i += 1
	rank = sorted(distance, key = lambda x : x[0])[:10]
	return rank

def CountEuclideanDistance(baseColor,comparedColor):
	length = len(baseColor)
	distance = 0
	for i in xrange(0,length):
		distance += math.pow((baseColor[i] - comparedColor[i]),2)
	distance = math.sqrt(distance)
	return distance