from sklearn.datasets import load_breast_cancer
data = load_breast_cancer()
df = pd.DataFrame(data.data, columns = data.feature_names)
oldPosData = df[data.target == 1].reset_index(drop=True)
oldNegData = df[data.target == 0].reset_index(drop=True)
var = list(oldPosData.columns.values)
trainPosIndex = random.sample(range(0,oldPosData.shape[0]), int(math.floor(oldPosData.shape[0]*0.8)))
trainNegIndex = random.sample(range(0,oldNegData.shape[0]), int(math.floor(oldNegData.shape[0]*0.8)))
posData = oldPosData.iloc[trainPosIndex].reset_index(drop=True)
negData = oldNegData.iloc[trainNegIndex].reset_index(drop=True)

testPosIndex = [i for i in range(0,oldPosData.shape[0]) if i not in trainPosIndex]
testNegIndex = [i for i in range(0,oldNegData.shape[0]) if i not in trainNegIndex]
trainData = pd.concat([oldPosData.loc[testPosIndex],oldNegData.loc[testNegIndex]])
trainData = trainData.reset_index(drop=True)

def available(a,b):
    return b
def info(a):
    return a

tree = fit_tree(2)
prediction = classify_tree(tree)
true_labels = np.append(np.zeros(len(testPosIndex)) + 1,np.zeros(len(testNegIndex)))
error = sum(abs(true - prediction))/trainData.shape[0]
error
rules = get_rules(tree,true_labels)


#var = ["a","b","c"]
#pData = [random.randint(0,10) for i in range(0,10)]
#pData.sort()
#nData = [random.randint(0,10) for i in range(0,10)]
#nData.sort()
if False:
    a = [random.randint(0,10) for i in range(0,10)]
    b = [random.randint(0,10) for i in range(0,10)]
    c = [random.randint(0,10) for i in range(0,10)]
    posData = pd.DataFrame.from_items([("a",a), ("b",b), ("c",c)])

    a = [random.randint(0,10) for i in range(0,10)]
    b = [random.randint(0,10) for i in range(0,10)]
    c = [random.randint(0,10) for i in range(0,10)]
    negData = pd.DataFrame.from_items([("a",a), ("b",b), ("c",c)])

    a = [random.randint(0,10) for i in range(0,10)]
    b = [random.randint(0,10) for i in range(0,10)]
    c = [random.randint(0,10) for i in range(0,10)]
    trainData = pd.DataFrame.from_items([("a",a), ("b",b), ("c",c)])

    var = ['a','b','c']
    def available(a,b):
        return b

    #pInd = [0,3,4,5,8]
    #nInd = [3,4,6,7,9]


if False:
    #levels = 1
    # Create the root of the tree
import math
import random
import pandas as pd
import numpy as np
import time

oldPosData = oldPosData.reset_index(drop=True)
oldNegData = oldNegData.reset_index(drop=True)
#oldPosData.drop('index', axis=1, inplace=True)
#oldNegData.drop('index', axis=1, inplace=True)


var = list(oldPosData.columns.values)

trainPosIndex = random.sample(range(0,oldPosData.shape[0]), int(math.floor(oldPosData.shape[0]*0.8)))
trainNegIndex = random.sample(range(0,oldNegData.shape[0]), int(math.floor(oldNegData.shape[0]*0.8)))

posData = oldPosData.iloc[trainPosIndex].reset_index(drop=True)
negData = oldNegData.iloc[trainNegIndex].reset_index(drop=True)

testPosIndex = [i for i in range(0,oldPosData.shape[0]) if i not in trainPosIndex]
testNegIndex = [i for i in range(0,oldNegData.shape[0]) if i not in trainNegIndex]
trainData = pd.concat([oldPosData.loc[testPosIndex],oldNegData.loc[testNegIndex]])
trainData = trainData.reset_index(drop=True)

start = time.time()
tree = fit_tree(3)
end = time.time()
prediction = classify_tree(tree)
true = np.append(np.zeros(len(testPosIndex)) + 1,np.zeros(len(testNegIndex)))
error = sum(abs(true - prediction))/trainData.shape[0]
error

print(end - start)
