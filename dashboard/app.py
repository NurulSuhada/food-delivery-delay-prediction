import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(
    page_title="Food Delivery Performance Dashboard",
    layout="wide"
)

st.title("Food Delivery Performance Monitoring and Delay Prediction System")

# Load data
df = pd.read_csv("order_history_kaggle_data.csv")

# Create delivery status if not already exists
df["Delivery_Status"] = df["KPT duration (minutes)"].apply(
    lambda x: "Late" if x > 30 else "On Time"
)

st.sidebar.header("Filter Options")

# Interactive Feature 1: Restaurant filter
restaurant_options = ["All"] + sorted(df["Restaurant name"].dropna().unique().tolist())
selected_restaurant = st.sidebar.selectbox("Select Restaurant", restaurant_options)

# Interactive Feature 2: Delivery status filter
status_options = ["All"] + sorted(df["Delivery_Status"].dropna().unique().tolist())
selected_status = st.sidebar.selectbox("Select Delivery Status", status_options)

# Apply filters
filtered_df = df.copy()

if selected_restaurant != "All":
    filtered_df = filtered_df[filtered_df["Restaurant name"] == selected_restaurant]

if selected_status != "All":
    filtered_df = filtered_df[filtered_df["Delivery_Status"] == selected_status]

# KPI Metrics
st.subheader("Key Performance Metrics")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Total Orders", len(filtered_df))

with col2:
    avg_duration = filtered_df["KPT duration (minutes)"].mean()
    st.metric("Average Delivery Time", f"{avg_duration:.2f} minutes")

with col3:
    late_rate = (filtered_df["Delivery_Status"] == "Late").mean() * 100
    st.metric("Late Delivery Rate", f"{late_rate:.2f}%")

# Visualization 1
st.subheader("Visualization 1: Distribution of Delivery Duration")

fig1, ax1 = plt.subplots(figsize=(8, 4))
ax1.hist(filtered_df["KPT duration (minutes)"].dropna(), bins=30, edgecolor="black")
ax1.set_xlabel("Delivery Duration (minutes)")
ax1.set_ylabel("Number of Orders")
ax1.set_title("Distribution of Delivery Duration")
st.pyplot(fig1)

# Visualization 2
st.subheader("Visualization 2: Number of Orders by Restaurant")

restaurant_counts = filtered_df["Restaurant name"].value_counts()

fig2, ax2 = plt.subplots(figsize=(8, 4))
restaurant_counts.plot(kind="bar", ax=ax2)
ax2.set_xlabel("Restaurant")
ax2.set_ylabel("Number of Orders")
ax2.set_title("Number of Orders by Restaurant")
plt.xticks(rotation=45)
st.pyplot(fig2)

# Visualization 3
st.subheader("Visualization 3: Average Delivery Duration by Restaurant")

avg_delivery_by_restaurant = filtered_df.groupby("Restaurant name")["KPT duration (minutes)"].mean().sort_values(ascending=False)

fig3, ax3 = plt.subplots(figsize=(8, 4))
avg_delivery_by_restaurant.plot(kind="bar", ax=ax3)
ax3.set_xlabel("Restaurant")
ax3.set_ylabel("Average Delivery Duration (minutes)")
ax3.set_title("Average Delivery Duration by Restaurant")
plt.xticks(rotation=45)
st.pyplot(fig3)

# Analytical Output
st.subheader("Analytical Output")

if late_rate > 10:
    st.warning("The late delivery rate is relatively high. Operations team should monitor restaurant preparation time and rider waiting time.")
else:
    st.success("The late delivery rate is within an acceptable range based on the selected filter.")

st.subheader("Filtered Dataset Preview")
st.dataframe(filtered_df.head(20))
