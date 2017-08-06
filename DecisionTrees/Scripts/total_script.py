execfile("DecisionTrees/split.py")
execfile("DecisionTrees/dict.py")
import pandas as pd
import time
import numpy as np
from sklearn import metrics

posData = np.fromfile("/lfs/local/camelo/DecisionTrees/posData.np")
posData = posData.reshape(403, 70208)
posData = pd.DataFrame(posData)

negData = np.fromfile("/lfs/local/camelo/DecisionTrees/negData.np")
negData = negData.reshape(18710, 70208)
negData = pd.DataFrame(negData)


testData = np.fromfile("/lfs/local/camelo/DecisionTrees/trainData.np")
testData = trainData.reshape(4779, 70208)
testData = pd.DataFrame(trainData)

true = np.fromfile("/lfs/local/camelo/DecisionTrees/true.np")
variables = list(posData.columns.values)


start = time.time()
tree = fit_tree(posData, negData, variables, 3, linear_weights(variables, 0.35))
end = time.time()
print(end - start)

prediction = classify_tree(tree, testData, true)
error = sum(abs(true - prediction))/trainData.shape[0]
rules = get_rules(tree)

fpr, tpr, thresholds = metrics.roc_curve(true, prediction, pos_label=1)
metrics.auc(fpr, tpr)
