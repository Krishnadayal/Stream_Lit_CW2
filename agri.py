import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import base64

# Load data
data = pd.read_csv("agriculture_and_rural.csv")

# Function to convert local image to base64
def get_base64(file_path):
    with open(file_path, "rb") as f:
        return base64.b64encode(f.read()).decode()

# Page selection
page = st.sidebar.radio("Go to", ["Home", "Agriculture", "Rural Development"])

# Apply background image conditionally
def set_background(image_path):
    base64_img = get_base64(image_path)
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url("data:image/avif;base64,{base64_img}");
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
            background-attachment: fixed;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

# --- Home Page ---
if page == "Home":
    set_background("default.avif")  # Set your default home background
    st.title("Sri Lanka Agriculture & Rural Dashboard")
    st.write("Welcome! Use the sidebar to navigate.")

# --- Agriculture Page ---
elif page == "Agriculture":
    set_background("image 4.avif")
    st.title("Agriculture Insights")
    agri_data = data[data["Indicator Code"].str.contains("AG|ER", case=False, na=False)]

    if st.checkbox("Show Raw Agriculture Data"):
        st.dataframe(agri_data)

    # --- Line Chart ---
    st.subheader("📈 Line Chart")
    indicators = agri_data["Indicator Name"].unique()
    selected_indicator = st.selectbox("Select an Indicator", indicators)
    filtered_df = agri_data[agri_data["Indicator Name"] == selected_indicator]

    fig, ax = plt.subplots(figsize=(13, 5))
    ax.plot(filtered_df["Year"], filtered_df["Value"], color="cyan", marker="o", linewidth=2)
    ax.set_title(f"{selected_indicator}", fontsize=16, color='white')
    ax.set_xlabel("Year", fontsize=12, color='white')
    ax.set_ylabel("Value", fontsize=12, color='white')
    ax.grid(True, linestyle='--', alpha=0.4)
    ax.tick_params(axis='x', colors='white')
    ax.tick_params(axis='y', colors='white')
    fig.patch.set_facecolor('#0E1117')  
    ax.set_facecolor('#0E1117')
    st.pyplot(fig)

    # --- Area Chart ---
    st.subheader("📊 Area Chart")
    indicator_list = agri_data["Indicator Name"].unique()
    selected_indicators = st.multiselect("Select indicators for area chart", indicator_list, default=indicator_list[:3])

    if selected_indicators:
        area_df = agri_data[agri_data["Indicator Name"].isin(selected_indicators)]
        area_df = area_df.pivot_table(index="Year", columns="Indicator Name", values="Value", aggfunc="first").dropna().sort_index()
        fig, ax = plt.subplots(figsize=(10, 6))
        area_df.plot.area(ax=ax, colormap="tab20", alpha=0.8)
        ax.set_title("Stacked Area Chart of Selected Indicators Over Time", fontsize=14)
        ax.set_xlabel("Year")
        ax.set_ylabel("Value")
        ax.grid(True)
        st.pyplot(fig)
    else:
        st.info("Please select at least one indicator.")

# --- Rural Development Page ---
elif page == "Rural Development":
    set_background("image 6.avif")  # Your rural image
    st.title("🏡 Rural Development Insights")
    rural_data = data[data["Indicator Code"].str.contains("EG|EN|RUR", case=False, na=False)]


    if st.checkbox("Show Raw Rural Data"):
        st.dataframe(rural_data)

    # --- Line Chart ---
    st.subheader("📈 Line Chart")
    indicators = rural_data["Indicator Name"].unique()
    selected_indicator = st.selectbox("Select an Indicator", indicators)
    filtered_df = rural_data[rural_data["Indicator Name"] == selected_indicator]

    fig, ax = plt.subplots(figsize=(13, 5))
    ax.plot(filtered_df["Year"], filtered_df["Value"], color="cyan", marker="o", linewidth=2)
    ax.set_title(f"{selected_indicator}", fontsize=16, color='white')
    ax.set_xlabel("Year", fontsize=12, color='white')
    ax.set_ylabel("Value", fontsize=12, color='white')
    ax.grid(True, linestyle='--', alpha=0.4)
    ax.tick_params(axis='x', colors='white')
    ax.tick_params(axis='y', colors='white')
    fig.patch.set_facecolor('#0E1117')  
    ax.set_facecolor('#0E1117')
    st.pyplot(fig)

    # --- Area Chart ---
    st.subheader("📊 Area Chart")
    indicator_list = rural_data["Indicator Name"].unique()
    selected_indicators = st.multiselect("Select indicators for area chart", indicator_list, default=indicator_list[:3])

    if selected_indicators:
        area_df = rural_data[rural_data["Indicator Name"].isin(selected_indicators)]
        area_df = area_df.pivot_table(index="Year", columns="Indicator Name", values="Value", aggfunc="first").dropna().sort_index()
        fig, ax = plt.subplots(figsize=(10, 6))
        area_df.plot.area(ax=ax, colormap="tab20", alpha=0.8)
        ax.set_title("Stacked Area Chart of Selected Indicators Over Time", fontsize=14)
        ax.set_xlabel("Year")
        ax.set_ylabel("Value")
        ax.grid(True)
        st.pyplot(fig)
    else:
        st.info("Please select at least one indicator.")



