import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
from datetime import datetime, timedelta
import math
import os

# Page Configuration
st.set_page_config(
    page_title="The Financial Evolution Toolkit",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for clean, professional design
st.markdown("""
<style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    /* Theme Variables */
    :root {
        --primary-color: #FF6600;
        --primary-color-light: #fff0e6;
        --primary-color-dark: #cc5200;
        --background-color: #ffffff;
        --secondary-background: #f5f8fa;
        --text-color: #181c32;
        --header-color: #666666;
    }
    
    /* Global Styles */
    .main {
        padding: 0;
        background-color: var(--secondary-background, #f5f8fa);
        min-height: 100vh;
        font-family: 'Inter', sans-serif;
    }
    
    /* Hide Streamlit elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stDeployButton {display: none;}
    
    /* Override Streamlit default styles */
    .stApp {
        background-color: var(--secondary-background, #f5f8fa);
        font-family: 'Inter', sans-serif;
    }
    
    /* Sidebar styling - Dark theme */
    section[data-testid="stSidebar"] {
        background: #1a202c !important;
        border-right: 1px solid #2d3748;
        width: 350px !important;
    }
    
    section[data-testid="stSidebar"] > div {
        background: transparent;
        padding: 0 !important;
    }
    
    /* Logo section - no padding */
    .sidebar-logo {
        text-align: center;
        padding: 0;
        margin-bottom: 2rem;
    }
    
    /* Sidebar text styling */
    section[data-testid="stSidebar"] {
        font-family: 'Inter', sans-serif !important;
    }
    
    section[data-testid="stSidebar"] h1,
    section[data-testid="stSidebar"] h2,
    section[data-testid="stSidebar"] h3,
    section[data-testid="stSidebar"] p,
    section[data-testid="stSidebar"] div:not([data-testid="stFileUploader"]),
    section[data-testid="stSidebar"] span:not([data-testid="stFileUploader"] span) {
        color: #e2e8f0;
    }
    
    section[data-testid="stSidebar"] h1,
    section[data-testid="stSidebar"] h2,
    section[data-testid="stSidebar"] h3 {
        color: #ffffff !important;
        font-weight: 600;
        margin: 0 0 1rem 0 !important;
    }
    
    /* Navigation styling */
    section[data-testid="stSidebar"] .stRadio > div {
        background: transparent !important;
        border: none !important;
        padding: 0 !important;
    }
    
    section[data-testid="stSidebar"] .stRadio label {
        background: rgba(255,255,255,0.05) !important;
        border: 1px solid rgba(255,255,255,0.1) !important;
        border-radius: 8px !important;
        padding: 12px 16px !important;
        margin: 4px 0 !important;
        cursor: pointer !important;
        transition: all 0.2s ease !important;
        font-weight: 500 !important;
    }
    
    section[data-testid="stSidebar"] .stRadio label:hover {
        background: rgba(255,255,255,0.1) !important;
        border-color: rgba(255,255,255,0.3) !important;
    }
    
    section[data-testid="stSidebar"] .stRadio input:checked + label {
        background: var(--primary-color, #FF6600) !important;
        border-color: var(--primary-color, #FF6600) !important;
        color: #ffffff !important;
    }
    
    /* Enhanced Primary button styling - Sidebar */
    section[data-testid="stSidebar"] button[data-testid="baseButton-primary"] {
        background: linear-gradient(135deg, #FF6600 0%, #FF8533 25%, #FF6600 50%, #E55A00 75%, #CC5200 100%) !important;
        background-size: 300% 300% !important;
        color: #ffffff !important;
        border: none !important;
        border-radius: 16px !important;
        padding: 1.2rem 2rem !important;
        font-weight: 700 !important;
        font-size: 1rem !important;
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1) !important;
        box-shadow: 
            0 8px 25px rgba(255, 102, 0, 0.4),
            0 4px 12px rgba(255, 102, 0, 0.3),
            inset 0 1px 0 rgba(255, 255, 255, 0.1) !important;
        margin-top: 1rem !important;
        position: relative !important;
        overflow: hidden !important;
        text-transform: uppercase !important;
        letter-spacing: 0.5px !important;
        animation: buttonGradientShift 6s ease-in-out infinite !important;
    }
    
    section[data-testid="stSidebar"] button[data-testid="baseButton-primary"]:before {
        content: '' !important;
        position: absolute !important;
        top: 0 !important;
        left: -100% !important;
        width: 100% !important;
        height: 100% !important;
        background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.3), transparent) !important;
        transition: left 0.6s ease !important;
    }
    
    section[data-testid="stSidebar"] button[data-testid="baseButton-primary"]:hover {
        background-position: 100% 50% !important;
        transform: translateY(-4px) scale(1.02) !important;
        box-shadow: 
            0 15px 40px rgba(255, 102, 0, 0.6),
            0 8px 25px rgba(255, 102, 0, 0.4),
            0 0 0 1px rgba(255, 255, 255, 0.1) !important;
        animation: buttonPulse 1.5s ease-in-out infinite !important;
    }
    
    section[data-testid="stSidebar"] button[data-testid="baseButton-primary"]:hover:before {
        left: 100% !important;
    }
    
    section[data-testid="stSidebar"] button[data-testid="baseButton-primary"]:active {
        transform: translateY(-1px) scale(0.98) !important;
        box-shadow: 
            0 5px 15px rgba(255, 102, 0, 0.4),
            0 2px 8px rgba(255, 102, 0, 0.3) !important;
        animation: none !important;
    }
    
    @keyframes buttonGradientShift {
        0%, 100% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
    }
    
    @keyframes buttonPulse {
        0%, 100% { box-shadow: 0 15px 40px rgba(255, 102, 0, 0.6), 0 8px 25px rgba(255, 102, 0, 0.4), 0 0 0 1px rgba(255, 255, 255, 0.1); }
        50% { box-shadow: 0 20px 50px rgba(255, 102, 0, 0.8), 0 12px 35px rgba(255, 102, 0, 0.6), 0 0 0 1px rgba(255, 255, 255, 0.2); }
    }
    
    /* Section headers in sidebar */
    .sidebar-section {
        padding: 0 1rem;
        margin: 0.5rem 0;
    }
    
    .sidebar-section:first-of-type {
        border-top: 1px solid #2d3748;
        padding-top: 1rem;
    }
    
    .sidebar-section h3 {
        color: #a0aec0 !important;
        font-size: 0.75rem !important;
        font-weight: 700 !important;
        text-transform: uppercase !important;
        letter-spacing: 0.05em !important;
        margin-bottom: 1rem !important;
    }
    
    /* Main content area */
    .main-content {
        max-width: 1400px;
        margin: 0 auto;
        padding: 2rem;
    }
    
    /* Page header */
    .page-header {
        background: linear-gradient(135deg, #FF6600 0%, #FF8533 25%, #FF6600 50%, #E55A00 75%, #CC5200 100%);
        background-size: 400% 400%;
        animation: gradientShift 8s ease-in-out infinite;
        border-radius: 20px;
        padding: 4rem 2rem;
        margin-bottom: 3rem;
        color: white;
        text-align: center;
        box-shadow: 
            0 20px 60px rgba(255, 102, 0, 0.4),
            0 10px 30px rgba(255, 102, 0, 0.3),
            inset 0 1px 0 rgba(255, 255, 255, 0.1);
        position: relative;
        overflow: hidden;
    }
    
    .page-header::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.2), transparent);
        animation: shimmer 3s ease-in-out infinite;
    }
    
    @keyframes gradientShift {
        0%, 100% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
    }
    
    @keyframes shimmer {
        0% { left: -100%; }
        100% { left: 100%; }
    }
    
    /* Creative Grey Header for Home Page */
    .page-header.home-header {
        background: 
            linear-gradient(135deg, #2d3748 0%, #4a5568 25%, #666666 50%, #718096 75%, #a0aec0 100%),
            linear-gradient(45deg, transparent 25%, rgba(255,255,255,0.03) 25%, rgba(255,255,255,0.03) 50%, transparent 50%, transparent 75%, rgba(255,255,255,0.03) 75%);
        background-size: 400% 400%, 60px 60px;
        animation: greyGradientShift 12s ease-in-out infinite, patternSlide 20s linear infinite;
        box-shadow: 
            0 25px 80px rgba(45, 55, 72, 0.4),
            0 15px 40px rgba(45, 55, 72, 0.3),
            inset 0 1px 0 rgba(255, 255, 255, 0.1),
            inset 0 -1px 0 rgba(0, 0, 0, 0.1);
        position: relative;
        overflow: hidden;
    }
    
    .page-header.home-header::before {
        background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.15), transparent);
        animation: shimmerGrey 4s ease-in-out infinite;
    }
    
    .page-header.home-header::after {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: 
            radial-gradient(circle at 20% 20%, rgba(255,255,255,0.1) 0%, transparent 50%),
            radial-gradient(circle at 80% 80%, rgba(255,255,255,0.08) 0%, transparent 50%),
            radial-gradient(circle at 40% 70%, rgba(255,255,255,0.05) 0%, transparent 50%);
        pointer-events: none;
        animation: orbs 15s ease-in-out infinite;
    }
    
    @keyframes greyGradientShift {
        0%, 100% { background-position: 0% 50%, 0 0; }
        33% { background-position: 100% 50%, 20px 20px; }
        66% { background-position: 0% 100%, 40px 40px; }
    }
    
    @keyframes patternSlide {
        0% { background-position: 0% 50%, 0 0; }
        100% { background-position: 400% 50%, 60px 60px; }
    }
    
    @keyframes shimmerGrey {
        0% { left: -100%; }
        100% { left: 100%; }
    }
    
    @keyframes orbs {
        0%, 100% { opacity: 1; transform: scale(1); }
        50% { opacity: 0.7; transform: scale(1.1); }
    }
    
    .page-header h1 {
        font-size: 2.75rem;
        font-weight: 800;
        margin: 0 0 1rem 0;
        color: white !important;
        text-shadow: 0 2px 8px rgba(0, 0, 0, 0.3);
        position: relative;
        z-index: 1;
    }
    
    .page-header p {
        font-size: 1.25rem;
        opacity: 0.95;
        margin: 0;
        color: white !important;
        text-shadow: 0 1px 4px rgba(0, 0, 0, 0.2);
        position: relative;
        z-index: 1;
    }
    
    /* Enhanced text styling for grey header */
    .page-header.home-header h1 {
        color: white !important;
        text-shadow: 
            0 3px 10px rgba(0, 0, 0, 0.4),
            0 1px 3px rgba(0, 0, 0, 0.2);
        font-weight: 900;
    }
    
    .page-header.home-header p {
        color: rgba(255, 255, 255, 0.95) !important;
        text-shadow: 
            0 2px 6px rgba(0, 0, 0, 0.3),
            0 1px 2px rgba(0, 0, 0, 0.1);
    }
    
    /* Dashboard cards */
    .dashboard-cards {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
        gap: 1.5rem;
        margin-bottom: 2rem;
    }
    
    .calculator-card {
        background: var(--background-color, #ffffff);
        border-radius: 16px;
        padding: 2rem;
        box-shadow: 0 4px 12px rgba(0,0,0,0.08);
        border: 1px solid #e2e8f0;
        transition: all 0.3s ease;
        cursor: pointer;
        text-decoration: none;
        color: inherit;
    }
    
    .calculator-card {
        transition: all 0.5s cubic-bezier(0.4, 0, 0.2, 1);
        position: relative;
        overflow: hidden;
    }
    
    .calculator-card:before {
        content: '';
        position: absolute;
        top: -2px;
        left: -2px;
        right: -2px;
        bottom: -2px;
        background: linear-gradient(135deg, #FF6600, #FF8533, #E55A00, #CC5200);
        background-size: 400% 400%;
        border-radius: 18px;
        opacity: 0;
        z-index: -1;
        animation: cardGradientShift 10s ease-in-out infinite;
        transition: opacity 0.5s ease;
    }
    
    .calculator-card:hover {
        transform: translateY(-15px) scale(1.03);
        box-shadow: 
            0 30px 80px rgba(255, 102, 0, 0.3),
            0 20px 40px rgba(0,0,0,0.15);
        border-color: transparent;
    }
    
    .calculator-card:hover:before {
        opacity: 1;
    }
    
    @keyframes cardGradientShift {
        0%, 100% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
    }
    
    .card-icon {
        width: 64px;
        height: 64px;
        border-radius: 16px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.75rem;
        margin-bottom: 1.5rem;
        font-weight: bold;
    }
    
    .card-icon.compound { background: var(--primary-color-light, #fff0e6); color: var(--primary-color, #FF6600); }
    .card-icon.investment { background: #f0fff4; color: #38a169; }
    .card-icon.debt { background: #fed7d7; color: #e53e3e; }
    
    .card-title {
        font-size: 1.5rem;
        font-weight: 700;
        color: var(--header-color, #666666);
        margin-bottom: 0.75rem;
    }
    
    .card-description {
        color: #718096;
        font-size: 1rem;
        line-height: 1.6;
        margin-bottom: 1.5rem;
    }
    
    .card-features {
        list-style: none;
        padding: 0;
        margin: 0;
    }
    
    .card-features li {
        color: #4a5568;
        font-size: 0.875rem;
        padding: 0.25rem 0;
        position: relative;
        padding-left: 1.5rem;
    }
    
    .card-features li:before {
        content: "✓";
        position: absolute;
        left: 0;
        color: #38a169;
        font-weight: bold;
    }
    
    /* Content sections */
    .content-section {
        background: var(--background-color, #ffffff);
        border-radius: 16px;
        padding: 2rem;
        box-shadow: 0 4px 12px rgba(0,0,0,0.08);
        border: 1px solid #e2e8f0;
        margin-bottom: 2rem;
    }
    
    .section-title {
        font-size: 1.5rem;
        font-weight: 700;
        color: var(--header-color, #666666);
        margin-bottom: 1.5rem;
    }
    
    /* Enhanced Results styling */
    .results-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
        gap: 1.5rem;
        margin: 2rem 0;
    }
    
    .result-card {
        background: var(--secondary-background, #f5f8fa);
        border-radius: 12px;
        padding: 1.5rem;
        text-align: center;
        border: 1px solid #e2e8f0;
        transition: all 0.3s ease;
        animation: floatGentle 6s ease-in-out infinite;
    }
    
    .result-card:nth-child(1) { animation-delay: 0s; }
    .result-card:nth-child(2) { animation-delay: 1.5s; }
    .result-card:nth-child(3) { animation-delay: 3s; }
    .result-card:nth-child(4) { animation-delay: 4.5s; }
    
    .result-card:hover {
        transform: translateY(-8px) scale(1.05);
        box-shadow: 0 15px 35px rgba(255, 102, 0, 0.2);
        border-color: var(--primary-color, #FF6600);
    }
    
    @keyframes floatGentle {
        0%, 100% { transform: translateY(0px); }
        50% { transform: translateY(-5px); }
    }
    
    .result-value {
        font-size: 1.75rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
    }
    
    .result-value.positive { color: #38a169; }
    .result-value.negative { color: #e53e3e; }
    .result-value.neutral { color: var(--primary-color, #FF6600); }
    
    .result-label {
        font-size: 0.875rem;
        color: #718096;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    
    /* Enhanced Main content button styling */
    button[data-testid="baseButton-primary"] {
        background: linear-gradient(135deg, #FF6600 0%, #FF8533 25%, #FF6600 50%, #E55A00 75%, #CC5200 100%) !important;
        background-size: 300% 300% !important;
        color: #ffffff !important;
        border: none !important;
        border-radius: 12px !important;
        padding: 0.75rem 1.5rem !important;
        font-weight: 700 !important;
        font-size: 0.95rem !important;
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1) !important;
        box-shadow: 
            0 6px 20px rgba(255, 102, 0, 0.4),
            0 3px 10px rgba(255, 102, 0, 0.3),
            inset 0 1px 0 rgba(255, 255, 255, 0.1) !important;
        position: relative !important;
        overflow: hidden !important;
        text-transform: uppercase !important;
        letter-spacing: 0.3px !important;
        animation: buttonGradientShift 8s ease-in-out infinite !important;
    }
    
    button[data-testid="baseButton-primary"]:before {
        content: '' !important;
        position: absolute !important;
        top: 0 !important;
        left: -100% !important;
        width: 100% !important;
        height: 100% !important;
        background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.2), transparent) !important;
        transition: left 0.5s ease !important;
    }
    
    button[data-testid="baseButton-primary"]:hover {
        background-position: 100% 50% !important;
        transform: translateY(-3px) scale(1.05) !important;
        box-shadow: 
            0 12px 30px rgba(255, 102, 0, 0.6),
            0 6px 20px rgba(255, 102, 0, 0.4),
            0 0 0 1px rgba(255, 255, 255, 0.1) !important;
        animation: buttonGlow 2s ease-in-out infinite !important;
    }
    
    button[data-testid="baseButton-primary"]:hover:before {
        left: 100% !important;
    }
    
    button[data-testid="baseButton-primary"]:active {
        transform: translateY(-1px) scale(1.02) !important;
        box-shadow: 
            0 4px 15px rgba(255, 102, 0, 0.4),
            0 2px 8px rgba(255, 102, 0, 0.3) !important;
        animation: none !important;
    }
    
    @keyframes buttonGlow {
        0%, 100% { 
            box-shadow: 
                0 12px 30px rgba(255, 102, 0, 0.6),
                0 6px 20px rgba(255, 102, 0, 0.4),
                0 0 0 1px rgba(255, 255, 255, 0.1);
        }
        50% { 
            box-shadow: 
                0 16px 40px rgba(255, 102, 0, 0.8),
                0 8px 25px rgba(255, 102, 0, 0.6),
                0 0 0 1px rgba(255, 255, 255, 0.2);
        }
    }
    
    /* Card heading styling */
    .stMarkdown h3 {
        color: var(--header-color, #666666) !important;
        font-weight: 700 !important;
    }
    
    /* Info/Notes sections styling */
    .stAlert > div {
        background-color: var(--primary-color-light, #fff0e6) !important;
        border-left: 4px solid var(--primary-color, #FF6600) !important;
        color: #663300 !important;
    }
    
    .stAlert p {
        color: #663300 !important;
    }
    
    /* Responsive design */
    @media (max-width: 1200px) {
        .dashboard-cards {
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 1rem;
        }
    }
    
    @media (max-width: 768px) {
        .main-content {
            padding: 1rem;
        }
        
        .dashboard-cards {
            grid-template-columns: 1fr;
            gap: 1rem;
        }
        
        .page-header {
            padding: 2rem 1rem;
        }
        
        .page-header h1 {
            font-size: 2rem;
        }
        
        .results-grid {
            grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
            gap: 1rem;
        }
    }
    
    @media (max-width: 480px) {
        .results-grid {
            grid-template-columns: 1fr;
            gap: 1rem;
        }
    }
</style>
""", unsafe_allow_html=True)

def format_currency(amount):
    """Format amount as currency"""
    return f"${amount:,.2f}"

def format_percentage(rate):
    """Format rate as percentage"""
    return f"{rate:.2f}%"

def create_sidebar():
    """Create the sidebar with logo and navigation"""
    with st.sidebar:
        # Logo section
        st.markdown('<div class="sidebar-logo">', unsafe_allow_html=True)
        
        # Try to display logo, fallback to text if not found
        try:
            if os.path.exists('assets/logo.png'):
                st.image('assets/logo.png', width=250)
            else:
                st.markdown("### The Financial Evolution Toolkit")
        except:
            st.markdown("### The Financial Evolution Toolkit")
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Navigation
        st.markdown("""
        <div class="sidebar-section">
            <h3>Calculators</h3>
        </div>
        """, unsafe_allow_html=True)
        
        # Get current page from session state for default selection
        current_page = st.session_state.get("selected_page", "Home")
        page_options = ["Home", "Compound Interest", "Investment Fees", "Debt Free Date", "Biweekly Payment"]
        default_index = page_options.index(current_page) if current_page in page_options else 0
        
        page = st.radio(
            "Navigation Menu",
            page_options,
            index=default_index,
            label_visibility="collapsed"
        )
        
        # Information Section
        st.markdown("""
        <div class="sidebar-section">
            <h3>About</h3>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        **About the Financial Evolution Toolkit**
        
        Professional-grade calculators designed to give you instant clarity around your money.
        
        Project your investment growth, see how much fees are costing you, and find your path to debt freedom — without spreadsheets or guesswork.
        """)
        
        # Add spacing to push copyright to bottom
        st.markdown("<br>" * 12, unsafe_allow_html=True)
        
        # Copyright notice at bottom
        st.markdown("""
        <div style="position: fixed; bottom: 20px; left: 20px; font-size: 1rem; color: #a0aec0;">
            © 2025 - Your Financial Evolution
        </div>
        """, unsafe_allow_html=True)
        
        return page

def home_page():
    """Home page with calculator cards"""
    st.markdown("""
    <div class="main-content">
        <div class="page-header home-header">
            <h1>The Financial Evolution Toolkit</h1>
            <p>Unlock financial clarity in minutes — not months.<br>These calculators give you the answers most people pay advisors to figure out.</p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Create four columns for the calculator cards
    col1, col2, col3, col4 = st.columns(4, gap="medium")
    
    with col1:
        # Compound Interest Calculator Card
        st.markdown("""
        <div style="
            background: var(--background-color, #ffffff);
            border-radius: 16px;
            padding: 1.5rem;
            box-shadow: 0 4px 12px rgba(0,0,0,0.08);
            border: 1px solid #e2e8f0;
            height: 350px;
            display: flex;
            flex-direction: column;
            justify-content: space-between;
        ">
            <div>
                <h3 style="color: var(--header-color, #666666); margin-bottom: 1rem; font-size: 1.25rem;">Compound Interest Calculator</h3>
                <p style="color: #4a5568; margin-bottom: 1rem; font-size: 0.95rem;">See exactly how your money grows — and how to grow it faster.</p>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("Launch Calculator", key="compound", use_container_width=True, type="primary"):
            st.session_state.selected_page = "Compound Interest"
            st.rerun()
    
    with col2:
        # Investment Fee Comparison Card
        st.markdown("""
        <div style="
            background: var(--background-color, #ffffff);
            border-radius: 16px;
            padding: 1.5rem;
            box-shadow: 0 4px 12px rgba(0,0,0,0.08);
            border: 1px solid #e2e8f0;
            height: 350px;
            display: flex;
            flex-direction: column;
            justify-content: space-between;
        ">
            <div>
                <h3 style="color: var(--header-color, #666666); margin-bottom: 1rem; font-size: 1.25rem;">Investment Fee Comparison</h3>
                <p style="color: #4a5568; margin-bottom: 1rem; font-size: 0.95rem;">Stop guessing what fees are costing you — start taking control.</p>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("Launch Calculator", key="investment", use_container_width=True, type="primary"):
            st.session_state.selected_page = "Investment Fees"
            st.rerun()
    
    with col3:
        # Debt-Free Date Calculator Card
        st.markdown("""
        <div style="
            background: var(--background-color, #ffffff);
            border-radius: 16px;
            padding: 1.5rem;
            box-shadow: 0 4px 12px rgba(0,0,0,0.08);
            border: 1px solid #e2e8f0;
            height: 350px;
            display: flex;
            flex-direction: column;
            justify-content: space-between;
        ">
            <div>
                <h3 style="color: var(--header-color, #666666); margin-bottom: 1rem; font-size: 1.25rem;">Debt-Free Date Calculator</h3>
                <p style="color: #4a5568; margin-bottom: 1rem; font-size: 0.95rem;">Know your timeline to freedom — and how to shorten it.</p>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("Launch Calculator", key="debt", use_container_width=True, type="primary"):
            st.session_state.selected_page = "Debt Free Date"
            st.rerun()
    
    with col4:
        # Biweekly Payment Calculator Card
        st.markdown("""
        <div style="
            background: var(--background-color, #ffffff);
            border-radius: 16px;
            padding: 1.5rem;
            box-shadow: 0 4px 12px rgba(0,0,0,0.08);
            border: 1px solid #e2e8f0;
            height: 350px;
            display: flex;
            flex-direction: column;
            justify-content: space-between;
        ">
            <div>
                <h3 style="color: var(--header-color, #666666); margin-bottom: 1rem; font-size: 1.25rem;">Biweekly Payment Calculator</h3>
                <p style="color: #4a5568; margin-bottom: 1rem; font-size: 0.95rem;">Convert monthly or annual payments into biweekly amounts that align with your pay schedule.</p>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("Launch Calculator", key="biweekly", use_container_width=True, type="primary"):
            st.session_state.selected_page = "Biweekly Payment"
            st.rerun()

def compound_interest_page():
    """Compound Interest Calculator"""
    st.markdown("""
    <div class="main-content">
        <div class="page-header">
            <h1>Compound Interest Calculator</h1>
            <p>Discover the power of compound interest and regular investments</p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Input section in a clean container
    with st.container():
        st.markdown("### Investment Parameters")
        st.markdown("---")
        
        # Create organized input layout
        col1, col2, col3 = st.columns(3)
        
        with col1:
            initial_amount = st.number_input("Initial Amount ($)", min_value=0.0, value=10000.0, step=100.0)
            annual_rate = st.number_input("Annual Interest Rate (%)", min_value=0.0, max_value=30.0, value=7.0, step=0.1)
        
        with col2:
            monthly_contribution = st.number_input("Monthly Contribution ($)", min_value=0.0, value=500.0, step=50.0)
            years = st.number_input("Number of Years", min_value=1, max_value=50, value=20, step=1)
        
        with col3:
            st.markdown("**Compounding:**")
            st.info("Interest compounds annually")
            n = 1  # Annual compounding
        
        # Form-style button positioning
        st.markdown("<br>", unsafe_allow_html=True)
        col1, col2, col3, col4 = st.columns([1, 1, 1, 1])
        with col4:
            calculate_clicked = st.button("Calculate", type="primary", use_container_width=True, key="compound_calc_button")
    
    # Results section
    if calculate_clicked:
        # Calculate compound interest with regular contributions (annual compounding)
        r = annual_rate / 100
        
        # Future value of initial investment
        future_value_initial = initial_amount * (1 + r)**years
        
        # Future value of monthly contributions with annual compounding
        if monthly_contribution > 0:
            # Calculate each monthly contribution's future value individually
            future_value_contributions = 0
            for month in range(1, int(12*years) + 1):
                # Years remaining for this contribution to compound
                years_remaining = years - (month - 1) / 12
                # Add the future value of this monthly contribution
                future_value_contributions += monthly_contribution * (1 + r)**years_remaining
        else:
            future_value_contributions = 0
        
        total_future_value = future_value_initial + future_value_contributions
        total_contributions = initial_amount + (monthly_contribution * 12 * years)
        total_interest = total_future_value - total_contributions
        
        # Display results
        st.markdown(f"""
        <div class="results-grid">
            <div class="result-card">
                <div class="result-value positive">{format_currency(total_future_value)}</div>
                <div class="result-label">Final Balance</div>
            </div>
            <div class="result-card">
                <div class="result-value neutral">{format_currency(total_contributions)}</div>
                <div class="result-label">Total Contributions</div>
            </div>
            <div class="result-card">
                <div class="result-value positive">{format_currency(total_interest)}</div>
                <div class="result-label">Interest Earned</div>
            </div>
            <div class="result-card">
                <div class="result-value neutral">{format_percentage((total_interest/total_contributions)*100 if total_contributions > 0 else 0)}</div>
                <div class="result-label">Return on Investment</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Create growth chart
        months = years * 12
        balance_data = []
        contribution_data = []
        
        for month in range(months + 1):
            # Calculate balance at this month
            years_elapsed = month / 12
            
            # Future value of initial investment at this point
            fv_initial = initial_amount * (1 + r)**years_elapsed
            
            # Future value of contributions made so far with annual compounding
            if month > 0 and monthly_contribution > 0:
                fv_contributions = 0
                for contrib_month in range(1, month + 1):
                    # Years this contribution has been compounding
                    years_compounding = years_elapsed - (contrib_month - 1) / 12
                    fv_contributions += monthly_contribution * (1 + r)**years_compounding
            else:
                fv_contributions = 0
            
            total_balance = fv_initial + fv_contributions
            total_contributed = initial_amount + (monthly_contribution * month)
            
            balance_data.append(total_balance)
            contribution_data.append(total_contributed)
        
        # Create DataFrame for plotting
        chart_data = pd.DataFrame({
            'Month': range(months + 1),
            'Balance': balance_data,
            'Contributions': contribution_data,
            'Interest': [b - c for b, c in zip(balance_data, contribution_data)]
        })
        
        # Create stacked area chart
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(
            x=chart_data['Month'],
            y=chart_data['Contributions'],
            fill='tozeroy',
            mode='none',
            name='Contributions',
            fillcolor='rgba(49, 130, 206, 0.6)'
        ))
        
        fig.add_trace(go.Scatter(
            x=chart_data['Month'],
            y=chart_data['Balance'],
            fill='tonexty',
            mode='none',
            name='Interest',
            fillcolor='rgba(56, 161, 105, 0.6)'
        ))
        
        fig.update_layout(
            title="Investment Growth Over Time",
            xaxis_title="Months",
            yaxis_title="Value ($)",
            font=dict(family="Inter, sans-serif"),
            paper_bgcolor='white',
            plot_bgcolor='white',
            showlegend=True,
            hovermode='x unified'
        )
        
        fig.update_xaxes(showgrid=True, gridcolor='rgba(0,0,0,0.1)')
        fig.update_yaxes(showgrid=True, gridcolor='rgba(0,0,0,0.1)')
        
        st.plotly_chart(fig, use_container_width=True)

def investment_fee_page():
    """Investment Fee Comparison Calculator"""
    st.markdown("""
    <div class="main-content">
        <div class="page-header">
            <h1>Investment Fee Comparison</h1>
            <p>Compare the long-term impact of investment fees on your portfolio</p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Input section in a clean container
    with st.container():
        st.markdown("### Investment Parameters")
        st.markdown("---")
        
        # Create organized input layout
        col1, col2 = st.columns(2)
        
        with col1:
            starting_amount = st.number_input("Starting Amount ($)", min_value=0.0, value=50000.0, step=1000.0)
            expected_return = st.number_input("Expected Annual Return (%)", min_value=0.0, max_value=20.0, value=8.0, step=0.1)
            self_managed_fee = st.number_input("Self-Managed Fee (%)", min_value=0.0, max_value=5.0, value=0.15, step=0.01)
        
        with col2:
            monthly_contribution = st.number_input("Monthly Contribution ($)", min_value=0.0, value=500.0, step=50.0)
            years = st.number_input("Investment Duration (Years)", min_value=1, max_value=50, value=25, step=1)
            advisor_fee = st.number_input("Advisor-Managed Fee (%)", min_value=0.0, max_value=5.0, value=1.25, step=0.01)
        
        # Form-style button positioning
        st.markdown("<br>", unsafe_allow_html=True)
        col1, col2, col3, col4 = st.columns([1, 1, 1, 1])
        with col4:
            calculate_clicked = st.button("Compare Scenarios", type="primary", use_container_width=True, key="investment_calc_button")
    
    # Results section
    if calculate_clicked:
        # Calculate both scenarios using monthly compounding
        r_gross = expected_return / 100
        monthly_gross_rate = r_gross / 12
        
        # Net monthly rates after fees
        monthly_self_rate = monthly_gross_rate - (self_managed_fee / 100 / 12)
        monthly_advisor_rate = monthly_gross_rate - (advisor_fee / 100 / 12)
        
        total_months = years * 12
        
        # Self-managed scenario with monthly compounding
        future_value_self_initial = starting_amount * (1 + monthly_self_rate)**total_months
        if monthly_contribution > 0:
            future_value_self_contributions = monthly_contribution * (((1 + monthly_self_rate)**total_months - 1) / monthly_self_rate)
        else:
            future_value_self_contributions = 0
        total_self = future_value_self_initial + future_value_self_contributions
        
        # Advisor-managed scenario with monthly compounding
        future_value_advisor_initial = starting_amount * (1 + monthly_advisor_rate)**total_months
        if monthly_contribution > 0:
            future_value_advisor_contributions = monthly_contribution * (((1 + monthly_advisor_rate)**total_months - 1) / monthly_advisor_rate)
        else:
            future_value_advisor_contributions = 0
        total_advisor = future_value_advisor_initial + future_value_advisor_contributions
        
        # Calculate total invested
        total_invested = starting_amount + (monthly_contribution * total_months)
        
        # Calculate actual fees paid (difference between gross and net returns)
        # Self-managed fees
        gross_self_initial = starting_amount * (1 + monthly_gross_rate)**total_months
        if monthly_contribution > 0:
            gross_self_contributions = monthly_contribution * (((1 + monthly_gross_rate)**total_months - 1) / monthly_gross_rate)
        else:
            gross_self_contributions = 0
        gross_self_total = gross_self_initial + gross_self_contributions
        fees_self = gross_self_total - total_self
        
        # Advisor fees
        fees_advisor = gross_self_total - total_advisor
        
        # Difference
        difference = total_self - total_advisor
        
        # Display results
        st.markdown(f"""
        <div class="results-grid">
            <div class="result-card">
                <div class="result-value positive">{format_currency(total_self)}</div>
                <div class="result-label">Self-Managed Value</div>
            </div>
            <div class="result-card">
                <div class="result-value neutral">{format_currency(total_advisor)}</div>
                <div class="result-label">Advisor-Managed Value</div>
            </div>
            <div class="result-card">
                <div class="result-value positive">{format_currency(difference)}</div>
                <div class="result-label">Difference</div>
            </div>
            <div class="result-card">
                <div class="result-value negative">{format_currency(fees_advisor - fees_self)}</div>
                <div class="result-label">Extra Fees Paid</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Create comparison chart
        years_array = np.arange(0, years + 1)
        self_values = []
        advisor_values = []
        
        for year in years_array:
            months_elapsed = year * 12
            
            # Self-managed with monthly compounding
            fv_self_initial = starting_amount * (1 + monthly_self_rate)**months_elapsed
            if monthly_contribution > 0 and months_elapsed > 0:
                fv_self_contrib = monthly_contribution * (((1 + monthly_self_rate)**months_elapsed - 1) / monthly_self_rate)
            else:
                fv_self_contrib = 0
            self_values.append(fv_self_initial + fv_self_contrib)
            
            # Advisor-managed with monthly compounding
            fv_advisor_initial = starting_amount * (1 + monthly_advisor_rate)**months_elapsed
            if monthly_contribution > 0 and months_elapsed > 0:
                fv_advisor_contrib = monthly_contribution * (((1 + monthly_advisor_rate)**months_elapsed - 1) / monthly_advisor_rate)
            else:
                fv_advisor_contrib = 0
            advisor_values.append(fv_advisor_initial + fv_advisor_contrib)
        
        # Create comparison chart
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(
            x=years_array,
            y=self_values,
            mode='lines',
            name=f'Self-Managed ({self_managed_fee}% fee)',
            line=dict(color='#38a169', width=3)
        ))
        
        fig.add_trace(go.Scatter(
            x=years_array,
            y=advisor_values,
            mode='lines',
            name=f'Advisor-Managed ({advisor_fee}% fee)',
            line=dict(color='#e53e3e', width=3)
        ))
        
        fig.update_layout(
            title="Investment Value Comparison Over Time",
            xaxis_title="Years",
            yaxis_title="Portfolio Value ($)",
            font=dict(family="Inter, sans-serif"),
            paper_bgcolor='white',
            plot_bgcolor='white',
            showlegend=True,
            hovermode='x unified'
        )
        
        fig.update_xaxes(showgrid=True, gridcolor='rgba(0,0,0,0.1)')
        fig.update_yaxes(showgrid=True, gridcolor='rgba(0,0,0,0.1)')
        
        st.plotly_chart(fig, use_container_width=True)

def debt_free_page():
    """Debt-Free Date Calculator"""
    st.markdown("""
    <div class="main-content">
        <div class="page-header">
            <h1>Debt-Free Date Calculator</h1>
            <p>Plan your path to financial freedom and see the impact of extra payments</p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Input section in a clean container
    with st.container():
        st.markdown("### Debt Information")
        st.markdown("---")
        
        # Create organized input layout
        col1, col2 = st.columns(2)
        
        with col1:
            total_debt = st.number_input("Total Debt Amount ($)", min_value=0.0, value=25000.0, step=500.0)
            annual_rate = st.number_input("Annual Interest Rate (%)", min_value=0.0, max_value=30.0, value=18.0, step=0.1)
        
        with col2:
            monthly_payment = st.number_input("Miminum Monthly Payment ($)", min_value=0.0, value=500.0, step=25.0)
            extra_payment = st.number_input("Extra Monthly Payment ($)", min_value=0.0, value=100.0, step=25.0)
        
        # Form-style button positioning
        st.markdown("<br>", unsafe_allow_html=True)
        col1, col2, col3, col4 = st.columns([1, 1, 1, 1])
        with col4:
            calculate_clicked = st.button("Calculate Payoff", type="primary", use_container_width=True, key="debt_calc_button")
    
    # Results section
    if calculate_clicked:
        monthly_rate = annual_rate / 100 / 12
        
        # Standard payoff calculation
        if monthly_rate > 0:
            months_standard = -np.log(1 - (total_debt * monthly_rate) / monthly_payment) / np.log(1 + monthly_rate)
            total_interest_standard = (monthly_payment * months_standard) - total_debt
        else:
            months_standard = total_debt / monthly_payment
            total_interest_standard = 0
        
        # With extra payments
        total_monthly_payment = monthly_payment + extra_payment
        if monthly_rate > 0 and total_monthly_payment > total_debt * monthly_rate:
            months_extra = -np.log(1 - (total_debt * monthly_rate) / total_monthly_payment) / np.log(1 + monthly_rate)
            total_interest_extra = (total_monthly_payment * months_extra) - total_debt
        else:
            months_extra = total_debt / total_monthly_payment
            total_interest_extra = 0
        
        # Calculate dates
        today = datetime.now()
        payoff_date_standard = today + timedelta(days=months_standard * 30.44)
        payoff_date_extra = today + timedelta(days=months_extra * 30.44)
        
        # Time and interest saved
        months_saved = months_standard - months_extra
        interest_saved = total_interest_standard - total_interest_extra
        
        # Display results
        st.markdown(f"""
        <div class="results-grid">
            <div class="result-card">
                <div class="result-value neutral">{math.ceil(months_standard)} months</div>
                <div class="result-label">Standard Payoff Time</div>
            </div>
            <div class="result-card">
                <div class="result-value positive">{math.ceil(months_extra)} months</div>
                <div class="result-label">With Extra Payments</div>
            </div>
            <div class="result-card">
                <div class="result-value positive">{math.ceil(months_saved)} months</div>
                <div class="result-label">Time Saved</div>
            </div>
            <div class="result-card">
                <div class="result-value positive">{format_currency(interest_saved)}</div>
                <div class="result-label">Interest Saved</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Display payoff dates
        col_a, col_b = st.columns(2)
        with col_a:
            st.markdown(f"""
            <div class="content-section">
                <div class="section-title">Standard Scenario</div>
                <p><strong>Debt-Free Date:</strong> {payoff_date_standard.strftime('%B %d, %Y')}</p>
                <p><strong>Total Interest:</strong> {format_currency(total_interest_standard)}</p>
                <p><strong>Total Paid:</strong> {format_currency(total_debt + total_interest_standard)}</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col_b:
            st.markdown(f"""
            <div class="content-section">
                <div class="section-title">With Extra Payments</div>
                <p><strong>Debt-Free Date:</strong> {payoff_date_extra.strftime('%B %d, %Y')}</p>
                <p><strong>Total Interest:</strong> {format_currency(total_interest_extra)}</p>
                <p><strong>Total Paid:</strong> {format_currency(total_debt + total_interest_extra)}</p>
            </div>
            """, unsafe_allow_html=True)
        
        # Create payoff progression chart
        months_to_show = math.ceil(max(months_standard, months_extra))
        month_numbers = list(range(1, months_to_show + 1))
        
        # Calculate remaining balance for each scenario
        balance_standard = []
        balance_extra = []
        
        remaining_debt_std = total_debt
        remaining_debt_ext = total_debt
        
        for month in month_numbers:
            # Standard payments
            if remaining_debt_std > 0:
                interest_payment_std = remaining_debt_std * monthly_rate
                principal_payment_std = min(monthly_payment - interest_payment_std, remaining_debt_std)
                remaining_debt_std -= principal_payment_std
                remaining_debt_std = max(0, remaining_debt_std)
            
            # Extra payments
            if remaining_debt_ext > 0:
                interest_payment_ext = remaining_debt_ext * monthly_rate
                principal_payment_ext = min(total_monthly_payment - interest_payment_ext, remaining_debt_ext)
                remaining_debt_ext -= principal_payment_ext
                remaining_debt_ext = max(0, remaining_debt_ext)
            
            balance_standard.append(remaining_debt_std)
            balance_extra.append(remaining_debt_ext)
        
        # Create chart
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(
            x=month_numbers,
            y=balance_standard,
            mode='lines',
            name='Standard Payments',
            line=dict(color='#e53e3e', width=3)
        ))
        
        fig.add_trace(go.Scatter(
            x=month_numbers,
            y=balance_extra,
            mode='lines',
            name='With Extra Payments',
            line=dict(color='#38a169', width=3)
        ))
        
        fig.update_layout(
            title="Debt Payoff Progress",
            xaxis_title="Months",
            yaxis_title="Remaining Debt ($)",
            font=dict(family="Inter, sans-serif"),
            paper_bgcolor='white',
            plot_bgcolor='white',
            showlegend=True,
            hovermode='x unified'
        )
        
        fig.update_xaxes(showgrid=True, gridcolor='rgba(0,0,0,0.1)')
        fig.update_yaxes(showgrid=True, gridcolor='rgba(0,0,0,0.1)')
        
        st.plotly_chart(fig, use_container_width=True)

def biweekly_payment_page():
    """Biweekly Payment Calculator"""
    st.markdown("""
    <div class="main-content">
        <div class="page-header">
            <h1>Biweekly Payment Calculator</h1>
            <p>Convert monthly or annual payments into biweekly amounts that align with your pay schedule</p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Input section in a clean container
    with st.container():
        st.markdown("### Payment Conversion")
        st.markdown("---")
        
        # Information about the calculator
        st.info("""
        **How it works:** This calculator converts any monthly or annual payment, savings goal, or investment 
        contribution into a biweekly amount. This allows you to set up automated transfers that align 
        with a biweekly pay schedule (26 pay periods per year).
        """)
        
        # Create organized input layout
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**Choose your input type:**")
            input_type = st.radio(
                "Input Type Selection",
                ["Monthly Amount", "Annual Amount"],
                label_visibility="collapsed",
                key="input_type_radio"
            )
        
        with col2:
            st.markdown("**Enter your amount:**")
            if input_type == "Monthly Amount":
                monthly_amount = st.number_input(
                    "Monthly Amount ($)", 
                    min_value=0.0, 
                    value=0.0, 
                    step=10.0,
                    help="Enter the monthly payment amount you want to convert",
                    key="monthly_input"
                )
                annual_amount = 0.0  # Reset annual when using monthly
            else:
                annual_amount = st.number_input(
                    "Annual Amount ($)", 
                    min_value=0.0, 
                    value=0.0, 
                    step=100.0,
                    help="Enter the annual payment amount you want to convert",
                    key="annual_input"
                )
                monthly_amount = 0.0  # Reset monthly when using annual
        
        # Form-style button positioning
        st.markdown("<br>", unsafe_allow_html=True)
        col1, col2, col3, col4 = st.columns([1, 1, 1, 1])
        with col4:
            calculate_clicked = st.button("Convert to Biweekly", type="primary", use_container_width=True, key="convert_button")
    
    # Results section
    if calculate_clicked:
        if monthly_amount > 0 or annual_amount > 0:
            # Calculate biweekly amount
            if input_type == "Monthly Amount" and monthly_amount > 0:
                # Convert monthly to biweekly: monthly * 12 / 26
                biweekly_amount = (monthly_amount * 12) / 26
                original_amount = monthly_amount
                original_type = "Monthly"
                # Also calculate the annual equivalent
                annual_equivalent = monthly_amount * 12
            else:
                # Convert annual to biweekly: annual / 26
                biweekly_amount = annual_amount / 26
                original_amount = annual_amount
                original_type = "Annual"
                # Also calculate the monthly equivalent
                annual_equivalent = annual_amount
            
            # Display results
            st.markdown(f"""
            <div class="results-grid">
                <div class="result-card">
                    <div class="result-value positive">{format_currency(biweekly_amount)}</div>
                    <div class="result-label">Biweekly Amount</div>
                </div>
                <div class="result-card">
                    <div class="result-value neutral">{format_currency(original_amount)}</div>
                    <div class="result-label">{original_type} Amount</div>
                </div>
                <div class="result-card">
                    <div class="result-value neutral">{format_currency(annual_equivalent)}</div>
                    <div class="result-label">Annual Equivalent</div>
                </div>
                <div class="result-card">
                    <div class="result-value neutral">26</div>
                    <div class="result-label">Pay Periods/Year</div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # Explanation section
            col_a, col_b = st.columns(2)
            with col_a:
                st.markdown(f"""
                <div class="content-section">
                    <div class="section-title">How This Works</div>
                    <p><strong>Biweekly Schedule:</strong> 26 pay periods per year (every 2 weeks)</p>
                    <p><strong>Calculation:</strong> {original_type} amount {'÷ 26' if original_type == "Annual" else '× 12 ÷ 26'} = Biweekly amount</p>
                    <p><strong>Total Annual:</strong> {format_currency(annual_equivalent)}</p>
                </div>
                """, unsafe_allow_html=True)
            
            with col_b:
                st.markdown(f"""
                <div class="content-section">
                    <div class="section-title">Action Steps</div>
                    <p><strong>Set up automated transfer:</strong> {format_currency(biweekly_amount)} every 2 weeks</p>
                    <p><strong>Timing:</strong> Align with your payday schedule</p>
                    <p><strong>Benefit:</strong> Smaller, more manageable amounts that build consistency</p>
                    <p><strong>Result:</strong> Stress-free progress toward your financial goals</p>
                </div>
                """, unsafe_allow_html=True)
            
            # Additional tips
            st.markdown("""
            <div class="content-section">
                <div class="section-title">Pro Tips</div>
                <ul style="margin: 0; padding-left: 1.2rem;">
                    <li><strong>Automation is key:</strong> Set up automatic transfers to remove the decision-making burden</li>
                    <li><strong>Start small:</strong> Even small biweekly amounts add up significantly over time</li>
                    <li><strong>Align with payday:</strong> Transfer money right after you get paid when funds are available</li>
                    <li><strong>Multiple goals:</strong> Use this for savings, debt payments, investments, or any recurring financial goal</li>
                    <li><strong>Momentum building:</strong> Biweekly payments create more frequent positive financial actions</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
            
        else:
            st.warning("Please enter either a monthly or annual amount to convert.")

def main():
    """Main application"""
    # Initialize session state
    if "selected_page" not in st.session_state:
        st.session_state.selected_page = "Home"
    if "last_sidebar_page" not in st.session_state:
        st.session_state.last_sidebar_page = "Home"
    
    # Create sidebar and get selected page
    sidebar_page = create_sidebar()
    
    # Only update if sidebar actually changed
    if sidebar_page != st.session_state.last_sidebar_page:
        st.session_state.selected_page = sidebar_page
        st.session_state.last_sidebar_page = sidebar_page
    
    # Use the session state page for routing
    selected_page = st.session_state.selected_page
    
    # Route to appropriate page
    if selected_page == "Home":
        home_page()
    elif selected_page == "Compound Interest":
        compound_interest_page()
    elif selected_page == "Investment Fees":
        investment_fee_page()
    elif selected_page == "Debt Free Date":
        debt_free_page()
    elif selected_page == "Biweekly Payment":
        biweekly_payment_page()

if __name__ == "__main__":
    main() 