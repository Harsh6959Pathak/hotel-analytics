"""
SerpAPI Integration Module
Allows users to fetch real-time hotel data from Google Hotels
"""

import requests
import pandas as pd
import streamlit as st
from datetime import datetime, timedelta
import time


class SerpAPIFetcher:
    """Handles real-time hotel data fetching from SerpAPI"""
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://serpapi.com/search"
    
    def validate_api_key(self) -> bool:
        """Test if API key is valid"""
        try:
            params = {
                "engine": "google",
                "q": "test",
                "api_key": self.api_key
            }
            response = requests.get(self.base_url, params=params, timeout=10)
            return response.status_code == 200
        except:
            return False
    
    def fetch_hotels(self, location: str, checkin_date: str, checkout_date: str, 
                    adults: int = 2, currency: str = "USD", max_results: int = 20) -> pd.DataFrame:
        """
        Fetch hotel data from Google Hotels via SerpAPI
        
        Args:
            location: City/location name (e.g., "Dubai")
            checkin_date: Check-in date (YYYY-MM-DD)
            checkout_date: Check-out date (YYYY-MM-DD)
            adults: Number of adults
            currency: Currency code (USD, AED, EUR, etc.)
            max_results: Maximum number of hotels to fetch
        
        Returns:
            DataFrame with hotel data
        """
        
        params = {
            "engine": "google_hotels",
            "q": location,
            "check_in_date": checkin_date,
            "check_out_date": checkout_date,
            "adults": adults,
            "currency": currency,
            "gl": "us",
            "hl": "en",
            "api_key": self.api_key
        }
        
        try:
            with st.spinner(f"🔍 Fetching hotels in {location}..."):
                response = requests.get(self.base_url, params=params, timeout=30)
                response.raise_for_status()
                data = response.json()
            
            # Extract properties
            properties = data.get("properties", [])
            
            if not properties:
                st.warning(f"No hotels found in {location}. Try different dates or location.")
                return pd.DataFrame()
            
            # Parse hotel data
            hotels = []
            for idx, prop in enumerate(properties[:max_results]):
                hotel = self._parse_hotel_data(prop, idx)
                hotels.append(hotel)
            
            df = pd.DataFrame(hotels)
            
            # Add metadata
            df['fetch_date'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            df['search_location'] = location
            df['search_checkin'] = checkin_date
            df['search_checkout'] = checkout_date
            
            st.success(f"✅ Successfully fetched {len(df)} hotels!")
            
            return df
        
        except requests.exceptions.RequestException as e:
            st.error(f"❌ API Error: {str(e)}")
            return pd.DataFrame()
        
        except Exception as e:
            st.error(f"❌ Error processing data: {str(e)}")
            return pd.DataFrame()
    
    def _parse_hotel_data(self, prop: dict, index: int) -> dict:
        """Parse individual hotel data from API response"""
        
        # Extract amenities
        amenities_list = prop.get("amenities", [])
        amenities_str = ", ".join(amenities_list) if amenities_list else ""
        
        # Check for specific amenities
        has_wifi = any("wi-fi" in a.lower() or "wifi" in a.lower() for a in amenities_list)
        has_pool = any("pool" in a.lower() for a in amenities_list)
        has_spa = any("spa" in a.lower() for a in amenities_list)
        has_gym = any("gym" in a.lower() or "fitness" in a.lower() for a in amenities_list)
        has_parking = any("parking" in a.lower() for a in amenities_list)
        has_breakfast = any("breakfast" in a.lower() for a in amenities_list)
        has_restaurant = any("restaurant" in a.lower() for a in amenities_list)
        
        # Extract price
        rate_info = prop.get("rate_per_night", {})
        price = rate_info.get("extracted_lowest", 0)
        if not price:
            price_str = rate_info.get("lowest", "0")
            try:
                price = float(price_str.replace("$", "").replace(",", "").strip())
            except:
                price = 0
        
        # Extract coordinates
        gps = prop.get("gps_coordinates", {})
        latitude = gps.get("latitude", 25.2048)
        longitude = gps.get("longitude", 55.2708)
        
        # Build hotel record
        hotel = {
            'hotel_name': prop.get("name", f"Hotel {index + 1}"),
            'price_per_night': price,
            'overall_rating': float(prop.get("overall_rating", 0)),
            'reviews_count': int(prop.get("reviews", 0)),
            'hotel_type': prop.get("type", "Hotel"),
            'location': prop.get("description", "Dubai"),
            'latitude': latitude,
            'longitude': longitude,
            'link': prop.get("link", ""),
            
            # Amenities
            'all_amenities': amenities_str,
            'total_amenities_count': len(amenities_list),
            'wifi': int(has_wifi),
            'pool': int(has_pool),
            'spa': int(has_spa),
            'gym': int(has_gym),
            'parking': int(has_parking),
            'breakfast': int(has_breakfast),
            'restaurant': int(has_restaurant),
            
            # Additional info
            'deal_description': prop.get("deal", ""),
            'room_type': 'Entire Place',  # Default
            'availability': 180,  # Default
            'minimum_nights': 1,
            'host_listings_count': 1,
        }
        
        return hotel
    
    def get_available_currencies(self) -> list:
        """Return list of supported currencies"""
        return ["USD", "AED", "EUR", "GBP", "INR", "JPY", "CAD", "AUD"]
    
    def estimate_api_cost(self, num_searches: int) -> str:
        """Estimate API cost for given number of searches"""
        # SerpAPI pricing: ~$50 for 5000 searches
        cost_per_search = 0.01
        total_cost = num_searches * cost_per_search
        return f"${total_cost:.2f}"


def render_data_fetch_page():
    """Render the data fetching interface"""
    import streamlit as st
    
    st.markdown("""
    <div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                padding: 30px; border-radius: 12px; margin-bottom: 30px; color: white;'>
        <h1 style='margin: 0; color: white; font-size: 36px;'>🔍 Fetch Live Hotel Data</h1>
        <p style='margin: 10px 0 0 0; font-size: 16px; opacity: 0.9;'>
            Search real-time hotel data from Google Hotels using SerpAPI
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Check if API key exists in session
    if 'serpapi_key' not in st.session_state:
        st.session_state['serpapi_key'] = ""
    
    # API Key input section
    st.markdown("## 🔑 API Configuration")
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        api_key = st.text_input(
            "Enter your SerpAPI Key",
            value=st.session_state['serpapi_key'],
            type="password",
            help="Get your free API key at https://serpapi.com"
        )
        
        if api_key:
            st.session_state['serpapi_key'] = api_key
    
    with col2:
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("🔐 Validate Key", use_container_width=True):
            if api_key:
                fetcher = SerpAPIFetcher(api_key)
                if fetcher.validate_api_key():
                    st.success("✅ API Key Valid!")
                else:
                    st.error("❌ Invalid API Key")
            else:
                st.warning("Please enter API key")
    
    # Info box
    with st.expander("ℹ️ How to get a SerpAPI Key"):
        st.markdown("""
        **Getting your SerpAPI Key (Free):**
        
        1. Visit [https://serpapi.com](https://serpapi.com)
        2. Click "Register" (top right)
        3. Sign up with email
        4. Go to Dashboard → API Key
        5. Copy your key and paste above
        
        **Free Plan Includes:**
        - ✅ 100 searches per month
        - ✅ No credit card required
        - ✅ Full access to Google Hotels data
        
        **Pricing:**
        - Free: 100 searches/month
        - Developer: $50/month (5,000 searches)
        - Production: $250/month (30,000 searches)
        """)
    
    st.markdown("---")
    
    # Search parameters section
    if api_key:
        st.markdown("## 🔍 Search Parameters")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            location = st.text_input(
                "📍 Location",
                value="Dubai",
                help="City or region name (e.g., 'Dubai', 'New York', 'Paris')"
            )
            
            checkin_date = st.date_input(
                "📅 Check-in Date",
                value=datetime.now() + timedelta(days=7),
                min_value=datetime.now()
            )
        
        with col2:
            currency = st.selectbox(
                "💵 Currency",
                ["USD", "AED", "EUR", "GBP", "INR", "JPY", "CAD", "AUD"],
                index=1  # AED default
            )
            
            checkout_date = st.date_input(
                "📅 Check-out Date",
                value=datetime.now() + timedelta(days=10),
                min_value=datetime.now() + timedelta(days=1)
            )
        
        with col3:
            adults = st.number_input(
                "👥 Number of Adults",
                min_value=1,
                max_value=10,
                value=2
            )
            
            max_results = st.slider(
                "🏨 Max Hotels",
                min_value=10,
                max_value=100,
                value=50,
                step=10,
                help="More hotels = longer fetch time"
            )
        
        # Validate dates
        if checkout_date <= checkin_date:
            st.error("⚠️ Check-out date must be after check-in date")
            return
        
        # Cost estimate
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("API Cost (Estimate)", f"${0.01:.2f}")
        with col2:
            st.metric("Fetch Time (Estimate)", f"~{5} seconds")
        with col3:
            nights = (checkout_date - checkin_date).days
            st.metric("Trip Duration", f"{nights} nights")
        
        st.markdown("---")
        
        # Fetch button
        col1, col2, col3 = st.columns([1, 1, 1])
        with col2:
            fetch_button = st.button(
                "🚀 Fetch Hotels",
                use_container_width=True,
                type="primary"
            )
        
        if fetch_button:
            # Validate inputs
            if not location.strip():
                st.error("Please enter a location")
                return
            
            # Create fetcher
            fetcher = SerpAPIFetcher(api_key)
            
            # Fetch data
            df = fetcher.fetch_hotels(
                location=location,
                checkin_date=checkin_date.strftime('%Y-%m-%d'),
                checkout_date=checkout_date.strftime('%Y-%m-%d'),
                adults=adults,
                currency=currency,
                max_results=max_results
            )
            
            if not df.empty:
                # Store in session state
                st.session_state['fetched_data'] = df
                st.session_state['data_source'] = 'live_api'
                
                # Show preview
                st.markdown("## ✅ Data Fetched Successfully!")
                
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    st.metric("Hotels Found", len(df))
                with col2:
                    st.metric("Avg Price", f"{currency} {df['price_per_night'].mean():.2f}")
                with col3:
                    st.metric("Avg Rating", f"{df['overall_rating'].mean():.2f}")
                with col4:
                    st.metric("Locations", df['location'].nunique())
                
                # Data preview
                st.markdown("### 📊 Data Preview")
                st.dataframe(
                    df[['hotel_name', 'price_per_night', 'overall_rating', 'location']].head(10),
                    use_container_width=True
                )
                
                # Download option
                csv = df.to_csv(index=False)
                st.download_button(
                    label="📥 Download Full Dataset (CSV)",
                    data=csv,
                    file_name=f"hotels_{location}_{checkin_date}.csv",
                    mime="text/csv"
                )
                
                st.success("💡 Data saved! Go to any analysis page to explore your fetched hotels.")
    
    else:
        st.info("👆 Please enter your SerpAPI key to start fetching live hotel data")
        
        # Show demo
        st.markdown("## 🎬 Demo Mode")
        st.markdown("""
        Without an API key, you can:
        - Use the **demo dataset** (500 pre-loaded hotels)
        - Explore all analysis features
        - See how the dashboard works
        
        **To fetch live data:**
        1. Get free API key from serpapi.com
        2. Enter it above
        3. Search any city worldwide!
        """)