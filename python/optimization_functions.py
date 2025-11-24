import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from datetime import datetime


def show_optimization_opportunities(df, data):
    st.header("💡 Optimization Opportunities")
    st.markdown("**Actionable insights to reduce costs by 15-20%**")

    opportunities = []
    potential_savings = 0

    st.markdown("---")
    st.subheader("🗺️ Route Optimization")
    route_savings = _analyze_route_optimization(df)
    if route_savings:
        opportunities.append(route_savings)
        potential_savings += route_savings['savings']
    st.markdown("---")
    st.subheader("⚡ Priority Level Optimization")
    priority_savings = _analyze_priority_optimization(df)
    if priority_savings:
        opportunities.append(priority_savings)
        potential_savings += priority_savings['savings']
    st.markdown("---")
    st.subheader("🏭 Warehouse Optimization")
    warehouse_savings = _analyze_warehouse_optimization(data['warehouse'])
    if warehouse_savings:
        opportunities.append(warehouse_savings)
        potential_savings += warehouse_savings['savings']
    st.markdown("---")
    st.subheader("⛽ Fuel Efficiency Improvements")
    fuel_savings = _analyze_fuel_efficiency(df)
    if fuel_savings:
        opportunities.append(fuel_savings)
        potential_savings += fuel_savings['savings']

    _show_optimization_summary(df, opportunities, potential_savings)


def _analyze_route_optimization(df):
    if 'Route' in df.columns and 'total_cost' in df.columns and 'cost_per_km' in df.columns:
        route_analysis = df.groupby('Route').agg({
            'total_cost': 'sum',
            'cost_per_km': 'mean',
            'Distance_KM': 'mean',
            'Order_ID': 'count'
        }).reset_index()
        route_analysis.columns = ['Route', 'Total Cost', 'Avg Cost/KM', 'Avg Distance', 'Orders']

        if 'Traffic_Delay_Minutes' in df.columns:
            traffic_by_route = df.groupby('Route')['Traffic_Delay_Minutes'].mean()
            route_analysis = route_analysis.merge(traffic_by_route.reset_index(), on='Route', how='left')
            route_analysis.columns = list(route_analysis.columns[:-1]) + ['Avg Delay']

        avg_route_cost = route_analysis['Avg Cost/KM'].mean()
        inefficient_routes = route_analysis[route_analysis['Avg Cost/KM'] > avg_route_cost * 1.3]

        if len(inefficient_routes) > 0:
            savings = inefficient_routes['Total Cost'].sum() * 0.20

            col1, col2 = st.columns(2)
            with col1:
                top_routes = inefficient_routes.nlargest(10, 'Total Cost')
                fig = px.bar(top_routes, x='Route', y='Total Cost',
                             title='Top 10 Most Expensive Routes',
                             color='Avg Cost/KM', color_continuous_scale='Reds')
                fig.update_xaxes(tickangle=-45)
                st.plotly_chart(fig, use_container_width=True)

            with col2:
                st.markdown(f"""
                <div class="alert-box">
                <h4>🗺️ Route Inefficiency Alert</h4>
                <p><strong>{len(inefficient_routes)} routes</strong> have significantly higher costs</p>
                <p><strong>Potential Annual Savings: ₹{savings:,.0f}</strong></p>
                <ul>
                <li>Consolidate shipments on expensive routes</li>
                <li>Use alternative routes during peak traffic</li>
                <li>Consider route splitting or combining</li>
                <li>Negotiate better rates with carriers</li>
                </ul>
                </div>
                """, unsafe_allow_html=True)

            return {
                'category': 'Route Optimization',
                'opportunity': f'{len(inefficient_routes)} routes with 30%+ higher cost per km',
                'savings': savings,
                'action': 'Optimize routing and scheduling'
            }
        else:
            st.success("✅ Route efficiency is optimized")
    else:
        st.warning("Route data not available for analysis")
    return None


def _analyze_priority_optimization(df):
    if 'Priority' in df.columns and 'total_cost' in df.columns:
        priority_analysis = df.groupby('Priority').agg({
            'total_cost': ['sum', 'mean'],
            'Order_ID': 'count'
        }).reset_index()
        priority_analysis.columns = ['Priority', 'Total Cost', 'Avg Cost', 'Orders']

        if 'Order_Value_INR' in df.columns:
            revenue_by_priority = df.groupby('Priority')['Order_Value_INR'].sum().reset_index()
            priority_analysis = priority_analysis.merge(revenue_by_priority, on='Priority', how='left')
            priority_analysis.columns = list(priority_analysis.columns[:-1]) + ['Total Revenue']
            priority_analysis['ROI'] = priority_analysis['Total Revenue'] / priority_analysis['Total Cost']

        priority_analysis['Cost %'] = (priority_analysis['Total Cost'] / priority_analysis['Total Cost'].sum()) * 100

        col1, col2 = st.columns(2)
        with col1:
            if 'Total Revenue' in priority_analysis.columns:
                fig = px.bar(priority_analysis, x='Priority', y=['Total Cost', 'Total Revenue'],
                             title='Cost vs Revenue by Priority', barmode='group')
                st.plotly_chart(fig, use_container_width=True)
            else:
                fig = px.bar(priority_analysis, x='Priority', y='Total Cost',
                             title='Total Cost by Priority',
                             color='Avg Cost', color_continuous_scale='Blues')
                st.plotly_chart(fig, use_container_width=True)

        with col2:
            st.dataframe(priority_analysis, use_container_width=True)

        if 'Express' in priority_analysis['Priority'].values:
            express_data = priority_analysis[priority_analysis['Priority'] == 'Express'].iloc[0]
            express_pct = express_data['Cost %']

            if express_pct > 30:
                savings = express_data['Total Cost'] * 0.25

                st.markdown(f"""
                <div class="alert-box">
                <h4>⚡ Priority Level Alert</h4>
                <p>Express deliveries are <strong>{express_pct:.1f}%</strong> of total costs</p>
                <p><strong>Potential Savings (if 25% shifted to Standard): ₹{savings:,.0f}</strong></p>
                <ul>
                <li>Review customer expectations vs actual needs</li>
                <li>Offer incentives for standard delivery</li>
                <li>Implement smart priority assignment</li>
                </ul>
                </div>
                """, unsafe_allow_html=True)

                return {
                    'category': 'Priority Optimization',
                    'opportunity': f'Express deliveries account for {express_pct:.1f}% of costs',
                    'savings': savings,
                    'action': 'Shift 25% of Express to Standard'
                }
    else:
        st.warning("Priority data not available for analysis")
    return None


def _analyze_warehouse_optimization(warehouse_df):
    if 'Warehouse_ID' in warehouse_df.columns:
        if 'Storage_Cost_per_Unit' in warehouse_df.columns and 'Current_Stock_Units' in warehouse_df.columns:
            warehouse_costs = warehouse_df.groupby('Warehouse_ID').agg({
                'Storage_Cost_per_Unit': 'mean',
                'Current_Stock_Units': 'sum'
            }).reset_index()
            warehouse_costs.columns = ['Warehouse', 'Avg Storage Cost/Unit', 'Total Stock']
            warehouse_costs['Total Storage Cost'] = warehouse_costs['Avg Storage Cost/Unit'] * warehouse_costs[
                'Total Stock']

            avg_storage_cost = warehouse_costs['Avg Storage Cost/Unit'].mean()
            expensive_warehouses = warehouse_costs[warehouse_costs['Avg Storage Cost/Unit'] > avg_storage_cost * 1.15]

            if len(expensive_warehouses) > 0:
                savings = expensive_warehouses['Total Storage Cost'].sum() * 0.12

                col1, col2 = st.columns(2)
                with col1:
                    fig = px.bar(warehouse_costs, x='Warehouse', y='Avg Storage Cost/Unit',
                                 title='Storage Cost per Unit by Warehouse',
                                 color='Total Storage Cost', color_continuous_scale='Oranges')
                    st.plotly_chart(fig, use_container_width=True)

                with col2:
                    st.markdown(f"""
                    <div class="alert-box">
                    <h4>🏭 Warehouse Cost Alert</h4>
                    <p><strong>{len(expensive_warehouses)} warehouses</strong> with higher storage costs</p>
                    <p><strong>Potential Annual Savings: ₹{savings:,.0f}</strong></p>
                    <ul>
                    <li>Negotiate better warehouse rates</li>
                    <li>Consolidate inventory to lower-cost locations</li>
                    <li>Implement just-in-time inventory</li>
                    <li>Review slow-moving inventory</li>
                    </ul>
                    </div>
                    """, unsafe_allow_html=True)

                return {
                    'category': 'Warehouse Optimization',
                    'opportunity': f'{len(expensive_warehouses)} warehouses with 15%+ higher storage costs',
                    'savings': savings,
                    'action': 'Consolidate or negotiate better rates'
                }
            else:
                st.success("✅ Warehouse costs are optimized")
        else:
            st.info("Warehouse cost data not available")
    else:
        st.warning("Warehouse data not available for analysis")
    return None


def _analyze_fuel_efficiency(df):
    if 'Fuel_Consumption_L' in df.columns and 'Distance_KM' in df.columns and 'Fuel_Cost' in df.columns:
        df_fuel = df.copy()
        df_fuel['fuel_efficiency'] = df_fuel['Distance_KM'] / df_fuel['Fuel_Consumption_L'].replace(0, np.nan)
        avg_efficiency = df_fuel['fuel_efficiency'].mean()

        inefficient_orders = df_fuel[df_fuel['fuel_efficiency'] < avg_efficiency * 0.8]

        if len(inefficient_orders) > 0:
            savings = df_fuel['Fuel_Cost'].sum() * 0.15

            col1, col2 = st.columns(2)
            with col1:
                fig = px.histogram(df_fuel.dropna(subset=['fuel_efficiency']), x='fuel_efficiency', nbins=30,
                                   title='Fuel Efficiency Distribution (km/L)',
                                   color_discrete_sequence=['steelblue'])
                fig.add_vline(x=avg_efficiency, line_dash="dash", line_color="red",
                              annotation_text="Average", annotation_position="top")
                st.plotly_chart(fig, use_container_width=True)

            with col2:
                st.markdown(f"""
                <div class="alert-box">
                <h4>⛽ Fuel Efficiency Alert</h4>
                <p>Significant variation in fuel efficiency across deliveries</p>
                <p><strong>Potential Annual Savings (15% improvement): ₹{savings:,.0f}</strong></p>
                <ul>
                <li>Driver training on fuel-efficient driving</li>
                <li>Regular vehicle maintenance</li>
                <li>Route optimization to reduce idle time</li>
                <li>Consider hybrid/electric vehicles</li>
                </ul>
                </div>
                """, unsafe_allow_html=True)

            return {
                'category': 'Fuel Efficiency',
                'opportunity': f'{len(inefficient_orders)} orders with poor fuel efficiency',
                'savings': savings,
                'action': 'Implement fuel efficiency program'
            }
    else:
        st.warning("Fuel data not available for efficiency analysis")
    return None


def _show_optimization_summary(df, opportunities, potential_savings):
    st.markdown("---")
    st.subheader("📊 Cost Optimization Summary")

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Opportunities Identified", len(opportunities))
    with col2:
        st.metric("Total Potential Savings", f"₹{potential_savings:,.0f}")
    with col3:
        if 'total_cost' in df.columns:
            current_total = df['total_cost'].sum()
            savings_pct = (potential_savings / current_total) * 100 if current_total > 0 else 0
            st.metric("Potential Cost Reduction", f"{savings_pct:.1f}%")

    if len(opportunities) > 0:
        opp_df = pd.DataFrame(opportunities)
        opp_df = opp_df.sort_values('savings', ascending=False)

        col1, col2 = st.columns(2)
        with col1:
            fig = px.bar(opp_df, x='category', y='savings',
                         title='Savings Potential by Category',
                         color='savings', color_continuous_scale='Greens',
                         labels={'savings': 'Potential Savings (₹)', 'category': 'Category'})
            st.plotly_chart(fig, use_container_width=True)

        with col2:
            fig = px.pie(opp_df, values='savings', names='category',
                         title='Savings Distribution', hole=0.4)
            st.plotly_chart(fig, use_container_width=True)

        st.subheader("📋 Action Plan")
        for idx, row in opp_df.iterrows():
            st.markdown(f"""
            <div class="success-box">
            <h4>{idx + 1}. {row['category']}</h4>
            <p><strong>Opportunity:</strong> {row['opportunity']}</p>
            <p><strong>Potential Savings:</strong> ₹{row['savings']:,.0f}</p>
            <p><strong>Recommended Action:</strong> {row['action']}</p>
            </div>
            """, unsafe_allow_html=True)

        csv = opp_df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Download Optimization Report",
            data=csv,
            file_name=f"optimization_opportunities_{datetime.now().strftime('%Y%m%d')}.csv",
            mime="text/csv"
        )
    else:
        st.info("No major optimization opportunities identified. Your operations are running efficiently!")