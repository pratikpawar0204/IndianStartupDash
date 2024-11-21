import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from wordcloud import WordCloud
import matplotlib.pyplot as plt

# Set page configuration for modern UI
st.set_page_config(
    page_title="Indian Unicorn Startups Dashboard",
    page_icon="🦄",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load data
def load_data():
    # Update with correct file path or URL
    data = pd.read_csv("Indian Unicorn startups 2023 updated.csv")
    data = data.rename(columns={
        'Entry Valuation^^ ($B)': 'Entry Valuation ($B)',
        'Valuation ($B)': 'Current Valuation ($B)'
    })
    data['Year'] = pd.to_datetime(data['Entry'], errors='coerce').dt.year
    return data

data = load_data()

# Sidebar filters
st.sidebar.title("Filters")
sector_filter = st.sidebar.multiselect("Select Sector", options=data["Sector"].unique(), default=data["Sector"].unique())
year_filter = st.sidebar.slider("Select Year", int(data["Year"].min()), int(data["Year"].max()), (int(data["Year"].min()), int(data["Year"].max())))
location_filter = st.sidebar.multiselect("Select Location", options=data["Location"].unique(), default=data["Location"].unique())

# Apply filters
filtered_data = data[
    (data["Sector"].isin(sector_filter)) &
    (data["Year"].between(*year_filter)) &
    (data["Location"].isin(location_filter))
]

# Header
st.title("🦄 Indian Unicorn Startups Dashboard")
st.markdown("Explore the trends, funding, and insights into Indian Unicorns of 2023.")

# KPI Section
st.markdown("### 📊 Key Metrics")
kpi_col1, kpi_col2, kpi_col3, kpi_col4 = st.columns(4)

with kpi_col1:
    st.metric("Total Unicorns", len(filtered_data))

with kpi_col2:
    st.metric("Total Valuation ($B)", round(filtered_data["Current Valuation ($B)"].sum(), 2))

with kpi_col3:
    st.metric("Average Entry Valuation ($B)", round(filtered_data["Entry Valuation ($B)"].mean(), 2))

with kpi_col4:
    st.metric("Median Valuation ($B)", round(filtered_data["Current Valuation ($B)"].median(), 2))

# Geographical Insights
st.markdown("### 🌍 Geographical Insights")
geo_col1, geo_col2 = st.columns(2)

# Top Locations by Unicorn Count
with geo_col1:
    top_locations = filtered_data['Location'].value_counts().head(10).reset_index()
    top_locations.columns = ['Location', 'Count']
    location_chart = px.bar(top_locations, x='Location', y='Count', color='Location', title='Top Locations by Unicorn Count')
    st.plotly_chart(location_chart, use_container_width=True)

# Total Valuation by Location
with geo_col2:
    total_valuation_by_location = filtered_data.groupby('Location')['Current Valuation ($B)'].sum().reset_index()
    total_valuation_by_location = total_valuation_by_location.sort_values('Current Valuation ($B)', ascending=False).head(10)
    valuation_chart = px.bar(total_valuation_by_location, x='Location', y='Current Valuation ($B)', color='Location', title='Total Valuation by Location')
    st.plotly_chart(valuation_chart, use_container_width=True)

# Sector Insights
st.markdown("### 📂 Sector Insights")
sector_col1, sector_col2 = st.columns(2)

with sector_col1:
    top_sectors = filtered_data['Sector'].value_counts().head(10).reset_index()
    top_sectors.columns = ['Sector', 'Count']
    sector_chart = px.bar(top_sectors, x='Sector', y='Count', color='Sector', title='Top Sectors by Unicorn Count')
    st.plotly_chart(sector_chart, use_container_width=True)

with sector_col2:
    sector_dist = filtered_data['Sector'].value_counts().head(5).reset_index()
    sector_dist.columns = ['Sector', 'Count']
    sector_pie_chart = px.pie(sector_dist, values='Count', names='Sector', title='Sector Distribution')
    st.plotly_chart(sector_pie_chart, use_container_width=True)

# Yearly Line Chart
st.markdown("### 📅 Yearly Unicorn Growth Trend")
yearly_data = filtered_data.groupby("Year").size().reset_index(name="Unicorn Count")
yearly_line_chart = px.line(yearly_data, x="Year", y="Unicorn Count", title="Yearly Unicorn Growth", markers=True)
st.plotly_chart(yearly_line_chart, use_container_width=True)

# Word Cloud for Investors
st.header("🤝 Key Investors")
st.subheader("Top Investors Word Cloud")

# Combine investors into a single string
investors = ' '.join(filtered_data['Select Investors'].dropna())

if investors.strip():  # Check if there is at least one valid word
    wordcloud = WordCloud(background_color='white', colormap='tab10', width=800, height=400).generate(investors)

    fig, ax = plt.subplots(figsize=(10, 5))
    ax.imshow(wordcloud, interpolation='bilinear')
    ax.axis('off')
    st.pyplot(fig)
else:
    st.info("No data available to generate the Word Cloud. Please adjust your filters.")

# Footer
st.markdown("""
    Dataset used: [Indian Unicorn Startups 2023](https://www.kaggle.com/datasets/infodatalab/indian-unicorn-startups-2023)
    <br>Created by: PSP
""", unsafe_allow_html=True)
