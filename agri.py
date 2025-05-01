import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go  # Importing the required module
import base64

st.set_page_config(page_title="Sri Lanka Dashboard", layout="wide", initial_sidebar_state="expanded")
data = pd.read_csv("agriculture_and_rural.csv")

def get_base64(file_path):
    with open(file_path, "rb") as f:
        return base64.b64encode(f.read()).decode()

def set_background(image_path):
    base64_img = get_base64(image_path)
    st.markdown(f"""
        <style>
        .stApp {{
            background-image: url("data:image/avif;base64,{base64_img}");
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
            background-attachment: fixed;
        }}
        .block-container {{
            padding: 5rem 2rem 2rem 2rem;
            background-color: rgba(0, 0, 0, 0.6);
            border-radius: 16px;
        }}
        .stPlotlyChart > div {{
            border-radius: 20px;
            overflow: hidden;
            box-shadow: 0 0 20px rgba(255, 255, 255, 0.05);
        }}
        .plot-container .main-svg {{
            overflow: visible !important;
        }}
        section.main > div {{
            max-width: 100%;
            padding-left: 1rem;
            padding-right: 1rem;
        }}
        </style>
    """, unsafe_allow_html=True)

def render_dashboard(filtered_data, name_prefix, color):
    indicators = filtered_data["Indicator Name"].unique()
    selected_indicator = st.sidebar.selectbox("Select one indicator for line & bar chart", indicators, key=f"{name_prefix}_line")
    filtered_df = filtered_data[filtered_data["Indicator Name"] == selected_indicator]

    years = filtered_df["Year"].dropna().unique()
    min_year, max_year = int(years.min()), int(years.max())
    year_range = st.sidebar.slider("Select year range", min_year, max_year, (min_year, max_year), key=f"{name_prefix}_year")
    range_df = filtered_df[(filtered_df["Year"] >= year_range[0]) & (filtered_df["Year"] <= year_range[1])]

    selected_area_indicators = st.sidebar.multiselect("Select indicators for area chart", indicators, default=indicators[:2], key=f"{name_prefix}_area")
    scatter_selection = st.sidebar.multiselect("Select 2 indicators for scatter plot", indicators, default=indicators[:2], key=f"{name_prefix}_scatter")

    col1, _, col2 = st.columns([1, 0.05, 1])
    with col1:
        st.markdown("#### 📈 Line Chart")
        fig = px.line(range_df, x="Year", y="Value", title=selected_indicator, markers=True, template="plotly_dark")
        fig.update_traces(line=dict(color=color, width=2), marker=dict(size=8, opacity=0.75))
        fig.update_layout(
            title=dict(text=selected_indicator, font=dict(size=14), x=0.3),
            xaxis_title="Year",
            yaxis_title="Value",
            xaxis=dict(title_font=dict(size=12), tickfont=dict(size=11)),
            yaxis=dict(title_font=dict(size=12), tickfont=dict(size=11)),
            margin=dict(t=75)
        )
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.markdown("#### 📊 Bar Chart")
        fig = px.bar(range_df.sort_values("Year"), x="Year", y="Value", title=selected_indicator, template="plotly_dark")
        fig.update_traces(marker_color=color, opacity=0.75)
        fig.update_layout(
            title=dict(text=selected_indicator, font=dict(size=14), x=0.3),
            xaxis_title="Year",
            yaxis_title="Value",
            xaxis=dict(title_font=dict(size=12), tickfont=dict(size=11)),
            yaxis=dict(title_font=dict(size=12), tickfont=dict(size=11)),
            margin=dict(t=75)
        )
        st.plotly_chart(fig, use_container_width=True)

    col3, _, col4 = st.columns([1, 0.05, 1])
    with col3:
        st.markdown("#### 🌿 Area Chart")
        if selected_area_indicators:
            area_df = filtered_data[filtered_data["Indicator Name"].isin(selected_area_indicators)]
            area_df = area_df.pivot_table(index="Year", columns="Indicator Name", values="Value").dropna().sort_index().reset_index()
            fig = px.area(area_df, x="Year", y=area_df.columns[1:], title="Area Chart of Selected Indicators", template="plotly_dark")
            fig.update_traces(opacity=0.75)
            
            # Customizing the layout for the area chart, including the legend
            fig.update_layout(
                title=dict(text="Area Chart of Selected Indicators", font=dict(size=14), x=0.3),
                xaxis_title="Year",
                yaxis_title="Value",
                xaxis=dict(title_font=dict(size=12), tickfont=dict(size=11)),
                yaxis=dict(title_font=dict(size=12), tickfont=dict(size=11)),
                legend=dict(
                    title="Indicators",  # Legend title
                    orientation="v",  # Horizontal orientation for the legend
                    yanchor="bottom",  # Anchor the legend to the bottom
                    y=0.15,  # Place the legend just above the chart
                    xanchor="center",  # Center the legend horizontally
                    x=0.60,  # Center the legend horizontally
                    font=dict(size=10, color="white"),  # Customize font size and color for the legend
                ),
                margin=dict(t=75)
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Please select at least one indicator.")

    with col4:
        st.markdown("#### 🔵 Scatter Plot & Correlation")
        if len(scatter_selection) == 2:
            scatter_df = filtered_data[filtered_data["Indicator Name"].isin(scatter_selection)]
            scatter_df = scatter_df.pivot(index="Year", columns="Indicator Name", values="Value").dropna()
            if not scatter_df.empty:
                corr = scatter_df.corr().iloc[0, 1]
                fig = px.scatter(scatter_df, x=scatter_selection[0], y=scatter_selection[1],
                                 title=f"{scatter_selection[0]} vs {scatter_selection[1]}", template="plotly_dark")
                fig.update_traces(marker=dict(color=color, opacity=0.75, line=dict(width=1, color="white")))
                fig.update_layout(
                    title=dict(text=f"{scatter_selection[0]} vs {scatter_selection[1]}", font=dict(size=14), x=0.3),
                    xaxis_title=scatter_selection[0],
                    yaxis_title=scatter_selection[1],
                    xaxis=dict(title_font=dict(size=12), tickfont=dict(size=11)),
                    yaxis=dict(title_font=dict(size=12), tickfont=dict(size=11)),
                    margin=dict(t=75),
                    legend=dict(
                        orientation="h",
                        yanchor="bottom",
                        y=0.23,
                        xanchor="center",
                        x=0.80,
                        font=dict(size=12, color="white"),
                        traceorder='normal',
                        itemsizing='constant',
                        itemwidth=30
                    )
                )
                # Add correlation as legend
                fig.add_trace(
                    go.Scatter(
                        x=[None], y=[None], mode='markers', marker=dict(size=2, color=color),
                        name=f"Correlation: {corr:.2f}"
                    )
                )
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.warning("Not enough data for scatter plot.")
        else:
            st.info("Please select exactly 2 indicators.")

# Page Navigation
page = st.sidebar.radio("Go to", ["Overview", "Agriculture", "Rural Development"])

if page == "Overview":
    set_background("image 1.png")
    st.title("🌾 Sri Lanka Agriculture & Rural Development Dashboard")
    st.markdown("### 📊 Dataset Summary")
    st.markdown("This dataset contains **1691 rows** and **4 columns**, from Sri Lanka’s Department of Census and Statistics.")
    st.markdown("### 🧾 Column Descriptions\n- Year\n- Indicator Name\n- Indicator Code\n- Value")

    search_keyword = st.sidebar.text_input("🔍 Search Indicator").strip().lower()
    all_indicators = sorted(data["Indicator Name"].unique())
    selected_indicator = st.sidebar.selectbox("📋 Select Indicator", ["All"] + all_indicators)
    years = data["Year"].dropna().unique()
    min_year, max_year = int(years.min()), int(years.max())
    year_range = st.sidebar.slider("📅 Select Year Range", min_year, max_year, (min_year, max_year))
    filtered_data = data[(data["Year"] >= year_range[0]) & (data["Year"] <= year_range[1])]
    if selected_indicator != "All":
        filtered_data = filtered_data[filtered_data["Indicator Name"] == selected_indicator]
    if search_keyword:
        filtered_data = filtered_data[filtered_data["Indicator Name"].str.lower().str.contains(search_keyword)]

    if st.checkbox("📂 Show Filtered Dataset"):
        st.dataframe(filtered_data)
        st.markdown(f"**🔢 Total Rows: {len(filtered_data)}**")

elif page == "Agriculture":
    set_background("image 4.avif")
    st.title("🌾 Agriculture Insights")
    agri_data = data[data["Indicator Code"].str.contains("AG|ER", case=False, na=False)]
    if st.checkbox("Show Agriculture Data"):
        st.dataframe(agri_data)
    render_dashboard(agri_data, "agri", color="lime")

elif page == "Rural Development":
    set_background("image 6.avif")
    st.title("🏡 Rural Development Insights")
    rural_data = data[data["Indicator Code"].str.contains("EG|EN|RUR", case=False, na=False)]
    if st.checkbox("Show Rural Data"):
        st.dataframe(rural_data)
    render_dashboard(rural_data, "rural", color="gold")









