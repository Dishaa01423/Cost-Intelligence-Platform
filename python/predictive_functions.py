import streamlit as st
from ml_models import train_cost_prediction_model


def show_predictive_analytics(df):
    st.header("🤖 Predictive Analytics")
    with st.spinner("Training predictive model..."):
        model, feature_cols, metrics = train_cost_prediction_model(df)

    if model is None:
        st.warning("Insufficient data to train predictive model")
        return

    st.metric("Model R² Score", f"{metrics['r2']:.3f}")