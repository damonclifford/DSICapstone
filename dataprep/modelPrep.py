import numpy as np
import pandas as pd
from sklearn.model_selection import StratifiedKFold
from sklearn.metrics import auc
from sklearn.metrics import roc_curve
from sklearn.preprocessing import PolynomialFeatures
from scipy import interp
from imblearn.over_sampling import SMOTE

def model_prep(df, xcols, ycol, standardize=True, higherTerms=False, termDict={}, interactionTerms=True, interactionList=[]):
    """ Prepares a feature matrix and response var from a dataset 
    
    Arguments:
        df {dataframe} -- dataframe to pass in for modeling
        xcols {any} -- columns to use as independent var, or ALL if you don't want filtering
        ycol {any} -- columns to use as response
        standardize -- True by default. Whether you would like to standardize the dataset
    
    Returns:
        X (feature matrix), y (response variable), xcolnames
    """
    # Set up response variable 
    y = df[ycol].values.astype(np.int)

    # Add in higher level terms if specified
    if higherTerms:
        for i in termDict:
            for j in range(termDict[i]-1):
                name = i + "_" + str(j+2) # Create name for dataset

                df[name] = df[i]**(j+2) # Transform the original variable to desired higher term

                xcols.append(name) # add the newly created column to filter list

    # Add in interaction level terms if specified
    if interactionTerms:
        for i in interactionList:
            name = i[0] + ' ' + i[1] # create the column name

            df[name] = df[i[0]]*df[i[1]] # create the interaction column

            xcols.append(name) # add the newly created column to filter list

    # Filter independent variables if needed
    if xcols != "ALL":
        X = df[xcols].copy()
    else:
        X = df.drop(ycol, axis=1, inplace=False)

    # Convert categoricals to one-hot encoding
    X = pd.get_dummies(X)

    # drop callcycle is being used for dummy encoding
    if 'callcycle_Yearly' in X.columns:
        X.drop("callcycle_Yearly", axis=1, inplace=True)

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

def plotROCCurve_smote(clf_class, X, y, axis, color, random_state, **kwargs):
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

        # Use SMOTE to boost training set
        sm = SMOTE(random_state = 33)
        X_train_new, y_train_new = sm.fit_sample(xtr, ytr.ravel())

        # fit models
        clf = clf_class(**kwargs)
        clf.fit(X_train_new,y_train_new)

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
    label=r'%s ROC (AUC = %0.2f) SMOTE' % (clf_class.__name__, mean_auc),lw=2, alpha=.8)