import streamlit as st
import pandas as pd

# ==========================================
# PAGE CONFIGURATION
# ==========================================

st.set_page_config(
    page_title="Fariha CFO",
    page_icon="💰",
    layout="wide"
)

# ==========================================
# HEADER
# ==========================================

st.title("💰 Fariha CFO")
st.subheader("Your AI-Powered Financial Manager")

st.write(
    "Enter your financial information and Fariha CFO "
    "will calculate key financial ratios automatically."
)

st.divider()

# ==========================================
# FINANCIAL DATA INPUT
# ==========================================

st.header("📊 Financial Data")

col1, col2 = st.columns(2)

with col1:

    st.markdown("### 💰 Income Statement")

    revenue = st.number_input(
        "Revenue",
        min_value=0.0,
        value=1000000.0
    )

    cogs = st.number_input(
        "Cost of Goods Sold (COGS)",
        min_value=0.0,
        value=600000.0
    )

    operating_expenses = st.number_input(
        "Operating Expenses",
        min_value=0.0,
        value=200000.0
    )

    interest_expense = st.number_input(
        "Interest Expense",
        min_value=0.0,
        value=20000.0
    )

    tax_expense = st.number_input(
        "Tax Expense",
        min_value=0.0,
        value=36000.0
    )

with col2:

    st.markdown("### 🏦 Balance Sheet")

    cash = st.number_input(
        "Cash & Cash Equivalents",
        min_value=0.0,
        value=100000.0
    )

    accounts_receivable = st.number_input(
        "Accounts Receivable",
        min_value=0.0,
        value=150000.0
    )

    inventory = st.number_input(
        "Inventory",
        min_value=0.0,
        value=200000.0
    )

    current_assets = st.number_input(
        "Current Assets",
        min_value=0.0,
        value=500000.0
    )

    total_assets = st.number_input(
        "Total Assets",
        min_value=0.0,
        value=1000000.0
    )

    current_liabilities = st.number_input(
        "Current Liabilities",
        min_value=0.0,
        value=300000.0
    )

    total_liabilities = st.number_input(
        "Total Liabilities",
        min_value=0.0,
        value=500000.0
    )

    equity = st.number_input(
        "Shareholders' Equity",
        min_value=0.0,
        value=500000.0
    )

st.divider()

# ==========================================
# CALCULATIONS
# ==========================================

gross_profit = revenue - cogs

operating_profit = (
    gross_profit - operating_expenses
)

profit_before_tax = (
    operating_profit - interest_expense
)

net_profit = (
    profit_before_tax - tax_expense
)

working_capital = (
    current_assets - current_liabilities
)

# ==========================================
# PROFITABILITY RATIOS
# ==========================================

if revenue > 0:

    gross_profit_margin = (
        gross_profit / revenue
    ) * 100

    operating_profit_margin = (
        operating_profit / revenue
    ) * 100

    net_profit_margin = (
        net_profit / revenue
    ) * 100

else:

    gross_profit_margin = 0
    operating_profit_margin = 0
    net_profit_margin = 0


if total_assets > 0:

    roa = (
        net_profit / total_assets
    ) * 100

else:

    roa = 0


if equity > 0:

    roe = (
        net_profit / equity
    ) * 100

else:

    roe = 0


# ==========================================
# LIQUIDITY RATIOS
# ==========================================

if current_liabilities > 0:

    current_ratio = (
        current_assets / current_liabilities
    )

    quick_ratio = (
        current_assets - inventory
    ) / current_liabilities

    cash_ratio = (
        cash / current_liabilities
    )

else:

    current_ratio = 0
    quick_ratio = 0
    cash_ratio = 0


# ==========================================
# SOLVENCY RATIOS
# ==========================================

if total_assets > 0:

    debt_ratio = (
        total_liabilities / total_assets
    ) * 100

    equity_ratio = (
        equity / total_assets
    ) * 100

else:

    debt_ratio = 0
    equity_ratio = 0


if equity > 0:

    debt_to_equity = (
        total_liabilities / equity
    )

else:

    debt_to_equity = 0


if interest_expense > 0:

    interest_coverage = (
        operating_profit / interest_expense
    )

else:

    interest_coverage = 0


# ==========================================
# EFFICIENCY RATIOS
# ==========================================

if total_assets > 0:

    asset_turnover = (
        revenue / total_assets
    )

else:

    asset_turnover = 0


if accounts_receivable > 0:

    receivables_turnover = (
        revenue / accounts_receivable
    )

    dso = (
        accounts_receivable / revenue
    ) * 365

else:

    receivables_turnover = 0
    dso = 0


if inventory > 