import streamlit as st
import pandas as pd
import datetime

st.set_page_config(page_title="Loyalty Tracker", layout="centered")
st.title("🍽️ Customer Loyalty Tracker")

# Initialize loyalty data
if "loyalty_df" not in st.session_state:
    st.session_state.loyalty_df = pd.DataFrame(columns=[
        "Customer Name", "Phone Number", "Order Count", "Last Order Date", "Reward Status"])

# Input section
st.header("➕ Add / Update Customer")
name = st.text_input("Customer Name")
phone = st.text_input("Phone Number")
submit = st.button("Add Order")

# Function to calculate reward status
def get_reward_status(order_count):
    if order_count == 3:
        return "🎉 30% Discount on Next"
    elif order_count == 6:
        return "🎁 7th Meal Free"
    elif order_count > 6 and (order_count - 6) % 3 == 0:
        return "🎉 30% Discount"
    else:
        return "Keep Ordering!"

# Add or update logic
if submit and name and phone:
    df = st.session_state.loyalty_df
    if phone in df["Phone Number"].values:
        idx = df[df["Phone Number"] == phone].index[0]
        df.at[idx, "Order Count"] += 1
        df.at[idx, "Last Order Date"] = datetime.date.today()
        df.at[idx, "Reward Status"] = get_reward_status(df.at[idx, "Order Count"])
    else:
        new_order = {
            "Customer Name": name,
            "Phone Number": phone,
            "Order Count": 1,
            "Last Order Date": datetime.date.today(),
            "Reward Status": get_reward_status(1)
        }
        df = df.append(new_order, ignore_index=True)
    st.session_state.loyalty_df = df
    st.success("Order added/updated successfully!")

# Display loyalty table
st.header("📋 Customer Loyalty Table")
st.dataframe(st.session_state.loyalty_df)
