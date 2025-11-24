import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
from config import COST_COMPONENTS


def show_executive_dashboard(df, data):
    st.header("📊 Executive Dashboard")
    st.markdown("**Real-time cost intelligence at a glance**")

    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        total_cost = df['total_cost'].sum() if 'total_cost' in df.columns else 0
        st.metric("Total Costs", f"₹{total_cost:,.0f}")
    with col2:
        avg_cost = df['total_cost'].mean() if 'total_cost' in df.columns else 0
        st.metric("Avg Cost/Order", f"₹{avg_cost:,.0f}")
    with col3:
        total_orders = len(df)
        st.metric("Total Orders", f"{total_orders:,}")
    with col4:
        avg_cost_per_km = df['cost_per_km'].mean() if 'cost_per_km' in df.columns else 0
        st.metric("Avg Cost/KM", f"₹{avg_cost_per_km:.2f}")
    with col5:
        avg_roi = df['revenue_to_cost_ratio'].mean() if 'revenue_to_cost_ratio' in df.columns else 0
        st.metric("Avg Revenue/Cost", f"{avg_roi:.2f}x")

    st.markdown("---")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### 🎯 Top Cost Drivers")
        existing_components = [col for col in COST_COMPONENTS if col in df.columns]

        if existing_components:
            cost_breakdown = df[existing_components].sum().sort_values(ascending=False)
            fig = px.bar(x=cost_breakdown.values, y=cost_breakdown.index, orientation='h',
                         labels={'x': 'Total Cost (₹)', 'y': 'Cost Category'},
                         color=cost_breakdown.values, color_continuous_scale='Blues')
            fig.update_layout(showlegend=False, height=400)
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.warning("Cost breakdown data not available")

    with col2:
        st.markdown("### 📈 Cost Trend Over Time")
        if 'Order_Date' in df.columns and 'total_cost' in df.columns:
            df_with_dates = df.dropna(subset=['Order_Date', 'total_cost'])

            if len(df_with_dates) > 0:
                try:
                    daily_costs = df_with_dates.groupby(df_with_dates['Order_Date'].dt.date)[
                        'total_cost'].sum().reset_index()
                    daily_costs.columns = ['Date', 'Total Cost']
                    daily_costs['Date'] = pd.to_datetime(daily_costs['Date'])

                    if len(daily_costs) > 0:
                        fig = px.line(daily_costs, x='Date', y='Total Cost', markers=True,
                                      title='Daily Cost Trend')
                        fig.update_layout(height=400, xaxis_title='Date', yaxis_title='Total Cost (₹)')
                        st.plotly_chart(fig, use_container_width=True)
                    else:
                        st.info("No date data available for cost trend")
                except Exception as e:
                    st.warning(f"Could not generate cost trend: {str(e)}")
            else:
                st.info("No valid date and cost data available")
        else:
            st.warning("Date or cost data not available")

    if 'Priority' in df.columns and 'total_cost' in df.columns:
        st.markdown("### 🚀 Cost by Priority Level")
        col1, col2 = st.columns(2)

        with col1:
            priority_costs = df.groupby('Priority').agg({'total_cost': 'sum', 'Order_ID': 'count'}).reset_index()
            priority_costs.columns = ['Priority', 'Total Cost', 'Order Count']
            fig = px.pie(priority_costs, values='Total Cost', names='Priority', title='Cost Distribution by Priority')
            st.plotly_chart(fig, use_container_width=True)

        with col2:
            priority_avg = df.groupby('Priority')['total_cost'].mean().reset_index()
            priority_avg.columns = ['Priority', 'Avg Cost']
            fig = px.bar(priority_avg, x='Priority', y='Avg Cost',
                         title='Average Cost per Order by Priority',
                         color='Avg Cost', color_continuous_scale='Reds')
            st.plotly_chart(fig, use_container_width=True)

    st.markdown("### 💡 Key Insights")
    insights = []

    if 'Priority' in df.columns and 'total_cost' in df.columns:
        priority_costs = df.groupby('Priority')['total_cost'].mean()
        if 'Express' in priority_costs.index and 'Economy' in priority_costs.index:
            ratio = priority_costs['Express'] / priority_costs['Economy']
            insights.append(f"🔸 Express deliveries cost {ratio:.1f}x more than Economy deliveries")

    if 'total_cost' in df.columns:
        expensive_orders = df.nlargest(5, 'total_cost')
        avg_expensive = expensive_orders['total_cost'].mean()
        insights.append(f"🔸 Top 5 most expensive orders average ₹{avg_expensive:,.0f} per delivery")

    if 'Fuel_Cost' in df.columns and 'total_cost' in df.columns:
        fuel_pct = (df['Fuel_Cost'].sum() / df['total_cost'].sum()) * 100
        insights.append(f"🔸 Fuel costs represent {fuel_pct:.1f}% of total operational costs")

    if 'Vehicle_Type' in df.columns and 'cost_per_km' in df.columns:
        vehicle_efficiency = df.groupby('Vehicle_Type')['cost_per_km'].mean().sort_values()
        if len(vehicle_efficiency) > 0:
            best_vehicle = vehicle_efficiency.index[0]
            insights.append(f"🔸 {best_vehicle} vehicles have the lowest cost per kilometer")

    for insight in insights:
        st.markdown(f'<div class="insight-box">{insight}</div>', unsafe_allow_html=True)

    st.markdown("---")
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Download Full Report (CSV)",
            data=csv,
            file_name=f"nexgen_cost_report_{datetime.now().strftime('%Y%m%d')}.csv",
            mime="text/csv"
        )