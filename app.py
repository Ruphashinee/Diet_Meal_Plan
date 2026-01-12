import streamlit as st
import pandas as pd
from data_loader import get_clean_data
from ep_algorithm import EP_Optimizer

st.set_page_config(page_title="Diet Optimizer (EP)", layout="wide")

# Sidebar
st.sidebar.header("🎯 Health Targets")
t_cal = st.sidebar.slider("Target Calories", 1200, 3000, 2000)
t_prot = st.sidebar.slider("Min Protein (g)", 20, 150, 80)
t_fat = st.sidebar.slider("Max Fat (g)", 20, 100, 70)

# Load Data
df = get_clean_data()

if st.sidebar.button("Run Optimization"):
    optimizer = EP_Optimizer(df, t_cal, t_prot, t_fat)
    best_idx, history = optimizer.run()
    best_row = df.iloc[int(best_idx)]

    st.success("✅ Optimization Results")
    
    # Summary Metrics
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Cost", f"RM {best_row['Price_RM']:.2f}")
    col2.metric("Total Calories", f"{best_row['Calories']} kcal")
    col3.metric("Total Protein", f"{best_row['Protein']}g")

    st.subheader("🥗 Selected Daily Meal Plan")
    # Show the full row in a table format like the PSO app
    st.table(df.iloc[[int(best_idx)]])

    st.subheader("📈 Convergence Analysis")
    st.line_chart(history)
