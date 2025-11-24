import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
from config import COST_COMPONENTS


def show_cost_analysis(df):
    st.header("💰 Cost Analysis")
    st.markdown("**Deep dive into cost components and patterns**")

    tab1, tab2, tab3 = st.tabs(["🗺️ By Route", "📦 By Product", "💵 Cost Breakdown"])

    with tab1:
        _show_route_analysis(df)

    with tab2:
        _show_product_analysis(df)

    with tab3:
        _show_cost_breakdown(df)


def _show_route_analysis(df):
    st.subheader("Route Efficiency Analysis")
    if 'Route' in df.columns and 'total_cost' in df.columns:
        route_costs = df.groupby('Route').agg({
            'total_cost': ['mean', 'sum', 'count'],
        }).reset_index()
        route_costs.columns = ['Route', 'Avg Cost', 'Total Cost', 'Orders']

        if 'Distance_KM' in df.columns:
            avg_distance = df.groupby('Route')['Distance_KM'].mean().reset_index()
            route_costs = route_costs.merge(avg_distance, on='Route', how='left')
            route_costs.columns = list(route_costs.columns[:-1]) + ['Avg Distance']

        if 'cost_per_km' in df.columns:
            cost_per_km = df.groupby('Route')['cost_per_km'].mean().reset_index()
            route_costs = route_costs.merge(cost_per_km, on='Route', how='left')
            route_costs.columns = list(route_costs.columns[:-1]) + ['Cost/KM']

        if 'Traffic_Delay_Minutes' in df.columns:
            avg_delay = df.groupby('Route')['Traffic_Delay_Minutes'].mean().reset_index()
            route_costs = route_costs.merge(avg_delay, on='Route', how='left')
            route_costs.columns = list(route_costs.columns[:-1]) + ['Avg Delay (min)']

        route_costs = route_costs.sort_values('Total Cost', ascending=False)

        col1, col2 = st.columns(2)

        with col1:
            top_routes = route_costs.head(10)
            if 'Avg Delay (min)' in route_costs.columns:
                fig = px.bar(top_routes, x='Route', y='Total Cost',
                             title='Top 10 Routes by Total Cost',
                             color='Avg Delay (min)', color_continuous_scale='Reds')
            else:
                fig = px.bar(top_routes, x='Route', y='Total Cost',
                             title='Top 10 Routes by Total Cost',
                             color='Total Cost', color_continuous_scale='Reds')
            fig.update_xaxes(tickangle=-45)
            st.plotly_chart(fig, use_container_width=True)

        with col2:
            if 'Avg Distance' in route_costs.columns and 'Cost/KM' in route_costs.columns:
                fig = px.scatter(route_costs, x='Avg Distance', y='Avg Cost',
                                 size='Orders', hover_data=['Route'],
                                 title='Cost vs Distance by Route',
                                 color='Cost/KM', color_continuous_scale='Viridis')
                st.plotly_chart(fig, use_container_width=True)
            else:
                fig = px.bar(route_costs.head(10), x='Route', y='Avg Cost',
                             title='Top 10 Routes by Average Cost',
                             color='Avg Cost', color_continuous_scale='Oranges')
                fig.update_xaxes(tickangle=-45)
                st.plotly_chart(fig, use_container_width=True)

        if 'Cost/KM' in route_costs.columns:
            st.markdown("#### Route Efficiency Metrics")
            col1, col2, col3 = st.columns(3)
            with col1:
                most_efficient = route_costs.nsmallest(1, 'Cost/KM').iloc[0]
                st.metric("Most Efficient Route", most_efficient['Route'],
                          f"₹{most_efficient['Cost/KM']:.2f}/km")
            with col2:
                least_efficient = route_costs.nlargest(1, 'Cost/KM').iloc[0]
                st.metric("Least Efficient Route", least_efficient['Route'],
                          f"₹{least_efficient['Cost/KM']:.2f}/km")
            with col3:
                efficiency_gap = least_efficient['Cost/KM'] / most_efficient['Cost/KM']
                st.metric("Efficiency Gap", f"{efficiency_gap:.1f}x",
                          "Opportunity for optimization")

        st.markdown("#### Detailed Route Cost Table")
        st.dataframe(route_costs, use_container_width=True)

        csv = route_costs.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Download Route Cost Report",
            data=csv,
            file_name=f"route_cost_analysis_{datetime.now().strftime('%Y%m%d')}.csv",
            mime="text/csv"
        )
    else:
        st.warning("Route data not available for analysis")


def _show_product_analysis(df):
    st.subheader("Product Category Cost Analysis")
    if 'Product_Category' in df.columns and 'total_cost' in df.columns:
        product_costs = df.groupby('Product_Category').agg({
            'total_cost': ['sum', 'mean', 'count'],
        }).reset_index()
        product_costs.columns = ['Category', 'Total Cost', 'Avg Cost', 'Orders']

        if 'Order_Value_INR' in df.columns:
            revenue = df.groupby('Product_Category')['Order_Value_INR'].sum().reset_index()
            product_costs = product_costs.merge(revenue, left_on='Category', right_on='Product_Category', how='left')
            product_costs = product_costs.drop('Product_Category', axis=1)
            product_costs.columns = list(product_costs.columns[:-1]) + ['Total Revenue']

        if 'revenue_to_cost_ratio' in df.columns:
            avg_roi = df.groupby('Product_Category')['revenue_to_cost_ratio'].mean().reset_index()
            product_costs = product_costs.merge(avg_roi, left_on='Category', right_on='Product_Category', how='left')
            product_costs = product_costs.drop('Product_Category', axis=1)
            product_costs.columns = list(product_costs.columns[:-1]) + ['Avg ROI']

        if 'Total Revenue' in product_costs.columns:
            product_costs['Profit'] = product_costs['Total Revenue'] - product_costs['Total Cost']
            product_costs['Profit Margin %'] = (product_costs['Profit'] / product_costs['Total Revenue']) * 100

        product_costs = product_costs.sort_values('Total Cost', ascending=False)

        col1, col2 = st.columns(2)

        with col1:
            if 'Total Revenue' in product_costs.columns:
                fig = px.bar(product_costs, x='Category', y=['Total Cost', 'Total Revenue'],
                             title='Cost vs Revenue by Product Category', barmode='group')
                st.plotly_chart(fig, use_container_width=True)
            else:
                fig = px.bar(product_costs, x='Category', y='Total Cost',
                             title='Total Cost by Product Category',
                             color='Total Cost', color_continuous_scale='Blues')
                st.plotly_chart(fig, use_container_width=True)

        with col2:
            if 'Avg ROI' in product_costs.columns and 'Profit' in product_costs.columns:
                fig = px.scatter(product_costs, x='Avg Cost', y='Avg ROI',
                                 size='Orders', hover_data=['Category'],
                                 title='ROI vs Cost by Product Category',
                                 color='Profit', color_continuous_scale='RdYlGn')
                st.plotly_chart(fig, use_container_width=True)
            else:
                fig = px.pie(product_costs, values='Total Cost', names='Category',
                             title='Cost Distribution by Category', hole=0.4)
                st.plotly_chart(fig, use_container_width=True)

        if 'Profit' in product_costs.columns:
            st.markdown("#### Profitability Analysis")
            col1, col2, col3 = st.columns(3)

            with col1:
                most_profitable = product_costs.nlargest(1, 'Profit').iloc[0]
                st.metric("Most Profitable Category", most_profitable['Category'],
                          f"₹{most_profitable['Profit']:,.0f}")

            with col2:
                best_margin = product_costs.nlargest(1, 'Profit Margin %').iloc[0]
                st.metric("Best Profit Margin", best_margin['Category'],
                          f"{best_margin['Profit Margin %']:.1f}%")

            with col3:
                total_profit = product_costs['Profit'].sum()
                st.metric("Total Profit", f"₹{total_profit:,.0f}")

        st.markdown("#### Detailed Product Category Table")
        st.dataframe(product_costs, use_container_width=True)

        csv = product_costs.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Download Product Cost Report",
            data=csv,
            file_name=f"product_cost_analysis_{datetime.now().strftime('%Y%m%d')}.csv",
            mime="text/csv"
        )
    else:
        st.warning("Product category data not available for analysis")


def _show_cost_breakdown(df):
    st.subheader("Detailed Cost Breakdown")
    existing_components = [col for col in COST_COMPONENTS if col in df.columns]

    if existing_components:
        cost_summary = df[existing_components].sum().reset_index()
        cost_summary.columns = ['Component', 'Total']
        cost_summary['Percentage'] = (cost_summary['Total'] / cost_summary['Total'].sum()) * 100
        cost_summary = cost_summary.sort_values('Total', ascending=False)

        col1, col2 = st.columns(2)

        with col1:
            fig = px.pie(cost_summary, values='Total', names='Component',
                         title='Cost Component Distribution', hole=0.4)
            st.plotly_chart(fig, use_container_width=True)

        with col2:
            fig = px.treemap(cost_summary, path=['Component'], values='Total',
                             title='Cost Component Hierarchy',
                             color='Total', color_continuous_scale='Blues')
            st.plotly_chart(fig, use_container_width=True)

        st.markdown("#### Cost Component Summary")
        display_summary = cost_summary.copy()
        display_summary['Total'] = display_summary['Total'].apply(lambda x: f"₹{x:,.0f}")
        display_summary['Percentage'] = display_summary['Percentage'].apply(lambda x: f"{x:.1f}%")
        st.dataframe(display_summary, use_container_width=True)

        if 'Order_Date' in df.columns:
            st.markdown("#### Cost Components Over Time")
            daily_breakdown = df.groupby(df['Order_Date'].dt.date)[existing_components].sum().reset_index()
            daily_breakdown = daily_breakdown.melt(id_vars='Order_Date', var_name='Component', value_name='Cost')

            fig = px.area(daily_breakdown, x='Order_Date', y='Cost', color='Component',
                          title='Cost Components Trend Over Time')
            st.plotly_chart(fig, use_container_width=True)

            st.markdown("#### Monthly Cost Breakdown")
            df_with_month = df.copy()
            df_with_month['Month'] = df_with_month['Order_Date'].dt.to_period('M').astype(str)
            monthly_breakdown = df_with_month.groupby('Month')[existing_components].sum().reset_index()
            monthly_breakdown = monthly_breakdown.melt(id_vars='Month', var_name='Component', value_name='Cost')

            fig = px.bar(monthly_breakdown, x='Month', y='Cost', color='Component',
                         title='Monthly Cost Breakdown', barmode='stack')
            st.plotly_chart(fig, use_container_width=True)

        st.markdown("#### Cost Component Statistics per Order")
        stats_data = []
        for component in existing_components:
            stats_data.append({
                'Component': component.replace('_', ' ').title(),
                'Mean': f"₹{df[component].mean():,.2f}",
                'Median': f"₹{df[component].median():,.2f}",
                'Min': f"₹{df[component].min():,.2f}",
                'Max': f"₹{df[component].max():,.2f}",
                'Std Dev': f"₹{df[component].std():,.2f}"
            })
        stats_df = pd.DataFrame(stats_data)
        st.dataframe(stats_df, use_container_width=True)

        csv = cost_summary.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Download Cost Breakdown Report",
            data=csv,
            file_name=f"cost_breakdown_{datetime.now().strftime('%Y%m%d')}.csv",
            mime="text/csv"
        )
    else:
        st.warning("Cost breakdown data not available")