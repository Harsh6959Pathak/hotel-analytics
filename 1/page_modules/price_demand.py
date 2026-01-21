"""
Page 2: Price & Demand Analysis
Analyzes pricing strategies, demand patterns, and price-quality relationships
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from scipy import stats
from utils import (
    page_header, create_insight_box, create_plotly_theme,
    format_currency, calculate_correlation
)


def render_page(df: pd.DataFrame):
    """Render the Price & Demand Analysis page"""
    
    page_header(
        "Price & Demand Analysis",
        "Deep dive into pricing strategies and demand dynamics",
        "💰"
    )
    
    if df.empty:
        st.warning("No data available with current filters.")
        return
    
    # ========================================================================
    # SECTION 1: PRICE DISTRIBUTION
    # ========================================================================
    
    st.markdown("## 💵 Price Distribution Analysis")
    
    if 'price_per_night' in df.columns:
        col1, col2 = st.columns(2)
        
        with col1:
            # Histogram with distribution curve
            fig1 = px.histogram(
                df,
                x='price_per_night',
                nbins=50,
                title='Price Distribution',
                labels={'price_per_night': 'Price per Night (AED)', 'count': 'Frequency'},
                marginal='box',
                color_discrete_sequence=['#3b82f6']
            )
            
            fig1.update_layout(**create_plotly_theme())
            st.plotly_chart(fig1, use_container_width=True)
        
        with col2:
            # Statistics
            st.markdown("### 📊 Price Statistics")
            
            price_stats = {
                'Mean': df['price_per_night'].mean(),
                'Median': df['price_per_night'].median(),
                'Std Dev': df['price_per_night'].std(),
                'Q1 (25%)': df['price_per_night'].quantile(0.25),
                'Q3 (75%)': df['price_per_night'].quantile(0.75),
                'IQR': df['price_per_night'].quantile(0.75) - df['price_per_night'].quantile(0.25),
                'Min': df['price_per_night'].min(),
                'Max': df['price_per_night'].max()
            }
            
            stats_df = pd.DataFrame({
                'Metric': price_stats.keys(),
                'Value (AED)': [f"{v:.2f}" for v in price_stats.values()]
            })
            
            st.dataframe(stats_df, use_container_width=True, hide_index=True)
    
    # ========================================================================
    # SECTION 2: PRICE BY PROPERTY TYPE
    # ========================================================================
    
    st.markdown("## 🏨 Price Comparison by Property Type")
    
    if 'hotel_type' in df.columns and 'price_per_night' in df.columns:
        col1, col2 = st.columns(2)
        
        with col1:
            # Box plot
            fig2 = px.box(
                df,
                x='hotel_type',
                y='price_per_night',
                title='Price Distribution by Property Type',
                color='hotel_type',
                labels={'price_per_night': 'Price per Night (AED)', 'hotel_type': 'Property Type'},
                points='outliers'
            )
            
            fig2.update_layout(**create_plotly_theme())
            fig2.update_layout(showlegend=False)
            st.plotly_chart(fig2, use_container_width=True)
        
        with col2:
            # Average price by type
            avg_price_by_type = df.groupby('hotel_type')['price_per_night'].agg([
                ('Average', 'mean'),
                ('Median', 'median'),
                ('Count', 'count')
            ]).round(2).sort_values('Average', ascending=False)
            
            fig3 = px.bar(
                avg_price_by_type.reset_index(),
                x='hotel_type',
                y='Average',
                title='Average Price by Property Type',
                color='Average',
                color_continuous_scale='YlOrRd',
                text='Average'
            )
            
            fig3.update_layout(**create_plotly_theme())
            fig3.update_traces(texttemplate='AED %{text:.0f}', textposition='outside')
            st.plotly_chart(fig3, use_container_width=True)
        
        st.dataframe(avg_price_by_type, use_container_width=True)
    
    # ========================================================================
    # SECTION 3: PRICE BY ROOM TYPE
    # ========================================================================
    
    st.markdown("## 🛏️ Price Comparison by Room Type")
    
    if 'room_type' in df.columns and 'price_per_night' in df.columns:
        # Violin plot
        fig4 = px.violin(
            df,
            x='room_type',
            y='price_per_night',
            title='Price Distribution by Room Type',
            color='room_type',
            box=True,
            points='outliers'
        )
        
        fig4.update_layout(**create_plotly_theme())
        fig4.update_layout(showlegend=False)
        st.plotly_chart(fig4, use_container_width=True)
        
        # Room type comparison table
        room_comparison = df.groupby('room_type')['price_per_night'].agg([
            ('Average Price', 'mean'),
            ('Median Price', 'median'),
            ('Min Price', 'min'),
            ('Max Price', 'max'),
            ('Properties', 'count')
        ]).round(2).sort_values('Average Price', ascending=False)
        
        st.dataframe(room_comparison, use_container_width=True)
    
    # ========================================================================
    # SECTION 4: PRICE VS RATING CORRELATION
    # ========================================================================
    
    st.markdown("## 📈 Price vs Rating Relationship")
    
    if 'price_per_night' in df.columns and 'overall_rating' in df.columns:
        # Calculate correlation
        correlation = calculate_correlation(df, 'price_per_night', 'overall_rating')
        
        col1, col2 = st.columns([3, 1])
        
        with col1:
            # Scatter plot with trendline
            fig5 = px.scatter(
                df,
                x='price_per_night',
                y='overall_rating',
                title=f'Price vs Rating Correlation (r = {correlation:.3f})',
                color='reviews_count' if 'reviews_count' in df.columns else None,
                size='reviews_count' if 'reviews_count' in df.columns else None,
                trendline='ols',
                labels={
                    'price_per_night': 'Price per Night (AED)',
                    'overall_rating': 'Overall Rating',
                    'reviews_count': 'Reviews'
                },
                hover_data=['hotel_name'] if 'hotel_name' in df.columns else None,
                color_continuous_scale='Viridis'
            )
            
            fig5.update_layout(**create_plotly_theme())
            st.plotly_chart(fig5, use_container_width=True)
        
        with col2:
            st.markdown("### 📊 Correlation")
            
            if correlation is not None:
                if correlation > 0.5:
                    strength = "Strong Positive"
                    color = "green"
                elif correlation > 0.3:
                    strength = "Moderate Positive"
                    color = "blue"
                elif correlation > -0.3:
                    strength = "Weak"
                    color = "gray"
                else:
                    strength = "Negative"
                    color = "red"
                
                st.markdown(f"""
                <div style='background-color: #{color}22; padding: 20px; border-radius: 10px; text-align: center;'>
                    <h2 style='color: {color}; margin: 0;'>{correlation:.3f}</h2>
                    <p style='margin: 10px 0 0 0;'>{strength}</p>
                </div>
                """, unsafe_allow_html=True)
                
                # Interpretation
                if correlation > 0.3:
                    st.info("Higher prices tend to correlate with better ratings")
                elif correlation < -0.1:
                    st.warning("Negative correlation - some budget options are highly rated")
                else:
                    st.info("Weak correlation - price doesn't strongly predict quality")
    
    # ========================================================================
    # SECTION 5: DEMAND ANALYSIS
    # ========================================================================
    
    st.markdown("## 📊 Demand vs Price Analysis")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Price vs Reviews (popularity proxy)
        if 'reviews_count' in df.columns and 'price_per_night' in df.columns:
            fig6 = px.scatter(
                df,
                x='price_per_night',
                y='reviews_count',
                title='Price vs Popularity (Review Count)',
                color='overall_rating' if 'overall_rating' in df.columns else None,
                size='overall_rating' if 'overall_rating' in df.columns else None,
                trendline='ols',
                labels={
                    'price_per_night': 'Price per Night (AED)',
                    'reviews_count': 'Number of Reviews'
                },
                hover_data=['hotel_name'] if 'hotel_name' in df.columns else None
            )
            
            fig6.update_layout(**create_plotly_theme())
            st.plotly_chart(fig6, use_container_width=True)
    
    with col2:
        # Price vs Availability (demand proxy - lower availability = higher demand)
        if 'availability' in df.columns and 'price_per_night' in df.columns:
            # Create demand indicator (inverse of availability)
            df_demand = df.copy()
            df_demand['occupancy_rate'] = 100 - (df_demand['availability'] / 365 * 100)
            
            fig7 = px.scatter(
                df_demand,
                x='price_per_night',
                y='occupancy_rate',
                title='Price vs Demand (Occupancy Rate)',
                color='overall_rating' if 'overall_rating' in df.columns else None,
                trendline='ols',
                labels={
                    'price_per_night': 'Price per Night (AED)',
                    'occupancy_rate': 'Estimated Occupancy Rate (%)'
                },
                hover_data=['hotel_name'] if 'hotel_name' in df.columns else None
            )
            
            fig7.update_layout(**create_plotly_theme())
            st.plotly_chart(fig7, use_container_width=True)
    
    # ========================================================================
    # SECTION 6: PRICE SEGMENTS ANALYSIS
    # ========================================================================
    
    if 'price_category' in df.columns:
        st.markdown("## 🎯 Price Segment Performance")
        
        segment_analysis = df.groupby('price_category').agg({
            'hotel_name': 'count',
            'overall_rating': 'mean',
            'reviews_count': 'sum',
            'availability': 'mean'
        }).round(2)
        
        segment_analysis.columns = ['Properties', 'Avg Rating', 'Total Reviews', 'Avg Availability']
        segment_analysis = segment_analysis.sort_index()
        
        st.dataframe(segment_analysis, use_container_width=True)
    
    # ========================================================================
    # SECTION 7: KEY INSIGHTS
    # ========================================================================
    
    st.markdown("## 💡 Demand & Pricing Insights")
    
    insights = generate_price_insights(df)
    create_insight_box(insights, title="💡 Key Findings")


def generate_price_insights(df: pd.DataFrame) -> list:
    """Generate insights for price and demand analysis"""
    
    insights = []
    
    # Price-rating correlation
    if 'price_per_night' in df.columns and 'overall_rating' in df.columns:
        correlation = calculate_correlation(df, 'price_per_night', 'overall_rating')
        if correlation and correlation > 0.3:
            insights.append(f"**Positive correlation** ({correlation:.2f}) between price and rating - higher prices generally deliver better experiences")
        elif correlation and correlation < 0:
            insights.append("**Inverse relationship** detected - some budget properties outperform premium options")
    
    # Price range
    if 'price_per_night' in df.columns:
        price_range = df['price_per_night'].max() - df['price_per_night'].min()
        insights.append(f"Wide price range of **AED {price_range:.0f}** indicates diverse market segments from budget to ultra-luxury")
    
    # Demand patterns
    if 'reviews_count' in df.columns and 'price_per_night' in df.columns:
        # Find sweet spot - high reviews in mid-price range
        mid_price = df['price_per_night'].quantile([0.4, 0.6])
        mid_range_df = df[(df['price_per_night'] >= mid_price.iloc[0]) & 
                          (df['price_per_night'] <= mid_price.iloc[1])]
        
        if len(mid_range_df) > 0:
            avg_reviews_mid = mid_range_df['reviews_count'].mean()
            avg_reviews_total = df['reviews_count'].mean()
            
            if avg_reviews_mid > avg_reviews_total * 1.2:
                insights.append(f"**Mid-range properties** show highest demand with {avg_reviews_mid:.0f} average reviews vs market average of {avg_reviews_total:.0f}")
    
    # Availability insights
    if 'availability' in df.columns:
        high_avail_pct = (df['availability'] > 300).sum() / len(df) * 100
        if high_avail_pct > 30:
            insights.append(f"**{high_avail_pct:.1f}%** of properties have high availability - potential pricing adjustments could improve occupancy")
    
    return insights