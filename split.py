import math
import random

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




	return entSplit, entMin


def find_split_old(posSort, negSort):
	entMin = 99999999999
	entSplit = -1

	posCount = 0
	negCount = 0

	val = min(posSort[0], negSort[0])

	posLength = len(posSort)
	negLength = len(negSort)

	while(True):
		a = sum(i <= val for i in posSort)
		b = sum(i <= val for i in negSort)

		# print a, b
		tot = max(a + b,0.1)
		rest = max(posLength + negLength - a - b,0.1)
		p1 = float(a)/float(tot)
		p2 = float(posLength - a) / float(rest)

		p1 = max(0.0001, min(p1, 0.9999))
		p2 = max(0.0001, min(p2, 0.9999))

		entropy = tot* (-p1*math.log(p1) - (1-p1) * math.log(1-p1)) + rest* (-p2*math.log(p2) - (1-p2) * math.log(1-p2))

		if (entropy < entMin):
			entMin = entropy
			entSplit = val

		if (math.isnan(val)):
			break
		elif (a < posLength and b < negLength):
			val = min(posSort[a], negSort[b])
		elif(a < posLength):
			val = posSort[a]
		elif(b < negLength):
			val = negSort[b]
		else:
			break

	return entSplit, entMin
