import os
import numpy as np
from sklearn.cluster import KMeans
from sklearn.metrics import pairwise
import sift
import csv
import pandas


fileList = os.listdir("./dataset/")
fileCount = len(fileList)
clustersNum = 50
for i in xrange(fileCount):
	fileList[i] = fileList[i][7:-4]

def Q4_offline_run(inputs,fileList):
	rank = []
	with open('./Q3.csv', 'rb') as csvfile:
		reader = csv.reader(csvfile)
		index = int(inputs[7:-4]) * (clustersNum+1)
		data = [row for row in reader]
		base = []

		for row in xrange(0,len(data),clustersNum+1):
			b = [0 for i in xrange(clustersNum)]
			for i in xrange(clustersNum):
				b[i] = int (data[row+i+1][1])
			base.append(b)
		refineBase, stopWordIndices = stopWords_preprocessed(5,base)

		query=[]
		for i in xrange(index+1,index+clustersNum+1):
			query.append(int(data[i][1]))
		newQuery = stopwordsRemoved(query,stopWordIndices)

	scoreList = countDistance(newQuery,refineBase)
	for x in xrange(0, len(scoreList)):
		rank.append([scoreList[x],'ukbench'+data[x*(clustersNum+1)][0][:-4]+'jpg'])
	rank = sorted(rank,key = lambda x: x[0],reverse=True)[:10]
	return rank

def countDistance(target, codewords):
    codewords.insert(0, target)
    scoreList = pairwise.cosine_similarity(np.array(codewords))[0][1:]
    return scoreList
def findStopWords(stopWordNum, codewordsHist):
    sumHistogram = np.zeros(len(codewordsHist[0])).astype('int')
    for i in codewordsHist:
        sumHistogram = sumHistogram + np.array(i).astype('int')
    index = [x for x in range(0, len(sumHistogram))]
    freq_lst = zip(index, sumHistogram)
    list.sort(freq_lst, key= lambda tup: tup[1], reverse= True)
    return [x[0] for x in freq_lst[:stopWordNum]]

def stopwordsRemoved(lst, swIndices):
    descending = sorted(swIndices, reverse=True)
    refinedLst = list()
    for index in descending:
        refinedLst = lst[:index] + lst[index+1:]
        lst = refinedLst
    return refinedLst

def stopWords_preprocessed(stopWordNum, codewords):
    stopWordIndices = findStopWords(5, codewords)
    refinedCodewords = list()
    for i in xrange(len(codewords)):
        refinedCodewords.append(stopwordsRemoved(codewords[i], stopWordIndices))
    return (refinedCodewords, stopWordIndices)
