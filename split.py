import math

#nData = [0,0,0,0,1,2,3,3,4,4,5,6,6,7,7,7,7]
#pData = [2,4,4,5,5,6,6,6,7,7,8,8,8,8,8,8,8,8]

def find_split(pData, nData, probSens = .0001):
	entMin = float('inf')
	posLength = len(pData)
	negLength = len(nData)
	posInd = 0
	negInd = 0
	posCount = 0
	negCount = 0
	posVal = pData[posInd]
	negVal = nData[negInd]
	# Set the indices at the last index with the same value
	while((posInd+1) < posLength and posVal == pData[posInd + 1]):
		posInd += 1
	while((negInd+1) < negLength and negVal == nData[negInd + 1]):
		negInd += 1
	val = 0
	while( True ):
		if (posVal < negVal):
			val = posVal
			if (posInd + 1 < posLength):
				posVal = pData[posInd + 1]
			posInd += 1
		elif (posVal > negVal):
			val = negVal
			if (negInd + 1 < negLength):
				negVal = nData[negInd + 1]
			negInd += 1

		else:
			val = negVal
			if (negInd + 1 < negLength):
				negVal = nData[negInd + 1]
			if (posInd + 1 < posLength):
				posVal = pData[posInd + 1]
			posInd += 1
			negInd += 1
		total = max(posInd + negInd, .1)
		rest = max(posLength + negLength - posInd - negInd, .1)
		p1 = float(posInd)/float(total)
		p2 = float(posLength - posInd)/float(rest)
		p1 = max(probSens, min(p1, 1 - probSens))
		p2 = max(probSens, min(p2, 1 - probSens))
		entropy =  (total * (-p1 * math.log(p1) - (1 - p1) * math.log(1 - p1)) +
		 			rest * (-p2 * math.log(p2) - (1 - p2) * math.log(1 - p2)))
		if (entropy < entMin):
			entMin = entropy
			entSplit = val
		while((posInd+1) < posLength and posVal == pData[posInd+1]):
			posInd += 1
		while((negInd+1) < negLength and negVal == nData[negInd+1]):
			negInd += 1
		if(posInd == posLength or  negInd == negLength):
			break
	return entSplit, entropy


def find_split_old(posSort, negSort):
	entMin = 99999999999
	entSplit = -1

	posCount = 0
	negCount = 0

	val = min(posSort[0], negSort[0])

	posLength = len(pData)
	negLength = len(nData)

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

	return entMin, entSplit
