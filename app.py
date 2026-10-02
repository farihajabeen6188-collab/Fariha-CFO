import streamlit as st
import pandas as pd
import plotly.express as px

# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="Fariha CFO",
    page_icon="💰",
    layout="wide"
)

# =========================================================
# HEADER
# =========================================================

st.title("💰 Fariha CFO")
st.subheader("Your AI-Powered Financial Manager")

st.write(
    "Upload your financial data or enter it manually "
    "to analyze your business performance."
)

st.divider()

# =========================================================
# DATA INPUT
# =========================================================

st.header("📊 Financial Data Input")

input_method = st.radio(
    "Choose how you want to provide your financial data:",
    [
        "📂 Upload Excel / CSV",
        "✍️ Enter Manually"
    ],
    horizontal=True
)

# =========================================================
# DEFAULT VALUES
# =========================================================

revenue = 0.0
cogs = 0.0
operating_expenses = 0.0
interest_expense = 0.0
tax_expense = 0.0

cash = 0.0
accounts_receivable = 0.0
inventory = 0.0
current_assets = 0.0
total_assets = 0.0
current_liabilities = 0.0
total_liabilities = 0.0
equity = 0.0

# =========================================================
# OPTION 1 — EXCEL / CSV
# =========================================================

if input_method == "📂 Upload Excel / CSV":

    st.subheader("📂 Upload Financial File")

    uploaded_file = st.file_uploader(
        "Choose your Excel or CSV file",
        type=["xlsx", "xls", "csv"]
    )

    if uploaded_file is not None:

        try:

            if uploaded_file.name.endswith(".csv"):
                uploaded_df = pd.read_csv(uploaded_file)

            else:
                uploaded_df = pd.read_excel(uploaded_file)

            st.success("✅ File uploaded successfully!")

            st.subheader("📋 Uploaded Data")

            st.dataframe(
                uploaded_df,
                use_container_width=True
            )

            st.info(
                f"Your file contains {uploaded_df.shape[0]} rows "
                f"and {uploaded_df.shape[1]} columns."
            )

            st.warning(
                "Automatic financial-statement mapping will be "
                "added in the next stage. For now, the uploaded "
                "data is being successfully read by Fariha CFO."
            )

        except Exception as e:

            st.error(
                f"Unable to read this file: {e}"
            )

    else:

        st.info(
            "👆 Upload an Excel or CSV file to get started."
        )


# =========================================================
# OPTION 2 — MANUAL ENTRY
# =========================================================

else:

    st.subheader("✍️ Enter Financial Data")

    st.write(
        "Enter your latest financial figures below."
    )

    col1, col2 = st.columns(2)

    # -----------------------------------------------------
    # INCOME STATEMENT
    # -----------------------------------------------------

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

    # -----------------------------------------------------
    # BALANCE SHEET
    # -----------------------------------------------------

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


# =========================================================
# FINANCIAL CALCULATIONS
# =========================================================

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


# =========================================================
# PROFITABILITY RATIOS
# =========================================================

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


# =========================================================
# LIQUIDITY RATIOS
# =========================================================

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


# =========================================================
# SOLVENCY RATIOS
# =========================================================

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


# =========================================================
# EFFICIENCY RATIOS
# =========================================================

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


if inventory > 0:

    inventory_turnover = (
        cogs / inventory
    )

else:

    inventory_turnover = 0


# =========================================================
# DASHBOARD
# =========================================================

st.divider()

st.header("📊 Financial Dashboard")


# =========================================================
# KPI CARDS
# =========================================================

k1, k2, k3, k4 = st.columns(4)

with k1:

    st.metric(
        "Revenue",
        f"{revenue:,.0f}"
    )

with k2:

    st.metric(
        "Gross Profit",
        f"{gross_profit:,.0f}"
    )

with k3:

    st.metric(
        "Operating Profit",
        f"{operating_profit:,.0f}"
    )

with k4:

    st.metric(
        "Net Profit",
        f"{net_profit:,.0f}"
    )


# =========================================================
# PROFITABILITY
# =========================================================

st.subheader("📈 Profitability Ratios")

p1, p2, p3, p4, p5 = st.columns(5)

with p1:
    st.metric(
        "Gross Margin",
        f"{gross_profit_margin:.2f}%"
    )

with p2:
    st.metric(
        "Operating Margin",
        f"{operating_profit_margin:.2f}%"
    )

with p3:
    st.metric(
        "Net Margin",
        f"{net_profit_margin:.2f}%"
    )

with p4:
    st.metric(
        "ROA",
        f"{roa:.2f}%"
    )

with p5:
    st.metric(
        "ROE",
        f"{roe:.2f}%"
    )


# =========================================================
# LIQUIDITY
# =========================================================

st.subheader("💧 Liquidity Ratios")

l1, l2, l3, l4 = st.columns(4)

with l1:

    st.metric(
        "Current Ratio",
        f"{current_ratio:.2f}"
    )

with l2:

    st.metric(
        "Quick Ratio",
        f"{quick_ratio:.2f}"
    )

with l3:

    st.metric(
        "Cash Ratio",
        f"{cash_ratio:.2f}"
    )

with l4:

    st.metric(
        "Working Capital",
        f"{working_capital:,.0f}"
    )


# =========================================================
# SOLVENCY
# =========================================================

st.subheader("🏦 Solvency Ratios")

s1, s2, s3, s4 = st.columns(4)

with s1:

    st.metric(
        "Debt Ratio",
        f"{debt_ratio:.2f}%"
    )

with s2:

    st.metric(
        "Debt-to-Equity",
        f"{debt_to_equity:.2f}"
    )

with s3:

    st.metric(
        "Equity Ratio",
        f"{equity_ratio:.2f}%"
    )

with s4:

    st.metric(
        "Interest Coverage",
        f"{interest_coverage:.2f}x"
    )


# =========================================================
# EFFICIENCY
# =========================================================

st.subheader("⚙️ Efficiency Ratios")

e1, e2, e3, e4 = st.columns(4)

with e1:

    st.metric(
        "Asset Turnover",
        f"{asset_turnover:.2f}x"
    )

with e2:

    st.metric(
        "Receivables Turnover",
        f"{receivables_turnover:.2f}x"
    )

with e3:

    st.metric(
        "DSO",
        f"{dso:.1f} days"
    )

with e4:

    st.metric(
        "Inventory Turnover",
        f"{inventory_turnover:.2f}x"
    )


# =========================================================
# PROFIT TABLE
# =========================================================

st.divider()

st.subheader("🧾 Profit Calculation")

profit_data = pd.DataFrame({
    "Metric": [
        "Revenue",
        "COGS",
        "Gross Profit",
        "Operating Expenses",
        "Operating Profit",
        "Interest Expense",
        "Profit Before Tax",
        "Tax Expense",
        "Net Profit"
    ],
    "Amount": [
        revenue,
        cogs,
        gross_profit,
        operating_expenses,
        operating_profit,
        interest_expense,
        profit_before_tax,
        tax_expense,
        net_profit
    ]
})

st.dataframe(
    profit_data,
    use_container_width=True,
    hide_index=True
)


# =========================================================
# CHART 1 — PROFIT BREAKDOWN
# =========================================================

st.divider()

st.header("📊 Financial Charts")

st.subheader("💰 Profit Breakdown")

profit_chart_data = pd.DataFrame({
    "Metric": [
        "Revenue",
        "Gross Profit",
        "Operating Profit",
        "Net Profit"
    ],
    "Amount": [
        revenue,
        gross_profit,
        operating_profit,
        net_profit
    ]
})

fig_profit = px.bar(
    profit_chart_data,
    x="Metric",
    y="Amount",
    title="Revenue & Profit Breakdown",
    text="Amount"
)

fig_profit.update_traces(
    texttemplate="%{text:,.0f}",
    textposition="outside"
)

fig_profit.update_layout(
    xaxis_title="",
    yaxis_title="Amount",
    showlegend=False
)

st.plotly_chart(
    fig_profit,
    use_container_width=True
)


# =========================================================
# CHART 2 — EXPENSE STRUCTURE
# =========================================================

st.subheader("💸 Expense Structure")

expense_chart_data = pd.DataFrame({
    "Expense": [
        "COGS",
        "Operating Expenses",
        "Interest Expense",
        "Tax Expense"
    ],
    "Amount": [
        cogs,
        operating_expenses,
        interest_expense,
        tax_expense
    ]
})

fig_expense = px.pie(
    expense_chart_data,
    names="Expense",
    values="Amount",
    title="Expense Distribution",
    hole=0.45
)

st.plotly_chart(
    fig_expense,
    use_container_width=True
)


# =========================================================
# CHART 3 — FINANCIAL POSITION
# =========================================================

st.subheader("🏦 Financial Position")

position_chart_data = pd.DataFrame({
    "Category": [
        "Total Assets",
        "Total Liabilities",
        "Equity"
    ],
    "Amount": [
        total_assets,
        total_liabilities,
        equity
    ]
})

fig_position = px.bar(
    position_chart_data,
    x="Category",
    y="Amount",
    title="Assets vs Liabilities vs Equity",
    text="Amount"
)

fig_position.update_traces(
    texttemplate="%{text:,.0f}",
    textposition="outside"
)

fig_position.update_layout(
    xaxis_title="",
    yaxis_title="Amount",
    showlegend=False
)

st.plotly_chart(
    fig_position,
    use_container_width=True
)


# =========================================================
# CHART 4 — RATIO OVERVIEW
# =========================================================

st.subheader("📈 Key Ratio Overview")

ratio_chart_data = pd.DataFrame({
    "Ratio": [
        "Current Ratio",
        "Quick Ratio",
        "Cash Ratio",
        "Debt-to-Equity"
    ],
    "Value": [
        current_ratio,
        quick_ratio,
        cash_ratio,
        debt_to_equity
    ]
})

fig_ratio = px.bar(
    ratio_chart_data,
    x="Ratio",
    y="Value",
    title="Liquidity & Leverage Ratios",
    text="Value"
)

fig_ratio.update_traces(
    texttemplate="%{text:.2f}",
    textposition="outside"
)

fig_ratio.update_layout(
    xaxis_title="",
    yaxis_title="Ratio",
    showlegend=False
)

st.plotly_chart(
    fig_ratio,
    use_container_width=True
)


# =========================================================
# FOOTER
# =========================================================

st.divider()

st.caption(
    "Fariha CFO • Financial analysis and decision-support tool"
