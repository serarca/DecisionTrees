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
	trainData = []
	trueLabels = []
	rules = []

def classify_tree(tree):
	size = trainData.shape[0]
	tree[0][0].trainData = trainData.index.values
	labels = np.zeros(size) - 1
	for l in range(0, len(tree)):
		for i in range(0, 2**l):
			if ((not tree[l][i].leaf) and (not tree[l][i].empty)):
				var = tree[l][i].varMin
				spl = tree[l][i].splMin
				lInd = (trainData[var].loc[tree[l][i].trainData]<=spl).values
				leftIndex = [j for j,b in enumerate(lInd) if b]
				rightIndex = [j for j,b in enumerate(lInd) if not b]
				tree[l+1][2*i].trainData = (tree[l][i].trainData)[leftIndex]
				tree[l+1][2*i + 1].trainData = (tree[l][i].trainData)[rightIndex]
			if (tree[l][i].leaf):
				labels[tree[l][i].trainData] = tree[l][i].prob
	return labels

# We fill the tree with its true labels to calculate error at each leaf later
def fill_true_labels(tree, true_labels):
	true_labels = np.asarray(true_labels)
	for l in range(0, len(tree)):
		for i in range(0, 2**l):
			tree[l][i].true_labels = true_labels[tree[l][i].trainData]

def leaves(tree):
	leaves = []
	for l in range(0, len(tree)):
		for i in range(0, 2**l):
			if (tree[l][i].leaf):
				leaves.append([l,i])
	return leaves

# Returns an array with the rules and their accuracy
def get_rules(tree, true_labels):
	fill_true_labels(tree, true_labels)
	rules = []
	lea = leaves(tree)
	size_pos = len(tree[0][0].pIndex) + 0.0
	size_neg = len(tree[0][0].nIndex) + 0.0
	for k in lea:
		l = k[0]
		i = k[1]
		node = tree[l][i]
		support = (len(node.nIndex)/size_pos + len(node.pIndex)/size_neg)/2
		if (node.prob>=0.5):
			if (len(node.true_labels) == 0):
				error = float('nan')
			else:
				error = sum(abs(node.true_labels - 1))/len(node.true_labels)
		else:
			if (len(node.true_labels) == 0):
				error = float('nan')
			else:
				error = sum(abs(node.true_labels))/len(node.true_labels)
		rules.append({"rule":node.rules, "prob": node.prob, "supp":support, "error":error, "position":[l,i]})
	return rules



# This fills the probabilities in the tree
def fill_prob(tree):
	for l in range(0,len(tree)):
		for i in range(0, 2**l):
			if (not tree[l][i].empty):
				tree[l][i].prob = len(tree[l][i].pIndex)/(len(tree[l][i].pIndex) + len(tree[l][i].nIndex) + 0.0)
	return tree

# This fills the rules in the tree
def fill_rule(tree):
	levels = len(tree)
	for l in range(0,levels):
		for i in range(0, 2**l):
			t = tree[l][i]
			if ((not t.leaf) and (not t.empty)):
				varMin = t.varMin
				splMin = t.splMin
				t1 = tree[l+1][2*i]
				t1.rules = list(t.rules)
				t1.rules.append([info(varMin),"<=",splMin])
				t2 = tree[l+1][2*i + 1]
				t2.rules = list(t.rules)
				t2.rules.append([info(varMin),">",splMin])
	return tree

def fit_tree(levels, weights):
	root = Node()
	root.pIndex = range(0, posData.shape[0])
	root.nIndex = range(0, negData.shape[0])
	root.level = 0
	root.index = 0
	root.leaf = False
	root.empty = False
	root.var = var
	tree = [[root]]
	for l in range(0,levels):
		tree.append([])
		for i in range(0, 2**l):
			t = tree[l][i]
			if ((not t.leaf) and (not t.empty)):
				varMin, splMin, left, right = search_split(t.pIndex, t.nIndex, t.var, weights)
				t.varMin = varMin
				t.splMin = splMin
				t1 = Node()
				t1.pIndex = left[0]
				t1.nIndex = left[1]
				t1.level = l + 1
				t1.index = l * 2
				t1.empty = False
				t1.var = available(varMin, var)
				t1.rules = list(t.rules)
				t1.rules.append([info(varMin),"<=",splMin])
				if (len(t1.pIndex) == 0 or len(t1.nIndex) == 0 or len(t1.var) == 0 or l == levels - 1):
					t1.leaf = True
				else:
					t1.leaf = False
				tree[l+1].append(t1)
				t2 = Node()
				t2.pIndex = right[0]
				t2.nIndex = right[1]
				t2.level = l + 1
				t2.index = l * 2
				t2.empty = False
				t2.var = available(varMin, var)
				t2.rules = list(t.rules)
				t2.rules.append([info(varMin),">",splMin])
				if (len(t2.pIndex) == 0 or len(t2.nIndex) == 0 or len(t2.var) == 0 or l == levels - 1):
					t2.leaf = True
				else:
					t2.leaf = False
				tree[l+1].append(t2)
			else:
				tree[l+1].append(Node())
				tree[l+1].append(Node())
	tree = fill_prob(tree)
	return tree


# Receives a set of indices and a set of variables and weights
def search_split(pInd, nInd, var, weights):
	entMin = float('inf')
	for i,v in enumerate(var):
		print i
		pData = (posData[v].values)[pInd]
		nData = (negData[v].values)[nInd]
		# Should improve this sorting
		pData.sort()
		nData.sort()
		split, ent = find_split(pData, nData)
		ent = ent * weights[v]
		if (ent < entMin):
			varMin = v
			entMin = ent
			splMin = split
	pIn = (posData[varMin][pInd] <= splMin).values
	nIn = (negData[varMin][nInd] <= splMin).values
	left = [[pInd[i] for i,b in enumerate(pIn) if b], [nInd[i] for i,b in enumerate(nIn) if b]]
	right = [[pInd[i] for i,b in enumerate(pIn) if not b], [nInd[i] for i,b in enumerate(nIn) if not b]]

	return varMin, splMin, left, right

def get_first_level_entropies(var):
	entMin = float('inf')
	entropies = []
	for i,v in enumerate(var):
		print i
		pData = posData[v].values
		nData = negData[v].values
		# Should improve this sorting
		pData.sort()
		nData.sort()
		split, ent = find_split(pData, nData)
		entropies.append(ent)
	return entropies

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
		#entropy =  (total * (-p1 * math.log(p1) - (1 - p1) * math.log(1 - p1)) + rest * (-p2 * math.log(p2) - (1 - p2) * math.log(1 - p2)))
		entropy = (total * (1 -p1**2 - (1 - p1)**2) + rest * (1 - p2 ** 2 - (1 - p2) ** 2))
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

	return entSplit, entMin#, pIndMin, nIndMin
