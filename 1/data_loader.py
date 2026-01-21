"""
Data Loader Module
Handles all data loading, cleaning, and preprocessing operations
"""

import pandas as pd
import numpy as np
import streamlit as st
from typing import Optional

@st.cache_data
def load_and_preprocess_data(file_path: Optional[str] = None) -> pd.DataFrame:
    """
    Load and preprocess hotel data with comprehensive cleaning
    
    Args:
        file_path: Path to CSV file (if None, uses default or demo data)
    
    Returns:
        Preprocessed pandas DataFrame
    """
    
    # Check if we have fetched data in session state
    if 'fetched_data' in st.session_state and not st.session_state['fetched_data'].empty:
        df = st.session_state['fetched_data'].copy()
    # Load data from file
    elif file_path:
        df = pd.read_csv(file_path)
    else:
        # Try to load from default location or create demo data
        try:
            df = pd.read_csv('data/dubai_hotels.csv')
        except FileNotFoundError:
            df = create_demo_data()
    
    # Start preprocessing pipeline
    df = df.copy()
    
    # ========================================================================
    # 1. COLUMN STANDARDIZATION
    # ========================================================================
    
    df.columns = df.columns.str.strip().str.lower().str.replace(' ', '_')
    
    # ========================================================================
    # 2. PRICE CLEANING
    # ========================================================================
    
    price_columns = ['price', 'price_per_night', 'price_display', 'before_taxes_fees']
    
    for col in price_columns:
        if col in df.columns:
            df[col] = clean_currency_column(df[col])
    
    # Ensure we have a main price column
    if 'price_per_night' not in df.columns:
        if 'price' in df.columns:
            df['price_per_night'] = df['price']
        elif 'price_display' in df.columns:
            df['price_per_night'] = df['price_display']
    
    # ========================================================================
    # 3. RATING CLEANING
    # ========================================================================
    
    rating_columns = ['overall_rating', 'rating', 'star_rating']
    
    for col in rating_columns:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')
            df[col] = df[col].clip(0, 5)  # Ratings should be 0-5
    
    # Ensure we have main rating column
    if 'overall_rating' not in df.columns:
        if 'rating' in df.columns:
            df['overall_rating'] = df['rating']
    
    # ========================================================================
    # 4. NUMERIC COLUMNS CLEANING
    # ========================================================================
    
    numeric_cols = [
        'reviews_count', 'reviews', 'number_of_reviews',
        'availability', 'availability_365',
        'minimum_nights', 'maximum_nights',
        'total_amenities_count', 'amenities_count'
    ]
    
    for col in numeric_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)
    
    # Standardize review count column
    if 'reviews_count' not in df.columns:
        if 'reviews' in df.columns:
            df['reviews_count'] = df['reviews']
        elif 'number_of_reviews' in df.columns:
            df['reviews_count'] = df['number_of_reviews']
    
    # ========================================================================
    # 5. DATE COLUMNS CLEANING
    # ========================================================================
    
    date_columns = ['scrape_date', 'last_review', 'host_since', 'first_review']
    
    for col in date_columns:
        if col in df.columns:
            df[col] = pd.to_datetime(df[col], errors='coerce')
    
    # ========================================================================
    # 6. CATEGORICAL COLUMNS CLEANING
    # ========================================================================
    
    categorical_cols = [
        'hotel_name', 'name', 'property_name',
        'hotel_type', 'property_type', 'room_type',
        'location', 'neighborhood', 'area',
        'host_name', 'host_id'
    ]
    
    for col in categorical_cols:
        if col in df.columns:
            df[col] = df[col].fillna('Unknown').astype(str).str.strip()
    
    # Standardize property name
    if 'hotel_name' not in df.columns:
        if 'name' in df.columns:
            df['hotel_name'] = df['name']
        elif 'property_name' in df.columns:
            df['hotel_name'] = df['property_name']
    
    # ========================================================================
    # 7. COORDINATE CLEANING
    # ========================================================================
    
    if 'latitude' in df.columns:
        df['latitude'] = pd.to_numeric(df['latitude'], errors='coerce')
        df['latitude'] = df['latitude'].fillna(25.2048)  # Dubai default
    
    if 'longitude' in df.columns:
        df['longitude'] = pd.to_numeric(df['longitude'], errors='coerce')
        df['longitude'] = df['longitude'].fillna(55.2708)  # Dubai default
    
    # ========================================================================
    # 8. FEATURE ENGINEERING
    # ========================================================================
    
    # Value Score: Rating / Price (normalized)
    if 'overall_rating' in df.columns and 'price_per_night' in df.columns:
        df['value_score'] = np.where(
            df['price_per_night'] > 0,
            (df['overall_rating'] / df['price_per_night']) * 100,
            0
        )
    
    # Demand Proxy: Reviews / Availability
    if 'reviews_count' in df.columns and 'availability' in df.columns:
        df['demand_score'] = np.where(
            (df['availability'] > 0) & (df['availability'] < 365),
            df['reviews_count'] / (365 - df['availability']),
            df['reviews_count']
        )
    
    # Price Category
    if 'price_per_night' in df.columns:
        df['price_category'] = pd.cut(
            df['price_per_night'],
            bins=[0, 200, 500, 1000, float('inf')],
            labels=['Budget', 'Mid-Range', 'Premium', 'Luxury']
        )
    
    # Rating Category
    if 'overall_rating' in df.columns:
        df['rating_category'] = pd.cut(
            df['overall_rating'],
            bins=[0, 3.5, 4.0, 4.5, 5.0],
            labels=['Poor', 'Good', 'Very Good', 'Excellent']
        )
    
    # Experience Level (based on host listings or years)
    if 'host_listings_count' in df.columns:
        df['host_type'] = pd.cut(
            df['host_listings_count'],
            bins=[0, 1, 5, 20, float('inf')],
            labels=['Individual', 'Small Host', 'Professional', 'Enterprise']
        )
    
    # ========================================================================
    # 9. FINAL CLEANING
    # ========================================================================
    
    # Drop duplicates
    df = df.drop_duplicates()
    
    # Drop rows with missing critical data
    critical_cols = ['hotel_name', 'price_per_night']
    df = df.dropna(subset=[col for col in critical_cols if col in df.columns])
    
    # Remove outliers in price (beyond 99.5th percentile)
    if 'price_per_night' in df.columns:
        price_99 = df['price_per_night'].quantile(0.995)
        df = df[df['price_per_night'] <= price_99]
    
    return df


def clean_currency_column(series: pd.Series) -> pd.Series:
    """
    Clean currency column by removing symbols and converting to float
    
    Args:
        series: Pandas series with currency values
    
    Returns:
        Cleaned numeric series
    """
    return (
        series.astype(str)
        .str.replace('$', '', regex=False)
        .str.replace('AED', '', regex=False)
        .str.replace(',', '', regex=False)
        .str.replace(r'[^\d.]', '', regex=True)
        .replace('', np.nan)
        .astype(float)
        .fillna(0)
    )


def create_demo_data() -> pd.DataFrame:
    """
    Create demo dataset if no real data is available
    
    Returns:
        Demo pandas DataFrame
    """
    
    np.random.seed(42)
    n_hotels = 500
    
    hotel_types = ['Hotel', 'Resort', 'Apartment', 'Villa', 'Hostel']
    room_types = ['Private Room', 'Entire Place', 'Shared Room']
    locations = ['Downtown Dubai', 'Dubai Marina', 'Jumeirah', 'Deira', 
                 'Business Bay', 'Palm Jumeirah', 'JBR', 'Al Barsha']
    
    df = pd.DataFrame({
        'hotel_name': [f'Hotel {i}' for i in range(n_hotels)],
        'price_per_night': np.random.gamma(2, 200, n_hotels),
        'overall_rating': np.random.uniform(3.0, 5.0, n_hotels),
        'reviews_count': np.random.poisson(50, n_hotels),
        'hotel_type': np.random.choice(hotel_types, n_hotels),
        'room_type': np.random.choice(room_types, n_hotels),
        'location': np.random.choice(locations, n_hotels),
        'availability': np.random.randint(0, 365, n_hotels),
        'latitude': np.random.uniform(25.0, 25.3, n_hotels),
        'longitude': np.random.uniform(55.1, 55.4, n_hotels),
        'total_amenities_count': np.random.randint(5, 30, n_hotels),
        'host_listings_count': np.random.randint(1, 50, n_hotels),
        'minimum_nights': np.random.randint(1, 7, n_hotels),
    })
    
    # Add amenity columns
    amenities = ['wifi', 'pool', 'parking', 'gym', 'spa', 'breakfast', 'restaurant']
    for amenity in amenities:
        df[amenity] = np.random.choice([0, 1], n_hotels, p=[0.3, 0.7])
    
    return df