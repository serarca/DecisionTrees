import pandas as pd
import time
import numpy as np
from sklearn import metrics
import random
import sys
import pickle
execfile("/lfs/local/0/camelo/DecisionTrees/split.py")
execfile("/lfs/local/0/camelo/DecisionTrees/dict.py")

posData = np.fromfile("/lfs/local/0/camelo/TreeData/posData.npy")
posData = posData.reshape(len(posData)/70208, 70208)
posData = pd.DataFrame(posData)
print(posData.shape)

negData = np.fromfile("/lfs/local/0/camelo/TreeData/negData.npy")
negData = negData.reshape(len(negData)/70208, 70208)
negData = pd.DataFrame(negData)
print(negData.shape)

testData = np.fromfile("/lfs/local/0/camelo/TreeData/valData.npy")
testData = testData.reshape(len(testData)/70208, 70208)
testData = pd.DataFrame(testData)
print(testData.shape)

true = np.load("/lfs/local/0/camelo/TreeData/true_label.npy")
variables = np.array(list(posData.columns.values))
weights = linear_weights(variables, 0)
# Sample a square root size of the number of variables
#sample = sample_sensors(16)

start = time.time()
tree = fit_tree(posData, negData, variables, 3, weights)
end = time.time()
print(end - start)

prediction = classify_tree(tree, testData, true)
error = sum(abs(true - prediction))/testData.shape[0]
rules = get_rules(tree)

fpr, tpr, thresholds = metrics.roc_curve(true, prediction, pos_label=1)
area = metrics.auc(fpr, tpr)

tree_info = {"area":area, "rules":rules}

file_number = sys.argv[1]
with open('/lfs/local/camelo/trees/trees'+file_number+'.pickle', 'w+') as handle:
    pickle.dump(tree, handle, protocol=pickle.HIGHEST_PROTOCOL)

with open('/lfs/local/camelo/rules/rules'+file_number+'.pickle', 'w+') as handle:
    pickle.dump(tree_info, handle, protocol=pickle.HIGHEST_PROTOCOL) 


