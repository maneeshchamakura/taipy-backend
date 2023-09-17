import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder
from sklearn.metrics import mean_squared_error
import numpy as np  # Import numpy for RMSE calculation
from prophet import Prophet


def build_message(name: str):
    return f"Hello {name}!"

def clean_data(initial_dataset: pd.DataFrame):
    return initial_dataset

def retrained_model(cleaned_dataset: pd.DataFrame):
    # Split the dataset into features (X) and target (y)
    X = cleaned_dataset.drop('Claim_Amount', axis=1)
    y = cleaned_dataset['Claim_Amount']

    # Split the data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Define the categorical columns for one-hot encoding
    categorical_cols = ['Procedure_Code', 'Diagnosis_Code', 'Provider_Specialty', 'Insurance_Plan']

    # Create a column transformer
    preprocessor = ColumnTransformer(
        transformers=[
            ('cat', OneHotEncoder(drop='first'), categorical_cols)
        ],
        remainder='passthrough'
    )

    # Create a pipeline with preprocessing and the Random Forest Regressor
    model = Pipeline([
        ('preprocessor', preprocessor),
        ('regressor', RandomForestRegressor(n_estimators=100, random_state=42))
    ])

    # Fit the model on the training data
    model.fit(X_train, y_train)

    # Make predictions on the test set
    predictions = model.predict(X_test)

    # Calculate Mean Squared Error (MSE)
    mse = mean_squared_error(y_test, predictions)

    # Calculate Root Mean Squared Error (RMSE)
    rmse = np.sqrt(mse)

    # Print the RMSE
    print(f"Mean Squared Error: {mse}")
    print(f"Root Mean Squared Error (RMSE): {rmse}")
    
    return model

def predict(model):
    # Example: Make a prediction for a new patient
    new_patient_data = pd.DataFrame({
        'Procedure_Code': ['CPT456'],
        'Diagnosis_Code': ['ICD-10-B'],
        'Provider_Specialty': ['Orthopedics'],
        'Patient_Age': [35],
        'Insurance_Plan': ['PPO'],
        'Deductible': [200],
        'Copayment': [30],
        'Coinsurance': [20],
    }, index=[0])

    # Predict the claim amount for the new patient
    new_patient_claim = model.predict(new_patient_data)
    print(f"Predicted Claim Amount for New Patient: ${new_patient_claim[0]:.2f}")