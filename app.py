import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Fariha CFO",
    page_icon="💰",
    layout="wide"
)

st.title("💰 Fariha CFO")
st.subheader("Your AI-Powered Financial Manager")

st.write(
    "Upload your financial data or enter it manually "
    "to start analyzing your business."
)

st.divider()

# ==========================================
# DATA INPUT OPTIONS
# ==========================================

st.header("📊 Financial Data Input")

input_method = st.radio(
    "How would you like to enter your financial data?",
    [
        "📂 Upload Excel / CSV",
        "✍️ Enter Manually"
    ],
    horizontal=True
)

# ==========================================
# EXCEL / CSV UPLOAD
# ==========================================

if input_method == "📂 Upload Excel / CSV":

    st.subheader("📂 Upload Financial File")

    uploaded_file = st.file_uploader(
        "Choose an Excel or CSV file",
        type=["xlsx", "xls", "csv"]
    )

    if uploaded_file is not None:

        try:

            if uploaded_file.name.endswith(".csv"):
                df = pd.read_csv(uploaded_file)

            else:
                df = pd.read_excel(uploaded_file)

            st.success("✅ File uploaded successfully!")

            st.subheader("📋 Your Financial Data")

            st.dataframe(
                df,
                use_container_width=True
            )

            st.info(
                f"Your file contains {df.shape[0]} rows "
                f"and {df.shape[1]} columns."
            )

        except Exception as e:

            st.error(
                f"Unable to read this file. Error: {e}"
            )

    else:

        st.info(
            "👆 Upload an Excel or CSV file to get started."
        )


# ==========================================
# MANUAL DATA ENTRY
# ==========================================

else:

    st.subheader("✍️ Enter Financial Data")

    st.write(
        "Enter your latest financial figures below."
    )

    col1, col2 = st.columns(2)

    with col1:

        st.markdown("### 💰 Income Statement")

        revenue = st.number_input(
            "Revenue",
            min_value=0.0,
            value=0.0
        )

        cogs = st.number_input(
            "Cost of Goods Sold (COGS)",
            min_value=0.0,
            value=0.0
        )

        operating_expenses = st.number_input(
            "Operating Expenses",
            min_value=0.0,
            value=0.0
        )

        interest_expense = st.number_input(
            "Interest Expense",
            min_value=0.0,
            value=0.0
        )

        tax_expense = st.number_input(
            "Tax Expense",
            min_value=0.0,
            value=0.0
        )

    with col2:

        st.markdown("### 🏦 Balance Sheet")

        cash = st.number_input(
            "Cash & Cash Equivalents",
            min_value=0.0,
            value=0.0
        )

        accounts_receivable = st.number_input(
            "Accounts Receivable",
            min_value=0.0,
            value=0.0
        )

        inventory = st.number_input(
            "Inventory",
            min_value=0.0,
            value=0.0
        )

        current_assets = st.number_input(
            "Current Assets",
            min_value=0.0,
            value=0.0
        )

        total_assets = st.number_input(
            "Total Assets",
            min_value=0.0,
            value=0.0
        )

        current_liabilities = st.number_input(
            "Current Liabilities",
            min_value=0.0,
            value=0.0
        )

        total_liabilities = st.number_input(
            "Total Liabilities",
            min_value=0.0,
            value=0.0
        )

        equity = st.number_input(
            "Shareholders' Equity",
            min_value=0.0,
            value=0.0
        )

    st.divider()

    if st.button("💾 Save Financial Data"):

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

        st.success(
            "✅ Financial data recorded successfully!"
        )

        st.subheader("📋 Financial Summary")

        summary_col1, summary_col2, summary_col3 = st.columns(3)

        with summary_col1:

            st.metric(
                "Revenue",
                f"{revenue:,.0f}"
            )

            st.metric(
                "Gross Profit",
                f"{gross_profit:,.0f}"
            )

        with summary_col2:

            st.metric(
                "Operating Profit",
                f"{operating_profit:,.0f}"
            )

            st.metric(
                "Profit Before Tax",
                f"{profit_before_tax:,.0f}"
            )

        with summary_col3:

            st.metric(
                "Net Profit",
                f"{net_profit:,.0f}"
            )

            st.metric(
                "Total Assets",
                f"{total_assets:,.0f}"
            )