import streamlit as st

def render_page(df=None):
    """
    Render the Notes & Methodology Page 
    Matches the style of the reference screenshot
    """
    
    # Main Title with Icon
    st.title("📘 Dashboard Notes & Methodology")
    st.markdown("---")

    # 1. What This Dashboard Shows
    st.subheader("🔍 What This Dashboard Shows")
    st.markdown("""
    This dashboard provides **price analysis, demand estimation, value scoring, and geospatial insights** for the Dubai hospitality market.
    
    It is designed for **analytical learning and market understanding**, aiding stakeholders in identifying revenue opportunities and competitive gaps.
    """)
    
    st.markdown("---")

    # 2. Data Source
    st.subheader("📊 Data Source")
    st.markdown("""
    * **Live Market Data** is fetched using the **SerpAPI (Google Hotels Engine)**.
    * **Historical Baselines** are generated using statistical distributions for trend analysis.
    * **Geospatial Data** includes GPS coordinates for cluster analysis.

    **Why APIs instead of web scraping?**
    * Modern hotel platforms use dynamic JavaScript rendering.
    * HTML scraping is unstable and unreliable for production dashboards.
    * APIs provide structured, consistent, and legal access to public pricing data.
    """)
    
    st.markdown("---")

    # 3. Key Metrics Explained
    st.subheader("📈 Key Metrics Explained")
    
    st.markdown("""
    **Value Score (Index)**
    Measures the quality-to-price ratio. calculated as $$(Rating \div Price) \\times 100$$. A higher score indicates a "Hidden Gem."

    **Demand Proxy (Ratio)**
    Estimates booking velocity based on review frequency and scarcity. Calculated as $$Reviews \div (365 - Availability)$$.

    **Price Category**
    Dynamic segmentation of properties into *Budget, Mid-Range, Premium,* and *Luxury* based on current market quartiles.

    **RevPAR Estimate**
    Revenue Per Available Room estimate derived from price and availability data.
    """)
    
    st.markdown("---")

    # 4. Peer Comparison
    st.subheader("🔄 Peer Comparison")
    st.markdown("""
    * **Strategic Grouping:** Hotels are compared only against their direct competitors (e.g., "5-Star Hotels in Jumeirah") rather than the whole city.
    * **Normalization:** Prices are normalized to a base index to allow fair comparison across different currency fluctuations.
    * **Cluster Analysis:** Geospatial grouping ensures "Apples-to-Apples" location benchmarking.
    """)

    st.markdown("---")

    # 5. Forecasting Method
    st.subheader("🔮 Forecasting Method")
    st.markdown("""
    * **Trend Analysis:** Uses **Descriptive Analytics** to visualize current pricing distributions.
    * **Seasonality:** Adjusts baseline expectations based on known Dubai high-seasons (e.g., December-January).
    * **Note:** Forecasts are **indicative trends** based on current availability calendars, not financial guarantees.
    """)
    
    st.markdown("---")

    # 6. Limitations
    st.subheader("⚠️ Limitations")
    st.markdown("""
    * **Snapshot Data:** Live prices reflect the exact moment of API extraction.
    * **Cookie Dependency:** Prices may vary slightly based on user location and browser history.
    * **API Constraints:** The free tier of SerpAPI limits the depth of historical data retrieval.
    """)
    
    st.markdown("---")

    # 7. Disclaimer
    st.subheader("⚖️ Disclaimer")
    st.markdown("""
    This dashboard is created **for educational and portfolio purposes only**.
    
    It does **NOT** constitute financial advice, investment recommendations, or commercial booking guidance. The developer is not affiliated with Google or any specific hotel property.
    
    <br>
    <div style='text-align: center; color: #666; font-size: 12px;'>
    © 2026 Hotel Analytics Dashboard | Portfolio Project
    </div>
    """, unsafe_allow_html=True)