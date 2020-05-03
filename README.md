# Modeling Customer Churn
Code created by Will Daniel, Winfred Hills, and Mo Lu

## File Overview

### dataprep

This folder contains the code needed to preprocess and prep the data for model creation. 

1. dataPrep.py: This file filters down the data set, performs data imputation, and data transformation.
        - Uses columnnames_dict.json to filter the data set and rename the columns
2. modelPrep.py: This file takes the dataframe prepped by dataPrep.py and creates a feature matrix, and response vector. It will also create specificed interaction terms, higher level terms, and will standardize the features as necessary. This file also creates ROC curves post-model creation.

### LogisticRegressionModel.ipynb

This jupyter notebook has the code that was used to create our final logistic regression model. It has code for feature selection, feature importance, and produces a ROC Curve for the model. 

### finalmodel.py

This is a convenient python file that can be called to produce the final logistic regression model used in the below two notebooks.

### ComparingModels.ipynb

This jupyter notebook looks at the specific Logistic Model against the baseline models: random forest and XGBoost

### feature_visualization.ipynb

This jupyter notebook explore feature visualization for the final logistic regression model pulled from finalmodel.py

### timeseries

In our data analysis we also explore time series models, specifically cox proportional hazards model. This file has the work done for that analysis. Specifically, "Surv Analysis.ipynb" is a jupyter notebook that has our final cox proportional hazards model.
