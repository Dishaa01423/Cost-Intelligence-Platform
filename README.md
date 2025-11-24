# 🚚 NexGen Cost Intelligence Platform

## Overview

The NexGen Cost Intelligence Platform is a comprehensive, interactive web application built with Python and Streamlit that enables data-driven cost optimization for logistics operations. This platform empowers NexGen Logistics to achieve their ambitious 15-20% cost reduction goal through advanced analytics, machine learning, and actionable insights.

## Key Features

### 📊 Executive Dashboard
- Real-time cost overview and KPI tracking
- Interactive cost trend analysis
- Priority-level cost distribution
- Key insights and recommendations
- Downloadable reports

### 💰 Detailed Cost Analysis
- **Vehicle Analysis**: Cost performance by vehicle fleet
- **Route Analysis**: Efficiency metrics by delivery routes
- **Product Analysis**: Cost and ROI by product categories
- **Cost Breakdown**: Granular view of all cost components

### 🚨 Anomaly Detection
- Machine learning-powered anomaly identification
- Automatic flagging of unusual cost patterns
- Detailed anomaly investigation and root cause analysis
- Potential savings calculations

### 🤖 Predictive Analytics
- Random Forest model for cost prediction
- Interactive cost prediction simulator
- Feature importance analysis
- Cost clustering and pattern recognition

### 💡 Optimization Opportunities
- Identifies 5+ optimization areas
- Quantifies potential savings for each opportunity
- Actionable recommendations with implementation steps
- Prioritized action plans

### 📈 What-If Scenario Analysis
- Fuel price impact modeling
- Priority mix optimization
- Fleet size and efficiency scenarios
- Route optimization simulations
- Combined impact analysis with implementation roadmap

## Installation & Setup

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Step 1: Clone or Download
```bash
# If using git
git clone <repository-url>
cd Cost-Intelligence-Platform

# Or simply download and extract the files
```

### Step 2: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 3: Prepare Data Files
Ensure all CSV files are in the data folder which is in the same directory as `main.py`:
- `orders.csv`
- `delivery_performance.csv`
- `cost_breakdown.csv`
- `routes_distance.csv`
- `vehicle_fleet.csv`
- `warehouse_inventory.csv`
- `customer_feedback.csv`

### Step 4: Run the Application
```bash
streamlit run main.py
```

The application will automatically open in your default web browser at `http://localhost:8501`

## Usage Guide

### Navigation
Use the sidebar to:
1. **Filter data** by date range, priority, vehicle type, and product category
2. **Navigate** between different pages using the radio buttons

### Interactive Features

#### Filters
- **Date Range**: Select specific time periods for analysis
- **Priority Levels**: Filter by Express, Standard, or Economy
- **Vehicle Types**: Focus on specific vehicle categories
- **Product Categories**: Analyze specific product segments

#### Visualizations
- Hover over charts for detailed information
- Click on legend items to show/hide data series
- Use zoom and pan controls on plots
- Download charts as PNG images

#### Data Export
- Download filtered data as CSV from any page
- Export specific reports (anomaly reports, optimization opportunities, etc.)
- Save scenario analysis results

### Page-by-Page Guide

#### 📊 Executive Dashboard
Start here for a high-level overview. Key metrics display total costs, averages, and efficiency ratios. Review top insights for immediate action items.

#### 💰 Cost Analysis
Deep-dive into costs across four dimensions:
- **By Vehicle**: Identify underperforming vehicles
- **By Route**: Find inefficient routes
- **By Product**: Understand product profitability
- **Cost Breakdown**: See detailed component costs

#### 🚨 Anomaly Detection
Automatically identifies unusual cost patterns. Review flagged orders and investigate root causes. Focus on high-impact anomalies first.

#### 🤖 Predictive Analytics
Use the cost prediction simulator to estimate costs for future orders. Review feature importance to understand key cost drivers. Examine cost clusters to identify patterns.

#### 💡 Optimization Opportunities
This is where ROI is quantified. Each opportunity includes:
- Clear description of the issue
- Quantified potential savings
- Specific recommended actions
- Implementation difficulty assessment

#### 📈 What-If Scenarios
Model different strategic decisions:
1. Adjust sliders to set scenario parameters
2. Review impact metrics and visualizations
3. Compare scenarios side-by-side
4. Export scenario results for stakeholder presentations

## Technical Architecture

### Data Processing
- **Pandas**: Data manipulation and analysis
- **NumPy**: Numerical computations
- **Caching**: @st.cache_data decorators for performance

### Machine Learning
- **Isolation Forest**: Anomaly detection
- **Random Forest Regressor**: Cost prediction
- **K-Means**: Cost clustering
- **StandardScaler**: Feature normalization

### Visualization
- **Plotly Express**: Interactive charts
- **Plotly Graph Objects**: Custom visualizations
- Responsive design for all screen sizes

### Web Framework
- **Streamlit**: Interactive web application
- Real-time data filtering and updates
- Session state management

## Key Insights Generated

The platform automatically surfaces insights such as:
- "Express deliveries cost 3.5x more than Economy but only represent 15% of revenue"
- "Vehicle V-042 has maintenance costs 2x fleet average - consider replacement"
- "Route Mumbai→Delhi has 40% higher fuel consumption - investigate optimization"
- "Potential savings of ₹2.5M through combined optimization strategies"

## Business Impact

### Quantified Benefits
- **15-20% cost reduction** achievable through identified opportunities
- **₹2-3M annual savings** potential (based on sample data)
- **Improved operational efficiency** through data-driven decisions
- **Proactive cost management** via anomaly detection
- **Predictive planning** using ML models

### ROI Timeline
- **Month 1-2**: Quick wins (route optimization, inefficiency identification)
- **Month 3-4**: Fleet optimization and training programs
- **Month 5-6**: Strategic changes (priority mix, advanced analytics)
