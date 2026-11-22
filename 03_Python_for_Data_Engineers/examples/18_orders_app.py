"""XYZ Company order dashboard. Run with:  streamlit run 18_orders_app.py"""
import pandas as pd
import streamlit as st

ORDERS = pd.DataFrame(
    {
        "order_id": [1001, 1002, 1003, 1004, 1005, 1006, 1007, 1008],
        "region": ["West", "East", "West", "North", "South", "West", "East", "North"],
        "status": ["completed", "completed", "cancelled", "completed", "completed", "pending", "completed", "completed"],
        "amount": [1200.0, 800.0, 300.0, 500.0, 950.0, 400.0, 650.0, 720.0],
    }
)

st.set_page_config(page_title="XYZ Orders", layout="centered")
st.title("XYZ Company: Orders")
st.write("Cleaned orders from the nightly pipeline.")

regions = st.sidebar.multiselect("Region", sorted(ORDERS["region"].unique()), default=sorted(ORDERS["region"].unique()))
only_completed = st.sidebar.checkbox("Completed orders only", value=True)

view = ORDERS[ORDERS["region"].isin(regions)]
if only_completed:
    view = view[view["status"] == "completed"]

left, right = st.columns(2)
left.metric("Orders", len(view))
right.metric("Revenue", f"{view['amount'].sum():,.2f}")

if view.empty:
    st.warning("No orders match the selected filters.")
else:
    st.subheader("Revenue by region")
    st.bar_chart(view.groupby("region")["amount"].sum())
    st.subheader("Orders")
    st.dataframe(view, hide_index=True)
