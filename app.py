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
    page_title="Financial Calculator Suite",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for clean, professional design
st.markdown("""
<style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    /* Global Styles */
    .main {
        padding: 0;
        background-color: #f8fafc;
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
        background-color: #f8fafc;
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
        background: #3182ce !important;
        border-color: #3182ce !important;
        color: #ffffff !important;
    }
    
    /* Primary button styling */
    section[data-testid="stSidebar"] button[data-testid="baseButton-primary"] {
        background: linear-gradient(135deg, #3182ce 0%, #2c5aa0 100%) !important;
        color: #ffffff !important;
        border: none !important;
        border-radius: 12px !important;
        padding: 1rem 1.5rem !important;
        font-weight: 600 !important;
        font-size: 0.9rem !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 12px rgba(49, 130, 206, 0.3) !important;
        margin-top: 1rem !important;
    }
    
    section[data-testid="stSidebar"] button[data-testid="baseButton-primary"]:hover {
        background: linear-gradient(135deg, #2c5aa0 0%, #2a4a7c 100%) !important;
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 20px rgba(49, 130, 206, 0.5) !important;
    }
    
    section[data-testid="stSidebar"] button[data-testid="baseButton-primary"]:active {
        transform: translateY(0px) !important;
        box-shadow: 0 2px 8px rgba(49, 130, 206, 0.3) !important;
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
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 16px;
        padding: 3rem 2rem;
        margin-bottom: 2rem;
        color: white;
        text-align: center;
        box-shadow: 0 10px 30px rgba(0,0,0,0.1);
    }
    
    .page-header h1 {
        font-size: 2.5rem;
        font-weight: 700;
        margin: 0 0 0.5rem 0;
        color: white !important;
    }
    
    .page-header p {
        font-size: 1.125rem;
        opacity: 0.9;
        margin: 0;
        color: white !important;
    }
    
    /* Dashboard cards */
    .dashboard-cards {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
        gap: 2rem;
        margin-bottom: 2rem;
    }
    
    .calculator-card {
        background: white;
        border-radius: 16px;
        padding: 2rem;
        box-shadow: 0 4px 12px rgba(0,0,0,0.08);
        border: 1px solid #e2e8f0;
        transition: all 0.3s ease;
        cursor: pointer;
        text-decoration: none;
        color: inherit;
    }
    
    .calculator-card:hover {
        transform: translateY(-8px);
        box-shadow: 0 16px 48px rgba(0,0,0,0.15);
        border-color: #3182ce;
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
    
    .card-icon.compound { background: #ebf8ff; color: #3182ce; }
    .card-icon.investment { background: #f0fff4; color: #38a169; }
    .card-icon.debt { background: #fed7d7; color: #e53e3e; }
    
    .card-title {
        font-size: 1.5rem;
        font-weight: 700;
        color: #1a202c;
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
        background: white;
        border-radius: 16px;
        padding: 2rem;
        box-shadow: 0 4px 12px rgba(0,0,0,0.08);
        border: 1px solid #e2e8f0;
        margin-bottom: 2rem;
    }
    
    .section-title {
        font-size: 1.5rem;
        font-weight: 700;
        color: #1a202c;
        margin-bottom: 1.5rem;
    }
    
    /* Results styling */
    .results-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
        gap: 1.5rem;
        margin: 2rem 0;
    }
    
    .result-card {
        background: #f7fafc;
        border-radius: 12px;
        padding: 1.5rem;
        text-align: center;
        border: 1px solid #e2e8f0;
    }
    
    .result-value {
        font-size: 1.75rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
    }
    
    .result-value.positive { color: #38a169; }
    .result-value.negative { color: #e53e3e; }
    .result-value.neutral { color: #3182ce; }
    
    .result-label {
        font-size: 0.875rem;
        color: #718096;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    
    /* Responsive design */
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
                st.image('assets/logo.png', width=200)
            else:
                st.markdown("### Financial Calculator Suite")
        except:
            st.markdown("### Financial Calculator Suite")
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Navigation
        st.markdown("""
        <div class="sidebar-section">
            <h3>Calculators</h3>
        </div>
        """, unsafe_allow_html=True)
        
        # Get current page from session state for default selection
        current_page = st.session_state.get("selected_page", "Home")
        page_options = ["Home", "Compound Interest", "Investment Fees", "Debt Free Date"]
        default_index = page_options.index(current_page) if current_page in page_options else 0
        
        page = st.radio(
            "",
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
        **Professional Financial Tools**
        
        Calculate compound interest, compare investment fees, and plan your debt-free journey with our suite of financial calculators.
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
        <div class="page-header">
            <h1>Financial Calculator Suite</h1>
            <p>Professional tools to help you make informed financial decisions</p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Create three columns for the calculator cards
    col1, col2, col3 = st.columns(3, gap="large")
    
    with col1:
        # Compound Interest Calculator Card
        with st.container():
            st.markdown("""
            <div style="
                background: white;
                border-radius: 16px;
                padding: 2rem;
                box-shadow: 0 4px 12px rgba(0,0,0,0.08);
                border: 1px solid #e2e8f0;
                height: 300px;
                cursor: pointer;
                transition: all 0.3s ease;
            ">
                <h3 style="color: #1a202c; margin-bottom: 1rem;">Compound Interest Calculator</h3>
                <p style="color: #718096; margin-bottom: 1.5rem;"><strong>Calculate how your money grows over time with compound interest and regular contributions.</strong></p>
                <ul style="color: #4a5568; padding-left: 1.2rem; margin: 0;">
                    <li>Initial investment & monthly contributions</li>
                    <li>Flexible compounding frequencies</li>
                    <li>Interactive growth visualization</li>
                    <li>Total interest earned breakdown</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
            
            if st.button("Access Calculator", key="compound", use_container_width=True, type="primary"):
                st.session_state.selected_page = "Compound Interest"
                st.rerun()
    
    with col2:
        # Investment Fee Comparison Card
        with st.container():
            st.markdown("""
            <div style="
                background: white;
                border-radius: 16px;
                padding: 2rem;
                box-shadow: 0 4px 12px rgba(0,0,0,0.08);
                border: 1px solid #e2e8f0;
                height: 300px;
                cursor: pointer;
                transition: all 0.3s ease;
            ">
                <h3 style="color: #1a202c; margin-bottom: 1rem;">Investment Fee Comparison</h3>
                <p style="color: #718096; margin-bottom: 1.5rem;"><strong>Compare the long-term impact of investment fees between self-managed and advisor-managed portfolios.</strong></p>
                <ul style="color: #4a5568; padding-left: 1.2rem; margin: 0;">
                    <li>Self-managed vs advisor comparison</li>
                    <li>Fee impact visualization</li>
                    <li>Total fees paid calculation</li>
                    <li>Side-by-side results</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
            
            if st.button("Access Calculator", key="investment", use_container_width=True, type="primary"):
                st.session_state.selected_page = "Investment Fees"
                st.rerun()
    
    with col3:
        # Debt-Free Date Calculator Card
        with st.container():
            st.markdown("""
            <div style="
                background: white;
                border-radius: 16px;
                padding: 2rem;
                box-shadow: 0 4px 12px rgba(0,0,0,0.08);
                border: 1px solid #e2e8f0;
                height: 300px;
                cursor: pointer;
                transition: all 0.3s ease;
            ">
                <h3 style="color: #1a202c; margin-bottom: 1rem;">Debt-Free Date Calculator</h3>
                <p style="color: #718096; margin-bottom: 1.5rem;"><strong>Plan your path to financial freedom by calculating when you'll be debt-free and how much you can save.</strong></p>
                <ul style="color: #4a5568; padding-left: 1.2rem; margin: 0;">
                    <li>Payoff timeline calculation</li>
                    <li>Extra payment impact analysis</li>
                    <li>Total interest savings</li>
                    <li>Monthly payment breakdown</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
            
            if st.button("Access Calculator", key="debt", use_container_width=True, type="primary"):
                st.session_state.selected_page = "Debt Free Date"
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
            compound_frequency = st.selectbox(
                "Compounding Frequency",
                ["Annually", "Semi-annually", "Quarterly", "Monthly", "Daily"],
                index=3
            )
            
            frequency_map = {
                "Annually": 1,
                "Semi-annually": 2, 
                "Quarterly": 4,
                "Monthly": 12,
                "Daily": 365
            }
            n = frequency_map[compound_frequency]
        
        # Form-style button positioning
        st.markdown("<br>", unsafe_allow_html=True)
        col1, col2, col3, col4 = st.columns([1, 1, 1, 1])
        with col4:
            calculate_clicked = st.button("Calculate", type="primary", use_container_width=True)
    
    # Results section
    if calculate_clicked:
        # Calculate compound interest with regular contributions
        r = annual_rate / 100
        
        # Future value of initial investment
        future_value_initial = initial_amount * (1 + r/n)**(n*years)
        
        # Future value of regular contributions (annuity)
        if monthly_contribution > 0:
            monthly_rate = r / 12
            future_value_contributions = monthly_contribution * (((1 + monthly_rate)**(12*years) - 1) / monthly_rate)
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
            fv_initial = initial_amount * (1 + r/n)**(n*years_elapsed)
            
            # Future value of contributions made so far
            if month > 0 and monthly_contribution > 0:
                months_contributing = month
                monthly_rate = r / 12
                fv_contributions = monthly_contribution * (((1 + monthly_rate)**months_contributing - 1) / monthly_rate)
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
            annual_contribution = st.number_input("Annual Contribution ($)", min_value=0.0, value=6000.0, step=500.0)
            years = st.number_input("Investment Duration (Years)", min_value=1, max_value=50, value=25, step=1)
            advisor_fee = st.number_input("Advisor-Managed Fee (%)", min_value=0.0, max_value=5.0, value=1.25, step=0.01)
        
        # Form-style button positioning
        st.markdown("<br>", unsafe_allow_html=True)
        col1, col2, col3, col4 = st.columns([1, 1, 1, 1])
        with col4:
            calculate_clicked = st.button("Compare Scenarios", type="primary", use_container_width=True)
    
    # Results section
    if calculate_clicked:
        # Calculate both scenarios
        r_gross = expected_return / 100
        r_self = r_gross - (self_managed_fee / 100)
        r_advisor = r_gross - (advisor_fee / 100)
        
        # Self-managed scenario
        future_value_self_initial = starting_amount * (1 + r_self)**years
        if annual_contribution > 0:
            future_value_self_contributions = annual_contribution * (((1 + r_self)**years - 1) / r_self)
        else:
            future_value_self_contributions = 0
        total_self = future_value_self_initial + future_value_self_contributions
        
        # Advisor-managed scenario  
        future_value_advisor_initial = starting_amount * (1 + r_advisor)**years
        if annual_contribution > 0:
            future_value_advisor_contributions = annual_contribution * (((1 + r_advisor)**years - 1) / r_advisor)
        else:
            future_value_advisor_contributions = 0
        total_advisor = future_value_advisor_initial + future_value_advisor_contributions
        
        # Calculate total invested
        total_invested = starting_amount + (annual_contribution * years)
        
        # Calculate fees paid
        fees_self = total_invested * (self_managed_fee / 100) * years
        fees_advisor = total_invested * (advisor_fee / 100) * years
        
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
            # Self-managed
            fv_self_initial = starting_amount * (1 + r_self)**year
            if annual_contribution > 0 and year > 0:
                fv_self_contrib = annual_contribution * (((1 + r_self)**year - 1) / r_self)
            else:
                fv_self_contrib = 0
            self_values.append(fv_self_initial + fv_self_contrib)
            
            # Advisor-managed
            fv_advisor_initial = starting_amount * (1 + r_advisor)**year
            if annual_contribution > 0 and year > 0:
                fv_advisor_contrib = annual_contribution * (((1 + r_advisor)**year - 1) / r_advisor)
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
            monthly_payment = st.number_input("Monthly Payment ($)", min_value=0.0, value=500.0, step=25.0)
            extra_payment = st.number_input("Extra Monthly Payment ($)", min_value=0.0, value=100.0, step=25.0)
        
        # Form-style button positioning
        st.markdown("<br>", unsafe_allow_html=True)
        col1, col2, col3, col4 = st.columns([1, 1, 1, 1])
        with col4:
            calculate_clicked = st.button("Calculate Payoff", type="primary", use_container_width=True)
    
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
                <div class="result-value neutral">{int(months_standard)} months</div>
                <div class="result-label">Standard Payoff Time</div>
            </div>
            <div class="result-card">
                <div class="result-value positive">{int(months_extra)} months</div>
                <div class="result-label">With Extra Payments</div>
            </div>
            <div class="result-card">
                <div class="result-value positive">{int(months_saved)} months</div>
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
        months_to_show = int(max(months_standard, months_extra))
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

def main():
    """Main application"""
    # Initialize session state
    if "selected_page" not in st.session_state:
        st.session_state.selected_page = "Home"
    
    # Create sidebar and get selected page
    selected_page = create_sidebar()
    
    # Update session state with sidebar selection
    st.session_state.selected_page = selected_page
    
    # Route to appropriate page
    if selected_page == "Home":
        home_page()
    elif selected_page == "Compound Interest":
        compound_interest_page()
    elif selected_page == "Investment Fees":
        investment_fee_page()
    elif selected_page == "Debt Free Date":
        debt_free_page()

if __name__ == "__main__":
    main() 