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

#pInd = [0,3,4,5,8]
#nInd = [3,4,6,7,9]



levels = 1
# Create the root of the tree
root = Node()
root.pIndex = range(0, posData.shape[0])
root.nIndex = range(0, negData.shape[0])
root.level = 0
root.index = 0
root.leaf = False
root.empty = False

tree = [[root]]

for l in range(0,levels):
	print l
	tree.append([])
	for i in range(0, 2**l):
		t = tree[l][i]
		if ((not t.leaf) and (not t.empty)):
			varMin, splMin, left, right = search_split(t.pIndex, t.nIndex, var)
			t.varMin = varMin
			t.splMin = splMin
			t1 = Node()
			t1.pIndex = left[0]
			t1.nIndex = left[1]
			t1.level = l + 1
			t1.index = l * 2
			t1.empty = False
			if (len(t1.pIndex) == 0 or len(t1.nIndex) == 0):
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
			if (len(t2.pIndex) == 0 or len(t2.nIndex) == 0):
				t2.leaf = True
			else:
				t2.leaf = False
			tree[l+1].append(t2)
		else:
			tree[l+1].append(Node())
			tree[l+1].append(Node())
