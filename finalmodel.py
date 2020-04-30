import numpy as np
import pandas as pd
from sklearn import linear_model

# Custom Python Files
from dataprep.dataPrep import cleanData
from dataprep.modelPrep import model_prep

def finalmodel():
    """ This will produce the final logistic regression model, using data from PSCCustomerData.xlsx

        The logistic regression model predicts churn and has the following univariate features:
            callsPerQuarter, associateddeals, sessionsPerDay, callcycle_numeric
        and the following interaction terms: 
            'callsPerQuarter * associateddeals', 'assoccontacts * associateddeals', 'assoccontacts * MRR'
    Returns:
        df - Cleaned and prepped dataframe for model building 
        X - feature matrix
        y - response variable
        lr - Logistic regression model trained on X & y
        predictions - prediction response from model 
        xcolnames - list of column names for reference
    """
    seed = 1234 # random state for consistency
    xcols = ['callsPerQuarter','associateddeals','sessionsPerDay','callcycle_numeric']

    # List of interaction terms (each their own sublist)
    interactionList = [ ['callsPerQuarter', 'associateddeals'],
                        ['assoccontacts', 'associateddeals'],
                        ['assoccontacts', 'MRR'],
    ]

    termDict = {
        "callcycle_numeric" : 2 # Higher level terms desired
    }

    ycol = "churn"

    df = cleanData("PSCCustomerData.csv", boxcox=True)

    X, y, xcolnames = model_prep(df,xcols,ycol, higherTerms=True, termDict=termDict, interactionTerms=True, interactionList = interactionList, standardize=False)

    # Model building and KFold
    lr = linear_model.LogisticRegression(class_weight='balanced',penalty='none', max_iter=10000, random_state=seed)

    # fit model
    lr.fit(X,y)

    # Produce predictions
    predictions = lr.predict_proba(X)[:,1]

    # return model and feature list
    return df, lr, predictions, xcolnames, X, y