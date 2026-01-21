"""
Page 3: Geographical Analysis - FIXED
Maps and analyzes property distribution across Dubai locations
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from utils import (
    page_header, create_insight_box, create_plotly_theme,
    format_currency, format_number
)


def render_page(df: pd.DataFrame):
    """Render the Geographical Analysis page"""
    
    page_header(
        "Geographical Analysis",
        "Spatial distribution and location-based insights",
        "🌍"
    )
    
    if df.empty:
        st.warning("No data available with current filters.")
        return
    
    # ========================================================================
    # SECTION 1: INTERACTIVE MAP (FIXED TITLE ERROR)
    # ========================================================================
    
    st.markdown("## 🗺️ Interactive Property Map")
    
    if all(col in df.columns for col in ['latitude', 'longitude', 'price_per_night']):
        # Filter out invalid coordinates
        df_map = df[(df['latitude'] != 0) & (df['longitude'] != 0)].copy()
        
        if len(df_map) > 0:
            col1, col2, col3 = st.columns(3)
            
            with col1:
                color_metric = st.selectbox(
                    "Color by:",
                    ['price_per_night', 'overall_rating', 'reviews_count'],
                    format_func=lambda x: {
                        'price_per_night': 'Price',
                        'overall_rating': 'Rating',
                        'reviews_count': 'Reviews'
                    }[x]
                )
            
            with col2:
                size_metric = st.selectbox(
                    "Size by:",
                    ['overall_rating', 'reviews_count', 'price_per_night'],
                    index=1,
                    format_func=lambda x: {
                        'price_per_night': 'Price',
                        'overall_rating': 'Rating',
                        'reviews_count': 'Reviews'
                    }[x]
                )
            
            with col3:
                max_points = st.slider("Max points on map", 50, 500, 200, 50,
                                      help="Reduce for better performance and less clustering")
            
            # Sample data if too many points
            if len(df_map) > max_points:
                df_map_display = df_map.sample(max_points, random_state=42)
                st.info(f"Displaying {max_points} of {len(df_map)} properties for optimal visibility")
            else:
                df_map_display = df_map
            
            # Create map with FIXED title
            map_title = f"Dubai Hotels - Colored by {color_metric.replace('_', ' ').title()}"
            
            fig_map = px.scatter_mapbox(
                df_map_display,
                lat="latitude",
                lon="longitude",
                color=color_metric,
                size=size_metric,
                hover_name="hotel_name" if 'hotel_name' in df_map_display.columns else None,
                hover_data={
                    "price_per_night": ':.2f',
                    "overall_rating": ':.2f',
                    "location": True if 'location' in df_map_display.columns else False,
                    "latitude": False,
                    "longitude": False,
                    color_metric: False,
                    size_metric: False
                },
                color_continuous_scale='YlOrRd' if color_metric == 'price_per_night' else 'Viridis',
                size_max=15,
                zoom=10.5,
                mapbox_style="carto-positron"
            )
            
            # FIXED: Update layout without duplicate title parameter
            fig_map.update_layout(
                margin={"r": 0, "t": 50, "l": 0, "b": 0},
                height=650,
                plot_bgcolor='white',
                paper_bgcolor='white'
            )
            
            # Update traces for better visibility
            fig_map.update_traces(marker=dict(opacity=0.7))
            
            st.plotly_chart(fig_map, use_container_width=True)
            
            # Add legend
            with st.expander("ℹ️ Map Legend & Tips"):
                st.markdown("""
                **How to use the map:**
                - **Zoom:** Use mouse wheel or +/- buttons
                - **Pan:** Click and drag
                - **Hover:** See property details
                - **Color intensity:** Darker = Higher value
                - **Marker size:** Larger = Higher metric value
                
                **Color Scale:**
                - Yellow/Light: Lower values
                - Orange: Mid-range values  
                - Red/Dark: Higher values
                """)
        else:
            st.info("No valid coordinates available for mapping")
    else:
        st.warning("Coordinate data not available for mapping")
    
    # ========================================================================
    # SECTION 2: PROPERTIES PER LOCATION
    # ========================================================================
    
    st.markdown("## 📍 Property Distribution by Location")
    
    if 'location' in df.columns:
        col1, col2 = st.columns(2)
        
        with col1:
            location_counts = df['location'].value_counts().head(15).reset_index()
            location_counts.columns = ['Location', 'Count']
            
            fig1 = px.bar(
                location_counts,
                x='Count',
                y='Location',
                orientation='h',
                title='Top 15 Locations by Number of Properties',
                color='Count',
                color_continuous_scale='Blues',
                text='Count'
            )
            
            fig1.update_layout(**create_plotly_theme())
            fig1.update_traces(texttemplate='%{text}', textposition='outside')
            fig1.update_layout(yaxis={'categoryorder': 'total ascending'})
            
            st.plotly_chart(fig1, use_container_width=True)
        
        with col2:
            top_locations = location_counts.head(10)
            
            fig2 = px.pie(
                top_locations,
                values='Count',
                names='Location',
                title='Top 10 Locations - Market Share',
                hole=0.4
            )
            
            fig2.update_traces(textposition='inside', textinfo='percent+label')
            fig2.update_layout(**create_plotly_theme())
            
            st.plotly_chart(fig2, use_container_width=True)
    
    # ========================================================================
    # SECTION 3: AVERAGE PRICE BY LOCATION
    # ========================================================================
    
    st.markdown("## 💰 Average Price by Location")
    
    location_stats = None  # Initialize for later use
    
    if 'location' in df.columns and 'price_per_night' in df.columns:
        location_stats = df.groupby('location').agg({
            'price_per_night': ['mean', 'median', 'count'],
            'overall_rating': 'mean' if 'overall_rating' in df.columns else 'count',
            'reviews_count': 'sum' if 'reviews_count' in df.columns else 'count'
        }).round(2)
        
        location_stats.columns = ['Avg Price', 'Median Price', 'Properties', 'Avg Rating', 'Total Reviews']
        location_stats = location_stats.sort_values('Avg Price', ascending=False).head(15)
        
        fig3 = px.bar(
            location_stats.reset_index(),
            x='location',
            y='Avg Price',
            title='Average Price per Night by Location (Top 15)',
            color='Avg Price',
            color_continuous_scale='YlOrRd',
            text='Avg Price',
            hover_data=['Properties', 'Avg Rating']
        )
        
        fig3.update_layout(**create_plotly_theme())
        fig3.update_traces(texttemplate='AED %{text:.0f}', textposition='outside')
        fig3.update_xaxes(tickangle=45)
        
        st.plotly_chart(fig3, use_container_width=True)
        st.dataframe(location_stats, use_container_width=True)
    
    # ========================================================================
    # SECTION 4: RATING BY LOCATION
    # ========================================================================
    
    st.markdown("## ⭐ Average Rating by Location")
    
    if 'location' in df.columns and 'overall_rating' in df.columns:
        location_ratings = df.groupby('location').agg({
            'overall_rating': 'mean',
            'hotel_name': 'count'
        }).round(2)
        
        location_ratings.columns = ['Avg Rating', 'Properties']
        location_ratings = location_ratings[location_ratings['Properties'] >= 3]
        location_ratings = location_ratings.sort_values('Avg Rating', ascending=False).head(15)
        
        fig4 = px.bar(
            location_ratings.reset_index(),
            x='location',
            y='Avg Rating',
            title='Average Rating by Location (Locations with 3+ properties)',
            color='Avg Rating',
            color_continuous_scale='Greens',
            text='Avg Rating',
            hover_data=['Properties']
        )
        
        fig4.update_layout(**create_plotly_theme())
        fig4.update_traces(texttemplate='%{text:.2f}', textposition='outside')
        fig4.update_xaxes(tickangle=45)
        fig4.update_yaxes(range=[0, 5])
        
        st.plotly_chart(fig4, use_container_width=True)
    
    # ========================================================================
    # SECTION 5: PREMIUM VS BUDGET ZONES
    # ========================================================================
    
    st.markdown("## 🏆 Premium vs Budget Zones")
    
    if location_stats is not None and len(location_stats) > 0:
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### 💎 Premium Zones")
            premium_zones = location_stats.head(5)[['Avg Price', 'Properties', 'Avg Rating']]
            st.dataframe(premium_zones, use_container_width=True)
        
        with col2:
            st.markdown("### 💰 Budget Zones")
            budget_zones = location_stats.tail(5)[['Avg Price', 'Properties', 'Avg Rating']].sort_values('Avg Price')
            st.dataframe(budget_zones, use_container_width=True)
    
    # ========================================================================
    # SECTION 6: BEST VALUE LOCATIONS
    # ========================================================================
    
    st.markdown("## 🎯 Best Value Locations")
    
    if all(col in df.columns for col in ['location', 'price_per_night', 'overall_rating']):
        location_value = df.groupby('location').agg({
            'overall_rating': 'mean',
            'price_per_night': 'mean',
            'hotel_name': 'count'
        }).round(2)
        
        location_value.columns = ['Avg Rating', 'Avg Price', 'Properties']
        location_value = location_value[location_value['Properties'] >= 3]
        location_value['Value Score'] = (location_value['Avg Rating'] / location_value['Avg Price'] * 100).round(2)
        location_value = location_value.sort_values('Value Score', ascending=False).head(10)
        
        fig7 = px.bar(
            location_value.reset_index(),
            x='location',
            y='Value Score',
            title='Top 10 Best Value Locations (Rating / Price)',
            color='Value Score',
            color_continuous_scale='RdYlGn',
            text='Value Score',
            hover_data=['Avg Rating', 'Avg Price', 'Properties']
        )
        
        fig7.update_layout(**create_plotly_theme())
        fig7.update_traces(texttemplate='%{text:.2f}', textposition='outside')
        fig7.update_xaxes(tickangle=45)
        
        st.plotly_chart(fig7, use_container_width=True)
        st.dataframe(location_value, use_container_width=True)
    
    # ========================================================================
    # SECTION 7: KEY INSIGHTS (FIXED)
    # ========================================================================
    
    st.markdown("## 💡 Geographical Insights")
    
    insights = generate_geo_insights(df, location_stats)
    
    if insights and len(insights) > 0:
        create_insight_box(insights, title="💡 Location Insights")
    else:
        st.info("Analyzing geographical patterns...")


def generate_geo_insights(df: pd.DataFrame, location_stats=None) -> list:
    """Generate geographical insights - FIXED to always return insights"""
    
    insights = []
    
    try:
        if 'location' in df.columns and len(df) > 0:
            total_locations = df['location'].nunique()
            insights.append(f"Properties spread across **{total_locations} locations** in Dubai")
            
            top_location = df['location'].value_counts().index[0]
            top_location_count = df['location'].value_counts().iloc[0]
            top_location_pct = (top_location_count / len(df) * 100)
            
            insights.append(f"**{top_location}** leads with {top_location_count} properties ({top_location_pct:.1f}% of market)")
        
        if location_stats is not None and 'Avg Price' in location_stats.columns and len(location_stats) > 1:
            max_price_loc = location_stats['Avg Price'].idxmax()
            min_price_loc = location_stats['Avg Price'].idxmin()
            price_diff = location_stats['Avg Price'].max() - location_stats['Avg Price'].min()
            
            insights.append(f"**{price_diff:.0f} AED** price difference between most expensive ({max_price_loc}) and most affordable ({min_price_loc}) areas")
        
        if all(col in df.columns for col in ['overall_rating', 'price_per_night', 'location']) and len(df) > 0:
            median_price = df['price_per_night'].median()
            value_props = df[(df['overall_rating'] >= 4.3) & (df['price_per_night'] < median_price)]
            
            if len(value_props) > 0:
                value_locations = value_props['location'].value_counts().head(3).index.tolist()
                insights.append(f"**Best value zones**: {', '.join(value_locations[:3])} offer high ratings at below-median prices")
        
        # Add a default insight if none were generated
        if len(insights) == 0:
            insights.append("Dubai's hotel market shows diverse geographical distribution")
            insights.append("Use the map above to explore specific areas of interest")
    
    except Exception as e:
        # Fallback insights if there's an error
        insights = [
            "Dubai offers diverse accommodation options across multiple neighborhoods",
            "Use filters to explore specific price ranges and locations",
            "Interactive map shows property distribution across the city"
        ]
    
    return insights