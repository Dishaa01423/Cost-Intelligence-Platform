import streamlit as st
import pandas as pd
from sklearn.ensemble import RandomForestRegressor, IsolationForest
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, r2_score
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from config import (FEATURE_COLS, CLUSTER_FEATURES, ANOMALY_CONTAMINATION,
                    ANOMALY_RANDOM_STATE, ML_RANDOM_STATE, ML_N_ESTIMATORS,
                    ML_MAX_DEPTH, ML_TEST_SIZE, N_CLUSTERS, CLUSTER_RANDOM_STATE)


@st.cache_data
def detect_cost_anomalies(df):
    required_cols = ['total_cost', 'Distance_KM', 'Fuel_Consumption_L']
    available_cols = [col for col in required_cols if col in df.columns]

    if len(available_cols) < 2:
        return pd.Series([False] * len(df))

    cost_features = df[available_cols].dropna()
    if len(cost_features) < 10:
        return pd.Series([False] * len(df))

    iso_forest = IsolationForest(
        contamination=ANOMALY_CONTAMINATION,
        random_state=ANOMALY_RANDOM_STATE
    )
    anomalies = iso_forest.fit_predict(cost_features)
    result = pd.Series([False] * len(df))
    result.iloc[cost_features.index] = anomalies == -1
    return result


@st.cache_data
def train_cost_prediction_model(df):
    available_features = [col for col in FEATURE_COLS if col in df.columns]

    if len(available_features) < 2 or 'total_cost' not in df.columns:
        return None, None, {}

    model_df = df[available_features + ['total_cost']].dropna()
    if len(model_df) < 20:
        return None, None, {}

    X = model_df[available_features]
    y = model_df['total_cost']

    if 'Priority' in df.columns:
        priority_dummies = pd.get_dummies(df.loc[model_df.index, 'Priority'], prefix='priority')
        X = pd.concat([X, priority_dummies], axis=1)

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=ML_TEST_SIZE, random_state=ML_RANDOM_STATE
    )

    model = RandomForestRegressor(
        n_estimators=ML_N_ESTIMATORS,
        random_state=ML_RANDOM_STATE,
        max_depth=ML_MAX_DEPTH
    )
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)
    metrics = {
        'mae': mean_absolute_error(y_test, y_pred),
        'r2': r2_score(y_test, y_pred),
        'feature_importance': dict(zip(X.columns, model.feature_importances_))
    }
    return model, X.columns, metrics


@st.cache_data
def perform_cost_clustering(df, n_clusters=N_CLUSTERS):
    available_cols = [col for col in CLUSTER_FEATURES if col in df.columns]

    if len(available_cols) < 2:
        return None, None

    cluster_df = df[available_cols].dropna()
    if len(cluster_df) < n_clusters:
        return None, None

    scaler = StandardScaler()
    scaled_features = scaler.fit_transform(cluster_df)
    kmeans = KMeans(n_clusters=n_clusters, random_state=CLUSTER_RANDOM_STATE)
    clusters = kmeans.fit_predict(scaled_features)

    cluster_series = pd.Series([pd.NA] * len(df))
    cluster_series.iloc[cluster_df.index] = clusters
    return cluster_series, kmeans