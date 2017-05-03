#var = ["a","b","c"]
#pData = [random.randint(0,10) for i in range(0,10)]
#pData.sort()
#nData = [random.randint(0,10) for i in range(0,10)]
#nData.sort()

#a = [random.randint(0,10) for i in range(0,10)]
#b = [random.randint(0,10) for i in range(0,10)]
#c = [random.randint(0,10) for i in range(0,10)]
#posData = pd.DataFrame.from_items([("a",a), ("b",b), ("c",c)])

#a = [random.randint(0,10) for i in range(0,10)]
#b = [random.randint(0,10) for i in range(0,10)]
#c = [random.randint(0,10) for i in range(0,10)]
#negData = pd.DataFrame.from_items([("a",a), ("b",b), ("c",c)])

#pInd = [0,3,4,5,8]
#nInd = [3,4,6,7,9]



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

start = time.time()
tree = fit_tree(3)
end = time.time()
print(end - start)
