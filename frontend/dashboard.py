
# ============================================================
# 1. IMPORT LIBRARIES
# ============================================================
import seaborn as sns
import matplotlib.ticker as ticker
import streamlit as st
import pandas as pd
import datetime
import matplotlib.pyplot as plt
import plotly.express as px
import requests


# ============================================================
# 2. PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Store Sales Forecasting",
    page_icon="📊",
    layout="wide"
)

# ============================================================
# 3. LOAD DATASET
# ============================================================

@st.cache_data
def load_data():

    data = pd.read_csv("frontend/train.csv.gz")

    data["date"] = pd.to_datetime(data["date"])

    return data


data = load_data()
data["year"] = data["date"].dt.year
data["month"] = data["date"].dt.month


# ============================================================
# 4. SIDEBAR NAVIGATION
# ============================================================

st.sidebar.title("Navigation")

section = st.sidebar.radio(
    "Select a section",
    [
        "Overview",
        "Sales Analysis",
        "Demand Forecasting",
        "Inventory Intelligence",
        "Promotion Analysis",
        "Model Performance"
    ]
)


# ============================================================
# 5. DASHBOARD HEADER
# ============================================================

st.title("Store Sales Forecasting")

st.caption(
    "Retail Demand Forecasting and Analytics Platform"
)



# ============================================================
# 6. OVERVIEW SECTION
# ============================================================

if section == "Overview":

    # --------------------------------------------------------
    # 6.1 CALCULATE KEY BUSINESS METRICS
    # --------------------------------------------------------

    total_sales = data["sales"].sum()

    total_stores = data["store_nbr"].nunique()

    total_families = data["family"].nunique()

    total_records = len(data)

    total_promotions = data["onpromotion"].sum()

    # --------------------------------------------------------
    # 6.2 DISPLAY KPI CARDS
    # --------------------------------------------------------

    st.subheader("Business Overview")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            label="Total Sales Volume",
            value=f"{total_sales:,.0f}"
        )

    with col2:
        st.metric(
            label="Total Stores",
            value=f"{total_stores:,}"
        )

    with col3:
        st.metric(
            label="Product Families",
            value=f"{total_families:,}"
        )

    with col4:
        st.metric(
            label="Total Records",
            value=f"{total_records:,}"
        )


    st.divider()

    # --------------------------------------------------------
    # 6.3 DAILY SALES TREND
    # --------------------------------------------------------

    daily_sales = (
        data.groupby("date")["sales"]
        .sum()
        .reset_index()
    )

    fig = px.line(
        daily_sales,
        x="date",
        y="sales",
        title="Daily Sales Trend",
        labels={
            "date": "Date",
            "sales": "Total Sales Volume"
        }
    )

    fig.update_layout(
        template="plotly_dark",
        hovermode="x unified",
        xaxis_title="Date",
        yaxis_title="Total Sales Volume"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    st.divider()

    # Montly Trend of sales
    # Calculate monthly sales by year
    yearly_sales = (
    data.groupby(["year", "month"])["sales"]
    .sum()
    .reset_index())

    # Create monthly sales trend chart
    fig = px.line(
    yearly_sales,
    x="month",
    y="sales",
    facet_col="year",
    facet_col_wrap=2,
    markers=True,
    title="Monthly Retail Sales Trend",
    labels={
        "month": "Month",
        "sales": "Total Sales Volume",
        "year": "Year"
    },
    color_discrete_sequence=["#2471A3"])

    # Format the chart
    fig.update_layout(
    template="plotly_white",
    height=700,
    hovermode="x unified",
    title_x=0.5)

    # Display month names instead of numbers
    fig.update_xaxes(
    tickmode="array",
    tickvals=list(range(1, 13)),
    ticktext=[
        "Jan", "Feb", "Mar", "Apr", "May", "Jun",
        "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"
    ])

    # Format sales values with commas
    fig.update_yaxes(tickformat=",")

    # Display chart in Streamlit
    st.plotly_chart(fig, use_container_width=True)

    # Sales plot
    st.divider()
    # Calculate total sales for each year

    col13,col14 = st.columns(2)
    with col13:
        yearly_sales = (
            data.groupby("year")["sales"]
            .sum()
            .reset_index())

    # Create pie chart
        fig = px.pie(
            yearly_sales,
            names="year",
            values="sales",
            title="Total Sales Distribution by Year",
            hole=0.4)

        fig.update_traces(
            textposition="inside",
            textinfo="percent+label",
            hovertemplate="Year: %{label}<br>Sales: %{value:,.0f}<br>Share: %{percent}<extra></extra>")

        fig.update_layout(
            template="plotly_dark",
            height=500)

        st.plotly_chart(fig, use_container_width=True)

    with col14:
        # Calculate total sales for each year
        yearly_sales = (
            data.groupby("year")["sales"]
            .sum()
            .reset_index())

# Create yearly sales trend
        fig = px.line(
            yearly_sales,
            x="year",
            y="sales",
            markers=True,
            title="Overall Yearly Sales Trend",
            labels={
                "year": "Year",
                "sales": "Total Sales Volume"
                })

        fig.update_traces(
            line=dict(color="#2471A3", width=3),
            marker=dict(size=10),
            hovertemplate="Year: %{x}<br>Total Sales: %{y:,.0f}<extra></extra>")

        fig.update_layout(
            template="plotly_dark",
            height=500,
            xaxis=dict(
                tickmode="linear",
                dtick=1),
                yaxis=dict(tickformat=",.0f"))

        st.plotly_chart(fig, use_container_width=True)

    # Add a line to separate chart

    st.divider()

    # --------------------------------------------------------
    # 6.4 TOP 10 PRODUCT FAMILIES
    # --------------------------------------------------------
    col11, col12 = st.columns(2)
    with col11:
        family_sales = (
            data.groupby("family")["sales"]
            .sum()
            .reset_index()
            .sort_values(by="sales", ascending=False))

        top_10_families = family_sales.head(10)

        fig = px.bar(
            top_10_families,
            x="family",       # Product Family moves to X-axis
            y="sales",        # Sales Volume moves to Y-axis
            title="Top 10 Product Families by Sales Volume",
            labels={
                "sales": "Total Sales Volume",
                "family": "Product Family"
                },
            color="sales",
            color_continuous_scale="Blues",
            text_auto=",.0f")

        fig.update_layout(
            template="plotly_dark",
            xaxis={"categoryorder": "total descending"},
            coloraxis_showscale=False,
            height=550,
            xaxis_title="Product Family",
            yaxis_title="Total Sales Volume",
            xaxis_tickangle=-45
            )

        st.plotly_chart(fig,use_container_width=True)

    # 10 best store 
    
    with col12:

        top_10_stores = (
            data.groupby("store_nbr")["sales"]
            .sum()
            .reset_index()
            .nlargest(10, "sales")
            .sort_values("sales", ascending=False))

        top_10_stores["store_nbr"] = top_10_stores["store_nbr"].astype(str)

        fig = px.bar(
            top_10_stores,
            x="store_nbr",
            y="sales",
            title="Top 10 Stores by Total Sales Volume",
            labels={
                "sales": "Total Sales Volume",
                "store_nbr": "Store Number"},
            color="sales",
            color_continuous_scale="Blues",
            text_auto=",.0f")

        fig.update_layout(
            template="plotly_dark",
            height=550,
            coloraxis_showscale=False,
            xaxis_title="Store Number",
            yaxis_title="Total Sales Volume")

        st.plotly_chart(fig, use_container_width=True)
        
# Sales Section 

elif section == "Sales Analysis":

    st.header("Sales Analysis")

    # Create two columns
    col5, col6 = st.columns(2)

    # With column 5:

    with col5:
        st.subheader("Sales Performance by Product Family")

        # Calculate total sales for each product family
        family_sales = (
            data.groupby("family")["sales"]
            .sum()
            .reset_index()
            .sort_values(by="sales", ascending=True)
            )
        # Create interactive Plotly chart
        fig = px.bar(
            family_sales,
            x="sales",
            y="family",
            orientation="h",
            title="Sales Volume by Product Family",
            labels={
                "sales": "Total Sales Volume",
                "family": "Product Family"
                },
                color="sales",
                color_continuous_scale="Blues"
                )
        # Customize chart
        fig.update_layout(
            template="plotly_dark",
            height=850,
            coloraxis_showscale=False,
            xaxis_title="Total Sales Volume",
            yaxis_title="Product Family",
            yaxis={"categoryorder": "total ascending"}
            )
         # Display chart
        
        st.plotly_chart(fig, use_container_width=True)



        # With column 6
    with col6 :
        # Sales Trend by Selected Product Family
        
        st.subheader("Sales Trend by Selected Product Family")

            # Allow users to select a product family
        selected_family = st.selectbox(
            "Select Product Family",
            options=sorted(data["family"].unique()))
        # Filter records for the selected family
        
        family_data = data[
            data["family"] == selected_family]
        
        # Calculate daily sales for the selected family
        
        family_daily_sales = (
            family_data.groupby("date")["sales"]
            .sum()
            .reset_index())
        
        # Create interactive sales trend chart
        
        fig = px.line(
            family_daily_sales,
            x="date",
            y="sales",
            markers=True,
            title=f"Daily Sales Trend - {selected_family}",
            labels={
                "date": "Date",
                "sales": "Total Sales Volume"
                })
        
        # Customize chart
        fig.update_layout(
            template="plotly_dark",
            hovermode="x unified",
            xaxis_title="Date",
            yaxis_title="Total Sales Volume")

        # Display chart
        st.plotly_chart(fig, use_container_width=True)



# Sales by Day of the Week for selected year

    # Define the correct order of weekdays
    weekday_order = [
    "Monday", "Tuesday", "Wednesday",
    "Thursday", "Friday", "Saturday", "Sunday"]

    # Extract weekday names from the date column
    data["day_name"] = data["date"].dt.day_name()

    # Create year selection dropdown
    selected_year = st.selectbox(
    "Select Year you want to Fliter for:",
    options=sorted(data["year"].unique()))

    # Filter data based on selected year
    year_data = data[data["year"] == selected_year]

    col7, col8 = st.columns(2)

    with col7:
        
        # Sales by Day of the week for selected year
        st.subheader("Weekly Sales Performance by Year")

        # Calculate total sales for each weekday
        weekday_sales = (
        year_data.groupby("day_name")["sales"]
        .sum()
        .reindex(weekday_order)
        .reset_index())

        # Create Plotly bar chart
        fig = px.bar(
        weekday_sales,
        x="day_name",
        y="sales",
        title=f"Total Sales Volume by Day of the Week - {selected_year}",
        labels={
            "day_name": "Day of the Week",
            "sales": "Total Sales Volume"},
            color="sales",
            color_continuous_scale="Blues")
        
        # Customize chart
        fig.update_layout(
        template="plotly_dark",
        coloraxis_showscale=False,
        xaxis_title="Day of the Week",
        yaxis_title="Total Sales Volume")

        # Display chart
        st.plotly_chart(fig, use_container_width=True)

    with col8:
        # Montly Sales Performance per year 
        st.subheader("Montly Sales Performance per year" )
        # Calculate monthly sales for the selected year
        monthly_sales = (
            year_data.groupby("month")["sales"]
            .sum()
            .reindex(range(1, 13), fill_value=0)
            .reset_index())
        
        # Define month names
        month_names = [
            "Jan", "Feb", "Mar", "Apr", "May", "Jun",
            "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]


        # Create interactive monthly sales chart
        fig = px.line(
        monthly_sales,
        x="month",
        y="sales",
        markers=True,
        title=f"Monthly Sales Performance - {selected_year}",
        labels={
            "month": "Month",
            "sales": "Total Sales Volume"
            },
                color_discrete_sequence=["#2471A3"])
        
        # Display month names on the x-axis
        fig.update_xaxes(
            tickmode="array",
            tickvals=list(range(1, 13)),
            ticktext=month_names)
        
        # Customize chart
        
        fig.update_layout(
            template="plotly_dark",
            hovermode="x unified",
            xaxis_title="Month",
            yaxis_title="Total Sales Volume")
        
        # Format sales values
        
        fig.update_yaxes(tickformat=",")
        
        # Display chart
        
        st.plotly_chart(fig, use_container_width=True)


# Demand Forecasting 

elif section == "Demand Forecasting":
    
    st.subheader("Retail Demand Forecasting")

    st.write(
        "Enter the details below to generate a retail sales forecast."
    )

    # Create forecasting form
    with st.form("forecast_form"):

        # Select forecast date
        forecast_date = st.date_input(
            "Forecast Date"
        )

        # Select store
        store_nbr = st.selectbox(
            "Select Store",
            options=sorted(data["store_nbr"].unique())
        )

        # Select product family
        family = st.selectbox(
            "Select Product Family",
            options=sorted(data["family"].unique())
        )

        # Enter promotion count
        onpromotion = st.number_input(
            "Number of Products on Promotion",
            min_value=0,
            step=1
        )

        # Submit button
        predict_button = st.form_submit_button(
            "Generate Forecast"
        )

    # Generate Prediction

    if predict_button:

        api_url = "https://store-sales-forecasting-api.onrender.com/predict"

        payload = {"date": str(forecast_date),
                   "store_nbr" : int(store_nbr),
                   "family" : str(family),
                   "onpromotion" : int(onpromotion)
                   }
        
        try:
            response = requests.post(
                api_url,
                json = payload,
                timeout= 120
            )

            response.raise_for_status()

            prediction = response.json()

            st.success("Forcast Generated Successful")

            st.write(
                f"The predicted sales volume for Store {prediction['store_nbr']} "
                f"(for {prediction['family']}) on {prediction['date']} is:"
                )
            
            st.metric(
                label=" ",
                value=f"{prediction['Predicted_sales']:,.2f}")

        except requests.exceptions.RequestException as error:
            st.error(f"Could not connect to the forecasting API: {error}")

# Inventory Intelligence Section. 

elif section == "Inventory Intelligence":
    st.subheader("Inventory Intelligence")

    st.divider()

    col9, col10 = st.columns(2)

    # Daily Average Demand of each produce 
    # Calculate daily sales for each product family
    with col9:
        family_daily_demand = (
            data.groupby(["family", "date"])["sales"]
            .sum()
            .reset_index())

    # Calculate average daily demand for each product family
        average_daily_demand = (
            family_daily_demand.groupby("family")["sales"]
            .mean()
            .reset_index()
            .sort_values(by="sales", ascending=True)
            )

    # Visualize average daily demand by product family
        fig = px.bar(
            average_daily_demand,
            x="sales",
            y="family",
            orientation="h",
            title="Average Daily Demand by Product Family",
            labels={
                "sales": "Average Daily Sales Volume",
                "family": "Product Family"
                },
            color="sales",
            color_continuous_scale="Blues"
            )

        fig.update_layout(
            template="plotly_dark",
            height=850,
            coloraxis_showscale=False,
            xaxis_title="Average Daily Sales Volume",
            yaxis_title="Product Family"
            )

        st.plotly_chart(fig, use_container_width=True)

    # Calculate demand variability for each product family

    with col10:
        demand_variability = (
            family_daily_demand.groupby("family")["sales"]
            .std()
            .reset_index()
            .sort_values(by="sales", ascending=True)
            )

    # Visualize demand variability by product family
        fig = px.bar(
            demand_variability,
            x="sales",
            y="family",
            orientation="h",
            title="Demand Variability by Product Family",
            labels={
                "sales": "Standard Deviation of Daily Sales",
                "family": "Product Family"
                },
            color="sales",
            color_continuous_scale="Reds"
            )

        fig.update_layout(
            template="plotly_dark",
            height=850,
            coloraxis_showscale=False,
            xaxis_title="Standard Deviation of Daily Sales",
            yaxis_title="Product Family"
            )

        st.plotly_chart(fig, use_container_width=True)

        st.divider()

    # Calculate average demand and standard deviation
        demand_stats = (
        family_daily_demand.groupby("family")["sales"]
        .agg(["mean", "std"])
        .reset_index()
        )

    # Calculate coefficient of variation
        demand_stats["CV"] = (
            demand_stats["std"] / demand_stats["mean"]
            ) * 100

    # Sort by coefficient of variation
        demand_stats = demand_stats.sort_values(
            by="CV",
            ascending=True)

    # Visualize demand volatility by product family
    fig = px.bar(
        demand_stats,
        x="CV",
        y="family",
        orientation="h",
        title="Demand Volatility by Product Family",
        labels={
            "CV": "Coefficient of Variation (%)",
            "family": "Product Family"
            },
        color="CV",
        color_continuous_scale="Reds"
        )

    fig.update_layout(
        template="plotly_dark",
        height=850,
        coloraxis_showscale=False,
        xaxis_title="Coefficient of Variation (%)",
        yaxis_title="Product Family"
        )

    st.plotly_chart(fig, use_container_width=True)

    st.divider()
    
# Store-Level Demand Analysis
    st.subheader("Store-Level Demand Analysis")



    # Allow users to select a product family
    selected_family = st.selectbox(
        "Select Product Family",
        options=sorted(data["family"].unique()),
        key="inventory_store_family")

    # Filter the dataset for the selected product family
    family_store_data = data[
        data["family"] == selected_family
        ]

    # Calculate average daily demand and total sales for each store
    store_level_demand = (
        family_store_data.groupby("store_nbr")
        .agg(
            average_daily_demand=("sales", "mean"),
            total_sales=("sales", "sum")
            )
            .reset_index()
            .sort_values(
                by="average_daily_demand",
                ascending=True
                )
                )

    
    # Convert store numbers to strings for categorical plotting
    store_level_demand["store_nbr"] = (
        store_level_demand["store_nbr"].astype(str)
        )

    # Create the Plotly chart
    fig = px.bar(
        store_level_demand,
        x="average_daily_demand",
        y="store_nbr",
        orientation="h",
        title=f"Average Daily Demand for {selected_family} Across Stores",
        labels={
            "average_daily_demand": "Average Daily Sales Volume",
            "store_nbr": "Store Number"
            },
            color="average_daily_demand",
            color_continuous_scale="Blues",
            hover_data={
                "total_sales": ":,.2f",
                "average_daily_demand": ":,.2f"
                })

    fig.update_layout(
        template="plotly_dark",
        height=850,
        coloraxis_showscale=False,
        xaxis_title="Average Daily Sales Volume",
        yaxis_title="Store Number")

    st.plotly_chart(fig, use_container_width=True)

    st.divider()
    
# Monthly Demand Trends for the selected year 
    st.subheader("Monthly Demand Trends")


# Create two columns for the filters
    col1, col2 = st.columns(2)

    with col1:
        selected_trend_family = st.selectbox(
            "Select Product Family",
            options=sorted(data["family"].unique()),
            key="monthly_trend_family"
            )

    with col2:
        selected_trend_year = st.selectbox(
            "Select Year",
            options=sorted(data["year"].unique()),
            key="monthly_trend_year")   

# Filter data by selected family and year
    monthly_trend_data = data[
        (data["family"] == selected_trend_family) &
        (data["year"] == selected_trend_year)
        ]

# Calculate total daily demand across all stores
    daily_trend_demand = (
        monthly_trend_data.groupby("date")["sales"]
        .sum()
        .reset_index()
        )

# Extract month from the date
    daily_trend_demand["month"] = (
        daily_trend_demand["date"].dt.month
        )

# Calculate average daily demand for each month
    monthly_demand = (
        daily_trend_demand.groupby("month")["sales"]
        .mean()
        .reset_index()
        .rename(columns={"sales": "average_daily_demand"}))

# Convert month numbers to month names
    month_names = [
        "January", "February", "March", "April",
        "May", "June", "July", "August",
        "September", "October", "November", "December"
        ]

    monthly_demand["month_name"] = (
        monthly_demand["month"].map(
            lambda month: month_names[month - 1]
            ))

# Create the Plotly line chart
    fig = px.line(
        monthly_demand,
        x="month_name",
        y="average_daily_demand",
        markers=True,
        title=(
            f"Monthly Demand Trend for {selected_trend_family} "
            f"({selected_trend_year})"
            ),
            labels={"month_name": "Month",
                    "average_daily_demand": "Average Daily Sales Volume"},
            category_orders={"month_name": month_names}
            )

    fig.update_layout(
        template="plotly_dark",
        height=500,
        xaxis_title="Month",
        yaxis_title="Average Daily Sales Volume"
        )

    st.plotly_chart(fig, use_container_width=True)

# Promotion Section 


elif section == "Promotion Analysis":
    st.subheader("Promotion Analysis")
    st.divider()

    # Classify records based on promotional activity
    data["promotion_status"] = data["onpromotion"].apply(
        lambda x: "Promotion Active" if x > 0 else "No Promotion"
    )

    # Calculate average sales by promotion status
    promotion_sales = (
        data.groupby("promotion_status")["sales"]
        .mean()
        .reset_index()
        .sort_values(by="sales", ascending=False)
    )

    # Visualize average sales by promotion status
    fig = px.bar(
        promotion_sales,
        x="promotion_status",
        y="sales",
        title="Average Sales: Promotional vs Non-Promotional Records",
        labels={
            "promotion_status": "Promotion Status",
            "sales": "Average Sales Volume"
        },
        color="promotion_status",
        color_discrete_sequence=["#2196F3", "#FF9800"],
        text_auto=".2f"
    )

    fig.update_layout(
        template="plotly_dark",
        height=500,
        showlegend=False,
        xaxis_title="Promotion Status",
        yaxis_title="Average Sales Volume"
    )

    st.plotly_chart(fig, use_container_width=True)

    st.divider()
    # Effect of Promotion on product 

    promotion_family_sales = (
        data.groupby(["family", "promotion_status"])["sales"]
        .mean()
        .reset_index()
        )

    fig = px.bar(
        promotion_family_sales,
        x="family",
        y="sales",
        color="promotion_status",
        barmode="group",
        title="Average Sales by Product Family and Promotion Status",
        labels={
            "family": "Product Family",
            "sales": "Average Sales Volume",
            "promotion_status": "Promotion Status"
            },
        color_discrete_map={
            "Promotion Active": "#2196F3",
            "No Promotion": "#FF9800"
            }
            )

    fig.update_layout(
        template="plotly_dark",
        height=650,
        xaxis_title="Product Family",
        yaxis_title="Average Sales Volume",
        xaxis_tickangle=-45
        )

    st.plotly_chart(fig, use_container_width=True)

    st.divider()
        # Promotion Activity 

    promotion_by_family = (
        data.groupby("family")["onpromotion"]
        .mean()
        .reset_index()
        .sort_values(by="onpromotion", ascending=True)
        )

    fig = px.bar(
        promotion_by_family,
        x="onpromotion",
        y="family",
        orientation="h",
        title="Average Promotional Product Count by Product Family",
        labels={
            "onpromotion": "Average Number of Products on Promotion",
            "family": "Product Family"
            },
        color="onpromotion",
        color_continuous_scale="Blues",
        text_auto=".2f"
        )

    fig.update_layout(
        template="plotly_dark",
        height=750,
        coloraxis_showscale=False,
        xaxis_title="Average Number of Products on Promotion",
        yaxis_title="Product Family"
        )

    st.plotly_chart(fig, use_container_width=True)

    # Relationship between promotion and sales 

    st.divider()

    promotion_data = data.copy()

    promotion_data["promotion_level"] = pd.cut(
        promotion_data["onpromotion"],
        bins=[-1, 0, 5, 10, 20, float("inf")],
        labels=[
            "No Promotion",
            "1–5 Products",
            "6–10 Products",
            "11–20 Products",
            "Above 20 Products"
            ])

    promotion_level_sales = (
        promotion_data.groupby("promotion_level", observed=False)["sales"]
        .mean()
        .reset_index()
        )

    fig = px.bar(
        promotion_level_sales,
        x="promotion_level",
        y="sales",
        title="Average Sales Volume by Promotion Level",
        labels={
            "promotion_level": "Promotion Level",
            "sales": "Average Sales Volume"
            },
        color="sales",
        color_continuous_scale="Blues",
        text_auto=".2f"
        )

    fig.update_layout(
        template="plotly_dark",
        height=500,
        coloraxis_showscale=False,
        xaxis_title="Promotion Level",
        yaxis_title="Average Sales Volume"
        )

    st.plotly_chart(fig, use_container_width=True)


    st.divider()
    # Promotion Activity Over Time

    
    monthly_promotion = (
        data.groupby(["year", "month"])["onpromotion"]
        .mean()
        .reset_index()
        )

    monthly_promotion["month_name"] = monthly_promotion["month"].map({
        1: "January",
        2: "February",
        3: "March",
        4: "April",
        5: "May",
        6: "June",
        7: "July",
        8: "August",
        9: "September",
        10: "October",
        11: "November",
        12: "December"
        })

    fig = px.line(
        monthly_promotion,
        x="month_name",
        y="onpromotion",
        color="year",
        markers=True,
        title="Monthly Promotional Activity Over the Years",
        labels={
            "month_name": "Month",
            "onpromotion": "Average Promotion Count",
            "year": "Year"
            },
        category_orders={
            "month_name": [
            "January", "February", "March", "April",
            "May", "June", "July", "August",
            "September", "October", "November", "December"
            ]
            }
            )

    fig.update_layout(
        template="plotly_dark",
        height=550,
        xaxis_title="Month",
        yaxis_title="Average Number of Products on Promotion"
        )

    st.plotly_chart(fig, use_container_width=True)

    # Promotion By Store 

    st.divider()

    store_promotion = (
        data.groupby("store_nbr")["onpromotion"]
        .mean()
        .reset_index()
        .sort_values(by="onpromotion", ascending=True)
        )

    store_promotion["store_nbr"] = store_promotion["store_nbr"].astype(str)

    fig = px.bar(
        store_promotion,
        x="onpromotion",
        y="store_nbr",
        orientation="h",
        title="Average Promotional Activity by Store",
        labels={
            "onpromotion": "Average Promotion Count",
            "store_nbr": "Store Number"
            },
        color="onpromotion",
        color_continuous_scale="Blues",
        text_auto=".2f"
        )

    fig.update_layout(
        template="plotly_dark",
        height=850,
        coloraxis_showscale=False,
        xaxis_title="Average Number of Products on Promotion",
        yaxis_title="Store Number"
        )

    st.plotly_chart(fig, use_container_width=True)

elif section == "Model Performance":
    st.subheader("Model Performance")

    st.write(
        "Evaluate the performance of the XGBoost model "
        "used for retail sales forecasting."
    )

    col1, col2 = st.columns(2)

    with col1:
        st.metric(
            label="R² Score",
            value="0.9294"
        )

    with col2:
        st.metric(
            label="RMSE",
            value="0.7158"
        )

    # import evaluation result 
    @st.cache_data
    def import_df():
        evaluation = pd.read_csv("frontend/evaluation_results.csv")
        return evaluation


# Load evaluation results
    evaluation = import_df()

    # Convert y_test and y_pred from log transform
    import numpy as np

    evaluation["actual_sales"] = np.expm1(evaluation["actual_sales"])

    evaluation["predicted_sales"] = np.expm1(evaluation["predicted_sales"])

    # Plot the Scatter plot

    fig = px.scatter(
        evaluation,
        x="actual_sales",
        y="predicted_sales",
        title="Actual vs Predicted Sales",
        labels={
            "actual_sales": "Actual Sales Volume",
            "predicted_sales": "Predicted Sales Volume"
            },
        opacity=0.5
        )

    # Calculate the range for the reference line
    min_value = min(
        evaluation["actual_sales"].min(),
        evaluation["predicted_sales"].min()
        )

    max_value = max(
        evaluation["actual_sales"].max(),
        evaluation["predicted_sales"].max())

# Add perfect-prediction line
    fig.add_shape(
        type="line",
        x0=min_value,
        y0=min_value,
        x1=max_value,
        y1=max_value,
        line=dict(
            color="red",
            dash="dash",
            width=2))

    fig.update_layout(
        template="plotly_dark",
        height=600,
        xaxis_title="Actual Sales Volume",
        yaxis_title="Predicted Sales Volume")

    st.plotly_chart(fig, use_container_width=True)

    # Add Resisdual Analysis
    st.subheader("Residual Analysis")

    st.write(
        "Examine the distribution of prediction errors "
        "to understand how the model performs.")

    evaluation["residual"] = (
        evaluation["actual_sales"] - evaluation["predicted_sales"])

    fig = px.histogram(
        evaluation,
        x="residual",
        nbins=50,
        title="Distribution of Prediction Errors",
        labels={
            "residual": "Residual (Actual - Predicted)"},
        color_discrete_sequence=["#2196F3"],
        opacity=0.8)

    fig.add_vline(
        x=0,
        line_dash="dash",
        line_color="red",
        line_width=2)

    fig.update_layout(
        template="plotly_dark",
        height=500,
        xaxis_title="Prediction Error",
        yaxis_title="Frequency",
        showlegend=False)

    st.plotly_chart(fig, use_container_width=True)

    # Feature importance
    import pickle

    st.subheader("Feature Importance")

    st.write(
        "Identify the features that contribute most to the "
        "XGBoost model's predictions.")

    # Load the saved model bundle
    with open("xgboost_bundle.pkl", "rb") as file:
        model_bundle = pickle.load(file)

    # Extract model and feature names
    model = model_bundle["model"]
    feature_names = model_bundle["feature_names"]

    # Create feature importance DataFrame
    feature_importance = pd.DataFrame({
        "feature": feature_names,
        "importance": model.feature_importances_
        })

    # Select the 15 most important features
    feature_importance = (
        feature_importance
        .sort_values(by="importance", ascending=True)
        .tail(15))

    # Plot feature importance
    fig = px.bar(
        feature_importance,
        x="importance",
        y="feature",
        orientation="h",
        title="Top 15 Most Important Features",
        labels={
            "importance": "Feature Importance",
            "feature": "Model Feature"
            },
        color="importance",
        color_continuous_scale="Blues")

    fig.update_layout(
        template="plotly_dark",
        height=650,
        coloraxis_showscale=False,
        xaxis_title="Feature Importance",
        yaxis_title="Feature")

    st.plotly_chart(fig, use_container_width=True)