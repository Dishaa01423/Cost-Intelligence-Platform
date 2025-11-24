import streamlit as st
import warnings
from config import PAGE_CONFIG
from styles import CSS_STYLES
from data_loader import load_data, apply_filters
from dashboard_functions import show_executive_dashboard
from cost_analysis_functions import show_cost_analysis
from anomaly_functions import show_anomaly_detection
from predictive_functions import show_predictive_analytics
from optimization_functions import show_optimization_opportunities
from scenario_functions import show_what_if_scenarios
warnings.filterwarnings('ignore')


def main():
    st.set_page_config(**PAGE_CONFIG)
    st.markdown(CSS_STYLES, unsafe_allow_html=True)
    st.markdown('<div class="main-header">🚚 NexGen Cost Intelligence Platform</div>', unsafe_allow_html=True)
    st.markdown("### Transform Your Operations with Data-Driven Cost Optimization")

    data = load_data()
    if data is None:
        st.error("Failed to load data. Please ensure all CSV files are in the correct directory.")
        st.info("""
        Expected files in 'data/' directory:
        - orders.csv
        - delivery_performance.csv
        - cost_breakdown.csv
        - routes_distance.csv
        - vehicle_fleet.csv
        - warehouse_inventory.csv
        - customer_feedback.csv
        """)
        return

    main_df = data['main']

    st.sidebar.header("🔍 Filters & Controls")
    main_df = apply_filters(main_df)
    st.sidebar.markdown("---")

    page = st.sidebar.radio(
        "Navigate",
        ["📊 Executive Dashboard", "💰 Cost Analysis", "🚨 Anomaly Detection",
         "🤖 Predictive Analytics", "💡 Optimization Opportunities", "📈 What-If Scenarios"]
    )

    if page == "📊 Executive Dashboard":
        show_executive_dashboard(main_df, data)
    elif page == "💰 Cost Analysis":
        show_cost_analysis(main_df)
    elif page == "🚨 Anomaly Detection":
        show_anomaly_detection(main_df)
    elif page == "🤖 Predictive Analytics":
        show_predictive_analytics(main_df)
    elif page == "💡 Optimization Opportunities":
        show_optimization_opportunities(main_df, data)
    elif page == "📈 What-If Scenarios":
        show_what_if_scenarios(main_df)


if __name__ == "__main__":
    main()