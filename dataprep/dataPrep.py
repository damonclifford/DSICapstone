import numpy as np
import pandas as pd
import sklearn
import json
import os

# Use the directory where this file is located
abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)

# Opening columnname dictionary
with open('columnnames_dict.json', 'r') as fp:
    columnlist_dict = json.load(fp)

def cleanData(filepath):
    # Load in raw dataset
    df = pd.read_csv(filepath)

    # 1. Grab columns to use and rename as necessary
    df = filterAndRename(df)

    # 2. Deal with missing values using the missingData_imputation method
    df = missingData_imputation(df)

    # 3. Transform variables using the variable_transformation method
    df = variable_transformation(df)

    return df

def filterAndRename(df, columnlist_dict=columnlist_dict):
    # Subset down the initial dataset
    df = df[columnlist_dict.keys()]

    # Rename the columns using the names specified in dictionary
    df = df.rename(columnlist_dict, axis=1)

    return df

def missingData_imputation(df):
    # Missing Value Imputation

    # Assume values of zero
    zerolist = ['pageviews', 'admins','contractdays','timescontacted', 'sessions','assoccontacts','MRR']
    df[zerolist] = df[zerolist].replace(np.NaN, 0.0)

    # Assume values of No
    nolist = ['FF','associatedpredictionlead','strategic']
    df[nolist] = df[nolist].replace(np.NaN, "No")

    # Assume values of False
    df[["publiclytraded"]] = df[["publiclytraded"]].replace(np.NaN, False)

    # Call Cycle Imputation
    df.loc[:,"callcycle"] = df.loc[:,"callcycle"].replace(np.NaN, "Yearly")

    # Gauge Imputation
    df[["gauge"]] = df[["gauge"]].replace(np.NaN, "Green")

    # Industry and OrigSource
    nonelist = ['industry', 'origsource']
    df[nonelist] = df[nonelist].replace(np.NaN, "Unknown")

    # Take average values for missing employees & revenue
    emp_avg = round(df.query("employees.notnull()", engine="python")["employees"].mean(),0)
    df["employees"] = df["employees"].replace(np.NaN, emp_avg)

    mrr_avg = round(df.query("MRR.notnull()", engine="python")["MRR"].mean(),0)
    df["MRR"] = df["MRR"].replace(np.NaN, mrr_avg)

    # Make associated deals equal to zero
    df[["associateddeals"]] = df[["associateddeals"]].replace(np.NaN, 0)

    return df

def variable_transformation(df):
    # Create a "callcycle_numeric" columns that breaks out the call cycle from categorical to numeric
    cc = {'Monthly':'12', 'Quarterly':'4', 'Yearly':'1','Half Year':'2', 'Every Other Month':'6', 'None':'0'}
    df["callcycle_numeric"] = df['callcycle'].replace(cc,inplace=False)
    df["callcycle_numeric"]= pd.to_numeric(df["callcycle_numeric"])

    # Create a competingProducts column that counts the number of competitors (instead of a binary)
    df["competingProducts"] = df["usecompetitors"].copy()
    df.loc[df.competingProducts.isnull(),"competingProducts"] = 0
    df.loc[df.competingProducts != 0,'competingProducts'] = df.loc[df.competingProducts != 0,('competingProducts')].str.split(pat=";").str.len()

    # Create churn column from contracttype, then drop
    df["churn"] = df["contracttype"].apply(lambda x: 1 if x=="CANCELLED" else 0)
    df.drop(['contracttype'], axis=1, inplace=True)

    # Change usecompetitors from text to binary
    df.loc[df.usecompetitors.isnull(),"usecompetitors"] = 0
    df.loc[df.usecompetitors != 0,"usecompetitors"] = 1

    # Change columns that have Yes/No, to binary
    nolist = ['FF','associatedpredictionlead','strategic']
    df[nolist] = df[nolist].replace("No", 0).replace("Yes", 1)

    # Change columns that have TRUE/FALSE to binary
    df[["publiclytraded"]] = df[["publiclytraded"]].replace(False, 0).replace(True, 1)

    # Fill in firstdealDT & Create daysAsCustomer column
    df["firstdealDT"] = pd.to_datetime(df["firstdealDT"].replace(np.NaN, df["createDT"]))
    df["daysAsCustomer"] = ((pd.datetime.today() - df["firstdealDT"]).dt.days).astype(int)
    df.drop(["createDT"], axis=1, inplace=True)

    return df