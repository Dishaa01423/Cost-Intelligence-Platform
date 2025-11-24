PAGE_CONFIG = {
    "page_title": "NexGen Cost Intelligence Platform",
    "page_icon": "📊",
    "layout": "wide",
    "initial_sidebar_state": "expanded"
}

COST_COMPONENTS = [
    'Fuel_Cost',
    'Labor_Cost',
    'Vehicle_Maintenance',
    'Insurance',
    'Packaging_Cost',
    'Technology_Platform_Fee',
    'Other_Overhead'
]

FEATURE_COLS = [
    'Distance_KM',
    'Fuel_Consumption_L',
    'Traffic_Delay_Minutes',
    'Capacity_KG',
    'Age_Years'
]

CLUSTER_FEATURES = ['total_cost', 'Distance_KM', 'cost_per_km']

DATE_FORMATS = [
    '%d %m %y',
    '%d/%m/%y',
    '%d-%m-%y',
    '%d/%m/%Y',
    '%d-%m-%Y',
    '%Y-%m-%d',
    '%d %m %Y',
    '%m/%d/%y',
    '%m/%d/%Y',
]

ANOMALY_CONTAMINATION = 0.1
ANOMALY_RANDOM_STATE = 42

ML_RANDOM_STATE = 42
ML_N_ESTIMATORS = 100
ML_MAX_DEPTH = 10
ML_TEST_SIZE = 0.2

N_CLUSTERS = 3
CLUSTER_RANDOM_STATE = 42