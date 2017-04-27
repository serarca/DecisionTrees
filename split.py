
def find_split(posData, negData, probSens = .0001):

	entMin = float('inf')

	posLength = len(posData)
	negLength = len(negData)

	posInd = 0
	negInd = 0

	while( posInd<posLength && negInd<negLength):
		# Should check this part of the code for equality instances
		if (posData[posInd] < negData[negInd]):
			val = posData[posInd]
			++posInd
		else:
			val = negData[negInd]
			++negInd

		total = max(posCount+negCount, .1)
		rest = max(posLength + negLength - posCount - negCount, .1)
		p1 = float(posData)/float(total)
		p2 = float(posLength - posData)/float(total)
		p1 = max(probSens, min(p1, 1 - probSens))
		p2 = max(probSens, min(p2, 1 - probSens))

		entropy =  total * (-p1 * math.log(p1) - (1 - p1) * math.log(1 - p1)) +
		 			rest * (-p2 * math.log(p2) - (1 - p2) * math.log(1 - p2))

		if (entropy < entMin):
			entMin = entropy
			entSplit = val



