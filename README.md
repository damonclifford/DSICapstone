# Modeling Customer Churn
Paper Abstract: With the widespread adoption of customer relationship management (CRM) systems such as Salesforce, HubSpot and Oracle, businesses are becoming increasingly aware of their customer churn rates. Churn rates describe how many customers stop using a product or service within a certain time period and provide a sense of the businesses' long-term viability. Business-to-Business (B2B) firms place high value on the ability to predict individual customer churn, as it presents an opportunity to retain key clients in an inherently limited customer portfolio. These predictions must be both actionable and timely if a manager hopes to retain their client, since a client's churn decision occurs months before the observed churn event. This study explores the HubSpot data of a B2B organization. The objective is to determine the client characteristics that predict sustained product usage and to analyze the indicators of potential churn. Our approach was to model the predictive features of client churn, which would allow managers to directly map churn probability to business strategies. Our final models flagged a handful of management-adjustable features that were significant for predicting customer churn and survival times.

## File Overview

### dataprep

This folder contains the code needed to preprocess and prep the data for model creation. 

1. dataPrep.py: This file filters down the data set, performs data imputation, and data transformation.
        - Uses columnnames_dict.json to filter the data set and rename the columns
2. modelPrep.py: This file takes the dataframe prepped by dataPrep.py and creates a feature matrix, and response vector. It will also create specificed interaction terms, higher level terms, and will standardize the features as necessary. This file also creates ROC curves post-model creation.

### LogReg.ipynb

This jupyter notebook has the code that was used to create our final logistic regression model. It has code for feature selection, feature importance, and produces a ROC Curve for the model. 

### finalmodel.py

This is a convenient python file that can be called to produce the final logistic regression model used in the below two notebooks.

### OverallModeling.ipynb

This jupyter notebook looks at the specific Logistic Model against the baseline models: random forest and XGBoost

### GAM.ipynb

This jupyter notebook experiments with using a GAM (Generalized Additive Model). Note - this was only preliminary work and was not included in final analysis.

### feature_visualization.ipynb

This jupyter notebook explore feature visualization for the final logistic regression model pulled from finalmodel.py

### timeseries

In our data analysis we also explore time series models, specifically cox proportional hazards model. This file has the work done for that analysis. Specifically, "Surv Analysis.ipynb" is a jupyter notebook that has our final cox proportional hazards model.
