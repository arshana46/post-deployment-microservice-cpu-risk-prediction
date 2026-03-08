# ============================================================
# Streamlit Dashboard: Post-Deployment Microservice Risk Monitoring
# ============================================================

import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

# ---------------------------
# 1️⃣ Page config
# ---------------------------
st.set_page_config(
    page_title="Post-Deployment Microservice Risk Dashboard",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------------------------
# 2️⃣ Load data
# ---------------------------
df = pd.read_csv("post_deploy_predictions_final.csv")
df['datetime'] = pd.to_datetime(df['datetime'])

# ---------------------------
# 3️⃣ Sidebar: Microservice filter
# ---------------------------
st.sidebar.header("🔍 Filter Microservice")
microservice_list = df['microservice'].unique()
selected_service = st.sidebar.selectbox("Select Microservice", microservice_list)

# Filter data for selected microservice
service_df = df[df['microservice'] == selected_service].copy()

# ---------------------------
# 4️⃣ Header & Description
# ---------------------------
st.title("🚀 Post-Deployment Microservice Risk Monitoring")
st.markdown(
    """
This dashboard provides early warning signals after a microservice deployment.
It helps identify whether a service is stable, degrading, or at risk of failure,
and estimates how soon an issue may occur.
"""
)
st.subheader(f"🧩 Microservice: {selected_service}")

# ---------------------------
# 5️⃣ KPI Cards
# ---------------------------
max_risk = service_df['risk_score_percent'].max()
current_risk = service_df['risk_score_percent'].mean()

# Estimated hours to failure (first positive)
if service_df['estimated_hours_to_failure'].notna().any():
    est_failure_hours = service_df['estimated_hours_to_failure'].min()
else:
    est_failure_hours = 0.0

# Display KPI cards
col1, col2, col3 = st.columns(3)
col1.metric("Max Risk Probability (%)", f"{max_risk:.2f} %")
col2.metric("Average Risk Probability (%)", f"{current_risk:.2f} %")
col3.metric("Estimated Time to Failure", f"{est_failure_hours:.2f} hrs")

# ---------------------------
# 6️⃣ Final Post-Deployment Assessment
# ---------------------------
st.subheader("🧠 Final Post-Deployment Assessment")

if current_risk < 30:
    assessment = "✅ Service is stable with no immediate risk indicators."
    suggestion = "Continue routine monitoring."
    color = "#d4edda"  # light green
elif current_risk < 60:
    assessment = "⚠️ Service shows warning signs, monitor closely."
    suggestion = "Investigate occasional CPU spikes and monitor logs."
    color = "#fff3cd"  # light yellow
else:
    assessment = "🚨 Service at high risk, immediate attention required!"
    suggestion = "Investigate CPU spikes, related microservices, and deployment logs."
    color = "#f8d7da"  # light red

st.markdown(
    f'<div style="background-color: {color}; padding: 15px; border-radius: 10px;">'
    f'<b>Assessment:</b> {assessment}<br>'
    f'<b>Suggestion:</b> {suggestion}'
    f'</div>', 
    unsafe_allow_html=True
)

# ---------------------------
# 7️⃣ Post-Deployment Behavior Analysis
# ---------------------------
st.subheader("📊 Post-Deployment Behavior Analysis")

def plot_line_chart(x, y, y_label, color="blue", threshold=None, threshold_label=None):
    fig, ax = plt.subplots(figsize=(10,3))
    ax.plot(x, y, color=color, linewidth=2)  # no points
    if threshold is not None:
        ax.axhline(threshold, color='orange', linestyle='--', linewidth=2, label=threshold_label)
        ax.legend()
    ax.set_ylabel(y_label)
    ax.set_xlabel("Datetime")
    ax.set_facecolor("white")
    fig.patch.set_facecolor("white")
    plt.xticks(rotation=45, ha='right')
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M\n%d-%b'))
    fig.tight_layout()
    plt.grid(alpha=0.3)
    return fig

# 7a. CPU Usage
st.markdown("**CPU Usage Over Time**")
fig1 = plot_line_chart(service_df['datetime'], service_df['cpu'], "CPU", color="blue")
st.pyplot(fig1)

# 7b. Risk Probability
st.markdown("**Risk Probability Over Time (%)**")
fig2 = plot_line_chart(service_df['datetime'], service_df['risk_score_percent'], "Risk Probability (%)", color="red")
st.pyplot(fig2)

# 7c. CPU Usage + Threshold
st.markdown("**CPU Usage vs CPU Threshold (70th percentile)**")
cpu_threshold = service_df['cpu'].quantile(0.70)
fig3 = plot_line_chart(
    service_df['datetime'], service_df['cpu'], "CPU", color="blue",
    threshold=cpu_threshold, threshold_label="CPU Threshold (70th percentile)"
)
st.pyplot(fig3)

# ---------------------------
# 8️⃣ High-Risk Instances Table
# ---------------------------
st.subheader("🚨 High-Risk Instances")
high_risk_df = service_df[service_df['risk_score_percent'] > 60][
    ['datetime', 'cpu', 'cpu_rolling_std', 'risk_score_percent']
]
if high_risk_df.empty:
    st.markdown("No high-risk instances detected for this microservice.")
else:
    st.dataframe(high_risk_df)

# ---------------------------
# 9️⃣ Insight Summary
# ---------------------------
st.subheader("🧠 Insight Summary")
st.markdown(
    f'<div style="background-color: {color}; padding: 15px; border-radius: 10px;">'
    f'<b>Observation:</b> Temporary risk observed after deployment; service has stabilized.<br>'
    f'<b>Suggestion:</b> {suggestion} Investigate if CPU spikes recur.'
    f'</div>', 
    unsafe_allow_html=True
)

# ---------------------------
# 🔟 Download Report
# ---------------------------
st.subheader("⬇️ Download Report")
csv = service_df.to_csv(index=False).encode('utf-8')
st.download_button(
    label="Download Microservice Report as CSV",
    data=csv,
    file_name=f"{selected_service}_post_deploy_report.csv",
    mime='text/csv'
)
