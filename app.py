# import library
import numpy as np
import pandas as pd 
from fastapi import FastAPI 
import uvicorn
import pickle


# Load the model bundle

with open("xgboost_bundle.pkl", "rb") as file:
    model_bundle = pickle.load(file)

# Retrieve feature names
feature_names = model_bundle["feature_names"]

model = model_bundle ["model"]


# Create the FastAPI application
app = FastAPI(
    title="Retail Demand Forecasting API",
    description="API for predicting retail product demand",
    version="1.0.0"
)

# import Variable 

from variable import Variable


# Create the homepage route
@app.get("/")
def index():
    return {"message": "Hello Stranger"}

# Create Prediction 
@app.post('/predict')
def predict_sales(data:Variable):

    # Create year, month and day columns 
    year = data.date.year
    month = data.date.month
    day_of_week = data.date.weekday

    # Equate each column
    store_nbr = data.store_nbr
    family  = data.family
    onpromotion = data.onpromotion

    # Create dictionary containing all model features 
    input_data = {feature : 0 for feature in feature_names}

    # # Assign numerical values
    input_data['year'] = year
    input_data['month'] = month
    input_data['day_of_week'] = day_of_week()
    input_data["store_nbr"] = store_nbr
    input_data["onpromotion"] = onpromotion
    
    # Activate selected family
    family_column = f"family_{family}"
    input_data[family_column] = 1

    # Convert input data to dataframe 

    input_df = pd.DataFrame([input_data], columns = feature_names)

    # Generate prediction
    prediction = model.predict(input_df)

    # Convert prediction back to original sales scale
    prediction = np.expm1(prediction[0])

    # Return Prediction 
    return{"store_nbr" : store_nbr,
           "date" : data.date,
           "family" : family,
           "Predicted_sales" : round(float(prediction), 2)}
# Run the application
if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
