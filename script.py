execfile("DecisionTrees/split.py")
execfile("DecisionTrees/dict.py")
import pandas as pd
import time

posData = np.fromfile("/lfs/local/camelo/DecisionTrees/posData.np")
posData = posData.reshape(403, 70208)
posData = pd.DataFrame(posData)

negData = np.fromfile("/lfs/local/camelo/DecisionTrees/negData.np")
negData = negData.reshape(18710, 70208)
negData = pd.DataFrame(negData)


trainData = np.fromfile("/lfs/local/camelo/DecisionTrees/trainData.np")
trainData = trainData.reshape(4779, 70208)
trainData = pd.DataFrame(trainData)

true = np.fromfile("/lfs/local/camelo/DecisionTrees/true.np")
var = list(posData.columns.values)


start = time.time()
tree = fit_tree(3, linear_weights(var, 0))
end = time.time()
print(end - start)

prediction = classify_tree(tree)
error = sum(abs(true - prediction))/trainData.shape[0.15]
rules = get_rules(tree,true)

import numpy as np
from sklearn import metrics
fpr, tpr, thresholds = metrics.roc_curve(true, prediction, pos_label=1)
metrics.auc(fpr, tpr)
