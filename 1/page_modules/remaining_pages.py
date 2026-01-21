"""
Consolidated Remaining Pages Module
Contains: Room & Amenities, Host Analysis, Time & Seasonality, Rating & Value
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from utils import (
    page_header, create_insight_box, create_plotly_theme,
    display_dataframe_with_download, format_currency
)

# ============================================================================
# ROOM & AMENITIES ANALYSIS (Page 4)
# ============================================================================

def render_room_amenities_page(df):
    """Page 4: Room Type & Amenities Analysis"""
    
    page_header("Rooms & Amenities Analysis", "Understanding room types and amenity impact on pricing", "🛏️")
    
    if df.empty:
        st.warning("No data available")
        return
    
    # Room Type Distribution
    st.markdown("## 🛏️ Room Type Analysis")
    
    if 'room_type' in df.columns:
        col1, col2 = st.columns(2)
        
        with col1:
            room_dist = df['room_type'].value_counts().reset_index()
            room_dist.columns = ['Room Type', 'Count']
            
            fig = px.bar(room_dist, x='Room Type', y='Count', title='Room Type Distribution',
                        color='Count', color_continuous_scale='Blues', text='Count')
            fig.update_layout(**create_plotly_theme())
            fig.update_traces(texttemplate='%{text}', textposition='outside')
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            if 'price_per_night' in df.columns:
                room_price = df.groupby('room_type')['price_per_night'].mean().sort_values(ascending=False).reset_index()
                
                fig = px.bar(room_price, x='room_type', y='price_per_night',
                           title='Average Price by Room Type', color='price_per_night',
                           color_continuous_scale='YlOrRd', text='price_per_night')
                fig.update_layout(**create_plotly_theme())
                fig.update_traces(texttemplate='AED %{text:.2f}', textposition='outside')
                st.plotly_chart(fig, use_container_width=True)
    
    # Amenities Analysis
    st.markdown("## 🎯 Amenities Impact Analysis")
    
    amenity_columns = ['wifi', 'pool', 'parking', 'gym', 'spa', 'breakfast', 'restaurant']
    available_amenities = [col for col in amenity_columns if col in df.columns]
    
    if available_amenities and 'price_per_night' in df.columns:
        col1, col2 = st.columns(2)
        
        with col1:
            amenity_counts = {am: df[am].sum() for am in available_amenities}
            amenity_df = pd.DataFrame(list(amenity_counts.items()), columns=['Amenity', 'Count'])
            amenity_df = amenity_df.sort_values('Count', ascending=False)
            
            fig = px.bar(amenity_df, x='Amenity', y='Count', title='Most Common Amenities',
                        color='Count', color_continuous_scale='Greens', text='Count')
            fig.update_layout(**create_plotly_theme())
            fig.update_traces(texttemplate='%{text}', textposition='outside')
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            price_impact = {}
            for amenity in available_amenities:
                with_amenity = df[df[amenity] == 1]['price_per_night'].mean()
                without_amenity = df[df[amenity] == 0]['price_per_night'].mean()
                price_impact[amenity] = with_amenity - without_amenity
            
            impact_df = pd.DataFrame(list(price_impact.items()), columns=['Amenity', 'Price Impact'])
            impact_df = impact_df.sort_values('Price Impact', ascending=False)
            
            fig = px.bar(impact_df, x='Amenity', y='Price Impact',
                        title='Amenity Price Premium (AED)', color='Price Impact',
                        color_continuous_scale='RdYlGn', text='Price Impact')
            fig.update_layout(**create_plotly_theme())
            fig.update_traces(texttemplate='AED %{text:.2f}', textposition='outside')
            st.plotly_chart(fig, use_container_width=True)
        
        if len(impact_df) > 0:
            top_amenity = impact_df.iloc[0]
            insights = [
                f"**{top_amenity['Amenity'].title()}** has the highest price premium at AED {top_amenity['Price Impact']:.2f}",
                f"**{amenity_df.iloc[0]['Amenity'].title()}** is the most common amenity ({amenity_df.iloc[0]['Count']:.0f} properties)",
            ]
            create_insight_box(insights)


# ============================================================================
# HOST ANALYSIS (Page 5) - COMPLETELY FIXED
# ============================================================================

def render_host_analysis_page(df):
    """Page 5: Host / Property Owner Analysis - FIXED FULL WIDTH"""
    
    page_header("Host Analysis", "Understanding host performance and professional vs individual operators", "👤")
    
    if df.empty:
        st.warning("No data available")
        return
    
    # Host listings count
    if 'host_listings_count' in df.columns:
        st.markdown("## 📊 Host Portfolio Size Distribution")
        
        col1, col2 = st.columns(2)
        
        with col1:
            if 'host_type' in df.columns:
                host_type_dist = df['host_type'].value_counts().reset_index()
                host_type_dist.columns = ['Host Type', 'Count']
                
                fig = px.pie(host_type_dist, values='Count', names='Host Type',
                           title='Distribution of Host Types', hole=0.4)
                fig.update_layout(**create_plotly_theme())
                st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            if 'host_type' in df.columns:
                # Bar chart showing host type counts
                fig2 = px.bar(
                    host_type_dist.sort_values('Count', ascending=True),
                    x='Count',
                    y='Host Type',
                    orientation='h',
                    title='Host Type Breakdown',
                    color='Count',
                    color_continuous_scale='Purples',
                    text='Count'
                )
                fig2.update_layout(**create_plotly_theme())
                fig2.update_traces(texttemplate='%{text}', textposition='outside')
                st.plotly_chart(fig2, use_container_width=True)
        
        # Top hosts by listings - FULL WIDTH
        if 'host_name' in df.columns or 'host_id' in df.columns:
            st.markdown("### 🏆 Top 10 Hosts by Portfolio Size")
            
            host_col = 'host_name' if 'host_name' in df.columns else 'host_id'
            top_hosts = df.groupby(host_col).size().sort_values(ascending=False).head(10).reset_index()
            top_hosts.columns = ['Host', 'Properties']
            
            fig = px.bar(top_hosts, x='Properties', y='Host', orientation='h',
                       title='Top Property Owners',
                       color='Properties',
                       color_continuous_scale='Blues',
                       text='Properties')
            fig.update_layout(**create_plotly_theme())
            fig.update_layout(
                yaxis={'categoryorder': 'total ascending'},
                height=400
            )
            fig.update_traces(texttemplate='%{text}', textposition='outside')
            st.plotly_chart(fig, use_container_width=True)
    
    # CRITICAL FIX: Host experience vs ratings - FULL WIDTH, NO COLUMNS
    if all(col in df.columns for col in ['host_listings_count', 'overall_rating']):
        st.markdown("## ⭐ Host Experience vs Quality")
        
        # Don't use columns - use full width directly
        fig = px.scatter(
            df, 
            x='host_listings_count', 
            y='overall_rating',
            title='Host Portfolio Size vs Average Rating',
            trendline='ols', 
            color='price_per_night' if 'price_per_night' in df.columns else None,
            labels={
                'host_listings_count': 'Number of Listings', 
                'overall_rating': 'Rating'
            },
            hover_data=['hotel_name'] if 'hotel_name' in df.columns else None,
            color_continuous_scale='Viridis'
        )
        
        # Apply theme and set dimensions
        fig.update_layout(**create_plotly_theme())
        fig.update_layout(
            height=600,  # Taller chart
            autosize=True,
            margin=dict(l=50, r=50, t=80, b=50)
        )
        
        # CRITICAL: Full container width
        st.plotly_chart(fig, use_container_width=True)
        
        # Analysis by host type
        if 'host_type' in df.columns:
            st.markdown("## 📈 Performance by Host Type")
            
            host_performance = df.groupby('host_type').agg({
                'overall_rating': 'mean',
                'price_per_night': 'mean' if 'price_per_night' in df.columns else 'count',
                'reviews_count': 'mean' if 'reviews_count' in df.columns else 'count',
                'hotel_name': 'count'
            }).round(2)
            host_performance.columns = ['Avg Rating', 'Avg Price', 'Avg Reviews', 'Properties']
            
            st.dataframe(host_performance, use_container_width=True)
            
            # Generate insights
            if len(host_performance) > 0:
                best_type = host_performance['Avg Rating'].idxmax()
                insights = [
                    f"**{best_type}** hosts have the highest average rating ({host_performance.loc[best_type, 'Avg Rating']:.2f})",
                ]
                
                if 'Professional' in host_performance.index:
                    insights.append(f"Professional hosts manage an average of {host_performance.loc['Professional', 'Properties']:.0f} properties")
                else:
                    insights.append("Various host types serve different market segments")
                
                create_insight_box(insights)


# ============================================================================
# TIME & SEASONALITY (Page 6)
# ============================================================================

def render_time_seasonality_page(df):
    """Page 6: Time, Availability & Seasonality Analysis"""
    
    page_header("Time & Seasonality Analysis", "Understanding temporal patterns and seasonal trends", "📅")
    
    if df.empty:
        st.warning("No data available")
        return
    
    if 'availability' in df.columns:
        st.markdown("## 📊 Availability Distribution")
        
        col1, col2 = st.columns(2)
        
        with col1:
            fig = px.histogram(df, x='availability', nbins=30,
                             title='Property Availability Distribution',
                             labels={'availability': 'Days Available', 'count': 'Properties'},
                             color_discrete_sequence=['#3b82f6'])
            fig.update_layout(**create_plotly_theme())
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            df_temp = df.copy()
            df_temp['occupancy_rate'] = ((365 - df_temp['availability']) / 365 * 100).clip(0, 100)
            
            fig = px.box(df_temp, y='occupancy_rate',
                        title='Estimated Occupancy Rate Distribution',
                        labels={'occupancy_rate': 'Occupancy Rate (%)'})
            fig.update_layout(**create_plotly_theme())
            st.plotly_chart(fig, use_container_width=True)
    
    # FULL WIDTH CHART
    if all(col in df.columns for col in ['availability', 'price_per_night']):
        st.markdown("## 💰 Availability vs Price Relationship")
        
        df_temp = df.copy()
        df_temp['occupancy_rate'] = ((365 - df_temp['availability']) / 365 * 100).clip(0, 100)
        
        fig = px.scatter(df_temp, x='price_per_night', y='occupancy_rate',
                        title='Price vs Occupancy Rate',
                        trendline='ols',
                        color='overall_rating' if 'overall_rating' in df.columns else None,
                        labels={'price_per_night': 'Price per Night (AED)', 'occupancy_rate': 'Occupancy Rate (%)'})
        fig.update_layout(**create_plotly_theme())
        fig.update_layout(height=600, autosize=True)
        st.plotly_chart(fig, use_container_width=True)
    
    insights = []
    if 'availability' in df.columns:
        high_avail = (df['availability'] > 300).sum()
        low_avail = (df['availability'] < 90).sum()
        insights.append(f"**{high_avail}** properties have high availability (300+ days), **{low_avail}** are in high demand (<90 days)")
    
    if insights:
        create_insight_box(insights)


# ============================================================================
# RATING & VALUE ANALYSIS (Page 7)
# ============================================================================

def render_rating_value_page(df):
    """Page 7: Rating, Popularity & Value Analysis"""
    
    page_header("Rating & Value Analysis", "Identifying top performers and hidden gems", "⭐")
    
    if df.empty:
        st.warning("No data available")
        return
    
    if 'overall_rating' in df.columns:
        st.markdown("## ⭐ Rating Distribution")
        
        col1, col2 = st.columns(2)
        
        with col1:
            fig = px.histogram(df, x='overall_rating', nbins=25,
                             title='Property Rating Distribution',
                             marginal='box',
                             color_discrete_sequence=['#3b82f6'])
            fig.update_layout(**create_plotly_theme())
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            if 'rating_category' in df.columns:
                rating_cat_dist = df['rating_category'].value_counts().reset_index()
                rating_cat_dist.columns = ['Rating Category', 'Count']
                
                fig = px.pie(rating_cat_dist, values='Count', names='Rating Category',
                           title='Rating Category Distribution', hole=0.4)
                fig.update_layout(**create_plotly_theme())
                st.plotly_chart(fig, use_container_width=True)
    
    # FULL WIDTH CHART
    if all(col in df.columns for col in ['reviews_count', 'overall_rating']):
        st.markdown("## 📊 Popularity vs Quality")
        
        fig = px.scatter(df, x='reviews_count', y='overall_rating',
                        title='Review Count vs Rating',
                        color='price_per_night' if 'price_per_night' in df.columns else None,
                        size='price_per_night' if 'price_per_night' in df.columns else None,
                        hover_name='hotel_name' if 'hotel_name' in df.columns else None,
                        trendline='ols')
        fig.update_layout(**create_plotly_theme())
        fig.update_layout(height=600, autosize=True)
        st.plotly_chart(fig, use_container_width=True)
    
    if 'overall_rating' in df.columns:
        st.markdown("## 🏆 Top Rated Properties")
        
        top_rated = df.nlargest(10, 'overall_rating')[[
            col for col in ['hotel_name', 'overall_rating', 'reviews_count', 'price_per_night', 'location']
            if col in df.columns
        ]]
        
        st.dataframe(top_rated, use_container_width=True)
    
    if 'value_score' in df.columns:
        st.markdown("## 💎 Best Value Properties")
        
        col1, col2 = st.columns(2)
        
        with col1:
            fig = px.histogram(df, x='value_score', nbins=30,
                             title='Value Score Distribution',
                             labels={'value_score': 'Value Score', 'count': 'Properties'},
                             color_discrete_sequence=['#22c55e'])
            fig.update_layout(**create_plotly_theme())
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            top_value = df.nlargest(10, 'value_score')[[
                col for col in ['hotel_name', 'value_score', 'overall_rating', 'price_per_night', 'location']
                if col in df.columns
            ]]
            
            st.markdown("### Top 10 Best Value Stays")
            display_dataframe_with_download(top_value, 'best_value_properties.csv', key='value_download')
    
    if all(col in df.columns for col in ['overall_rating', 'price_per_night', 'reviews_count']):
        st.markdown("## 💎 Hidden Gems")
        st.info("High quality properties with fewer reviews - potentially undiscovered value")
        
        median_reviews = df['reviews_count'].median()
        hidden_gems = df[
            (df['overall_rating'] >= 4.5) &
            (df['reviews_count'] < median_reviews) &
            (df['price_per_night'] < df['price_per_night'].median())
        ]
        
        if len(hidden_gems) > 0:
            hidden_gems_display = hidden_gems.nlargest(10, 'overall_rating')[[
                col for col in ['hotel_name', 'overall_rating', 'reviews_count', 'price_per_night', 'location']
                if col in hidden_gems.columns
            ]]
            
            st.dataframe(hidden_gems_display, use_container_width=True)
            
            insights = [
                f"Found **{len(hidden_gems)} hidden gems** - high-rated properties with below-median reviews and prices",
                f"Average rating: **{hidden_gems['overall_rating'].mean():.2f}**",
                f"Average price: **AED {hidden_gems['price_per_night'].mean():.2f}** vs market avg **AED {df['price_per_night'].mean():.2f}**"
            ]
            create_insight_box(insights)
        else:
            st.info("No hidden gems found with current filters")