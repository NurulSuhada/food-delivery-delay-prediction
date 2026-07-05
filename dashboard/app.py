import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# ===========================
# PAGE CONFIG
# ===========================

st.set_page_config(
    page_title="Food Delivery Dashboard",
    page_icon="🚚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ===========================
# SMALL CSS STYLING
# ===========================

st.markdown("""
<style>
.main {
    padding-top: 1rem;
}
h2 {
    font-size: 1.6rem !important;
}
h3 {
    font-size: 1.1rem !important;
}
[data-testid="stMetricValue"] {
    font-size: 1.8rem;
}
</style>
""", unsafe_allow_html=True)

# ===========================
# LOAD DATA
# ===========================

df = pd.read_csv("order_history_kaggle_data.csv")

# Create delivery status
df["Delivery_Status"] = df["KPT duration (minutes)"].apply(
    lambda x: "Late" if x > 30 else "On Time"
)

# ===========================
# SIDEBAR FILTERS
# ===========================

st.sidebar.header("Filter Options")

restaurant_options = ["All"] + sorted(df["Restaurant name"].dropna().unique().tolist())
selected_restaurant = st.sidebar.selectbox("Select Restaurant", restaurant_options)

status_options = ["All"] + sorted(df["Delivery_Status"].dropna().unique().tolist())
selected_status = st.sidebar.selectbox("Select Delivery Status", status_options)

# Apply filters
filtered_df = df.copy()

if selected_restaurant != "All":
    filtered_df = filtered_df[filtered_df["Restaurant name"] == selected_restaurant]

if selected_status != "All":
    filtered_df = filtered_df[filtered_df["Delivery_Status"] == selected_status]

# ===========================
# TITLE
# ===========================

st.markdown("""
<h2>🚚 Food Delivery Performance Monitoring and Delay Prediction System</h2>
<hr>
""", unsafe_allow_html=True)

# ===========================
# KPI SECTION
# ===========================

kpi1, kpi2, kpi3 = st.columns(3)

total_orders = len(filtered_df)
avg_delivery_time = filtered_df["KPT duration (minutes)"].mean()
late_rate = (filtered_df["Delivery_Status"] == "Late").mean() * 100

with kpi1:
    st.metric("Total Orders", f"{total_orders:,}")

with kpi2:
    st.metric("Average Delivery Time", f"{avg_delivery_time:.2f} min")

with kpi3:
    st.metric("Late Delivery Rate", f"{late_rate:.2f}%")

# ===========================
# ANALYTICAL OUTPUT
# ===========================

if late_rate > 10:
    st.error(
        "Analytical Output: Late delivery rate is high. "
        "The Operations Team should investigate restaurant preparation time and rider waiting time."
    )
else:
    st.success(
        "Analytical Output: Delivery performance is within the acceptable range based on the selected filter."
    )

# ===========================
# VISUALIZATIONS
# ===========================

st.markdown("### Dashboard Visualizations")

chart1, chart2, chart3 = st.columns(3)

# Visualization 1: Distribution of Delivery Duration
with chart1:
    st.markdown("**Visualization 1: Delivery Duration**")

    fig1, ax1 = plt.subplots(figsize=(4, 3))

    ax1.hist(
        filtered_df["KPT duration (minutes)"].dropna(),
        bins=20,
        color="#4C78A8",
        edgecolor="black"
    )

    ax1.set_title("Distribution of Delivery Duration", fontsize=10)
    ax1.set_xlabel("Minutes", fontsize=8)
    ax1.set_ylabel("Orders", fontsize=8)
    ax1.tick_params(axis="both", labelsize=8)

    st.pyplot(fig1, use_container_width=True)

# Visualization 2: Number of Orders by Restaurant
with chart2:
    st.markdown("**Visualization 2: Orders by Restaurant**")

    restaurant_counts = (
        filtered_df["Restaurant name"]
        .value_counts()
        .head(6)
    )

    fig2, ax2 = plt.subplots(figsize=(4, 3))

    ax2.bar(
        restaurant_counts.index,
        restaurant_counts.values,
        color="#4C78A8"
    )

    ax2.set_title("Number of Orders by Restaurant", fontsize=10)
    ax2.set_xlabel("Restaurant", fontsize=8)
    ax2.set_ylabel("Orders", fontsize=8)
    ax2.tick_params(axis="x", rotation=45, labelsize=7)
    ax2.tick_params(axis="y", labelsize=8)

    st.pyplot(fig2, use_container_width=True)

# Visualization 3: Average Delivery Duration by Restaurant
with chart3:
    st.markdown("**Visualization 3: Avg Delivery Time**")

    avg_delivery_by_restaurant = (
        filtered_df
        .groupby("Restaurant name")["KPT duration (minutes)"]
        .mean()
        .sort_values(ascending=False)
        .head(6)
    )

    fig3, ax3 = plt.subplots(figsize=(4, 3))

    ax3.bar(
        avg_delivery_by_restaurant.index,
        avg_delivery_by_restaurant.values,
        color="#54A24B"
    )

    ax3.set_title("Average Delivery Duration by Restaurant", fontsize=10)
    ax3.set_xlabel("Restaurant", fontsize=8)
    ax3.set_ylabel("Avg Duration", fontsize=8)
    ax3.tick_params(axis="x", rotation=45, labelsize=7)
    ax3.tick_params(axis="y", labelsize=8)

    st.pyplot(fig3, use_container_width=True)

# ===========================
# FILTERED DATASET PREVIEW
# ===========================

st.markdown("### Filtered Dataset Preview")

preview_columns = [
    "Order ID",
    "Restaurant name",
    "City",
    "Order Status",
    "KPT duration (minutes)",
    "Rider wait time (minutes)",
    "Delivery_Status"
]

available_columns = [col for col in preview_columns if col in filtered_df.columns]

st.dataframe(
    filtered_df[available_columns].head(10),
    use_container_width=True,
    height=280
)
