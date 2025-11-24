import streamlit as st
import pandas as pd
import numpy as np
from config import DATE_FORMATS, COST_COMPONENTS


def parse_dates(date_series):
    result = pd.to_datetime(date_series, errors='coerce', infer_datetime_format=True)

    if result.isna().sum() > len(result) * 0.5:
        for fmt in DATE_FORMATS:
            try:
                result = pd.to_datetime(date_series, format=fmt, errors='coerce')
                if result.notna().sum() > len(result) * 0.5:
                    st.sidebar.success(f"Date format detected: {fmt}")
                    break
            except:
                continue

    return result


@st.cache_data
def load_data():

    try:
        orders = pd.read_csv('data/orders.csv')
        delivery = pd.read_csv('data/delivery_performance.csv')
        costs = pd.read_csv('data/cost_breakdown.csv')
        routes = pd.read_csv('data/routes_distance.csv')
        fleet = pd.read_csv('data/vehicle_fleet.csv')
        warehouse = pd.read_csv('data/warehouse_inventory.csv')
        feedback = pd.read_csv('data/customer_feedback.csv')

        orders['Order_Date'] = parse_dates(orders['Order_Date'])
        delivery['Promised_Delivery_Days'] = pd.to_numeric(delivery['Promised_Delivery_Days'], errors='coerce')
        delivery['Actual_Delivery_Days'] = pd.to_numeric(delivery['Actual_Delivery_Days'], errors='coerce')
        feedback['Feedback_Date'] = parse_dates(feedback['Feedback_Date'])
        warehouse['Last_Restocked_Date'] = parse_dates(warehouse['Last_Restocked_Date'])

        main_df = orders.copy()

        if 'Order_ID' in delivery.columns:
            main_df = main_df.merge(delivery, on='Order_ID', how='left', suffixes=('', '_delivery'))

        if 'Order_ID' in costs.columns:
            main_df = main_df.merge(costs, on='Order_ID', how='left')

        if 'Order_ID' in routes.columns:
            main_df = main_df.merge(routes, on='Order_ID', how='left')

        if 'Vehicle_ID' in main_df.columns and 'Vehicle_ID' in fleet.columns:
            main_df = main_df.merge(fleet, on='Vehicle_ID', how='left', suffixes=('', '_fleet'))

        existing_cost_cols = [col for col in COST_COMPONENTS if col in main_df.columns]

        if existing_cost_cols:
            main_df['total_cost'] = main_df[existing_cost_cols].sum(axis=1)
        else:
            st.error("No cost columns found in data!")
            return None

        if 'Distance_KM' in main_df.columns and 'total_cost' in main_df.columns:
            main_df['cost_per_km'] = main_df['total_cost'] / main_df['Distance_KM'].replace(0, np.nan)

        if 'Order_Value_INR' in main_df.columns and 'total_cost' in main_df.columns:
            main_df['revenue_to_cost_ratio'] = main_df['Order_Value_INR'] / main_df['total_cost'].replace(0, np.nan)

        if 'Actual_Delivery_Days' in main_df.columns and 'Promised_Delivery_Days' in main_df.columns:
            main_df['delivery_delay_days'] = main_df['Actual_Delivery_Days'] - main_df['Promised_Delivery_Days']

        return {
            'main': main_df,
            'orders': orders,
            'delivery': delivery,
            'costs': costs,
            'routes': routes,
            'fleet': fleet,
            'warehouse': warehouse,
            'feedback': feedback
        }
    except FileNotFoundError as e:
        st.error(f"File not found: {str(e)}")
        st.info("Please ensure all CSV files are in the 'data/' directory")
        return None
    except Exception as e:
        st.error(f"Error loading data: {str(e)}")
        import traceback
        st.error(traceback.format_exc())
        return None


def apply_filters(main_df):
    if 'Order_Date' in main_df.columns and not main_df['Order_Date'].isna().all():
        date_range = st.sidebar.date_input(
            "Select Date Range",
            value=(main_df['Order_Date'].min(), main_df['Order_Date'].max()),
            key='date_range'
        )
        if len(date_range) == 2:
            main_df = main_df[
                (main_df['Order_Date'] >= pd.Timestamp(date_range[0])) &
                (main_df['Order_Date'] <= pd.Timestamp(date_range[1]))
                ]

    if 'Priority' in main_df.columns:
        priorities = st.sidebar.multiselect(
            "Priority Level",
            options=main_df['Priority'].dropna().unique(),
            default=main_df['Priority'].dropna().unique()
        )
        if priorities:
            main_df = main_df[main_df['Priority'].isin(priorities)]

    if 'Vehicle_Type' in main_df.columns:
        vehicle_types = st.sidebar.multiselect(
            "Vehicle Type",
            options=main_df['Vehicle_Type'].dropna().unique(),
            default=main_df['Vehicle_Type'].dropna().unique()
        )
        if vehicle_types:
            main_df = main_df[main_df['Vehicle_Type'].isin(vehicle_types)]

    if 'Product_Category' in main_df.columns:
        categories = st.sidebar.multiselect(
            "Product Category",
            options=main_df['Product_Category'].dropna().unique(),
            default=main_df['Product_Category'].dropna().unique()
        )
        if categories:
            main_df = main_df[main_df['Product_Category'].isin(categories)]

    return main_df