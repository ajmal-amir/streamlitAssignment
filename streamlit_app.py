import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import math

st.title("Data App Assignment, on June 20th")

st.write("### Input Data and Examples")
df = pd.read_csv("Superstore_Sales_utf8.csv", parse_dates=True)
st.dataframe(df)

# Print the column names to verify the presence of 'Sub-Category'
st.write("### Column Names")
st.write(df.columns)

# This bar chart will not have solid bars--but lines--because the detail data is being graphed independently
st.bar_chart(df, x="Category", y="Sales")

# Now let's do the same graph where we do the aggregation first in Pandas... (this results in a chart with solid bars)
st.dataframe(df.groupby("Category").sum())
# Using as_index=False here preserves the Category as a column. If we exclude that, Category would become the dataframe index and we would need to use x=None to tell bar_chart to use the index
st.bar_chart(df.groupby("Category", as_index=False).sum(), x="Category", y="Sales", color="#04f")

# Aggregating by time
# Here we ensure Order_Date is in datetime format, then set it as an index to our dataframe
df["Order_Date"] = pd.to_datetime(df["Order_Date"])
df.set_index('Order_Date', inplace=True)
# Here the Grouper is using our newly set index to group by Month ('ME')
sales_by_month = df.filter(items=['Sales']).groupby(pd.Grouper(freq='ME')).sum()

st.dataframe(sales_by_month)

# Here the grouped months are the index and automatically used for the x axis
st.line_chart(sales_by_month, y="Sales")

st.write("## Your additions")

# (1) Add a drop-down for Category
category = st.selectbox("Select a Category", df["Category"].unique())

# Check if 'Sub-Category' exists in the dataframe
if 'Sub-Category' in df.columns:
    # (2) Add a multi-select for Sub-Category in the selected Category
    sub_categories = st.multiselect(
        "Select Sub-Categories",
        df[df["Category"] == category]["Sub-Category"].unique()
    )

    if sub_categories:
        # Filter the dataframe based on the selected Sub-Categories
        filtered_df = df[(df["Category"] == category) & (df["Sub-Category"].isin(sub_categories))]

        # (3) Show a line chart of sales for the selected items
        sales_by_month_filtered = filtered_df.filter(items=['Sales']).groupby(pd.Grouper(freq='ME')).sum()
        st.line_chart(sales_by_month_filtered, y="Sales")

        # (4) Show three metrics for the selected items: total sales, total profit, and overall profit margin
        total_sales = filtered_df["Sales"].sum()
        total_profit = filtered_df["Profit"].sum()
        overall_profit_margin = (total_profit / total_sales) * 100 if total_sales else 0

        # Overall average profit margin for all products across all categories
        total_sales_all = df["Sales"].sum()
        total_profit_all = df["Profit"].sum()
        overall_profit_margin_all = (total_profit_all / total_sales_all) * 100 if total_sales_all else 0

        # (5) Use the delta option in the overall profit margin metric
        profit_margin_delta = overall_profit_margin - overall_profit_margin_all

        st.metric("Total Sales", f"${total_sales:,.2f}")
        st.metric("Total Profit", f"${total_profit:,.2f}")
        st.metric("Overall Profit Margin", f"{overall_profit_margin:.2f}%", delta=f"{profit_margin_delta:.2f}%")
else:
    st.write("The 'Sub-Category' column does not exist in the dataset.")
