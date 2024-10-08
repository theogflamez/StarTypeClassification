# -*- coding: utf-8 -*-
"""StarClassificationML.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1PpVHIE5xrjhQWda8fRrcD2PIvE61Zp3w
"""

#import all necessary libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix, mean_squared_error, r2_score
import joblib

#display parts of the CSV file such as first few rows and information on columns and data types
df = pd.read_csv('StarClasses.csv')
df.head()
df.info()


X = df.drop('Star type', axis = 1) #declares x axis to have all the input variables except "Star Type"
y = df['Star type'] # Declares y axis as Target variable "Star Type" that will need to be predicted

#separeate features into categorical and numerical data
categorical_features = ['Star color', 'Spectral Class']
numeric_features = ['Temperature (K)', 'Luminosity(L/Lo)', 'Radius(R/Ro)', 'Absolute magnitude(Mv)']

preprocessor = ColumnTransformer(
    transformers = [
        ('num', StandardScaler(), numeric_features), #Normalizing numeric data to standardize them
        ('cat', OneHotEncoder(), categorical_features) #Makes categorical data binary units to make it easier
    ])

X_processed = preprocessor.fit_transform(X) #placed into preprocessor to refurbish data set

X_train, X_test, y_train, y_test = train_test_split(X_processed, y, test_size=0.3, random_state=42) #Split the data to 70% training, and 30% testing

#Random forest classifier is a machine learning algorithm to classify data into categories using randomization within the dataset and binding multiple trees together
#The data is split with trees and 100 trees are created, trees are data splits that help train the idea with randomizing and expanding the possibilities
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train) #model is fitted to the training data

#Now the trained model will make predictions on the training set and the test set
y_train_pred = model.predict(X_train)
y_test_pred = model.predict(X_test)

#Creates the scatter plot to compare the true vs predicted star types for both training and test sets, red line shows perfection
plt.figure(figsize=(12, 6))
plt.subplot(1, 2, 1)
plt.scatter(y_train, y_train_pred, color="blue")
plt.plot([min(y_train), max(y_train)], [min(y_train), max(y_train)], color="red", linewidth=2) # Perfect prediction line
plt.title('Training Set: True vs Predicted')
plt.xlabel('True Star Type')
plt.ylabel('Predicted Star Type')
plt.subplot(1, 2, 2)
plt.scatter(y_test, y_test_pred, color="green")
plt.plot([min(y_test), max(y_test)], [min(y_test), max(y_test)], color="red", linewidth=2) # Perfect prediction line
plt.title('Test Set: True vs Predicted')
plt.xlabel('True Star Type')
plt.ylabel('Predicted Star Type')
plt.tight_layout()
plt.show()


#Calculate r^2 performance
train_r2 = r2_score(y_train, y_train_pred)
test_r2 = r2_score(y_test, y_test_pred)
print(f"R^2 Score for Training Set: {train_r2}")
print(f"R^2 Score for Testing Set: {test_r2}")

#Creates confusion matrix to see true vs. false predictions on the model
y_pred = model.predict(X_test)
print(confusion_matrix(y_test, y_pred))
print(classification_report(y_test, y_pred))

#plotted the confusion matrix using Seaborn’s heatmap for a better visual understanding of the model’s performance.
plt.figure(figsize=(10, 7))
sns.heatmap(confusion_matrix(y_test, y_pred), annot=True, fmt='d', cmap='Blues')
plt.xlabel('Predicted')
plt.ylabel('True')
plt.show()

def predict_star_type(temperature, luminosity, radius, absolute_magnitude, star_color, spectral_class):

    input_data = pd.DataFrame({
        'Temperature (K)': [temperature],
        'Luminosity(L/Lo)': [luminosity],
        'Radius(R/Ro)': [radius],
        'Absolute magnitude(Mv)': [absolute_magnitude],
        'Star color': [star_color],
        'Spectral Class': [spectral_class]
    })


    input_processed = preprocessor.transform(input_data)  #takes input data and adds it to the data set


    prediction = model.predict(input_processed)  #uses the input data to predict


    star_types = {
        0: "Brown Dwarf",
        1: "Red Dwarf",
        2: "White Dwarf",
        3: "Main Sequence",
        4: "Supergiant",
        5: "Hypergiant"
    }
    return star_types[prediction[0]]


def interactive_predictor():
    print("Please input the following features to predict the star type:")


    temperature = float(input("Temperature (K): "))
    luminosity = float(input("Luminosity(L/Lo): "))
    radius = float(input("Radius(R/Ro): "))
    absolute_magnitude = float(input("Absolute magnitude(Mv): "))
    star_color = input("Star color: ")
    spectral_class = input("Spectral class: ")


    star_type = predict_star_type(temperature, luminosity, radius, absolute_magnitude, star_color, spectral_class) #calls back function


    print(f"The predicted star type is: {star_type}")


interactive_predictor()

