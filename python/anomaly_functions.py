import streamlit as st
from ml_models import detect_cost_anomalies


def show_anomaly_detection(df):
    st.header("🚨 Anomaly Detection")
    if 'total_cost' not in df.columns:
        st.warning("Required data for anomaly detection not available")
        return

    with st.spinner("Detecting anomalies..."):
        df['is_anomaly'] = detect_cost_anomalies(df)

    anomaly_count = df['is_anomaly'].sum()
    st.metric("Anomalies Detected", anomaly_count)