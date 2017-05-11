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


trainData = np.fromfile("/lfs/local/camelo/DecisionTrees/trainData.np")
trainData = trainData.reshape(4779, 70208)
trainData = pd.DataFrame(trainData)

true = np.fromfile("/lfs/local/camelo/DecisionTrees/true.np")
variables = list(posData.columns.values)
weights = linear_weights(variables, 0.35)
# Sample a square root size of the number of variables
sample = random.sample(range(0,len(variables)), int(np.floor(len(variables)**0.5))


start = time.time()
tree = fit_tree(posData, negData, variables, 3, random.sa)
end = time.time()
print(end - start)
