#importing libraries
import pandas as pd
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import seaborn as sns
#import statsmodels.api as smimport % matplotlib inline
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.feature_selection import RFE, SelectKBest, chi2, f_classif, mutual_info_classif
from sklearn.linear_model import RidgeCV, LassoCV, Ridge, Lasso
from importlib import reload
import FE
reload(FE)
from FE import FE

#Loading the dataset
df = pd.read_csv('data.csv')

xcols = ['usecompetitors','sessions', 'FF', 'strategic', 'callcycle']

ycol = df['churn']

 
cc = {'Monthly':'12', 'Quarterly':'4', 'Yearly':'1','Half Year':'2', 'Every Other Month':'6', 'None':'0'}
df['callcycle'].replace(cc,inplace=True)
df['callcycle']= pd.to_numeric(df['callcycle'])
df['callcycle']

X, y, xcolnames = FE(df,xcols,ycol, standardize=False)


sel_chi2 = SelectKBest(chi2, k=4)    # select 4 features
X_train_chi2 = sel_chi2.fit_transform(X, y)
print(sel_chi2.get_support())

sel_f = SelectKBest(f_classif, k=4)
X_train_f = sel_f.fit_transform(X, y)
print(sel_f.get_support())

sel_mutual = SelectKBest(mutual_info_classif, k=4)
X_train_mutual = sel_mutual.fit_transform(X, y)
print(sel_mutual.scores_)

#Target Variable
df.head()

def stratified_cv(X, y, clf_class, shuffle=True, n_folds=10, **kwargs):
    stratified_k_fold = StratifiedKFold(n_splits=n_folds, shuffle=shuffle)
    y_pred = y.copy()
    # ii -> train
    # jj -> test indices
    for ii, jj in stratified_k_fold.split(X,y): 
        X_train, X_test = X[ii], X[jj]
        y_train = y[ii]
        clf = clf_class(**kwargs)
        clf.fit(X_train,y_train)
        y_pred[jj] = clf.predict(X_test)
    return y_pred



#Using Pearson Correlation
plt.figure(figsize=(16,16))
cor = df.corr()
sns.heatmap(cor, annot=True, cmap=plt.cm.Reds)
plt.show()

#Correlation with output variable
cor_target = abs(cor["churn"])
#Selecting highly correlated features
relevant_features = cor_target[cor_target>0.2]
relevant_features

import matplotlib
matplotlib.rcParams['figure.figsize'] = (8.0, 10.0)
imp_coef.plot(kind = "barh")
plt.title("Feature importance using Lasso Model")