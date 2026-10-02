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
    "Upload your financial data and turn your numbers into "
    "clear financial insights."
)

st.divider()

# ==============================
# DATA INPUT
# ==============================

st.header("📂 Upload Financial Data")

st.write(
    "Upload an Excel or CSV file containing your financial data."
)

uploaded_file = st.file_uploader(
    "Choose your financial file",
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