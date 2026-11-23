# Store Sales Forecasting & Retail Intelligence System

**An End-to-End Machine Learning Solution for Retail Sales Prediction, Demand Analysis, and Inventory Intelligence.**

[![Python](https://img.shields.io/badge/Python-3.12-blue?logo=python)](https://www.python.org/)
[![XGBoost](https://img.shields.io/badge/Model-XGBoost-orange)](https://xgboost.readthedocs.io/)
[![FastAPI](https://img.shields.io/badge/API-FastAPI-009688?logo=fastapi)](https://fastapi.tiangolo.com/)
[![Streamlit](https://img.shields.io/badge/Dashboard-Streamlit-FF4B4B?logo=streamlit)](https://streamlit.io/)
[![Plotly](https://img.shields.io/badge/Visualization-Plotly-3F4F75?logo=plotly)](https://plotly.com/)

**Live Applications:** [Interactive Dashboard](https://store-sales-forecastingg.streamlit.app/) | [Prediction API](https://store-sales-forecasting-api.onrender.com) | [API Documentation](https://store-sales-forecasting-api.onrender.com/docs)

---

## Project Overview

Retail businesses need reliable sales forecasts to make informed decisions about inventory management, product distribution, promotional strategies, and operational planning.

However, historical sales data often contains complex patterns influenced by product categories, store locations, seasonal variations, calendar events, and promotional activities.

This project develops an end-to-end Machine Learning solution that predicts retail sales using historical transaction data and provides an interactive business intelligence dashboard for exploring sales patterns and supporting demand-related decisions.

The solution combines **XGBoost, FastAPI, and Streamlit** to demonstrate how a machine learning model can move beyond experimentation into an accessible, deployable application.

## Business Objectives

The project addresses the following business questions:

- How can retail businesses estimate future sales across different stores and product families?
- Which product families generate the highest sales?
- How does demand vary across stores and time periods?
- What relationship exists between promotional activities and sales?
- How can historical demand patterns support inventory planning?
- How can model predictions be made accessible to business users?

## Dataset

The project uses the Corporación Favorita Grocery Sales Forecasting dataset.

**Dataset characteristics:**

| Description | Value |
|---|---:|
| Training records | 3,000,888 |
| Number of stores | 54 |
| Product families | 33 |
| Total sales volume (dataset KPI) | 1,073,644,952 |

**Key features used in the prediction system:**

| Feature | Description |
|---|---|
| Date | Date of the requested prediction |
| Store number | Identifies the retail store |
| Product family | Product category |
| On promotion | Number of products on promotion |

The dataset provides historical sales information that supports the exploration of retail demand patterns and the development of predictive models.

## Machine Learning Approach

### Model Development

The project uses **XGBoost Regressor** to predict retail sales.

During experimentation, Random Forest was initially explored. However, its large model size and computational demands motivated a transition to XGBoost, which provided a more manageable model for deployment.

The target variable was log-transformed during model development.

### Model Evaluation

The selected XGBoost model achieved the following evaluation results:

| Evaluation metric | Result |
|---|---:|
| RMSE | 0.7158 |
| R² Score | 0.9294 |
| Model size | Approximately 0.48 MB |

The model achieved an R² score of approximately 92.94% on the evaluation split.

**Note:** The RMSE is reported on the log-transformed target scale, not directly in original sales units.

Further chronological validation is important for assessing how well the model generalizes to genuinely future sales periods.

## System Architecture

The application follows an end-to-end architecture connecting model development, API deployment, and interactive visualization.

```text
          Historical Sales Data
                   |
                   v
       Data Cleaning & Preparation
                   |
                   v
        Feature Engineering
                   |
                   v
          XGBoost Regressor
                   |
                   v
           Saved Model
                   |
                   v
             FastAPI
           (Render Hosting)
                   |
                   v
         Prediction Endpoint
                   |
                   v
        Streamlit Dashboard
        (Streamlit Hosting)
                   |
                   v
       Interactive Predictions
       Sales & Demand Analysis
       Inventory Intelligence
       Promotion Analysis
       Model Performance
```

## Application Features

### 1. Overview

Provides a high-level summary of retail performance through key performance indicators and interactive visualizations.

### 2. Sales Analysis

Explores historical sales patterns across stores, product families, and different time periods.

### 3. Demand Forecasting

Allows users to generate sales predictions by providing:

- Prediction date
- Store number
- Product family
- Number of products on promotion

### 4. Inventory Intelligence

Explores demand patterns and product-level sales variability to support inventory planning and stock management decisions.

### 5. Promotion Analysis

Investigates promotional activities and their relationship with retail sales performance.

### 6. Model Performance

Presents model evaluation results to help users understand the predictive performance of the machine learning solution.

## Technology Stack

| Technology | Application |
|---|---|
| Python | Core programming language |
| Pandas | Data manipulation and analysis |
| NumPy | Numerical computation |
| Scikit-learn | Machine learning utilities and evaluation |
| XGBoost | Sales prediction model |
| FastAPI | REST API development |
| Streamlit | Interactive dashboard |
| Plotly | Interactive data visualization |
| Uvicorn | API server |
| Render | Backend deployment |
| Streamlit Community Cloud | Dashboard deployment |
| Git & GitHub | Version control and project management |

## Live Deployment

The project has been deployed as two connected applications.

**1. Interactive Dashboard**

Explore historical sales, analyze demand patterns, examine promotional activities, and generate predictions.

[Launch Store Sales Forecasting Dashboard](https://store-sales-forecastingg.streamlit.app/)

**2. Prediction API**

The FastAPI backend exposes a prediction endpoint that receives user inputs and returns predicted sales.

[Access API](https://store-sales-forecasting-api.onrender.com/docs)

[Explore Interactive API Documentation](https://store-sales-forecasting-api.onrender.com/docs)

## API Usage

The prediction API exposes a `POST /predict` endpoint.

**Example request:**

```json
{
    "date": "2026-11-07",
    "store_nbr": 1,
    "family": "BEVERAGES",
    "onpromotion": 5
}
```

**Example response:**

```json
{
    "predicted_sales": 1753.54
}
```

The response represents the model's predicted sales volume for the specified store, product family, date, and promotional input.

## Running the Project Locally

### 1. Clone the repository

```bash
git clone https://github.com/Sodiq-Raifu/Store-Sales-Forecasting.git

cd Store-Sales-Forecasting
```

### 2. Create a virtual environment

```bash
python -m venv .venv
```

Activate the environment:

**Windows:**

```bash
.venv\Scripts\activate
```

**Linux/macOS:**

```bash
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the FastAPI application

```bash
uvicorn main:app --reload
```

If your API entry-point module has a different name, replace `main:app` with the appropriate module and application variable.

Access the interactive API documentation:

```text
http://127.0.0.1:8000/docs
```

### 5. Run the Streamlit dashboard

```bash
streamlit run frontend/dashboard.py
```

The dashboard will be accessible through the local Streamlit URL displayed in your terminal.

Ensure the model artifacts and required dataset files are available in their expected project locations before running the applications.

## Key Project Achievements

- Developed an end-to-end retail sales prediction solution using XGBoost.
- Experimented with multiple machine learning approaches before selecting a deployment-friendly model.
- Built a REST API using FastAPI to serve machine learning predictions.
- Deployed the prediction API using Render.
- Developed an interactive business intelligence dashboard using Streamlit and Plotly.
- Integrated the prediction service into an accessible application.
- Explored retail demand variability, promotional activities, and inventory-related patterns.


## Author

**Sodiq Raifu Adepoju**

Statistics Student | Machine Learning Engineer | AI Enthusiast

I am interested in building practical machine learning systems that transform data into actionable insights and solve real-world problems.

- **GitHub:** [Sodiq-Raifu](https://github.com/Sodiq-Raifu)
- **Portfolio:** [Personal Portfolio](https://sodiq-raifu.github.io/sodiqraifu.github.io/)

---

*This project demonstrates the development of a complete machine learning application, from data preparation and predictive modelling to API development, deployment, and interactive business intelligence.*
