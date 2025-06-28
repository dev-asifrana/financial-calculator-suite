# Financial Calculator Suite

A professional, mobile-friendly web application that provides four essential financial calculators to help users make informed financial decisions. Built with Streamlit and designed with a clean, modern interface.

## 🚀 Features

- **Responsive Design**: Works seamlessly on desktop, tablet, and mobile devices
- **Professional UI**: Clean, modern interface with consistent styling
- **Interactive Charts**: Visual representations of financial data using Plotly
- **Real-time Calculations**: Instant results as you adjust parameters
- **Professional Branding**: Logo support and corporate styling

## 📊 Calculators Included

### 1. Compound Interest Calculator
Calculate how your money grows over time with compound interest and regular contributions.

**Features:**
- Initial investment and monthly contribution inputs
- Flexible compounding frequencies (daily, monthly, quarterly, etc.)
- Interactive growth visualization
- Total interest earned breakdown
- Return on investment percentage

### 2. Investment Fee Comparison
Compare the long-term impact of investment fees between self-managed and advisor-managed portfolios.

**Features:**
- Self-managed vs advisor-managed comparison
- Fee impact visualization over time
- Total fees paid calculation
- Side-by-side results display
- Portfolio value projections

### 3. Debt-Free Date Calculator
Plan your path to financial freedom by calculating when you'll be debt-free and potential savings.

**Features:**
- Payoff timeline calculation
- Extra payment impact analysis
- Total interest savings calculation
- Monthly payment breakdown
- Interactive debt reduction chart

### 4. Biweekly Payment Calculator
Convert monthly or annual payments into biweekly amounts that align with your pay schedule.

**Features:**
- Monthly to biweekly conversion
- Annual to biweekly conversion
- 26 pay periods per year calculation
- Automated transfer planning
- Payment automation guidance

## 🛠️ Installation

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/yourusername/financial-calculator-suite.git
   cd financial-calculator-suite
   ```

2. **Create a virtual environment (recommended):**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application:**
   ```bash
   streamlit run app.py
   ```

5. **Open your browser:**
   The application will automatically open in your default browser at `http://localhost:8501`

## 🎯 Usage

### Navigation
- Use the sidebar to navigate between different calculators
- Click on cards from the home page to access specific calculators
- All calculators maintain your inputs during the session

### Calculator Usage
1. **Select a calculator** from the home page or sidebar
2. **Enter your financial parameters** in the input fields
3. **Click the calculate button** to see results
4. **View interactive charts** to visualize your financial projections
5. **Adjust parameters** to explore different scenarios

## 📁 Project Structure

```
financial-calculator-suite/
├── app.py                 # Main Streamlit application
├── requirements.txt       # Python dependencies
├── README.md             # Project documentation
└── assets/               # Static assets (optional)
    └── logo.png          # Application logo (optional)
```

## 🎨 Customization

### Logo
Place your logo file as `assets/logo.png` to display it in the sidebar. The application will gracefully fall back to text if no logo is found.

### Styling
The application uses custom CSS defined in `app.py`. You can modify the styling by updating the CSS in the `st.markdown()` section.

### Calculations
All financial calculations are implemented using standard financial formulas:
- **Compound Interest**: Future Value with regular payments
- **Investment Fees**: Net return calculation with fee deduction
- **Debt Payoff**: Amortization with optional extra payments

## 🔧 Dependencies

- **Streamlit**: Web application framework
- **Pandas**: Data manipulation and analysis
- **Plotly**: Interactive charting library
- **NumPy**: Numerical computing

## 📱 Browser Compatibility

- Chrome (recommended)
- Firefox
- Safari
- Edge
- Mobile browsers

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🏢 About

© 2025 - Your Financial Evolution

Professional financial calculator suite designed to help individuals make informed financial decisions through interactive calculations and visualizations.

## 🆘 Support

If you encounter any issues or have questions:

1. Check the [Issues](https://github.com/yourusername/financial-calculator-suite/issues) page
2. Create a new issue with detailed information
3. Include steps to reproduce any bugs

## 🎉 Acknowledgments

- Built with [Streamlit](https://streamlit.io/)
- Charts powered by [Plotly](https://plotly.com/)
- Inspired by professional financial planning tools

---

**Note**: This tool is for educational and planning purposes only. Always consult with financial professionals for important financial decisions. 