
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(
    page_title="ERP Sales Dashboard",
    page_icon="📊",
    layout="wide"
)

st.title("ERP Sales Analysis Dashboard")
st.caption("Interactive sales analytics using Python")

df = pd.read_csv("sales_data.csv")
df["Order_Date"] = pd.to_datetime(df["Order_Date"])
df["Total_Amount"] = df["Quantity"] * df["Unit_Price"]

st.sidebar.header("Filters")

cities = ["All"] + sorted(df["City"].dropna().unique().tolist())
selected_city = st.sidebar.selectbox("Select City", cities)

products = ["All"] + sorted(df["Product_Name"].dropna().unique().tolist())
selected_product = st.sidebar.selectbox("Select Product", products)

filtered = df.copy()

if selected_city != "All":
    filtered = filtered[filtered["City"] == selected_city]

if selected_product != "All":
    filtered = filtered[filtered["Product_Name"] == selected_product]

revenue = filtered["Total_Amount"].sum()
orders = filtered["Order_ID"].nunique()
customers = filtered["Customer_Name"].nunique()
units = filtered["Quantity"].sum()

c1, c2, c3, c4 = st.columns(4)
c1.metric("Total Revenue", f"₹{revenue:,.0f}")
c2.metric("Total Orders", f"{orders:,}")
c3.metric("Unique Customers", f"{customers:,}")
c4.metric("Units Sold", f"{units:,}")

st.divider()

left, right = st.columns(2)

with left:
    st.subheader("Monthly Sales Trend")
    monthly = (
        filtered.assign(Month=filtered["Order_Date"].dt.to_period("M").astype(str))
        .groupby("Month")["Total_Amount"].sum()
        .sort_index()
    )
    st.line_chart(monthly)

with right:
    st.subheader("Product-wise Revenue")
    product_sales = (
        filtered.groupby("Product_Name")["Total_Amount"]
        .sum().sort_values(ascending=False)
    )
    st.bar_chart(product_sales)

st.subheader("City-wise Revenue")
city_sales = (
    filtered.groupby("City")["Total_Amount"]
    .sum().sort_values(ascending=False)
)
st.bar_chart(city_sales)

st.subheader("Sales Records")
st.dataframe(filtered, use_container_width=True)

st.download_button(
    "Download Filtered Sales CSV",
    data=filtered.to_csv(index=False).encode("utf-8"),
    file_name="filtered_sales_data.csv",
    mime="text/csv"
)
