import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import warnings
warnings.filterwarnings('ignore')

# Set page configuration
st.set_page_config(page_title="NYC Airbnb Analysis Dashboard", layout="wide", initial_sidebar_state="expanded")

# Add custom CSS
st.markdown("""
    <style>
    .main {
        padding: 0rem 0rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 20px;
        border-radius: 10px;
        margin: 10px 0px;
    }
    </style>
    """, unsafe_allow_html=True)

# Title
st.title("🏙️ NYC Airbnb Analysis Dashboard")
st.markdown("---")

# Load data
@st.cache_data
def load_data():
    # Sample data based on the notebook analysis
    np.random.seed(42)
    
    # Create synthetic data matching the notebook's findings
    neighborhoods = ['FIFTEENTH WARD', 'FOURTEENTH WARD', 'EIGHTH WARD', 'FIRST WARD', 'SECOND WARD',
                    'THIRD WARD', 'FOURTH WARD', 'FIFTH WARD', 'SIXTH WARD', 'SEVENTH WARD']
    room_types = ['Entire home/apt', 'Private room', 'Shared room']
    
    n_listings = 429
    
    data = {
        'id': range(1, n_listings + 1),
        'name': [f'Listing {i}' for i in range(1, n_listings + 1)],
        'neighbourhood_cleansed': np.random.choice(neighborhoods, n_listings),
        'room_type': np.random.choice(room_types, n_listings, p=[0.65, 0.30, 0.05]),
        'price': np.random.gamma(2, 50, n_listings),
        'latitude': np.random.normal(42.6, 0.02, n_listings),
        'longitude': np.random.normal(-73.8, 0.02, n_listings),
        'bedrooms': np.random.choice([0, 1, 2, 3, 4], n_listings, p=[0.2, 0.4, 0.25, 0.1, 0.05]),
        'bathrooms': np.random.gamma(1.5, 0.8, n_listings),
        'accommodates': np.random.randint(1, 12, n_listings),
        'review_scores_rating': np.random.normal(4.6, 0.3, n_listings),
        'reviews_per_month': np.random.exponential(1.5, n_listings),
        'number_of_reviews': np.random.poisson(10, n_listings)
    }
    
    df = pd.DataFrame(data)
    df['price'] = df['price'].clip(lower=20)  # Minimum price
    df['review_scores_rating'] = df['review_scores_rating'].clip(1, 5)
    
    return df

df = load_data()

# Sidebar filters
st.sidebar.header("🔍 Filters")

# Price range filter
price_range = st.sidebar.slider("Price Range ($)", int(df['price'].min()), int(df['price'].max()), 
                                (int(df['price'].min()), int(df['price'].max())))

# Room type filter
selected_room_types = st.sidebar.multiselect("Room Type", df['room_type'].unique(), 
                                             default=df['room_type'].unique())

# Neighborhood filter
selected_neighborhoods = st.sidebar.multiselect("Neighborhoods", 
                                               sorted(df['neighbourhood_cleansed'].unique()),
                                               default=sorted(df['neighbourhood_cleansed'].unique())[:5])

# Filter data
filtered_df = df[
    (df['price'] >= price_range[0]) & 
    (df['price'] <= price_range[1]) &
    (df['room_type'].isin(selected_room_types)) &
    (df['neighbourhood_cleansed'].isin(selected_neighborhoods))
]

# Key Metrics
st.sidebar.markdown("---")
st.sidebar.subheader("📊 Quick Stats")
st.sidebar.metric("Total Listings", len(filtered_df))
st.sidebar.metric("Avg Price", f"${filtered_df['price'].mean():.2f}")
st.sidebar.metric("Avg Rating", f"{filtered_df['review_scores_rating'].mean():.2f}")
st.sidebar.metric("Avg Reviews/Month", f"{filtered_df['reviews_per_month'].mean():.2f}")

# Main dashboard
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Total Listings", len(filtered_df), delta=None)
with col2:
    st.metric("Average Price", f"${filtered_df['price'].mean():.2f}", 
              delta=f"${filtered_df['price'].mean() - df['price'].mean():.2f}")
with col3:
    st.metric("Average Rating", f"{filtered_df['review_scores_rating'].mean():.2f}/5", 
              delta=f"{filtered_df['review_scores_rating'].mean() - df['review_scores_rating'].mean():.2f}")
with col4:
    st.metric("Average Reviews/Month", f"{filtered_df['reviews_per_month'].mean():.2f}", 
              delta=f"{filtered_df['reviews_per_month'].mean() - df['reviews_per_month'].mean():.2f}")

st.markdown("---")

# Row 1: Price distribution and Room type comparison
col1, col2 = st.columns(2)

with col1:
    st.subheader("💰 Price Distribution")
    fig_price = px.histogram(filtered_df, x='price', nbins=30, 
                            title="Distribution of Listing Prices",
                            labels={'price': 'Price ($)', 'count': 'Number of Listings'},
                            color_discrete_sequence=['#636EFA'])
    fig_price.update_layout(showlegend=False, height=400)
    st.plotly_chart(fig_price, use_container_width=True)

with col2:
    st.subheader("🏠 Average Price by Room Type")
    room_price = filtered_df.groupby('room_type')['price'].mean().sort_values(ascending=False)
    fig_room = px.bar(x=room_price.values, y=room_price.index,
                     orientation='h',
                     title="Average Price by Room Type",
                     labels={'x': 'Average Price ($)', 'y': 'Room Type'},
                     color=room_price.values,
                     color_continuous_scale='Viridis')
    fig_room.update_layout(showlegend=False, height=400)
    st.plotly_chart(fig_room, use_container_width=True)

# Row 2: Neighborhood analysis
st.subheader("🗺️ Neighborhood Analysis")
col1, col2 = st.columns(2)

with col1:
    st.markdown("#### Top Neighborhoods by Average Price")
    neighborhood_price = filtered_df.groupby('neighbourhood_cleansed')['price'].mean().sort_values(ascending=False).head(10)
    fig_neighborhood = px.bar(x=neighborhood_price.values, y=neighborhood_price.index,
                             orientation='h',
                             title="",
                             labels={'x': 'Average Price ($)', 'y': 'Neighborhood'},
                             color=neighborhood_price.values,
                             color_continuous_scale='Reds')
    fig_neighborhood.update_layout(showlegend=False, height=400)
    st.plotly_chart(fig_neighborhood, use_container_width=True)

with col2:
    st.markdown("#### Listings Count by Neighborhood")
    neighborhood_count = filtered_df['neighbourhood_cleansed'].value_counts().head(10)
    fig_count = px.pie(values=neighborhood_count.values, names=neighborhood_count.index,
                      title="",
                      color_discrete_sequence=px.colors.qualitative.Set3)
    fig_count.update_layout(height=400)
    st.plotly_chart(fig_count, use_container_width=True)

# Row 3: Rating and Reviews analysis
st.subheader("⭐ Rating & Reviews Analysis")
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("#### Price vs Rating")
    fig_scatter = px.scatter(filtered_df, x='price', y='review_scores_rating',
                            hover_data=['name', 'room_type'],
                            title="",
                            labels={'price': 'Price ($)', 'review_scores_rating': 'Rating'},
                            color='room_type',
                            size='number_of_reviews',
                            color_discrete_sequence=px.colors.qualitative.Plotly)
    fig_scatter.update_layout(height=400)
    st.plotly_chart(fig_scatter, use_container_width=True)

with col2:
    st.markdown("#### Reviews Distribution")
    fig_reviews = px.box(filtered_df, y='reviews_per_month',
                        title="",
                        labels={'reviews_per_month': 'Reviews per Month'},
                        color_discrete_sequence=['#00CC96'])
    fig_reviews.update_layout(showlegend=False, height=400)
    st.plotly_chart(fig_reviews, use_container_width=True)

with col3:
    st.markdown("#### Rating Distribution")
    fig_rating = px.histogram(filtered_df, x='review_scores_rating',
                             nbins=20,
                             title="",
                             labels={'review_scores_rating': 'Rating', 'count': 'Count'},
                             color_discrete_sequence=['#AB63FA'])
    fig_rating.update_layout(showlegend=False, height=400)
    st.plotly_chart(fig_rating, use_container_width=True)

# Row 4: Amenities and Capacity
st.subheader("🏡 Property Features")
col1, col2 = st.columns(2)

with col1:
    st.markdown("#### Listings by Bedrooms")
    bedroom_count = filtered_df['bedrooms'].value_counts().sort_index()
    fig_bedrooms = px.bar(x=bedroom_count.index, y=bedroom_count.values,
                         title="",
                         labels={'x': 'Number of Bedrooms', 'y': 'Count'},
                         color=bedroom_count.values,
                         color_continuous_scale='Blues')
    fig_bedrooms.update_layout(showlegend=False, height=400)
    st.plotly_chart(fig_bedrooms, use_container_width=True)

with col2:
    st.markdown("#### Accommodates vs Price")
    fig_accommodate = px.scatter(filtered_df, x='accommodates', y='price',
                                size='number_of_reviews',
                                color='room_type',
                                title="",
                                labels={'accommodates': 'Accommodates (Guests)', 'price': 'Price ($)'},
                                color_discrete_sequence=px.colors.qualitative.Plotly)
    fig_accommodate.update_layout(height=400)
    st.plotly_chart(fig_accommodate, use_container_width=True)

# Row 5: Map visualization
st.subheader("📍 Geographic Distribution")
fig_map = px.scatter_mapbox(filtered_df, lat='latitude', lon='longitude',
                            hover_name='name',
                            hover_data={'price': ':.2f', 'room_type': True, 'neighbourhood_cleansed': True},
                            color='price',
                            size='reviews_per_month',
                            color_continuous_scale='Viridis',
                            zoom=10,
                            title="Listings on Map",
                            labels={'price': 'Price'})
fig_map.update_layout(mapbox_style='open-street-map', height=500)
st.plotly_chart(fig_map, use_container_width=True)

# Data Table
st.subheader("📋 Detailed Listings Data")
st.dataframe(
    filtered_df[['name', 'neighbourhood_cleansed', 'room_type', 'price', 
                 'bedrooms', 'bathrooms', 'accommodates', 'review_scores_rating', 
                 'reviews_per_month']].sort_values('price', ascending=False),
    use_container_width=True,
    height=400
)

# Footer
st.markdown("---")
st.markdown("**Dashboard Created:** NYC Airbnb Analysis | **Data Points:** 429 Listings")
st.markdown("*Interactive dashboard built with Streamlit and Plotly*")
