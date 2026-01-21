"""
Dubai Hotel Analytics Dashboard - Main Application
With Real-time Data Fetching via SerpAPI
"""

import streamlit as st
import pandas as pd
from datetime import datetime
import sys
import os

# ============================================================================
# PAGE CONFIGURATION (Must be first Streamlit command)
# ============================================================================

st.set_page_config(
    page_title="Dubai Hotel Analytics Dashboard",
    page_icon="🏨",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': None,
        'Report a bug': None,
        'About': "Dubai Hotel Analytics Dashboard - Professional Portfolio Project with Live Data Integration"
    }
)

# ============================================================================
# IMPORT MODULES WITH ERROR HANDLING
# ============================================================================

# Add page_modules directory to Python path
pages_path = os.path.join(os.path.dirname(__file__), 'page_modules')
if os.path.exists(pages_path) and pages_path not in sys.path:
    sys.path.insert(0, pages_path)

# Import authentication module
try:
    import auth
except ImportError as e:
    st.error(f"Cannot import auth module: {e}")
    st.stop()

# Import data loader, utils, and SerpAPI fetcher
try:
    import data_loader
    import utils
    import serpapi_fetcher
except ImportError as e:
    st.error(f"Cannot import required modules: {e}")
    st.stop()

# Apply styling
utils.apply_custom_styling()

# --- FIXED IMPORT SECTION (Simplified) ---
try:
    # Import directly from page_modules since we know it exists
    from page_modules import overview, price_demand, geographical, remaining_pages, notes
    
    # Store modules in a dictionary for easy access
    page_modules = {
        'overview': overview,
        'price_demand': price_demand,
        'geographical': geographical,
        'remaining': remaining_pages,
        'notes': notes
    }

except ImportError as e:
    st.error(f"❌ Critical Error: Could not import page modules.")
    st.error(f"Details: {e}")
    st.stop()
# ------------------------------------------

# ============================================================================
# MAIN APPLICATION
# ============================================================================

def render_sidebar():
    """Render sidebar navigation and filters"""
    
    with st.sidebar:
        st.markdown("""
        <div style='text-align: center; padding: 20px;'>
            <h1 style='color: #60a5fa; margin: 0;'>🏨</h1>
            <h2 style='margin: 10px 0; color: #f1f5f9;'>Dubai Hotels</h2>
            <p style='color: #94a3b8; font-size: 14px;'>Analytics Dashboard</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Data source indicator
        data_source = st.session_state.get('data_source', 'demo')
        if data_source == 'live_api':
            st.success("🔴 LIVE DATA")
        else:
            st.info("📊 DEMO DATA")
        
        st.markdown("---")
        
        # Page navigation
        st.markdown("### 📊 Navigation")
        
        page = st.radio(
            "Select Analysis Page:",
            [
                "🔍 Fetch Live Data",
                "📈 Overview & Insights",
                "💰 Price & Demand Analysis",
                "🌍 Geographical Analysis",
                "🛏️ Rooms & Amenities",
                "👤 Host Analysis",
                "📅 Time & Seasonality",
                "⭐ Rating & Value Analysis",
                "📘 Notes & Methodology"
            ],
            label_visibility="collapsed"
        )
        
        st.markdown("---")
        
        # Global filters (Show for all pages EXCEPT Fetch Live Data and Notes)
        if page != "🔍 Fetch Live Data" and page != "📘 Notes & Methodology":
            st.markdown("### 🎛️ Global Filters")
            
            st.markdown("**Price Range (AED)**")
            col1, col2 = st.columns(2)
            with col1:
                price_min = st.number_input("Min", min_value=0, value=0, step=50, key="price_min")
            with col2:
                price_max = st.number_input("Max", min_value=0, value=10000, step=50, key="price_max")
            
            min_rating = st.slider("Minimum Rating", 0.0, 5.0, 0.0, 0.5)
        else:
            price_min = 0
            price_max = 10000
            min_rating = 0.0
        
        # User info
        auth.render_user_info()
        
        st.markdown("---")
        
        st.markdown("### ℹ️ About")
        st.info("""
        **Dubai Hotel Analytics**
        
        Professional analytics dashboard with **live data fetching**.
        
        Built with Python, Streamlit, Plotly & SerpAPI
        """)
        
        st.markdown("---")
        st.markdown(
            f"<p style='text-align: center; color: #64748b; font-size: 12px;'>"
            f"© {datetime.now().year} | Portfolio Project"
            "</p>",
            unsafe_allow_html=True
        )
    
    return page, price_min, price_max, min_rating


def load_and_filter_data(price_min, price_max, min_rating):
    """Load and apply filters to data"""
    
    # Check if we have fetched data
    if 'fetched_data' in st.session_state and not st.session_state['fetched_data'].empty:
        df = st.session_state['fetched_data'].copy()
        # Clean fetched data if needed
        df = data_loader.load_and_preprocess_data()
    else:
        # Load demo data
        try:
            with st.spinner("Loading hotel data..."):
                df = data_loader.load_and_preprocess_data()
        except Exception as e:
            st.warning(f"Could not load data: {e}. Using demo data.")
            df = data_loader.create_demo_data()
    
    if df.empty:
        st.warning("Dataset is empty. Using demo data.")
        df = data_loader.create_demo_data()
    
    # Apply filters
    df_filtered = df.copy()
    
    if 'price_per_night' in df_filtered.columns:
        df_filtered = df_filtered[
            (df_filtered['price_per_night'] >= price_min) &
            (df_filtered['price_per_night'] <= price_max)
        ]
    
    if 'overall_rating' in df_filtered.columns:
        df_filtered = df_filtered[df_filtered['overall_rating'] >= min_rating]
    
    # Show filter info
    if len(df_filtered) < len(df):
        st.info(f"📊 Showing {len(df_filtered):,} of {len(df):,} properties (filters applied)")
    
    return df_filtered


def route_to_page(page_name, df):
    """Route to the selected page"""
    
    try:
        if page_name == "🔍 Fetch Live Data":
            serpapi_fetcher.render_data_fetch_page()
        
        elif page_name == "📈 Overview & Insights":
            page_modules['overview'].render_page(df)
        
        elif page_name == "💰 Price & Demand Analysis":
            page_modules['price_demand'].render_page(df)
        
        elif page_name == "🌍 Geographical Analysis":
            page_modules['geographical'].render_page(df)
        
        elif page_name == "🛏️ Rooms & Amenities":
            page_modules['remaining'].render_room_amenities_page(df)
        
        elif page_name == "👤 Host Analysis":
            page_modules['remaining'].render_host_analysis_page(df)
        
        elif page_name == "📅 Time & Seasonality":
            page_modules['remaining'].render_time_seasonality_page(df)
        
        elif page_name == "⭐ Rating & Value Analysis":
            page_modules['remaining'].render_rating_value_page(df)

        elif page_name == "📘 Notes & Methodology":
            page_modules['notes'].render_page(df)
    
    except Exception as e:
        st.error(f"Error rendering page: {str(e)}")
        with st.expander("🐛 Show Error Details"):
            st.exception(e)


def main():
    """Main application function"""
    
    # Check authentication
    if not auth.check_authentication():
        auth.render_login_page()
        return
    
    # Render sidebar and get selections
    page, price_min, price_max, min_rating = render_sidebar()
    
    # Case 1: Fetch Page (No data needed)
    if page == "🔍 Fetch Live Data":
        route_to_page(page, pd.DataFrame())
    
    # Case 2: Notes Page (No data needed)
    elif page == "📘 Notes & Methodology":
        route_to_page(page, pd.DataFrame())

    # Case 3: All other pages (Need Data)
    else:
        # Load and filter data
        df_filtered = load_and_filter_data(price_min, price_max, min_rating)
        
        # Store in session state
        st.session_state['df_filtered'] = df_filtered
        
        # Route to selected page
        route_to_page(page, df_filtered)

# ============================================================================
# RUN APPLICATION
# ============================================================================

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        st.error(f"Application Error: {str(e)}")
        with st.expander("🐛 Show Full Error"):
            st.exception(e)