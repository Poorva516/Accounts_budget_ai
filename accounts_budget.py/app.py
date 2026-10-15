import streamlit as st
import pandas as pd
from datetime import datetime
import json

st.set_page_config(page_title="Accounts & Budget", page_icon="💰")
st.title("💰 Accounts & Budget - With AI Advisor")

# Init
if 'data' not in st.session_state:
    st.session_state.data = []

menu = st.sidebar.selectbox("Menu", ["Add Expense", "View Accounts", "Budget Planner", "AI Advisor"])

if menu == "Add Expense":
    st.header("Add Expense")
    item = st.text_input("Item Name")
    amount = st.number_input("Amount Rs.", min_value=0, step=10)
    category = st.selectbox("Category", ["Stock", "Rent", "Food", "Transport", "Investment", "Other"])
    date = st.date_input("Date", datetime.now())

    if st.button("Save"):
        if item:
            st.session_state.data.append({
                "Item": item, "Amount": amount, "Category": category, "Date": str(date)
            })
            st.success(f"Saved {item} - Rs. {amount}")
        else:
            st.error("Please enter Item Name")

elif menu == "View Accounts":
    st.header("View Accounts")
    if st.session_state.data:
        df = pd.DataFrame(st.session_state.data)
        st.dataframe(df, use_container_width=True)
        st.metric("Total Spent", f"Rs. {df['Amount'].sum()}")
        st.bar_chart(df.groupby("Category")["Amount"].sum())
    else:
        st.info("No data yet. Add expense first.")

elif menu == "Budget Planner":
    st.header("Budget Planner")
    budget = st.number_input("Monthly Budget Rs.", min_value=0, value=10000, step=500)
    if st.session_state.data:
        total = pd.DataFrame(st.session_state.data)["Amount"].sum()
        left = budget - total
        st.metric("Budget Left", f"Rs. {left}")
        if left < 0:
            st.error("Over Budget! Cut expenses.")
        elif left < budget*0.2:
            st.warning("Budget almost finished!")
        else:
            st.success("On track!")

elif menu == "AI Advisor":
    st.header("🤖 AI Advisor (Gemma)")
    st.write("This feature will use Gemma 3 model for smart budgeting tips.")
    q = st.text_input("Ask about your budget:")
    if q:
        st.info(f"Gemma Suggestion: For '{q}', try to save 20% in {st.session_state.data[0]['Category'] if st.session_state.data else 'Food'} category. Track daily!")
        st.write("In production, this connects to Ollama + Gemma 3 via API for real AI insights.")