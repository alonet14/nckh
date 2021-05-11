import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn import metrics

col_names = ['Heart rate', 'Respiratory rate', 'Temperature', 'Label']
pima = pd.read_csv("vitalsign2.csv", header=None, names=col_names)
pima = pima.iloc[1:]
pima.head()

feature_cols = ['Heart rate', 'Respiratory rate', 'Temperature']
X = pima[feature_cols]
y = pima.Label

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=1)

clf = LogisticRegression()
clf = clf.fit(X_train, y_train)
y_pred = clf.predict(X_test)

test_data = [[70, 20, 39]]
test = clf.predict(test_data)
print("Accuracy: ", metrics.accuracy_score(y_test, y_pred))
print("F1 score: ", metrics.f1_score(y_test, y_pred, pos_label="fever"))
print("Test: ", test)
