import time
import numpy as np
from sklearn import metrics
import random
import sys
import pickle
import pandas as pd
execfile("/lfs/local/camelo/DecisionTrees/split.py")
execfile("/lfs/local/camelo/DecisionTrees/dict.py")
execfile("/lfs/local/camelo/DecisionTrees/set_cover.py")

# This code produces random trees, then reads the rules generated
# by them and finally goes and solve a set cover problem

# Write a shell file to produce trees
n_trees = 16
with open("/lfs/local/camelo/DecisionTrees/gen_random_trees.sh", "w+") as f:
	for i in range(0, n_trees):
		f.write("python /lfs/local/camelo/DecisionTrees/Scripts/random_script.py "+str(i)+"\n")

# After running the shell file read the trees
trees = []
for i in range(0, n_trees):
	with open('/lfs/local/camelo/trees/rules'+str(i)+'.pickle', 'rb') as handle:
    		trees.append(pickle.load(handle))

# Load the data
posData = np.fromfile("/lfs/local/camelo/DecisionTrees/TreeData/posData.np")
posData = posData.reshape(403, 70208)
posData = pd.DataFrame(posData)

negData = np.fromfile("/lfs/local/camelo/DecisionTrees/TreeData/negData.np")
negData = negData.reshape(18710, 70208)
negData = pd.DataFrame(negData)


testData = np.fromfile("/lfs/local/camelo/DecisionTrees/TreeData/trainData.np")
testData = testData.reshape(4779, 70208)
testData = pd.DataFrame(testData)

true = np.fromfile("/lfs/local/camelo/DecisionTrees/TreeData/true.np")
variables = np.array(list(posData.columns.values))

# We paste all rules together
rules = []
for t in trees:
	auc = t["area"]
	rul = t["rules"]	
	pos_r = positive_rules(rul, 0.5)
	for r in pos_r:
		r["area"] = auc
		rules.append(r)
	


# These vectors hold the number of times that data is covered
train_cover = np.zeros(posData.shape[0])
test_cover = np.zeros(testData.shape[0])
for i in range(0, n_trees):
	tr_cover = rules[i]["cover_train"]
	te_cover = rules[i]["cover_test"]
	for j in tr_cover:
		train_cover[j]+=1
	for j in te_cover:
		test_cover[j]+=1

test_cover = test_cover[true == 1]

print(sum(train_cover==0)/(len(train_cover) +0.0))
print(sum(test_cover==0)/(len(test_cover) +0.0))

# We construct an array of dictionaries and a universe to solve the set cover problem
sets = []
weights = []
for i,r in enumerate(rules):
	sets.append(["tr"+str(x) for x in r['cover_train']] + ["te"+str(x) for x in r['cover_test']])
	weights.append(1-r["area"])

universe = ["tr"+str(x) for x in range(0,len(train_cover))]+["te"+str(x) for x in range(0,testData.shape[0]) if true[x] == 1]

# Solve the set cover problem
sol = set_cover(sets, weights, universe)
cover_rules = [r for i,r in enumerate(rules) if sol[i]>0]














