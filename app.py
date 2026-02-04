import streamlit as st
import pandas as pd
from database import init_db, add_holding, get_holdings

st.set_page_config(page_title="Investor Dashboard", layout="centered")

# Initialize DB
init_db()

st.header("Investor Dashboard")

# Load users CSV
users_df = pd.read_csv("users.csv")
users_df.columns = users_df.columns.str.strip().str.lower()
valid_emails = users_df["email"].astype(str).str.strip().tolist()

# -------- Add Holding --------
with st.form("add_holding"):
    email = st.text_input("Investor Email").strip().lower()

    if email and email not in valid_emails:
        st.error("Email not found in approved user list")
        st.stop()

    symbol = st.text_input("Stock Symbol")
    shares = st.number_input("Shares", min_value=1, step=1)
    buy_price = st.number_input("Buy Price", min_value=0.0)
    threshold = st.number_input("Alert Threshold", min_value=0.0)

    submitted = st.form_submit_button("Add Holding")

    if submitted:
        add_holding(email, symbol, shares, buy_price, threshold)
        st.success("Holding added successfully!")

# -------- View Holdings --------
st.divider()
st.subheader("View Holdings")

view_email = st.text_input("Enter email to view saved holdings").strip().lower()

if view_email:
    if view_email not in valid_emails:
        st.error("Email not found in approved user list")
    else:
        holdings = get_holdings(view_email)
        if holdings:
            for h in holdings:
                st.write(
                    f"📈 {h['symbol']} | Shares: {h['shares']} | "
                    f"Buy: {h['buy_price']} | Alert: {h['threshold']}"
                )
        else:
            st.info("No holdings found.")
