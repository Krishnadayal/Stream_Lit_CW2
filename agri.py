import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import base64

st.set_page_config( page_title = "Sri Lanka Dashboard", layout = "wide", initial_sidebar_state = "expanded")

data = pd.read_csv("agriculture_and_rural.csv")

# Background Image
def get_base64(file_path):
    with open(file_path, "rb") as f:
        return base64.b64encode(f.read()).decode()

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
            background-attachment: fixed }}

        .block-container {{
            padding: 5rem 2rem 2rem 2rem;
            background-color: rgba(0, 0, 0, 0.6);
            border-radius: 12px;}}

        .css-1d391kg, .css-1v3fvcr, .css-1r6slb0, .css-1y4p8pa {{
            background-color: transparent !important;
            backdrop-filter: blur(4px);}} 

        section.main > div {{
            max-width: 100%;
            padding-left: 1rem;
            padding-right: 1rem;}}
        </style>
        """,
        unsafe_allow_html = True)

# Sidebar 
page = st.sidebar.radio("Go to", ["Overview", "Agriculture", "Rural Development"])

# Overview Page
if page == "Overview":
    set_background("image 1.png")
    st.title("🌾 Sri Lanka Agriculture & Rural Development Dashboard")

    st.markdown("""
    ### 📊 Dataset Summary
    This dataset contains **1691 rows** and **4 columns**, compiled from the Sri Lanka Department of Census and Statistics.
    It focuses on **key indicators** related to agriculture and rural development, spanning multiple years.
    """)

    st.markdown("""
    ### 🧾 Column Descriptions
    - **Year**: The year of the recorded data (e.g., 2005, 2010)
    - **Indicator Name**: Full name of the development indicator
    - **Indicator Code**: Abbreviated or coded form of the indicator
    - **Value**: The actual numerical value for that indicator in that year
    """)

    st.sidebar.markdown("## 🔎 Filter Dataset")

    search_keyword = st.sidebar.text_input("🔍 Search Indicator (optional)").strip().lower()
    all_indicators = sorted(data["Indicator Name"].unique())
    indicator_options = ["All"] + all_indicators
    selected_indicator = st.sidebar.selectbox("📋 Select Indicator", indicator_options)

    years = data["Year"].dropna().unique()
    min_year, max_year = int(years.min()), int(years.max())
    year_range = st.sidebar.slider("📅 Select Year Range", min_value=min_year, max_value=max_year, value=(min_year, max_year))

    filtered_data = data[(data["Year"] >= year_range[0]) & (data["Year"] <= year_range[1])]
    if selected_indicator != "All":
        filtered_data = filtered_data[filtered_data["Indicator Name"] == selected_indicator]
    if search_keyword:
        filtered_data = filtered_data[filtered_data["Indicator Name"].str.lower().str.contains(search_keyword)]

    if st.checkbox("📂 Show Filtered Dataset"):
        st.markdown("### 📄 Filtered Dataset")
        st.dataframe(filtered_data)
        st.markdown(f"**🔢 Total Filtered Rows: {len(filtered_data)}**")

# Charts
def render_dashboard(filtered_data, name_prefix, color, cmap):
    indicators = filtered_data["Indicator Name"].unique()

    st.sidebar.markdown(f"## 🎯 {name_prefix.title()} Filters")
    st.sidebar.markdown("### Line & Bar Chart Filters")

    selected_indicator = st.sidebar.selectbox("Select one indicator for line & bar chart", indicators, key = f"{name_prefix}_line")
    filtered_df = filtered_data[filtered_data["Indicator Name"] == selected_indicator]

    years = filtered_df["Year"].dropna().unique()
    min_year, max_year = int(years.min()), int(years.max())
    year_range = st.sidebar.slider("Select the year range for line & bar chart", min_value = min_year, max_value = max_year, value = (min_year, max_year), key = f"{name_prefix}_year")
    range_df = filtered_df[(filtered_df["Year"] >= year_range[0]) & (filtered_df["Year"] <= year_range[1])]

    st.sidebar.markdown("### Area Chart Filters")
    selected_area_indicators = st.sidebar.multiselect("Select indicators for area chart", indicators, default = indicators[:2], key = f"{name_prefix}_area")

    st.sidebar.markdown("### Scatter Plot Filters")
    scatter_selection = st.sidebar.multiselect("Select two indicators for scatter plot", indicators, default = indicators[:2], key = f"{name_prefix}_scatter")

    col1, _, col2 = st.columns([1, 0.05, 1])  # Added gap here

    with col1:
        st.markdown("#### 📈 Line Chart")
        fig, ax = plt.subplots(figsize = (12, 8))
        ax.plot(range_df["Year"], range_df["Value"], color = color, marker = "o", linewidth = 2, alpha = 0.75)
        ax.set_title(f"{selected_indicator} (Line Chart)", fontsize = 14, color = "white")
        ax.set_xlabel("Year", fontsize=12, color = "white", labelpad = 10)
        ax.set_ylabel("Value", fontsize=12, color = "white", labelpad = 10)
        ax.grid(True, linestyle = '--', alpha = 0.4)
        ax.tick_params(axis = "x", colors = "white")
        ax.tick_params(axis = "y", colors = "white")
        fig.patch.set_facecolor('#0E1117')
        ax.set_facecolor('#0E1117')
        fig.tight_layout()
        st.pyplot(fig)

    with col2:
        st.markdown("#### 📊 Bar Chart")
        bar_df = range_df.sort_values("Year")
        fig, ax = plt.subplots(figsize = (12, 8))
        ax.bar(bar_df["Year"], bar_df["Value"], color = color, alpha = 0.75)
        ax.set_title(f"{selected_indicator} (Bar Chart)", fontsize = 14, color = "white")
        ax.set_xlabel("Year", fontsize = 12, color = "white", labelpad = 10)
        ax.set_ylabel("Value", fontsize = 12, color = "white", labelpad = 10)
        ax.grid(True, linestyle = "--", alpha = 0.3)
        ax.tick_params(axis = "x", colors = "white")
        ax.tick_params(axis = "y", colors = "white")
        fig.patch.set_facecolor("#0E1117")
        ax.set_facecolor("#0E1117")
        fig.tight_layout()
        st.pyplot(fig)

    col3, _, col4 = st.columns([1, 0.05, 1])  # Added gap here

    with col3:
        st.markdown("#### 🌿 Area Chart")
        if selected_area_indicators:
            area_df = filtered_data[filtered_data["Indicator Name"].isin(selected_area_indicators)]
            area_df = area_df.pivot_table(index = "Year", columns = "Indicator Name", values = "Value", aggfunc = "first").dropna().sort_index()
            fig, ax = plt.subplots(figsize = (12, 8))
            area_df.plot.area(ax = ax, colormap = cmap, alpha = 0.75)
            ax.set_title("Area Chart of Selected Indicators", fontsize = 14, color = 'white')
            ax.set_xlabel("Year", fontsize = 12, color = "white", labelpad = 10)
            ax.set_ylabel("Value", fontsize = 12, color = "white", labelpad = 10)
            ax.grid(True, linestyle = "--", alpha = 0.3)
            ax.tick_params(axis = "x", colors = "white")
            ax.tick_params(axis = "y", colors = "white")
            fig.patch.set_facecolor("#0E1117")
            ax.set_facecolor("#0E1117")
            fig.tight_layout()
            st.pyplot(fig)
        else:
            st.info("Please select at least one indicator for the area chart.")

    with col4:
        st.markdown("#### 🔵 Scatter Plot & Correlation")
        if len(scatter_selection) == 2:
            scatter_df = filtered_data[filtered_data["Indicator Name"].isin(scatter_selection)]
            scatter_df = scatter_df.pivot(index = "Year", columns = "Indicator Name", values = "Value").dropna()

            if not scatter_df.empty:
                correlation = scatter_df.corr().iloc[0, 1]
                fig, ax = plt.subplots(figsize = (12, 8))
                ax.scatter(scatter_df[scatter_selection[0]], scatter_df[scatter_selection[1]], color = color, edgecolor = "white", alpha = 0.75)
                ax.set_xlabel(scatter_selection[0], fontsize = 12, color = "white", labelpad = 10)
                ax.set_ylabel(scatter_selection[1], fontsize = 12, color = "white", labelpad = 10)
                ax.set_title(f"{scatter_selection[0]} vs {scatter_selection[1]}", fontsize = 14, color = "white", pad = 15)
                ax.text(0.5, -0.15, f"Pearson Correlation Coefficient: {correlation:.2f}", transform = ax.transAxes, fontsize = 12, color = "white", ha = "center")
                ax.grid(True, linestyle = "--", alpha = 0.3)
                ax.tick_params(axis = "x", colors = "white")
                ax.tick_params(axis = "y", colors = "white")
                fig.patch.set_facecolor("#0E1117")
                ax.set_facecolor("#0E1117")
                fig.tight_layout()
                st.pyplot(fig)
            else:
                st.warning("Not enough data to create scatter plot.")
        else:
            st.info("Please select 2 indicators for the scatter plot.")

# Agriculture Page
if page == "Agriculture":
    set_background("image 4.avif")
    st.title("🌾 Agriculture Insights")
    agri_data = data[data["Indicator Code"].str.contains("AG|ER", case = False, na = False)]
    if st.checkbox("Show Agriculture Data"):
        st.dataframe(agri_data)
    render_dashboard(agri_data, "agri", color = "lime", cmap = "Greens")

# Rural Development Page
elif page == "Rural Development":
    set_background("image 6.avif")
    st.title("🏡 Rural Development Insights")
    rural_data = data[data["Indicator Code"].str.contains("EG|EN|RUR", case = False, na = False)]
    if st.checkbox("Show Rural Data"):
        st.dataframe(rural_data)
    render_dashboard(rural_data, "rural", color = "gold", cmap = "YlOrBr")




