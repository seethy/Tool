import numpy as np
from sklearn import svm

X = np.array([[-1, -1], [-2, -1], [1, 1], [2, 1]])
y = np.array([1, 1, 2, 2])

clt = svm.SVC(probability=True)
clt.fit(X, y)

print(clt.predict([[-0.8, -1]]))
print(clt.predict_proba([[-0.8, -1]]))