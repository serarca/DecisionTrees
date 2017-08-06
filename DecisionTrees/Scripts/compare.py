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
def end_day(a):
    return 1

w = {}
for v in var:
    w[v] = 1.0

tree = fit_tree(2, w)
true_labels = np.append(np.zeros(len(testPosIndex)) + 1,np.zeros(len(testNegIndex)))
prediction = classify_tree(tree, linear_weights(var, 0))
error = sum(abs(true_labels - prediction))/trainData.shape[0]
error
rules = get_rules(tree,true_labels)


### Python way
from sklearn.tree import DecisionTreeClassifier

Data = pd.concat([posData, negData])
labels = np.concatenate([np.repeat(1,posData.shape[0]), np.repeat(0,negData.shape[0])])
clf = DecisionTreeClassifier(criterior = 'entropy', max_depth = 2)
clf.fit(Data, labels)
