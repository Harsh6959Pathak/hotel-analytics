"""
Authentication Module
Handles user login and session management
"""

import hashlib
from datetime import datetime


# Predefined users (in production, use database)
USERS = {
    "admin": hashlib.sha256("admin123".encode()).hexdigest(),
    "analyst": hashlib.sha256("analyst123".encode()).hexdigest(),
    "demo": hashlib.sha256("demo".encode()).hexdigest()
}


def hash_password(password: str) -> str:
    """Hash password using SHA-256"""
    return hashlib.sha256(password.encode()).hexdigest()


def check_credentials(username: str, password: str) -> bool:
    """Verify username and password"""
    if username in USERS:
        return USERS[username] == hash_password(password)
    return False


def render_login_page():
    """Render the login page with DARK THEME"""
    import streamlit as st
    
    # Apply DARK THEME styling for login page
    st.markdown("""
    <style>
        /* Hide the stale/loading elements */
        [data-testid="stStatusWidget"] {
            display: none !important;
        }
        
        div[data-stale="true"] {
            display: none !important;
        }
        
        /* Hide spinner container at top */
        .stSpinner {
            display: none !important;
        }
        
        /* Remove ALL top spacing and margins */
        .main .block-container {
            padding-top: 1rem !important;
            max-width: 100% !important;
        }
        
        /* Remove stale element container spacing */
        [data-testid="stVerticalBlock"] > [style*="flex-direction: column;"] > [data-testid="stVerticalBlock"] {
            gap: 0rem !important;
        }
        
        /* Force remove top padding from main container */
        section.main > div {
            padding-top: 0 !important;
        }
        
        /* Dark theme for entire login page */
        .stApp {
            background-color: #0e1117 !important;
        }
        
        /* Login container - Dark theme - REDUCED TOP MARGIN */
        .login-container {
            max-width: 500px;
            margin: 20px auto;
            padding: 50px;
            background: #1a1f2e;
            border-radius: 20px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.5);
            border: 1px solid #2d3748;
        }
        
        .login-header {
            text-align: center;
            margin-bottom: 40px;
        }
        
        .login-header h1 {
            color: #f1f5f9;
            margin-bottom: 10px;
            font-size: 32px;
        }
        
        .login-header p {
            color: #94a3b8;
            font-size: 16px;
        }
        
        /* Credentials info box - Dark */
        .credentials-info {
            background: #0f172a;
            padding: 25px;
            border-radius: 12px;
            margin: 25px 0;
            border: 1px solid #334155;
        }
        
        .credentials-info h4 {
            color: #60a5fa;
            margin-top: 0;
            margin-bottom: 15px;
        }
        
        .credentials-info p {
            color: #cbd5e0;
            margin: 8px 0;
            font-size: 14px;
        }
        
        .credentials-info ul {
            margin: 8px 0;
            padding-left: 20px;
        }
        
        .credentials-info li {
            color: #94a3b8;
            margin: 6px 0;
        }
        
        .credentials-info code {
            background: #1e293b;
            padding: 3px 8px;
            border-radius: 4px;
            color: #60a5fa;
            font-family: 'Courier New', monospace;
            font-size: 13px;
        }
        
        /* Button styling */
        .stButton>button {
            width: 100%;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            padding: 15px;
            font-size: 16px;
            font-weight: 600;
            border-radius: 10px;
            margin-top: 15px;
            cursor: pointer;
            transition: all 0.3s ease;
        }
        
        .stButton>button:hover {
            transform: translateY(-2px);
            box-shadow: 0 10px 25px rgba(102, 126, 234, 0.4);
        }
        
        /* Input fields - Dark theme */
        .stTextInput input {
            background-color: #0f172a !important;
            color: #e2e8f0 !important;
            border: 1px solid #334155 !important;
            border-radius: 8px !important;
            padding: 12px !important;
        }
        
        .stTextInput input:focus {
            border-color: #60a5fa !important;
            box-shadow: 0 0 0 2px rgba(96, 165, 250, 0.2) !important;
        }
        
        .stTextInput label {
            color: #cbd5e0 !important;
            font-weight: 500 !important;
        }
        
        /* Footer */
        .login-footer {
            text-align: center;
            margin-top: 30px;
            color: #64748b;
            font-size: 13px;
        }
    </style>
    """, unsafe_allow_html=True)
    
    # Login container
  
    
    # Header
    # Login container & Header (Combined to fix the layout)
    # Login Header Card
    st.markdown("""
    <div class="login-container">
        <div class="login-header">
            <h1>🏨 Hotel Analytics</h1>
            <p>Professional Analytics Dashboard</p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Login form
    with st.form("login_form", clear_on_submit=False):
        username = st.text_input(
            "Username",
            placeholder="Enter your username",
            key="username_input"
        )
        
        password = st.text_input(
            "Password",
            type="password",
            placeholder="Enter your password",
            key="password_input"
        )
        
        submitted = st.form_submit_button("🔐 Login")
        
        if submitted:
            if not username or not password:
                st.error("⚠️ Please enter both username and password")
            elif check_credentials(username, password):
                st.session_state['authenticated'] = True
                st.session_state['username'] = username
                st.session_state['login_time'] = datetime.now()
                st.success("✅ Login successful! Redirecting...")
                st.rerun()
            else:
                st.error("❌ Invalid username or password")
    
    # Demo credentials
    st.markdown("""
    <div class="credentials-info">
        <h4>🔑 Demo Credentials</h4>
        <p><strong>Admin Access:</strong></p>
        <ul>
            <li>Username: <code>admin</code> | Password: <code>admin123</code></li>
        </ul>
        <p><strong>Analyst Access:</strong></p>
        <ul>
            <li>Username: <code>analyst</code> | Password: <code>analyst123</code></li>
        </ul>
        <p><strong>Quick Demo:</strong></p>
        <ul>
            <li>Username: <code>demo</code> | Password: <code>demo</code></li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    # Footer
    st.markdown("""
    <div class="login-footer">
        <p>Secure Analytics Platform • Data-Driven Insights</p>
        <p>© 2026 Dubai Hotel Analytics</p>
    </div>
    """, unsafe_allow_html=True)
    
    


def check_authentication():
    """Check if user is authenticated"""
    import streamlit as st
    return st.session_state.get('authenticated', False)


def logout():
    """Logout current user"""
    import streamlit as st
    st.session_state['authenticated'] = False
    st.session_state['username'] = None
    st.session_state['login_time'] = None
    st.rerun()


def render_user_info():
    """Render user info in sidebar"""
    import streamlit as st
    
    if check_authentication():
        username = st.session_state.get('username', 'User')
        login_time = st.session_state.get('login_time')
        
        st.sidebar.markdown("---")
        st.sidebar.markdown("### 👤 User Session")
        
        st.sidebar.markdown(f"""
        <div style='background: #0f172a; padding: 15px; border-radius: 10px; border: 1px solid #334155;'>
            <p style='margin: 0; color: #94a3b8;'><strong>Logged in as:</strong></p>
            <p style='margin: 5px 0; color: #60a5fa; font-weight: 600;'>{username}</p>
            <p style='margin: 5px 0 0 0; font-size: 11px; color: #64748b;'>
                Since: {login_time.strftime('%H:%M:%S') if login_time else 'N/A'}
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        if st.sidebar.button("🚪 Logout", use_container_width=True):
            logout()


def require_authentication(func):
    """Decorator to require authentication for a function"""
    def wrapper(*args, **kwargs):
        if check_authentication():
            return func(*args, **kwargs)
        else:
            render_login_page()
            import streamlit as st
            st.stop()
    return wrapper