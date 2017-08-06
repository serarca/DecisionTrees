# This script is a validation of the procedure for training rules
import numpy as np
import scipy as sp
import pandas as pd
import os
import math
import sys
import random
import pickle
import time

execfile("/lfs/local/0/camelo/DecisionTrees/split.py")
execfile("/lfs/local/0/camelo/DecisionTrees/dict.py")
execfile("/lfs/local/0/camelo/DecisionTrees/set_cover.py")

# Get name of files
filenames = os.listdir("/dfs/scratch0/sergio/PositiveData/")
random.shuffle(filenames)


# Divide in train and test
train_filenames = filenames[:int(len(filenames)*0.8)]
test_filenames = filenames[int(len(filenames)*0.8):]


# Load the positive data
pos_tr = []
for f in train_filenames:
	data = np.fromfile("/dfs/scratch0/sergio/PositiveData/"+f)
	data = data.reshape(len(data)/70208, 70208)
	data = pd.DataFrame(data)
	pos_tr.append(data)
	print(f)

pos_te = []
for f in test_filenames:
        data = np.fromfile("/dfs/scratch0/sergio/PositiveData/"+f)
        data = data.reshape(len(data)/70208, 70208)
        data = pd.DataFrame(data)
        pos_te.append(data)
	print(f)

TrainPositiveData = pd.concat(pos_tr)
TrainPositiveData = TrainPositiveData.reset_index(drop = True)

TestPositiveData = pd.concat(pos_te)
TestPositiveData = TestPositiveData.reset_index(drop = True)

# Load the negative data

neg_tr = []
for f in train_filenames:
	if (os.path.isfile("/dfs/scratch0/sergio/NegativeData/"+f)):
		data = np.fromfile("/dfs/scratch0/sergio/NegativeData/"+f)
		data = data.reshape(len(data)/70208, 70208)
		data = pd.DataFrame(data)
		neg_tr.append(data)
		print(f)
neg_te = []
for f in test_filenames:
	if (os.path.isfile("/dfs/scratch0/sergio/NegativeData/"+f)):
		data = np.fromfile("/dfs/scratch0/sergio/NegativeData/"+f)
		data = data.reshape(len(data)/70208, 70208)
		data = pd.DataFrame(data)
		neg_te.append(data)
		print(f)

TrainNegativeData = pd.concat(neg_tr)
TrainNegativeData = TrainNegativeData.reset_index(drop = True)

TestNegativeData = pd.concat(neg_te)
TestNegativeData = TestNegativeData.reset_index(drop = True)

# We need to split the train data randomly so that we fit trees in one portion and validate in the
# other portion

fitPosIndex = random.sample(range(0,TrainPositiveData.shape[0]), int(math.floor(TrainPositiveData.shape[0]*0.8)))
fitNegIndex = random.sample(range(0,TrainNegativeData.shape[0]), int(math.floor(TrainNegativeData.shape[0]*0.8)))
valPosIndex = [i for i in range(0,TrainPositiveData.shape[0]) if i not in fitPosIndex]
valNegIndex = [i for i in range(0,TrainNegativeData.shape[0]) if i not in fitNegIndex]

posData = TrainPositiveData.iloc[fitPosIndex].reset_index(drop = True)
negData = TrainNegativeData.iloc[fitNegIndex].reset_index(drop = True)
valData = pd.concat([TrainPositiveData.iloc[valPosIndex],TrainNegativeData.iloc[valNegIndex]])
valData = valData.reset_index(drop = True)

posData = posData.as_matrix()
negData = negData.as_matrix()
valData = valData.as_matrix()
true_labels = [1 for i in range(0, len(valPosIndex))] + [0 for i in range(0, len(valNegIndex))]

# Save the data

posData.tofile("/lfs/local/0/camelo/TreeData/posData.npy")
negData.tofile("/lfs/local/0/camelo/TreeData/negData.npy")
valData.tofile("/lfs/local/0/camelo/TreeData/valData.npy")
np.save("/lfs/local/0/camelo/TreeData/true_label.npy",true_labels)

# Write a shell file to produce trees
n_trees = 1
with open("/lfs/local/camelo/DecisionTrees/gen_random_trees.sh", "w+") as f:
        for i in range(0, n_trees):
                f.write("python /lfs/local/camelo/DecisionTrees/Scripts/random_script.py "+str(i)+"\n")


# After running the shell file read the trees
trees = []
for i in range(0, n_trees):
        with open('/lfs/local/camelo/rules/rules'+str(i)+'.pickle', 'rb') as handle:
                trees.append(pickle.load(handle))

# We paste all rules together
rules = []
for t in trees:
        auc = t["area"]
        rul = t["rules"]
        pos_r = positive_rules(rul, 0.8)
        for r in pos_r:
                r["area"] = auc
                rules.append(r)


# These vectors hold the number of times that data is covered
train_cover = np.zeros(posData.shape[0])
val_cover = np.zeros(valData.shape[0])
for i in range(0, n_trees):
        tr_cover = rules[i]["cover_train"]
        va_cover = rules[i]["cover_test"]
        for j in tr_cover:
                train_cover[j]+=1
        for j in va_cover:
                val_cover[j]+=1

val_cover = [v for i,v in enumerate(val_cover) if true_labels[i]==1]

print(sum(train_cover>0)/(len(train_cover) +0.0))
print(sum(np.array(val_cover)>0)/(len(val_cover) +0.0))

# We construct an array of dictionaries and a universe to solve the set cover problem
sets = []
weights = []
for i,r in enumerate(rules):
        sets.append(["tr"+str(x) for x in r['cover_train']] + ["te"+str(x) for x in r['cover_test']])
        weights.append(1-r["area"])

universe = ["tr"+str(x) for x in range(0,len(train_cover))]+["te"+str(x) for x in range(0,valData.shape[0]) if true_labels[x] == 1]

# Solve the set cover problem
sol = set_cover(sets, weights, universe)
cover_rules = [r for i,r in enumerate(rules) if sol[i]==1]

# This function applies a rule to data
def apply_rule(data, rule):
	checked = np.zeros(data.shape[0])
	for i,r in enumerate(rule):
		values = data[r[0]]
		if r[1] == '<=':
			checked += (values<= r[2])
		else:
			checked += (values> r[2])
	return (checked==len(rule))

# We apply the rules to the test data
result_pos = np.zeros(TestPositiveData.shape[0])
result_neg = np.zeros(neg[0].shape[0])
for i,r in enumerate(cover_rules):
	result_pos += apply_rule(TestPositiveData, r['f_rule'])
	result_neg+= apply_rule(neg[0], r['f_rule'])

sum(result_pos>0)/(len(result_pos)+0.0)
sum(result_neg>0)/(len(result_neg)+0.0)









