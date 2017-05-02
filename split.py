import math
import random
import pandas as pd
import numpy as np

var = ["a","b","c"]
pData = [random.randint(0,10) for i in range(0,10)]
pData.sort()
nData = [random.randint(0,10) for i in range(0,10)]
nData.sort()

a = [random.randint(0,10) for i in range(0,10)]
b = [random.randint(0,10) for i in range(0,10)]
c = [random.randint(0,10) for i in range(0,10)]
posData = pd.DataFrame.from_items([("a",a), ("b",b), ("c",c)])

a = [random.randint(0,10) for i in range(0,10)]
b = [random.randint(0,10) for i in range(0,10)]
c = [random.randint(0,10) for i in range(0,10)]
negData = pd.DataFrame.from_items([("a",a), ("b",b), ("c",c)])

posOrder = {v:np.argsort(posData[v].values) for v in var}
negOrder = {v:np.argsort(negData[v].values) for v in var}

# Receives a set of indices and a set of variables
def search_split(pIndex, nIndex, pOrder, nOrder, var):
	entMin = float('inf')
	for v in var:
		pData = (posData[v][pIndex].values)[pOrder[v]]
		nData = (negData[v][nIndex].values)[nOrder[v]]
		split, ent, pInd, nInd = find_split(pData, nData)
		if (ent < entMin):
			varMin = v
			entMin = ent
			splMin = split
			nIndMin = nInd
			pIndMin = pInd
	left = [pIndex[0:(pIndMin + 1)], nIndex[0:(nIndMin + 1)]]
	right = [pIndex[(pIndMin + 1):], nIndex[(nIndMin + 1):]]
	return varMin, splMin, left, right









def find_split(pData, nData, probSens = .0001):
	entMin = float('inf')
	posLength = len(pData)
	negLength = len(nData)
	posInd = 0
	negInd = 0
	posVal = pData[posInd]
	negVal = nData[negInd]

	while((posInd+1) < posLength and posVal == pData[posInd + 1]):
		posInd += 1
	while((negInd+1) < negLength and negVal == nData[negInd + 1]):
		negInd += 1

	if (posInd == 0 and posVal > negVal):
		posInd = -1
		negInd = 0
	elif (negInd == 0 and posVal < negVal):
		posInd = 0
		negInd = -1

	# Set the indices at the last index with the same value

	val = min(posVal,negVal)
	i=0

	while( True ):

		posCount = posInd + 1
		negCount = negInd + 1
		total = max(posCount + negCount, .1)
		rest = max(posLength + negLength - posCount - negCount, .1)
		p1 = float(posCount)/float(total)
		p2 = float(posLength - posCount)/float(rest)
		p1 = max(probSens, min(p1, 1 - probSens))
		p2 = max(probSens, min(p2, 1 - probSens))
		entropy =  (total * (-p1 * math.log(p1) - (1 - p1) * math.log(1 - p1)) +
		 			rest * (-p2 * math.log(p2) - (1 - p2) * math.log(1 - p2)))

		if (entropy < entMin):
			entMin = entropy
			entSplit = val
			pIndMin = posInd
			nIndMin = negInd

		if (posInd == posLength - 1):
			break
		else:
			posNext = pData[posInd+1]
		if (negInd == negLength - 1):
			break
		else:
			negNext = nData[negInd+1]

		if (posVal == negVal):
			if (posNext == negNext):
				posVal = posNext
				negVal = negNext
				val = posVal
				posInd += 1
				negInd += 1
				while((posInd+1) < posLength and posVal == pData[posInd+1]):
					posInd += 1
				while((negInd+1) < negLength and negVal == nData[negInd+1]):
					negInd += 1
			elif (posNext < negNext):
				posVal = posNext
				val = posVal
				posInd += 1
				while((posInd+1) < posLength and posVal == pData[posInd+1]):
					posInd += 1
			elif (posNext > negNext):
				negVal = negNext
				val = negVal
				negInd += 1
				while((negInd+1) < negLength and negVal == nData[negInd+1]):
					negInd += 1
		else:
			if (posNext < negNext):
				posVal = posNext
				val = posVal
				posInd += 1
				while((posInd+1) < posLength and posVal == pData[posInd+1]):
					posInd += 1
			elif (posNext > negNext):
				negVal = negNext
				val = negVal
				negInd += 1
				while((negInd+1) < negLength and negVal == nData[negInd+1]):
					negInd += 1
			else:
				posVal = posNext
				negVal = negNext
				val = posVal
				posInd += 1
				negInd += 1
				while((posInd+1) < posLength and posVal == pData[posInd+1]):
					posInd += 1
				while((negInd+1) < negLength and negVal == nData[negInd+1]):
					negInd += 1

	return entSplit, entMin, pIndMin, nIndMin
