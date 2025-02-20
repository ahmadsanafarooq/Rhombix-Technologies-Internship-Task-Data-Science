# -*- coding: utf-8 -*-
"""TITANIC CLASSIFICATION.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1G6xgm3F706nXwHb-xIeDeUeBc_xYe5iO
"""

# Import necessary libraries
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report
from warnings import filterwarnings
filterwarnings("ignore")

#Load the Titanic dataset
url = "https://raw.githubusercontent.com/datasciencedojo/datasets/master/titanic.csv"
df = pd.read_csv(url)

# Display the first few rows of the dataset
df.head()

#Drop unnecessary columns
df.drop(["PassengerId", "Name", "Ticket", "Cabin"], axis=1, inplace=True)

df.isnull().sum()

#  Handle missing values
# Fill missing Age values with the median age
imputer = SimpleImputer(strategy="median")
df["Age"] = imputer.fit_transform(df[["Age"]])

# Fill missing Embarked values with the most common port
df["Embarked"].fillna(df["Embarked"].mode()[0], inplace=True)

#Encode categorical variables
label_encoder = LabelEncoder()
df["Sex"] = label_encoder.fit_transform(df["Sex"])  # Male = 1, Female = 0
df["Embarked"] = label_encoder.fit_transform(df["Embarked"])  # C, Q, S → Numeric

#Define features (X) and target variable (y)
X = df.drop("Survived", axis=1)
y = df["Survived"]

#Split the dataset into training and testing sets (80% train, 20% test)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Normalize numerical features
scaler = StandardScaler()
X_train[["Age", "Fare"]] = scaler.fit_transform(X_train[["Age", "Fare"]])
X_test[["Age", "Fare"]] = scaler.transform(X_test[["Age", "Fare"]])

# the Logistic Regression model
model = LogisticRegression(max_iter=200)
model.fit(X_train, y_train)

#Make predictions on the test set
y_pred = model.predict(X_test)

#Evaluate the model
accuracy = accuracy_score(y_test, y_pred)
print(f"Model Accuracy: {accuracy * 100:.2f}%")
print(classification_report(y_test, y_pred))

#Function to predict survival for a new passenger
def predict_survival(pclass, sex, age, sibsp, parch, fare, embarked):
    # Encode categorical values
    sex = 1 if sex.lower() == "male" else 0
    embarked = {"C": 0, "Q": 1, "S": 2}.get(embarked.upper(), 2)  # Default to 'S'

    # Scale numerical values
    age = scaler.transform([[age, fare]])[0][0]
    fare = scaler.transform([[age, fare]])[0][1]

    # Prepare input data
    input_data = np.array([[pclass, sex, age, sibsp, parch, fare, embarked]])

    # Make a prediction
    prediction = model.predict(input_data)

    return "Survived" if prediction[0] == 1 else "Did Not Survive"

# Example Prediction
example = predict_survival(3, "male", 22, 1, 0, 7.25, "S")
example

