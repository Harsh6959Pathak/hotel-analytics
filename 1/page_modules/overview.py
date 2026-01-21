"""
Page 1: Overview & Dataset Insights
Provides high-level KPIs and market positioning analysis
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from utils import (
    page_header, create_metric_card, create_insight_box,
    create_plotly_theme, format_currency, format_number
)


def render_page(df: pd.DataFrame):
    """Render the Overview & Insights page"""
    
    page_header(
        "Overview & Dataset Insights",
        "High-level market analysis and key performance indicators",
        "📈"
    )
    
    if df.empty:
        st.warning("No data available with current filters.")
        return
    
    # ========================================================================
    # SECTION 1: KEY METRICS
    # ========================================================================
    
    st.markdown("## 📊 Key Performance Indicators")
    
    # Calculate metrics
    total_properties = len(df)
    unique_locations = df['location'].nunique() if 'location' in df.columns else 0
    avg_price = df['price_per_night'].mean() if 'price_per_night' in df.columns else 0
    avg_rating = df['overall_rating'].mean() if 'overall_rating' in df.columns else 0
    avg_availability = df['availability'].mean() if 'availability' in df.columns else 0
    
    # Display metrics in columns
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        create_metric_card(
            "Total Properties",
            format_number(total_properties),
            icon="🏨"
        )
    
    with col2:
        create_metric_card(
            "Unique Locations",
            str(unique_locations),
            icon="📍"
        )
    
    with col3:
        create_metric_card(
            "Avg Price/Night",
            format_currency(avg_price),
            icon="💰"
        )
    
    with col4:
        create_metric_card(
            "Avg Rating",
            f"{avg_rating:.2f} / 5.0",
            icon="⭐"
        )
    
    with col5:
        create_metric_card(
            "Avg Availability",
            f"{avg_availability:.0f} days",
            icon="📅"
        )
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # ========================================================================
    # SECTION 2: PROPERTY TYPE DISTRIBUTION
    # ========================================================================
    
    st.markdown("## 🏘️ Property Type Distribution")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        if 'hotel_type' in df.columns:
            type_counts = df['hotel_type'].value_counts().reset_index()
            type_counts.columns = ['Property Type', 'Count']
            
            fig1 = px.bar(
                type_counts,
                x='Property Type',
                y='Count',
                title='Number of Properties by Type',
                color='Count',
                color_continuous_scale='Blues',
                text='Count'
            )
            
            fig1.update_layout(**create_plotly_theme())
            fig1.update_traces(texttemplate='%{text}', textposition='outside')
            
            st.plotly_chart(fig1, use_container_width=True)
        else:
            st.info("Property type data not available")
    
    with col2:
        if 'hotel_type' in df.columns:
            fig2 = px.pie(
                type_counts,
                values='Count',
                names='Property Type',
                title='Property Type Mix',
                hole=0.4
            )
            
            fig2.update_traces(textposition='inside', textinfo='percent+label')
            fig2.update_layout(**create_plotly_theme())
            
            st.plotly_chart(fig2, use_container_width=True)
    
    # ========================================================================
    # SECTION 3: RATING DISTRIBUTION
    # ========================================================================
    
    st.markdown("## ⭐ Rating Distribution")
    
    if 'overall_rating' in df.columns:
        col1, col2 = st.columns(2)
        
        with col1:
            fig3 = px.histogram(
                df,
                x='overall_rating',
                nbins=20,
                title='Distribution of Property Ratings',
                labels={'overall_rating': 'Rating', 'count': 'Number of Properties'},
                color_discrete_sequence=['#3b82f6']
            )
            
            fig3.update_layout(**create_plotly_theme())
            fig3.add_vline(
                x=avg_rating,
                line_dash="dash",
                line_color="#f59e0b",
                annotation_text=f"Mean: {avg_rating:.2f}",
                annotation_font_color="#f59e0b"
            )
            
            st.plotly_chart(fig3, use_container_width=True)
        
        with col2:
            if 'hotel_type' in df.columns:
                fig4 = px.box(
                    df,
                    x='hotel_type',
                    y='overall_rating',
                    title='Rating Distribution by Property Type',
                    color='hotel_type',
                    labels={'overall_rating': 'Rating', 'hotel_type': 'Property Type'}
                )
                
                fig4.update_layout(**create_plotly_theme())
                fig4.update_layout(showlegend=False)
                
                st.plotly_chart(fig4, use_container_width=True)
    
    # ========================================================================
    # SECTION 4: PRICE OVERVIEW
    # ========================================================================
    
    st.markdown("## 💵 Price Range Overview")
    
    if 'price_per_night' in df.columns:
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric(
                "Minimum Price",
                format_currency(df['price_per_night'].min()),
                help="Lowest price in the dataset"
            )
        
        with col2:
            st.metric(
                "Median Price",
                format_currency(df['price_per_night'].median()),
                help="Middle value - 50% of properties are cheaper"
            )
        
        with col3:
            st.metric(
                "Maximum Price",
                format_currency(df['price_per_night'].max()),
                help="Highest price in the dataset"
            )
        
        if 'price_category' in df.columns:
            st.markdown("### 📊 Price Segmentation")
            
            category_counts = df['price_category'].value_counts().reset_index()
            category_counts.columns = ['Price Category', 'Count']
            
            fig5 = px.bar(
                category_counts,
                x='Price Category',
                y='Count',
                title='Number of Properties by Price Segment',
                color='Price Category',
                color_discrete_map={
                    'Budget': '#22c55e',
                    'Mid-Range': '#3b82f6',
                    'Premium': '#f59e0b',
                    'Luxury': '#ef4444'
                }
            )
            
            fig5.update_layout(**create_plotly_theme())
            fig5.update_layout(showlegend=False)
            
            st.plotly_chart(fig5, use_container_width=True)
    
    # ========================================================================
    # SECTION 5: KEY INSIGHTS - FIXED
    # ========================================================================
    
    st.markdown("## 💡 Market Insights")
    
    insights = generate_insights(df)
    
    if insights and len(insights) > 0:
        create_insight_box(insights, title="💡 Key Takeaways")
    else:
        st.info("Analyzing market data...")
    
    # ========================================================================
    # SECTION 6: DATA QUALITY SUMMARY
    # ========================================================================
    
    with st.expander("📋 Data Quality Summary"):
        st.markdown("### Dataset Completeness")
        
        missing_data = pd.DataFrame({
            'Column': df.columns,
            'Missing Values': df.isnull().sum(),
            'Missing %': (df.isnull().sum() / len(df) * 100).round(2)
        })
        missing_data = missing_data[missing_data['Missing Values'] > 0].sort_values('Missing %', ascending=False)
        
        if len(missing_data) > 0:
            st.dataframe(missing_data, use_container_width=True)
        else:
            st.success("✅ No missing values detected in the dataset!")
        
        st.markdown("### Dataset Shape")
        st.write(f"**Rows:** {len(df):,} | **Columns:** {len(df.columns)}")


def generate_insights(df: pd.DataFrame) -> list:
    """Generate data-driven insights - FIXED to always return insights"""
    
    insights = []
    
    try:
        # Market size insight
        total_properties = len(df)
        insights.append(f"Dubai's hotel market contains **{total_properties:,} properties** across various segments")
        
        # Price insight
        if 'price_per_night' in df.columns and len(df) > 0:
            avg_price = df['price_per_night'].mean()
            median_price = df['price_per_night'].median()
            
            if avg_price > median_price * 1.2:
                insights.append(f"Market shows **positive skew** - luxury properties drive average price (AED {avg_price:.0f}) above median (AED {median_price:.0f})")
            else:
                insights.append(f"Pricing is **well-distributed** with average (AED {avg_price:.0f}) close to median (AED {median_price:.0f})")
        
        # Rating insight
        if 'overall_rating' in df.columns and len(df) > 0:
            high_rated = (df['overall_rating'] >= 4.5).sum()
            high_rated_pct = (high_rated / total_properties * 100)
            insights.append(f"**{high_rated_pct:.1f}%** of properties have excellent ratings (4.5+), indicating strong service quality")
        
        # Property type insight
        if 'hotel_type' in df.columns and len(df) > 0:
            dominant_type = df['hotel_type'].mode()[0]
            dominant_pct = (df['hotel_type'] == dominant_type).sum() / total_properties * 100
            insights.append(f"**{dominant_type}s** dominate the market at {dominant_pct:.1f}% of all properties")
        
        # Availability insight
        if 'availability' in df.columns and len(df) > 0:
            high_avail = (df['availability'] > 300).sum()
            if high_avail > total_properties * 0.3:
                insights.append(f"**{high_avail:,} properties** have high availability (300+ days), suggesting potential oversupply in some segments")
        
        # Add default insight if none generated
        if len(insights) == 0:
            insights = [
                "Dubai offers a diverse range of accommodation options",
                "The market caters to various budget segments and preferences",
                "Use the filters to explore specific property types and price ranges"
            ]
    
    except Exception as e:
        # Fallback insights
        insights = [
            "Dubai offers a diverse range of accommodation options",
            "The market caters to various budget segments",
            "Explore different pages for detailed analysis"
        ]
    
    return insights