import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime


def show_what_if_scenarios(df):
    st.header("📈 What-If Scenario Analysis")
    st.markdown("**Model the impact of strategic decisions on costs**")

    # Current baseline
    _show_baseline_metrics(df)

    st.markdown("---")
    st.subheader("🎯 Scenario Builder")

    tab1, tab2, tab3, tab4 = st.tabs(
        ["⛽ Fuel Price Change", "📦 Priority Mix", "🚗 Fleet Optimization", "🗺️ Route Efficiency"])

    with tab1:
        _show_fuel_scenario(df)

    with tab2:
        _show_priority_scenario(df)

    with tab3:
        _show_fleet_scenario(df)

    with tab4:
        _show_route_scenario(df)

    # Combined impact
    _show_combined_impact(df)


def _show_baseline_metrics(df):
    st.subheader("📊 Current Baseline Metrics")

    current_total_cost = df['total_cost'].sum() if 'total_cost' in df.columns else 0
    current_avg_cost = df['total_cost'].mean() if 'total_cost' in df.columns else 0
    current_fuel_cost = df['Fuel_Cost'].sum() if 'Fuel_Cost' in df.columns else 0
    current_labor_cost = df['Labor_Cost'].sum() if 'Labor_Cost' in df.columns else 0

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Cost", f"₹{current_total_cost:,.0f}")
    with col2:
        st.metric("Avg Cost/Order", f"₹{current_avg_cost:,.0f}")
    with col3:
        st.metric("Fuel Costs", f"₹{current_fuel_cost:,.0f}")
    with col4:
        st.metric("Labor Costs", f"₹{current_labor_cost:,.0f}")


def _show_fuel_scenario(df):
    st.markdown("### ⛽ Fuel Price Impact Analysis")

    current_fuel_cost = df['Fuel_Cost'].sum() if 'Fuel_Cost' in df.columns else 0
    current_total_cost = df['total_cost'].sum() if 'total_cost' in df.columns else 0

    if current_fuel_cost > 0:
        fuel_change = st.slider("Fuel Price Change (%)", -30, 50, 0, 5)

        new_fuel_cost = current_fuel_cost * (1 + fuel_change / 100)
        fuel_diff = new_fuel_cost - current_fuel_cost
        new_total = current_total_cost + fuel_diff

        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("New Fuel Cost", f"₹{new_fuel_cost:,.0f}", delta=f"₹{fuel_diff:,.0f}")
        with col2:
            st.metric("New Total Cost", f"₹{new_total:,.0f}",
                      delta=f"{(fuel_diff / current_total_cost) * 100:.1f}%")
        with col3:
            impact_pct = (fuel_diff / current_total_cost) * 100
            st.metric("Overall Impact", f"{impact_pct:.2f}%")

        scenario_data = pd.DataFrame({
            'Scenario': ['Current', 'Projected'],
            'Fuel Cost': [current_fuel_cost, new_fuel_cost],
            'Other Costs': [current_total_cost - current_fuel_cost, current_total_cost - current_fuel_cost],
            'Total': [current_total_cost, new_total]
        })

        fig = px.bar(scenario_data, x='Scenario', y=['Fuel Cost', 'Other Costs'],
                     title='Cost Comparison: Current vs Fuel Price Change',
                     barmode='stack')
        st.plotly_chart(fig, use_container_width=True)

        if fuel_change > 0:
            st.markdown(f"""
            <div class="alert-box">
            <strong>⚠️ Risk Alert:</strong> A {fuel_change}% increase in fuel prices would add 
            ₹{fuel_diff:,.0f} to annual costs. Consider:
            <ul>
            <li>Locking in fuel contracts</li>
            <li>Investing in fuel-efficient vehicles</li>
            <li>Route optimization to reduce fuel consumption</li>
            </ul>
            </div>
            """, unsafe_allow_html=True)
        elif fuel_change < 0:
            st.markdown(f"""
            <div class="success-box">
            <strong>💰 Savings Opportunity:</strong> A {abs(fuel_change)}% decrease in fuel prices would save 
            ₹{abs(fuel_diff):,.0f} annually.
            </div>
            """, unsafe_allow_html=True)
    else:
        st.warning("Fuel cost data not available")


def _show_priority_scenario(df):
    st.markdown("### 📦 Priority Mix Optimization")

    if 'Priority' in df.columns and 'total_cost' in df.columns:
        current_mix = df['Priority'].value_counts(normalize=True) * 100

        st.markdown("**Current Priority Mix:**")
        for priority, pct in current_mix.items():
            st.write(f"- {priority}: {pct:.1f}%")

        st.markdown("---")
        st.markdown("**Adjust Priority Mix:**")

        new_mix = {}
        for priority in sorted(df['Priority'].unique()):
            new_mix[priority] = st.slider(f"{priority} (%)", 0, 100, int(current_mix.get(priority, 0)))

        total_pct = sum(new_mix.values())
        if total_pct != 100:
            st.warning(f"⚠️ Total percentage is {total_pct}%. Please adjust to 100%.")

        priority_costs = df.groupby('Priority')['total_cost'].mean().to_dict()

        current_weighted_cost = sum([current_mix.get(p, 0) / 100 * priority_costs.get(p, 0)
                                     for p in priority_costs.keys()])
        new_weighted_cost = sum([new_mix.get(p, 0) / 100 * priority_costs.get(p, 0)
                                 for p in priority_costs.keys()])

        total_orders = len(df)
        current_scenario_cost = current_weighted_cost * total_orders
        new_scenario_cost = new_weighted_cost * total_orders
        cost_diff = new_scenario_cost - current_scenario_cost

        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Current Mix Cost", f"₹{current_scenario_cost:,.0f}")
        with col2:
            st.metric("New Mix Cost", f"₹{new_scenario_cost:,.0f}", delta=f"₹{cost_diff:,.0f}")
        with col3:
            pct_change = (cost_diff / current_scenario_cost) * 100 if current_scenario_cost > 0 else 0
            st.metric("Cost Change", f"{pct_change:.1f}%")

        comparison_df = pd.DataFrame({
            'Priority': list(current_mix.keys()) * 2,
            'Percentage': list(current_mix.values) + [new_mix.get(p, 0) for p in current_mix.keys()],
            'Scenario': ['Current'] * len(current_mix) + ['Proposed'] * len(current_mix)
        })

        fig = px.bar(comparison_df, x='Priority', y='Percentage', color='Scenario',
                     title='Priority Mix: Current vs Proposed', barmode='group')
        st.plotly_chart(fig, use_container_width=True)

        if cost_diff < 0:
            st.markdown(f"""
            <div class="success-box">
            <strong>💰 Cost Savings:</strong> This priority mix would save ₹{abs(cost_diff):,.0f} 
            ({abs(pct_change):.1f}%) annually.
            </div>
            """, unsafe_allow_html=True)
        elif cost_diff > 0:
            st.markdown(f"""
            <div class="alert-box">
            <strong>⚠️ Cost Increase:</strong> This priority mix would increase costs by ₹{cost_diff:,.0f} 
            ({pct_change:.1f}%) annually.
            </div>
            """, unsafe_allow_html=True)
    else:
        st.warning("Priority data not available")


def _show_fleet_scenario(df):
    st.markdown("### 🚗 Fleet Optimization Scenario")

    current_fuel_cost = df['Fuel_Cost'].sum() if 'Fuel_Cost' in df.columns else 0
    current_labor_cost = df['Labor_Cost'].sum() if 'Labor_Cost' in df.columns else 0

    if 'Vehicle_Maintenance' in df.columns and 'Insurance' in df.columns:
        fleet_reduction = st.slider("Reduce Fleet by (%)", 0, 30, 10)
        efficiency_gain = st.slider("Improve Efficiency by (%)", 0, 25, 10)

        fixed_costs = df['Vehicle_Maintenance'].sum() + df['Insurance'].sum()
        variable_costs = current_fuel_cost + current_labor_cost

        new_fixed = fixed_costs * (1 - fleet_reduction / 100)
        new_variable = variable_costs * (1 - efficiency_gain / 100)
        new_total_fleet = new_fixed + new_variable

        current_fleet_costs = fixed_costs + variable_costs
        savings = current_fleet_costs - new_total_fleet

        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Current Fleet Costs", f"₹{current_fleet_costs:,.0f}")
        with col2:
            st.metric("Optimized Fleet Costs", f"₹{new_total_fleet:,.0f}", delta=f"-₹{savings:,.0f}")
        with col3:
            savings_pct = (savings / current_fleet_costs) * 100 if current_fleet_costs > 0 else 0
            st.metric("Cost Reduction", f"{savings_pct:.1f}%")

        breakdown_df = pd.DataFrame({
            'Scenario': ['Current', 'Current', 'Optimized', 'Optimized'],
            'Category': ['Fixed Costs', 'Variable Costs', 'Fixed Costs', 'Variable Costs'],
            'Amount': [fixed_costs, variable_costs, new_fixed, new_variable]
        })

        fig = px.bar(breakdown_df, x='Scenario', y='Amount', color='Category',
                     title='Fleet Costs: Current vs Optimized', barmode='stack')
        st.plotly_chart(fig, use_container_width=True)

        st.markdown(f"""
        <div class="success-box">
        <h4>🎯 Fleet Optimization Recommendations</h4>
        <p><strong>Potential Annual Savings: ₹{savings:,.0f}</strong></p>
        <ul>
        <li>Right-size fleet by retiring {fleet_reduction}% of underutilized vehicles</li>
        <li>Implement predictive maintenance to improve efficiency by {efficiency_gain}%</li>
        <li>Use route optimization software</li>
        <li>Consider vehicle replacement with more efficient models</li>
        </ul>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.warning("Fleet cost data not available")


def _show_route_scenario(df):
    st.markdown("### 🗺️ Route Efficiency Scenario")

    current_fuel_cost = df['Fuel_Cost'].sum() if 'Fuel_Cost' in df.columns else 0
    current_labor_cost = df['Labor_Cost'].sum() if 'Labor_Cost' in df.columns else 0

    if current_fuel_cost > 0 and current_labor_cost > 0:
        distance_reduction = st.slider("Reduce Average Distance by (%)", 0, 25, 10)
        time_reduction = st.slider("Reduce Traffic Delays by (%)", 0, 40, 15)

        toll_charges = df['Toll_Charges_INR'].sum() if 'Toll_Charges_INR' in df.columns else 0
        current_distance_costs = current_fuel_cost + toll_charges
        current_time_costs = current_labor_cost

        new_distance_costs = current_distance_costs * (1 - distance_reduction / 100)
        new_time_costs = current_time_costs * (1 - time_reduction / 100)

        total_route_savings = (current_distance_costs - new_distance_costs) + (current_time_costs - new_time_costs)

        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Current Route Costs", f"₹{current_distance_costs + current_time_costs:,.0f}")
        with col2:
            st.metric("Optimized Route Costs", f"₹{new_distance_costs + new_time_costs:,.0f}",
                      delta=f"-₹{total_route_savings:,.0f}")
        with col3:
            route_savings_pct = (total_route_savings / (current_distance_costs + current_time_costs)) * 100
            st.metric("Cost Reduction", f"{route_savings_pct:.1f}%")

        route_comparison = pd.DataFrame({
            'Metric': ['Distance Costs', 'Time Costs', 'Distance Costs', 'Time Costs'],
            'Scenario': ['Current', 'Current', 'Optimized', 'Optimized'],
            'Amount': [current_distance_costs, current_time_costs, new_distance_costs, new_time_costs]
        })

        fig = px.bar(route_comparison, x='Scenario', y='Amount', color='Metric',
                     title='Route Costs: Current vs Optimized', barmode='group')
        st.plotly_chart(fig, use_container_width=True)

        st.markdown(f"""
        <div class="success-box">
        <h4>🎯 Route Optimization Recommendations</h4>
        <p><strong>Potential Annual Savings: ₹{total_route_savings:,.0f}</strong></p>
        <ul>
        <li>Implement AI-powered route optimization software</li>
        <li>Use real-time traffic data for dynamic routing</li>
        <li>Consolidate deliveries in same geographic areas</li>
        <li>Schedule deliveries to avoid peak traffic hours</li>
        </ul>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.warning("Route cost data not available")


def _show_combined_impact(df):
    st.markdown("---")
    st.subheader("🎯 Combined Impact Analysis")
    st.markdown("**If all optimizations were implemented simultaneously:**")

    current_total_cost = df['total_cost'].sum() if 'total_cost' in df.columns else 0
    current_fuel_cost = df['Fuel_Cost'].sum() if 'Fuel_Cost' in df.columns else 0
    current_labor_cost = df['Labor_Cost'].sum() if 'Labor_Cost' in df.columns else 0

    if current_total_cost > 0:
        fuel_saving = current_fuel_cost * 0.10
        fleet_saving = (df['Vehicle_Maintenance'].sum() if 'Vehicle_Maintenance' in df.columns else 0) * 0.12
        route_saving = (current_fuel_cost + current_labor_cost) * 0.15
        priority_saving = current_total_cost * 0.08

        total_combined_savings = (fuel_saving + fleet_saving + route_saving + priority_saving) * 0.85
        final_cost = current_total_cost - total_combined_savings
        reduction_pct = (total_combined_savings / current_total_cost) * 100

        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Current Total Cost", f"₹{current_total_cost:,.0f}")
        with col2:
            st.metric("Projected Total Cost", f"₹{final_cost:,.0f}")
        with col3:
            st.metric("Total Savings", f"₹{total_combined_savings:,.0f}", delta=f"-{reduction_pct:.1f}%")
        with col4:
            if reduction_pct >= 15:
                st.metric("Goal Achievement", "✅ Target Met!", delta=f"{reduction_pct:.1f}% vs 15-20% goal")
            else:
                st.metric("Goal Progress", f"{reduction_pct:.1f}%", delta=f"{reduction_pct - 15:.1f}% vs 15% goal")

        waterfall_data = {
            'Category': ['Current Cost', 'Fuel Optimization', 'Fleet Optimization',
                         'Route Optimization', 'Priority Mix', 'Final Cost'],
            'Value': [current_total_cost, -fuel_saving, -fleet_saving, -route_saving,
                      -priority_saving, final_cost]
        }
        waterfall_df = pd.DataFrame(waterfall_data)

        fig = go.Figure(go.Waterfall(
            x=waterfall_df['Category'],
            y=waterfall_df['Value'],
            measure=['absolute', 'relative', 'relative', 'relative', 'relative', 'total'],
            text=[f"₹{abs(v):,.0f}" for v in waterfall_df['Value']],
            textposition="outside",
            connector={"line": {"color": "rgb(63, 63, 63)"}},
            decreasing={"marker": {"color": "#27ae60"}},
            increasing={"marker": {"color": "#e74c3c"}},
            totals={"marker": {"color": "#3498db"}}
        ))

        fig.update_layout(title="Cumulative Cost Reduction Waterfall", showlegend=False, height=500)
        st.plotly_chart(fig, use_container_width=True)

        if reduction_pct >= 15:
            st.markdown(f"""
            <div class="success-box">
            <h3>🎉 Congratulations! Target Achievable!</h3>
            <p>The combined optimization strategies can achieve <strong>{reduction_pct:.1f}% cost reduction</strong>, 
            exceeding the 15-20% target.</p>
            <p><strong>Total Annual Savings: ₹{total_combined_savings:,.0f}</strong></p>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="insight-box">
            <h3>📊 Progress Toward Goal</h3>
            <p>Current scenarios achieve <strong>{reduction_pct:.1f}% cost reduction</strong>.</p>
            <p>Additional {15 - reduction_pct:.1f}% needed to reach minimum 15% target.</p>
            </div>
            """, unsafe_allow_html=True)

        scenario_summary = pd.DataFrame({
            'Optimization Area': ['Fuel Efficiency', 'Fleet Management', 'Route Optimization', 'Priority Mix'],
            'Potential Savings': [fuel_saving, fleet_saving, route_saving, priority_saving],
            'Savings %': [
                (fuel_saving / current_total_cost) * 100,
                (fleet_saving / current_total_cost) * 100,
                (route_saving / current_total_cost) * 100,
                (priority_saving / current_total_cost) * 100
            ]
        })

        csv = scenario_summary.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Download Scenario Analysis Report",
            data=csv,
            file_name=f"what_if_analysis_{datetime.now().strftime('%Y%m%d')}.csv",
            mime="text/csv"
        )
    else:
        st.warning("Insufficient cost data for combined impact analysis")