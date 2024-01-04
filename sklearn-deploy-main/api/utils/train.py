import sys
import pickle

import numpy as np
import pandas as pd
from sklearn.neighbors import KNeighborsClassifier
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.model_selection import train_test_split

from utils import remove_outliers_iqr

datafile = sys.argv[1]
df = pd.read_csv(datafile)

df = df[["Credit_Utilization_Ratio", 'Credit_History_Age', 'Amount_invested_monthly', 'Monthly_Balance',\
        'Annual_Income', 'Monthly_Inhand_Salary','Changed_Credit_Limit', 'Outstanding_Debt', \
        'Total_EMI_per_month', 'Credit_Score']] 
df = df.replace([np.inf, -np.inf], np.nan)

columns_to_remove_outliers = ['Credit_History_Age', 'Monthly_Balance', 'Outstanding_Debt', 'Total_EMI_per_month']


for col in columns_to_remove_outliers:
    df = remove_outliers_iqr(df, col)

le = LabelEncoder()
col_list = df.select_dtypes(include="object").columns

for col in col_list:
    df["Credit_Score"] = le.fit_transform(df["Credit_Score"].astype(str))

y = df["Credit_Score"]
final_features = ['Credit_History_Age', 'Monthly_Balance', 'Annual_Income', 'Changed_Credit_Limit', 'Outstanding_Debt']
X = df[final_features]

scaler = StandardScaler()
X = scaler.fit_transform(X)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20, random_state=42)

neigh = KNeighborsClassifier(n_neighbors=3)
neigh.fit(X_train, y_train)

with open('model_artifacts/label_encoder', 'wb') as f:
    pickle.dump(le, f, protocol=pickle.HIGHEST_PROTOCOL)

with open('model_artifacts/scaler', 'wb') as f:
    pickle.dump(scaler, f,  protocol=pickle.HIGHEST_PROTOCOL)

with open('model_artifacts/model', 'wb') as f:
    pickle.dump(neigh, f,  protocol=pickle.HIGHEST_PROTOCOL)