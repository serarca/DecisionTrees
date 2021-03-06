class Node:
	prob = float('nan')
	nIndex = []
	pIndex = []
	varMin = ""
	splMin = 0
	level = 0
	index = 0
	leaf = False
	empty = True
	var = []
	testData = []
	trueLabels = []
	rules = []
	entropies = []
	f_rules = []

def classify_tree(tree, testData, true_labels):
	size = testData.shape[0]
	tree[0][0].testData = testData.index.values
	labels = np.zeros(size) - 1
	for l in range(0, len(tree)):
		for i in range(0, 2**l):
			if ((not tree[l][i].leaf) and (not tree[l][i].empty)):
				var = tree[l][i].varMin
				spl = tree[l][i].splMin
				lInd = (testData[var].loc[tree[l][i].testData]<=spl).values
				leftIndex = [j for j,b in enumerate(lInd) if b]
				rightIndex = [j for j,b in enumerate(lInd) if not b]
				tree[l+1][2*i].testData = (tree[l][i].testData)[leftIndex]
				tree[l+1][2*i + 1].testData = (tree[l][i].testData)[rightIndex]
			if (tree[l][i].leaf):
				labels[tree[l][i].testData] = tree[l][i].prob
	true_labels = np.asarray(true_labels)
	for l in range(0, len(tree)):
		for i in range(0, 2**l):
			tree[l][i].true_labels = true_labels[tree[l][i].testData]
	return labels


# Returns the coordinates of the leaves of the tree
def leaves(tree):
	leaves = []
	for l in range(0, len(tree)):
		for i in range(0, 2**l):
			if (tree[l][i].leaf):
				leaves.append([l,i])
	return leaves

# Returns an array with the rules and their accuracy
def get_rules(tree):
	rules = []
	lea = leaves(tree)
	size_pos = len(tree[0][0].pIndex) + 0.0
	size_neg = len(tree[0][0].nIndex) + 0.0
	for k in lea:
		l = k[0]
		i = k[1]
		node = tree[l][i]
		support = (len(node.nIndex)/size_neg + len(node.pIndex)/size_pos)/2
		if (node.prob[len(node.prob)-1]>=0.5):
			if (len(node.true_labels) == 0):
				error = float('nan')
			else:
				error = sum(abs(node.true_labels - 1))/(len(node.true_labels)+0.0)
		else:
			if (len(node.true_labels) == 0):
				error = float('nan')
			else:
				error = sum(abs(node.true_labels))/(len(node.true_labels)+0.0)
		rules.append({"rule":node.rules, "f_rule":node.f_rules, "prob": node.prob, "supp":support, "error":error, "position":[l,i], "cover_train":node.pIndex, "cover_test":[v for i,v in enumerate(node.testData) if (node.true_labels[i]==1)]})
	return rules

# Filters rules and returns only those rules that lead to positive outcomes
def positive_rules(rules, threshold):
	pos_rules = []
	for r in rules:
		l = len(r["prob"])
		if r["prob"][l-1]>threshold:
			pos_rules.append(r)
	return pos_rules



def fit_tree(posData, negData, variables, levels, weights):
	variables = longer_intervals(variables, levels, 24)
	print(variables)
	root = Node()
	root.pIndex = range(0, posData.shape[0])
	root.nIndex = range(0, negData.shape[0])
	root.level = 0
	root.index = 0
	root.leaf = False
	root.empty = False
	root.var = available(0,1/(levels+0.0),variables)
	#root.var = available(0,1,variables)
	root.prob = [len(root.pIndex)/(len(root.pIndex) + len(root.nIndex) + 0.0)]
	tree = [[root]]
	for l in range(0,levels):
		tree.append([])
		for i in range(0, 2**l):
			t = tree[l][i]
			if ((not t.leaf) and (not t.empty)):
				varMin, splMin, left, right, entropies = search_split(posData, negData, t.pIndex, t.nIndex, t.var, weights)
				t.varMin = varMin
				t.splMin = splMin
				t.entropies = entropies
				t1 = Node()
				t1.pIndex = left[0]
				t1.nIndex = left[1]
				t1.prob = list(t.prob) + [len(t1.pIndex)/(len(t1.pIndex) + len(t1.nIndex) + 0.0)]
				t1.level = l + 1
				t1.index = l * 2
				t1.empty = False
				#t1.var = available(varMin, variables)
				#t1.var = available((l+1)/(levels+0.0),(l+2)/(levels+0.0),variables)
				t1.var = available(0,(l+2)/(levels+0.0),variables)
				#t1.var = available(0,1,variables)
				t1.rules = list(t.rules)
				t1.f_rules = list(t.f_rules)
				t1.rules.append([info(varMin),"<=",splMin])
				t1.f_rules.append([varMin,"<=",splMin])
				if (len(t1.pIndex) == 0 or len(t1.nIndex) == 0 or len(t1.var) == 0 or l == levels - 1):
					t1.leaf = True
				else:
					t1.leaf = False
				tree[l+1].append(t1)
				t2 = Node()
				t2.pIndex = right[0]
				t2.nIndex = right[1]
				t2.prob = list(t.prob) + [len(t2.pIndex)/(len(t2.pIndex) + len(t2.nIndex) + 0.0)]
				t2.level = l + 1
				t2.index = l * 2
				t2.empty = False
				#t2.var = available(varMin, variables)
				#t2.var = available((l+1)/(levels+0.0),(l+2)/(levels+0.0),variables)
				t2.var = available(0,(l+2)/(levels+0.0),variables)
				#t2.var = available(0,1,variables)
				t2.rules = list(t.rules)
				t2.f_rules = list(t.f_rules)
				t2.rules.append([info(varMin),">",splMin])
				t2.f_rules.append([varMin,">",splMin])
				if (len(t2.pIndex) == 0 or len(t2.nIndex) == 0 or len(t2.var) == 0 or l == levels - 1):
					t2.leaf = True
				else:
					t2.leaf = False
				tree[l+1].append(t2)
			else:
				tree[l+1].append(Node())
				tree[l+1].append(Node())
	return tree


# Receives a set of indices and a set of variables and weights
def search_split(posData, negData, pInd, nInd, variables, weights):
	# Here we will save the entropies of each variable
	entropies = np.zeros(len(variables))
	entMin = float('inf')
	for i,v in enumerate(variables):
		print i
		pData = (posData[v].values)[pInd]
		nData = (negData[v].values)[nInd]
		# Should improve this sorting
		pData.sort()
		nData.sort()
		split, ent = find_split(pData, nData)
		entropies[i] = ent
		ent = ent * weights[v]
		if (ent < entMin):
			varMin = v
			entMin = ent
			splMin = split
	pIn = (posData[varMin][pInd] <= splMin).values
	nIn = (negData[varMin][nInd] <= splMin).values
	left = [[pInd[i] for i,b in enumerate(pIn) if b], [nInd[i] for i,b in enumerate(nIn) if b]]
	right = [[pInd[i] for i,b in enumerate(pIn) if not b], [nInd[i] for i,b in enumerate(nIn) if not b]]

	return varMin, splMin, left, right, entropies


def find_split(pData, nData, probSens = .0001):
	prePosLength = len(pData)
	preNegLength = len(nData)
	pData = [v for v in pData if not math.isnan(v)]
	nData = [v for v in nData if not math.isnan(v)]
	entMin = float('inf')
	entSplit = float('nan')
	posLength = len(pData)
	negLength = len(nData)
	if (posLength == 0 or negLength == 0):
		return entSplit, entMin
	posInd = 0
	negInd = 0
	posVal = pData[posInd]
	negVal = nData[negInd]

	if (posVal > negVal):
		posInd = -1
		negInd = 0
		while ((negInd+1) < negLength and negVal == nData[negInd + 1]):
			negInd += 1
	elif (posVal < negVal):
		posInd = 0
		negInd = -1
		while ((posInd+1) < posLength and posVal == pData[posInd + 1]):
			posInd += 1
	else:
		posInd = 0
		negInd = 0
		while ((posInd+1) < posLength and posVal == pData[posInd + 1]):
			posInd += 1
		while ((negInd+1) < negLength and negVal == nData[negInd + 1]):
			negInd += 1

	# Set the indices at the last index with the same value
	val = min(posVal,negVal)
	i=0
	while( True ):
		# Should look into this
		posCount = posInd + 1
		negCount = negInd + 1
		total = max(posCount + negCount, .1)
		rest = max(prePosLength + preNegLength - posCount - negCount, .1)
		p1 = float(posCount)/float(total)
		p2 = float(prePosLength - posCount)/float(rest)
		p1 = max(probSens, min(p1, 1 - probSens))
		p2 = max(probSens, min(p2, 1 - probSens))
		entropy =  (total * (-p1 * math.log(p1) - (1 - p1) * math.log(1 - p1)) + rest * (-p2 * math.log(p2) - (1 - p2) * math.log(1 - p2)))
		#entropy = (total * (1 -p1**2 - (1 - p1)**2) + rest * (1 - p2 ** 2 - (1 - p2) ** 2))
		#print val, entropy
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
	return entSplit, entMin
