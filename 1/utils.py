"""
Utility Functions Module
Contains reusable helper functions for styling, metrics, and visualizations
"""

import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np


def apply_custom_styling():
    """Apply custom CSS styling to the Streamlit app with FIXED CONTRAST and NO TOP SPACING"""
    
    st.markdown("""
    <style>
        /* AGGRESSIVE: Remove all default Streamlit top spacing */
        .main .block-container {
            padding-top: 1rem !important;
            padding-bottom: 2rem !important;
        }
        
        section.main > div:has(> .block-container) {
            padding-top: 0 !important;
        }
        
        section.main > div {
            padding-top: 0 !important;
        }
        
        /* Remove gap between elements */
        [data-testid="stVerticalBlock"] {
            gap: 0.5rem !important;
        }
        
        /* Main app background */
        .main {
            background-color: #0e1117;
        }
        
        /* Remove extra spacing from Streamlit elements */
        .element-container {
            margin-top: 0 !important;
        }
        
        /* First element should have no top margin */
        .main .block-container > div:first-child {
            margin-top: 0 !important;
            padding-top: 0 !important;
        }
        
        /* Remove stale element spacing */
        div[data-stale="false"] {
            margin-top: 0 !important;
        }
        
        /* SIDEBAR - High Contrast Fix */
        [data-testid="stSidebar"] {
            background-color: #1a1f2e !important;
            border-right: 2px solid #2d3748;
        }
        
        [data-testid="stSidebar"] .stMarkdown {
            color: #e2e8f0 !important;
        }
        
        [data-testid="stSidebar"] h1, 
        [data-testid="stSidebar"] h2, 
        [data-testid="stSidebar"] h3,
        [data-testid="stSidebar"] h4 {
            color: #ffffff !important;
        }
        
        [data-testid="stSidebar"] p {
            color: #cbd5e0 !important;
        }
        
        [data-testid="stSidebar"] label {
            color: #e2e8f0 !important;
            font-weight: 500;
        }
        
        /* Radio buttons in sidebar */
        [data-testid="stSidebar"] .stRadio > label {
            color: #f7fafc !important;
            font-weight: 600;
        }
        
        [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] {
            color: #e2e8f0 !important;
        }
        
        /* Metric cards */
        .metric-card {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 20px;
            border-radius: 12px;
            color: white;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            margin: 10px 0;
        }
        
        /* Insight boxes - High Contrast */
        .insight-box {
            background-color: #1e293b;
            padding: 20px;
            border-left: 5px solid #3b82f6;
            border-radius: 8px;
            margin: 15px 0;
            color: #e2e8f0;
        }
        
        .insight-box h4 {
            color: #60a5fa !important;
            margin-top: 0;
        }
        
        .insight-box li {
            color: #cbd5e0;
            margin: 8px 0;
        }
        
        .insight-box ul {
            color: #cbd5e0;
        }
        
        /* Success boxes */
        .success-box {
            background-color: #064e3b;
            padding: 20px;
            border-left: 5px solid #22c55e;
            border-radius: 8px;
            margin: 15px 0;
            color: #d1fae5;
        }
        
        /* Warning boxes */
        .warning-box {
            background-color: #451a03;
            padding: 20px;
            border-left: 5px solid #f59e0b;
            border-radius: 8px;
            margin: 15px 0;
            color: #fef3c7;
        }
        
        /* Headers - High Contrast */
        h1 {
            color: #f1f5f9 !important;
            font-weight: 700;
        }
        
        h2 {
            color: #e2e8f0 !important;
            font-weight: 600;
            margin-top: 30px;
        }
        
        h3 {
            color: #cbd5e0 !important;
        }
        
        /* Content text */
        .stMarkdown p {
            color: #cbd5e0;
        }
        
        /* Button styling */
        .stButton>button {
            background-color: #3b82f6;
            color: white;
            border-radius: 8px;
            padding: 10px 24px;
            border: none;
            font-weight: 500;
        }
        
        .stButton>button:hover {
            background-color: #2563eb;
        }
        
        /* Dataframe styling */
        .dataframe {
            font-size: 14px;
        }
        
        /* Input fields - Better contrast */
        .stTextInput input, .stNumberInput input {
            background-color: #1e293b;
            color: #e2e8f0;
            border: 1px solid #475569;
        }
        
        /* Selectbox - Better contrast */
        .stSelectbox select {
            background-color: #1e293b;
            color: #e2e8f0;
            border: 1px solid #475569;
        }
        
        /* Slider - Better visibility */
        .stSlider {
            color: #e2e8f0;
        }
        
        /* Info/Warning/Error boxes */
        .stAlert {
            background-color: #1e293b;
            border: 1px solid #475569;
            color: #e2e8f0;
        }
    </style>
    """, unsafe_allow_html=True)


def create_metric_card(title: str, value: str, delta: str = None, icon: str = "📊"):
    """Create a styled metric card"""
    delta_html = f"<p style='font-size: 14px; margin: 5px 0 0 0; opacity: 0.9;'>{delta}</p>" if delta else ""
    
    st.markdown(f"""
    <div class="metric-card">
        <div style="font-size: 24px; margin-bottom: 5px;">{icon}</div>
        <div style="font-size: 14px; opacity: 0.9; margin-bottom: 5px;">{title}</div>
        <div style="font-size: 32px; font-weight: bold; margin: 5px 0;">{value}</div>
        {delta_html}
    </div>
    """, unsafe_allow_html=True)


def create_insight_box(insights: list, title: str = "💡 Key Insights"):
    """Create an insight box with bullet points - HIGH CONTRAST"""
    if not insights or len(insights) == 0:
        return
    
    insights_html = "".join([f"<li style='margin: 10px 0; color: #cbd5e0; line-height: 1.6;'>{insight}</li>" for insight in insights])
    
    st.markdown(f"""
    <div class="insight-box">
        <h4 style='color: #60a5fa !important; margin-top: 0; font-size: 18px;'>{title}</h4>
        <ul style='margin: 10px 0; padding-left: 20px; color: #cbd5e0;'>
            {insights_html}
        </ul>
    </div>
    """, unsafe_allow_html=True)


def create_plotly_theme():
    """Return a consistent Plotly theme configuration"""
    return {
        'plot_bgcolor': '#0e1117',
        'paper_bgcolor': '#0e1117',
        'font': {'family': 'Arial, sans-serif', 'size': 12, 'color': '#e2e8f0'},
        'title': {'font': {'size': 18, 'color': '#f1f5f9'}},
        'xaxis': {
            'showgrid': True,
            'gridcolor': '#1e293b',
            'linecolor': '#475569',
            'tickfont': {'color': '#cbd5e0'}
        },
        'yaxis': {
            'showgrid': True,
            'gridcolor': '#1e293b',
            'linecolor': '#475569',
            'tickfont': {'color': '#cbd5e0'}
        },
        'hovermode': 'closest',
        'legend': {
            'font': {'color': '#e2e8f0'},
            'bgcolor': '#1e293b'
        }
    }


def safe_divide(numerator, denominator, default=0):
    """Safely divide two numbers"""
    try:
        return numerator / denominator if denominator != 0 else default
    except:
        return default


def format_currency(value, currency='AED'):
    """Format number as currency"""
    return f"{currency} {value:,.2f}"


def format_number(value, decimals=0):
    """Format number with thousand separators"""
    if decimals == 0:
        return f"{value:,.0f}"
    return f"{value:,.{decimals}f}"


def get_color_scale(metric='price'):
    """Get appropriate color scale for different metrics"""
    color_scales = {
        'price': 'YlOrRd',
        'rating': 'Viridis',
        'demand': 'Blues',
        'value': 'RdYlGn',
        'default': 'Plotly3'
    }
    return color_scales.get(metric, color_scales['default'])


def calculate_correlation(df, col1, col2):
    """Calculate correlation between two columns"""
    try:
        if col1 in df.columns and col2 in df.columns:
            return df[col1].corr(df[col2])
    except:
        pass
    return None


def create_distribution_stats(series, name='Variable'):
    """Calculate distribution statistics for a series"""
    return {
        'name': name,
        'count': len(series),
        'mean': series.mean(),
        'median': series.median(),
        'std': series.std(),
        'min': series.min(),
        'max': series.max(),
        'q25': series.quantile(0.25),
        'q75': series.quantile(0.75),
        'skew': series.skew(),
    }


def display_dataframe_with_download(df, filename='data.csv', key=None):
    """Display dataframe with download button"""
    st.dataframe(df, use_container_width=True)
    
    csv = df.to_csv(index=False)
    st.download_button(
        label="📥 Download CSV",
        data=csv,
        file_name=filename,
        mime="text/csv",
        key=key
    )


def create_comparison_table(df, group_col, metric_cols, agg_func='mean'):
    """Create a comparison table grouped by a column"""
    if group_col not in df.columns:
        return pd.DataFrame()
    
    available_metrics = [col for col in metric_cols if col in df.columns]
    
    if not available_metrics:
        return pd.DataFrame()
    
    result = df.groupby(group_col)[available_metrics].agg(agg_func).round(2)
    result = result.sort_values(available_metrics[0], ascending=False)
    
    return result


def page_header(title, subtitle=None, icon="📊"):
    """Create a consistent page header - OPTIMIZED with no top margin"""
    st.markdown(f"""
    <div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                padding: 25px 30px; border-radius: 12px; margin: 0 0 20px 0; color: white;'>
        <h1 style='margin: 0; padding: 0; color: white; font-size: 32px; line-height: 1.2;'>{icon} {title}</h1>
        {f"<p style='margin: 8px 0 0 0; padding: 0; font-size: 15px; opacity: 0.9; line-height: 1.3;'>{subtitle}</p>" if subtitle else ""}
    </div>
    """, unsafe_allow_html=True)
