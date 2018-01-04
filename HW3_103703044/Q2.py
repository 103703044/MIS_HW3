import numpy as np
import math
from PIL import Image
from scipy.fftpack import dct
import pandas
import os
import csv
import sift

partitionSize = 8
def Q2_offline_run(inputs,fileList):
	rank = []
	distance = [[1.0,""]for j in xrange(len(fileList))]
	index = int(inputs[7:-4]) * 4
	with open('./offline/Q2_DCTData.csv','rb') as file:
		reader = csv.reader(file)
		data = [row for row in reader]
		length = partitionSize
		bases = [[0 for _ in xrange(int(math.pow(length,2)))]for _ in xrange(3)]
		comparison = [[0 for _ in xrange(int(math.pow(length,2)))]for _ in xrange(3)]
		for i in xrange(len(data[index])-1):
			for j in xrange(3):
				bases[j][i] = float(data[index+j+1][i+1])

		for x in xrange(len(fileList)):
			for i in xrange(len(data[x*4])-1):
				for j in xrange(3):
					comparison[j][i] = float(data[x*4+j+1][i+1])
			distance[x][0] = matchFunc(bases,comparison)
			distance[x][1] = data[x*4][0]
		rank = sorted(distance, key = lambda x : x[0])[:10]
		return rank


def Q2_run(inputs,fileList):
	partition = partitionFunc(inputs)
	imageYcbCr = YCbCrConverter(partition)
	imageDCT = DCTConverter(imageYcbCr)
	zigZagDCT = zigZagConverter(imageDCT)
	rank = []
	i = 0
	distance = [[1.0,""]for j in xrange(len(fileList))]
	for comparedFile in fileList:
		comparedImage = Image.open("./dataset/" + comparedFile)
		cpPartition = partitionFunc(comparedImage)
		cpImageYcbCr = YCbCrConverter(cpPartition)
		cpImageDCT = DCTConverter(cpImageYcbCr)
		cpZigZagDCT = zigZagConverter(cpImageDCT)
		distance[i][0] = matchFunc(zigZagDCT,cpZigZagDCT)
		distance[i][1] = comparedFile
		i += 1
	rank = sorted(distance, key = lambda x : x[0])[:10]
	return rank

def partitionFunc(inputs):
		width,height = inputs.size
		partitionW = width / partitionSize
		partitionH = height / partitionSize
		pixel = inputs.load()
		partitionRGB = [[[0 for _ in xrange(partitionSize)] for _ in xrange(partitionSize)]for _ in xrange(3)]
		for xIndex in xrange(partitionSize):
			for yIndex in xrange(partitionSize):
				count = 0
				for i in xrange(partitionW):
					for j in xrange(partitionH):
						if (xIndex*partitionW + i < width) and (yIndex*partitionH + j < height):
							partitionRGB[0][xIndex][yIndex] += pixel[xIndex*partitionW + i , yIndex*partitionH + j][0]
							partitionRGB[1][xIndex][yIndex] += pixel[xIndex*partitionW + i , yIndex*partitionH + j][1]
							partitionRGB[2][xIndex][yIndex] += pixel[xIndex*partitionW + i , yIndex*partitionH + j][2]
							count += 1
				partitionRGB[0][xIndex][yIndex] /= count
				partitionRGB[1][xIndex][yIndex] /= count
				partitionRGB[2][xIndex][yIndex] /= count
		return partitionRGB

def YCbCrConverter(inputs):
	partitionYCbCr = [[[0 for _ in xrange(partitionSize)] for _ in xrange(partitionSize)]for _ in xrange(3)]
	for i in xrange(partitionSize):
		for j in xrange(partitionSize):
			R = inputs[0][i][j]
			G = inputs[1][i][j]
			B = inputs[2][i][j]
			Y = 0.299*R + 0.587*G + 0.114*B
			Cb = 0.564*(B - Y)
			Cr = 0.713*(R - Y)
			partitionYCbCr[0][i][j] = Y
			partitionYCbCr[1][i][j] = Cb
			partitionYCbCr[2][i][j] = Cr
	return partitionYCbCr

def DCTConverter(inputs):
	DCT = [0 for _ in xrange(3)]
	for i in xrange(3):
		DCT[i] = dct(inputs[i])
	return DCT

def zigZagConverter(inputs):
	length = partitionSize
	zigZag = [[0 for _ in xrange(int(math.pow(length,2)))]for _ in xrange(3)]
	for i in xrange(3):
		count = 0
		x = 0
		y = 0
		direction = "UP"
		while x + y != (length-1)*2:
			zigZag[i][count] = inputs[i][x][y]
			count += 1
			if x == 0:
				if y == length - 1:
					if direction == "UP":
						direction = "DOWN"
						x += 1
					elif direction == "DOWN":
						x += 1
						y -= 1
				elif direction == "UP":
					direction = "DOWN"
					y += 1
				elif direction == "DOWN":
					y -= 1
					x += 1 
			elif x == length - 1:
				if direction == "UP":
					y += 1
					x -= 1
				elif direction == "DOWN":
					direction = "UP"
					y += 1

			elif y == 0:
				if direction == "UP":
					y += 1
					x -= 1
				elif direction == "DOWN":
					direction = "UP"
					x += 1
			elif y == length - 1:
				if direction == "DOWN":
					y -= 1
					x += 1
				elif direction == "UP":
					direction = "DOWN"
					x += 1

			elif direction == "DOWN":
				x += 1
				y -= 1
			elif direction == "UP":
				x -= 1
				y += 1
		zigZag[i][count] = inputs[i][x][y]
	return zigZag

def matchFunc(bases,comparison):
	DYSum = 0
	DCbSum = 0
	DCrSum = 0
	for i in xrange(partitionSize*partitionSize):
		if i < 8 or i > 55:
			w = 0.7
		elif i < 16 or i > 47:
			w = 0.9
		elif i < 24 or i > 39:
			w = 1.1
		else:
			w = 1.3
		DYSum += w*math.pow(bases[0][i] - comparison[0][i],2)
		DCbSum += w*math.pow(bases[1][i] - comparison[1][i],2)
		DCrSum += w*math.pow(bases[2][i] - comparison[2][i],2)

	DYSum = math.sqrt(DYSum)
	DCbSum = math.sqrt(DCbSum)
	DCrSum = math.sqrt(DCrSum)
	distance = DYSum + DCbSum + DCrSum
	return distance

def matrixConverter(inputs):
	length = int(math.sqrt(len(inputs)))
	matrix = [[ 0 for _ in xrange(length)]for _ in xrange(length)]
	count = 0
	for i in xrange(length):
		for j in xrange(length):
				matrix[i][j] = inputs[count]
				count += 1
	return matrix

def data_generator(inputs):
	image = Image.open("./dataset/" + inputs)
	imagePartition = partitionFunc(image)
	imageYcbCr = YCbCrConverter(imagePartition)
	imageDCT = DCTConverter(imageYcbCr)
	zigZagDCT = zigZagConverter(imageDCT)
	return zigZagDCT

if __name__ == '__main__':
	path = "./dataset/"
	fileList = os.listdir("./dataset/")
	if os.path.exists("./offline/Q2_DCTData.csv"):
		os.remove("./offline/Q2_DCTData.csv")
	with open("./offline/Q2_DCTData.csv",'a') as save:
		for imageName in fileList:
			data = pandas.DataFrame(data_generator(imageName))
			data.to_csv(save,header=True,index_label = imageName)
