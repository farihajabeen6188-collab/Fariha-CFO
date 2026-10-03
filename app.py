import streamlit as st
import pandas as pd
import plotly.express as px
import re

# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="Fariha CFO",
    page_icon="💼",
    layout="wide"
)

# ============================================================
# HELPER FUNCTIONS
# ============================================================

def clean_text(value):
    """Clean text for easier matching."""
    if pd.isna(value):
        return ""

    value = str(value).strip().lower()
    value = re.sub(r"\s+", " ", value)

    return value


def find_label_column(df):
    """
    Find the column most likely containing financial statement labels.
    """

    possible_names = [
        "particulars",
        "particular",
        "description",
        "account",
        "account name",
        "item",
        "line item",
        "statement item",
        "name"
    ]

    for col in df.columns:
        cleaned = clean_text(col)

        if cleaned in possible_names:
            return col

    # Fallback:
    # choose the column with the most text values
    text_scores = {}

    for col in df.columns:
        non_empty = df[col].dropna()

        if len(non_empty) == 0:
            text_scores[col] = 0
            continue

        text_count = sum(
            isinstance(x, str) and not str(x).replace(",", "").replace(".", "").isdigit()
            for x in non_empty
        )

        text_scores[col] = text_count

    if text_scores:
        return max(text_scores, key=text_scores.get)

    return None


def find_year_columns(df):
    """
    Detect columns containing years such as:
    2021, 2022, 2023, 2024, 2025
    """

    year_columns = {}

    for col in df.columns:

        # Convert column name to string
        col_text = str(col)

        # Find 4 digit year
        matches = re.findall(r"\b(20\d{2})\b", col_text)

        if matches:
            year = int(matches[-1])
            year_columns[year] = col

    return dict(sorted(year_columns.items()))


def normalize_label(label):
    """
    Normalize financial statement labels.
    """

    label = clean_text(label)

    label = label.replace("&", "and")
    label = label.replace("-", " ")
    label = label.replace("_", " ")

    label = re.sub(r"\s+", " ", label)

    return label.strip()


def convert_to_number(value):
    """
    Convert financial values into numbers.

    Handles:
    1,500,000
    1,500,000.00
    (500,000)
    $500,000
    PKR 500,000
    """

    if pd.isna(value):
        return None

    if isinstance(value, (int, float)):
        return float(value)

    value = str(value).strip()

    if value == "":
        return None

    negative = False

    # Handle brackets
    if value.startswith("(") and value.endswith(")"):
        negative = True

    # Remove currency and commas
    value = value.replace(",", "")
    value = value.replace("$", "")
    value = value.replace("PKR", "")
    value = value.replace("Rs.", "")
    value = value.replace("Rs", "")
    value = value.replace("%", "")
    value = value.replace("(", "")
    value = value.replace(")", "")

    try:
        number = float(value)

        if negative:
            number = -number

        return number

    except:
        return None


# ============================================================
# FINANCIAL LINE ITEM MAPPING
# ============================================================

FINANCIAL_LABELS = {

    "revenue": [
        "revenue",
        "sales",
        "net sales",
        "sales revenue",
        "turnover",
        "net revenue",
        "total revenue"
    ],

    "cogs": [
        "cogs",
        "cost of goods sold",
        "cost of sales",
        "cost of revenue",
        "cost of goods"
    ],

    "operating_expenses": [
        "operating expenses",
        "operating expense",
        "opex",
        "operating costs",
        "selling general and administrative expenses",
        "selling general administrative expenses"
    ],

    "interest_expense": [
        "interest expense",
        "interest cost",
        "finance cost",
        "finance costs",
        "financial charges"
    ],

    "tax_expense": [
        "tax expense",
        "income tax",
        "income tax expense",
        "taxation",
        "tax"
    ],

    "cash": [
        "cash",
        "cash and cash equivalents",
        "cash & cash equivalents",
        "cash equivalents"
    ],

    "accounts_receivable": [
        "accounts receivable",
        "account receivable",
        "trade receivables",
        "trade receivable",
        "receivables",
        "debtor",
        "debtors"
    ],

    "inventory": [
        "inventory",
        "inventories",
        "stock"
    ],

    "current_assets": [
        "current assets",
        "total current assets"
    ],

    "total_assets": [
        "total assets"
    ],

    "current_liabilities": [
        "current liabilities",
        "total current liabilities"
    ],

    "total_liabilities": [
        "total liabilities"
    ],

    "equity": [
        "equity",
        "total equity",
        "shareholders equity",
        "shareholders' equity",
        "stockholders equity",
        "total shareholders equity"
    ]
}


def match_financial_item(label):
    """
    Match a financial statement row to our standardized field.
    """

    label = normalize_label(label)

    # Exact match first
    for field, possible_names in FINANCIAL_LABELS.items():

        for name in possible_names:

            if label == normalize_label(name):
                return field

    # Partial match second
    for field, possible_names in FINANCIAL_LABELS.items():

        for name in possible_names:

            name = normalize_label(name)

            if name in label or label in name:
                return field

    return None


# ============================================================
# EXTRACT FINANCIAL DATA
# ============================================================

def extract_financial_data(df):
    """
    Extract multi-year financial data from uploaded dataframe.
    """

    label_column = find_label_column(df)

    year_columns = find_year_columns(df)

    result = {}

    if label_column is None:
        return result, None, year_columns

    for _, row in df.iterrows():

        label = row[label_column]

        field = match_financial_item(label)

        if field is None:
            continue

        result[field] = {}

        for year, column in year_columns.items():

            value = convert_to_number(row[column])

            if value is not None:
                result[field][year] = value

    return result, label_column, year_columns


# ============================================================
# HEADER
# ============================================================

st.title("💼 Fariha CFO")

st.subheader("Your Personal AI Financial Manager")

st.write(
    "Upload your financial statements or enter your financial data manually. "
    "Fariha CFO will calculate financial metrics, create visual dashboards, "
    "and help you understand your numbers."
)

st.divider()


# ============================================================
# INPUT METHOD
# ============================================================

input_method = st.radio(
    "Choose how you want to provide your financial data:",
    ["Upload Excel / CSV", "Enter Manually"],
    horizontal=True
)


# ============================================================
# DEFAULT VALUES
# ============================================================

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

multi_year_data = {}
selected_year = None


# ============================================================
# UPLOAD EXCEL / CSV
# ============================================================

if input_method == "Upload Excel / CSV":

    st.subheader("📂 Upload Financial Statement")

    uploaded_file = st.file_uploader(
        "Upload Excel or CSV file",
        type=["xlsx", "xls", "csv"]
    )

    if uploaded_file is not None:

        try:

            # Read file
            if uploaded_file.name.lower().endswith(".csv"):
                df = pd.read_csv(uploaded_file)

            else:
                df = pd.read_excel(uploaded_file)

            st.success("Financial statement uploaded successfully! ✅")

            # Show original data
            st.subheader("📋 Uploaded Data")

            st.dataframe(
                df,
                use_container_width=True
            )

            # Extract data
            extracted_data, label_column, year_columns = extract_financial_data(df)

            # ------------------------------------------------
            # DETECTED STRUCTURE
            # ------------------------------------------------

            st.subheader("🔍 Statement Structure")

            col1, col2, col3 = st.columns(3)

            with col1:
                st.metric(
                    "Rows",
                    len(df)
                )

            with col2:
                st.metric(
                    "Columns",
                    len(df.columns)
                )

            with col3:
                st.metric(
                    "Years Detected",
                    len(year_columns)
                )

            if label_column:
                st.info(
                    f"Financial line-item column detected: **{label_column}**"
                )

            if year_columns:

                detected_years = list(year_columns.keys())

                st.success(
                    f"Years detected: {', '.join(map(str, detected_years))}"
                )

                # Select year
                selected_year = st.selectbox(
                    "Select the year you want to analyze:",
                    detected_years,
                    index=len(detected_years) - 1
                )

            else:

                st.warning(
                    "No year columns were detected. "
                    "Please make sure your Excel columns contain years such as 2023, 2024 or 2025."
                )

            # ------------------------------------------------
            # MULTI-YEAR DATA
            # ------------------------------------------------

            multi_year_data = extracted_data

            # ------------------------------------------------
            # DISPLAY DETECTED ITEMS
            # ------------------------------------------------

            st.subheader("🧠 Fariha CFO Detected")

            detected_rows = []

            for field, yearly_values in extracted_data.items():

                latest_value = None

                if selected_year in yearly_values:
                    latest_value = yearly_values[selected_year]

                elif yearly_values:
                    latest_value = list(yearly_values.values())[-1]

                detected_rows.append({
                    "Financial Item": field.replace("_", " ").title(),
                    "Selected Year": selected_year,
                    "Value": latest_value
                })

            if detected_rows:

                detected_df = pd.DataFrame(detected_rows)

                st.dataframe(
                    detected_df,
                    use_container_width=True
                )

            else:

                st.warning(
                    "No recognizable financial line items were found."
                )

            # ------------------------------------------------
            # ASSIGN SELECTED YEAR VALUES
            # ------------------------------------------------

            if selected_year is not None:

                revenue = extracted_data.get(
                    "revenue", {}
                ).get(selected_year, 0)

                cogs = extracted_data.get(
                    "cogs", {}
                ).get(selected_year, 0)

                operating_expenses = extracted_data.get(
                    "operating_expenses", {}
                ).get(selected_year, 0)

                interest_expense = extracted_data.get(
                    "interest_expense", {}
                ).get(selected_year, 0)

                tax_expense = extracted_data.get(
                    "tax_expense", {}
                ).get(selected_year, 0)

                cash = extracted_data.get(
                    "cash", {}
                ).get(selected_year, 0)

                accounts_receivable = extracted_data.get(
                    "accounts_receivable", {}
                ).get(selected_year, 0)

                inventory = extracted_data.get(
                    "inventory", {}
                ).get(selected_year, 0)

                current_assets = extracted_data.get(
                    "current_assets", {}
                ).get(selected_year, 0)

                total_assets = extracted_data.get(
                    "total_assets", {}
                ).get(selected_year, 0)

                current_liabilities = extracted_data.get(
                    "current_liabilities", {}
                ).get(selected_year, 0)

                total_liabilities = extracted_data.get(
                    "total_liabilities", {}
                ).get(selected_year, 0)

                equity = extracted_data.get(
                    "equity", {}
                ).get(selected_year, 0)


        except Exception as e:

            st.error(
                f"Something went wrong while reading the file: {e}"
            )


# ============================================================
# MANUAL INPUT
# ============================================================

else:

    st.subheader("✍️ Enter Financial Data")

    col1, col2, col3 = st.columns(3)

    with col1:

        revenue = st.number_input(
            "Revenue",
            min_value=0.0,
            value=0.0
        )

        cogs = st.number_input(
            "COGS",
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

        cash = st.number_input(
            "Cash",
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

    with col3:

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
            "Equity",
            min_value=0.0,
            value=0.0
        )


# ============================================================
# CALCULATIONS
# ============================================================

gross_profit = revenue - cogs

operating_profit = gross_profit - operating_expenses

profit_before_tax = operating_profit - interest_expense

net_profit = profit_before_tax - tax_expense


# ============================================================
# RATIOS
# ============================================================

gross_margin = (
    gross_profit / revenue * 100
    if revenue != 0 else 0
)

operating_margin = (
    operating_profit / revenue * 100
    if revenue != 0 else 0
)

net_margin = (
    net_profit / revenue * 100
    if revenue != 0 else 0
)

roa = (
    net_profit / total_assets * 100
    if total_assets != 0 else 0
)

roe = (
    net_profit / equity * 100
    if equity != 0 else 0
)

current_ratio = (
    current_assets / current_liabilities
    if current_liabilities != 0 else 0
)

quick_ratio = (
    (current_assets - inventory) / current_liabilities
    if current_liabilities != 0 else 0
)

cash_ratio = (
    cash / current_liabilities
    if current_liabilities != 0 else 0
)

working_capital = (
    current_assets - current_liabilities
)

debt_ratio = (
    total_liabilities / total_assets
    if total_assets != 0 else 0
)

debt_to_equity = (
    total_liabilities / equity
    if equity != 0 else 0
)

equity_ratio = (
    equity / total_assets
    if total_assets != 0 else 0
)

interest_coverage = (
    operating_profit / interest_expense
    if interest_expense != 0 else 0
)

asset_turnover = (
    revenue / total_assets
    if total_assets != 0 else 0
)

receivables_turnover = (
    revenue / accounts_receivable
    if accounts_receivable != 0 else 0
)

dso = (
    accounts_receivable / revenue * 365
    if revenue != 0 else 0
)

inventory_turnover = (
    cogs / inventory
    if inventory != 0 else 0
)


# ============================================================
# DASHBOARD
# ============================================================

st.divider()

st.header("📊 Financial Dashboard")

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
        "Net Profit",
        f"{net_profit:,.0f}"
    )

with k4:

    st.metric(
        "Current Ratio",
        f"{current_ratio:.2f}"
    )


# ============================================================
# PROFITABILITY RATIOS
# ============================================================

st.subheader("💰 Profitability")

p1, p2, p3, p4, p5 = st.columns(5)

with p1:
    st.metric(
        "Gross Margin",
        f"{gross_margin:.2f}%"
    )

with p2:
    st.metric(
        "Operating Margin",
        f"{operating_margin:.2f}%"
    )

with p3:
    st.metric(
        "Net Margin",
        f"{net_margin:.2f}%"
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


# ============================================================
# LIQUIDITY
# ============================================================

st.subheader("💧 Liquidity")

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


# ============================================================
# SOLVENCY
# ============================================================

st.subheader("🏦 Solvency")

s1, s2, s3, s4 = st.columns(4)

with s1:
    st.metric(
        "Debt Ratio",
        f"{debt_ratio:.2f}"
    )

with s2:
    st.metric(
        "Debt / Equity",
        f"{debt_to_equity:.2f}"
    )

with s3:
    st.metric(
        "Equity Ratio",
        f"{equity_ratio:.2f}"
    )

with s4:
    st.metric(
        "Interest Coverage",
        f"{interest_coverage:.2f}"
    )


# ===