execfile("DecisionTrees/split.py")
execfile("DecisionTrees/dict.py")
import pandas as pd
import time
import numpy as np
from sklearn import metrics
import random

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
variables = np.array(list(posData.columns.values))
weights = linear_weights(variables, 0.35)
# Sample a square root size of the number of variables
sample = random.sample(range(0,len(variables)), int(np.floor(len(variables)**0.5)))


start = time.time()
tree = fit_tree(posData, negData, variables[sample], 3, weights)
end = time.time()
print(end - start)
