"""
Streamlit Demo — Plots & Graphs
================================
Run with:  streamlit run main.py

This file demonstrates several core Streamlit concepts:
  1. Page config & layout
  2. Sidebar widgets (sliders, selectbox, checkbox)
  3. Built-in charts (st.line_chart, st.area_chart, st.bar_chart)
  4. Matplotlib integration (st.pyplot)
  5. Plotly integration (st.plotly_chart)
  6. Metrics & columns
  7. Data display (st.dataframe)
"""

import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go

# ──────────────────────────────────────────────
# 1. PAGE CONFIG
# ──────────────────────────────────────────────
st.set_page_config(
    page_title="Streamlit Charts Demo",
    page_icon="📊",
    layout="wide",
)

# ──────────────────────────────────────────────
# 2. SIDEBAR — interactive controls
# ──────────────────────────────────────────────
st.sidebar.title("⚙️ Controls")
num_points = st.sidebar.slider("Number of data points", 50, 500, 200, step=50)
chart_theme = st.sidebar.selectbox("Plotly colour theme", ["plotly", "plotly_dark", "ggplot2", "seaborn"])
show_raw_data = st.sidebar.checkbox("Show raw data table", value=False)

# ──────────────────────────────────────────────
# 3. GENERATE SAMPLE DATA
# ──────────────────────────────────────────────
np.random.seed(42)
dates = pd.date_range(start="2025-01-01", periods=num_points, freq="D")
df = pd.DataFrame({
    "Date": dates,
    "Revenue": np.cumsum(np.random.randn(num_points) * 10 + 5),
    "Expenses": np.cumsum(np.random.randn(num_points) * 8 + 3),
    "Profit": np.cumsum(np.random.randn(num_points) * 6 + 2),
}).set_index("Date")

# ──────────────────────────────────────────────
# 4. HEADER & METRICS
# ──────────────────────────────────────────────
st.title("📊 Streamlit Charts & Graphs Demo")
st.markdown("A quick tour of **plots, charts, and interactive widgets** in Streamlit.")

col1, col2, col3 = st.columns(3)
col1.metric("Total Revenue", f"${df['Revenue'].iloc[-1]:,.0f}", f"{df['Revenue'].diff().iloc[-1]:+,.0f}")
col2.metric("Total Expenses", f"${df['Expenses'].iloc[-1]:,.0f}", f"{df['Expenses'].diff().iloc[-1]:+,.0f}")
col3.metric("Total Profit", f"${df['Profit'].iloc[-1]:,.0f}", f"{df['Profit'].diff().iloc[-1]:+,.0f}")

st.divider()

# ──────────────────────────────────────────────
# 5. BUILT-IN STREAMLIT CHARTS
# ──────────────────────────────────────────────
st.header("1 · Built-in Streamlit Charts")

tab1, tab2, tab3 = st.tabs(["📈 Line Chart", "📊 Bar Chart", "🏔️ Area Chart"])

with tab1:
    st.subheader("Line Chart — st.line_chart")
    st.line_chart(df)

with tab2:
    st.subheader("Bar Chart — st.bar_chart")
    st.bar_chart(df.tail(30))  # last 30 days for readability

with tab3:
    st.subheader("Area Chart — st.area_chart")
    st.area_chart(df)

st.divider()

# ──────────────────────────────────────────────
# 6. MATPLOTLIB CHART (st.pyplot)
# ──────────────────────────────────────────────
st.header("2 · Matplotlib Chart")

fig, axes = plt.subplots(1, 2, figsize=(14, 5))

# Subplot 1 — histogram
axes[0].hist(df["Revenue"].diff().dropna(), bins=30, color="#6C63FF", edgecolor="white", alpha=0.85)
axes[0].set_title("Daily Revenue Change — Histogram")
axes[0].set_xlabel("Change ($)")
axes[0].set_ylabel("Frequency")

# Subplot 2 — scatter
colors = df["Profit"].diff().dropna()
scatter = axes[1].scatter(
    df["Revenue"].diff().dropna(),
    df["Expenses"].diff().dropna(),
    c=colors,
    cmap="coolwarm",
    alpha=0.7,
    edgecolors="white",
    linewidths=0.5,
)
axes[1].set_title("Revenue Δ vs Expenses Δ — Scatter")
axes[1].set_xlabel("Revenue Change ($)")
axes[1].set_ylabel("Expenses Change ($)")
fig.colorbar(scatter, ax=axes[1], label="Profit Change")

fig.tight_layout()
st.pyplot(fig)

st.divider()

# ──────────────────────────────────────────────
# 7. PLOTLY INTERACTIVE CHARTS
# ──────────────────────────────────────────────
st.header("3 · Plotly Interactive Charts")

left, right = st.columns(2)

with left:
    st.subheader("Stacked Area")
    fig_area = px.area(
        df.reset_index(),
        x="Date",
        y=["Revenue", "Expenses", "Profit"],
        template=chart_theme,
        title="Cumulative Trends",
    )
    fig_area.update_layout(height=400)
    st.plotly_chart(fig_area, use_container_width=True)

with right:
    st.subheader("Pie Chart — Latest Proportions")
    latest = df.iloc[-1].abs()
    fig_pie = px.pie(
        names=latest.index,
        values=latest.values,
        template=chart_theme,
        title="Revenue / Expenses / Profit Split",
        hole=0.4,  # donut style
    )
    fig_pie.update_layout(height=400)
    st.plotly_chart(fig_pie, use_container_width=True)

# Plotly GO — candlestick-style range chart
st.subheader("Range Chart (Plotly Graph Objects)")
fig_go = go.Figure()
fig_go.add_trace(go.Scatter(
    x=df.index, y=df["Revenue"],
    mode="lines", name="Revenue",
    line=dict(color="#6C63FF", width=2),
))
fig_go.add_trace(go.Scatter(
    x=df.index, y=df["Expenses"],
    mode="lines", name="Expenses",
    line=dict(color="#FF6584", width=2),
    fill="tonexty", fillcolor="rgba(255,101,132,0.15)",
))
fig_go.update_layout(
    template=chart_theme,
    title="Revenue vs Expenses — Filled Range",
    xaxis_title="Date",
    yaxis_title="Cumulative ($)",
    height=420,
)
st.plotly_chart(fig_go, use_container_width=True)

st.divider()

# ──────────────────────────────────────────────
# 8. OPTIONAL RAW DATA TABLE
# ──────────────────────────────────────────────
if show_raw_data:
    st.header("4 · Raw Data")
    st.dataframe(df.style.format("${:,.2f}"), use_container_width=True)

# ──────────────────────────────────────────────
# FOOTER
# ──────────────────────────────────────────────
st.markdown("---")
st.caption("Built with ❤️ using Streamlit · Data is randomly generated for demo purposes.")
