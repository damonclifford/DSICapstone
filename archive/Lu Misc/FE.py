import numpy as np
import pandas as pd
from sklearn.model_selection import StratifiedKFold
from sklearn.metrics import auc
from sklearn.metrics import roc_curve
from scipy import interp

def FE(df, xcols, ycol, standardize=True):
    """ Prepares a feature matrix and response var from a dataset 
    
    Arguments:
        df {dataframe} -- dataframe to pass in for modeling
        xcols {any} -- columns to use as independent var
        ycol {any} -- columns to use as response
    
    Returns:
        [type] -- [description]
    """
    # Set up response variable 
    y = df[ycol].values.astype(np.int)

    # Set up independent variables
    X = df[xcols]

    # Competitors - count instead or 1-0
    if 'competingProducts' in X.columns:
        X.loc[X.competingProducts.isnull(),"competingProducts"] = 0
        X.loc[X.competingProducts != 0,'competingProducts'] = X.loc[X.competingProducts != 0,('competingProducts')].str.split(pat=";").str.len()

    # Convert categoricals to one-hot encoding
    X = pd.get_dummies(X)

    # save colnames
    xcolnames = X.columns

    # Build Feature Matrix
    X = X.values.astype(np.float)

    # Standardize
    if standardize:
        X_mean = X.mean(axis=0)
        X_std = X.std(axis=0)
        X = (X - X_mean)/X_std

    # Return X, y, and X_metrics (for potential use later)
    return X, y, xcolnames

def plotROCCurve(clf_class, X, y, axis, color, random_state, **kwargs):
    """Takes in a calssification model and data set and returns a plotted ROC Curve
    
    Arguments:
        clf_class -- classifiction model
        X {numpy array} -- feature matrix to predict response variable, y
        y {numpy array} -- response variable
        axis {var} -- ax variable to plot the figure on
        random_state --- For reproducibility
    """

    # KFold
    kf = StratifiedKFold(n_splits=3,shuffle=True,random_state=random_state)

    # Data Range
    mean_fpr = np.linspace(0, 1, 100)

    # initialization params
    tprs = []

    for train_index,test_index in kf.split(X,y):
        xtr,xvl = X[train_index],X[test_index]
        ytr,yvl = y[train_index],y[test_index]

        # fit models
        clf = clf_class(**kwargs)
        clf.fit(xtr,ytr)

        #get prediction data
        pred_test = clf.predict_proba(xvl)[:,1]

        # ROC Curve Plotting
        fpr, tpr, thresh = roc_curve(yvl, pred_test)
        interp_tpr = interp(mean_fpr, fpr, tpr)
        interp_tpr[0] = 0.0
        tprs.append(interp_tpr)

    # Return mean true positive rate & AUC
    mean_tpr = np.mean(tprs, axis=0)
    mean_auc = auc(mean_fpr, mean_tpr)

    # Plot object
    axis.plot(mean_fpr, mean_tpr, color=color,
    label=r'%s ROC (AUC = %0.2f)' % (clf_class.__name__, mean_auc),lw=2, alpha=.8)