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
		#print val, entropy
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
