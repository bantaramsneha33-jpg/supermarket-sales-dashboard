import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path


# ======================================================
# PAGE CONFIGURATION
# ======================================================

st.set_page_config(
    page_title="Supermarket Sales Dashboard",
    page_icon="🛒",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ======================================================
# CUSTOM CSS
# ======================================================

st.markdown(
    """
    <style>

    .block-container {
        padding-top: 1.5rem;
        padding-bottom: 2rem;
        padding-left: 2rem;
        padding-right: 2rem;
    }

    h1, h2, h3 {
        font-family: Arial, sans-serif;
    }

    [data-testid="metric-container"] {
        background-color: #ffffff;
        border: 1px solid #e6e6e6;
        border-radius: 12px;
        padding: 18px;
        box-shadow: 0px 2px 8px rgba(0, 0, 0, 0.06);
    }

    section[data-testid="stSidebar"] {
        border-right: 1px solid #e6e6e6;
    }

    </style>
    """,
    unsafe_allow_html=True
)
st.markdown(
    """
    <style>

    .block-container {
        padding-top: 1.5rem;
        padding-bottom: 2rem;
        padding-left: 2rem;
        padding-right: 2rem;
    }

    h1, h2, h3 {
        font-family: Arial, sans-serif;
    }

    [data-testid="metric-container"] {
        background-color: #ffffff;
        border: 1px solid #e6e6e6;
        border-radius: 12px;
        padding: 18px;
        box-shadow: 0px 2px 8px rgba(0, 0, 0, 0.06);
    }

    /* Wider sidebar */
    section[data-testid="stSidebar"] {
        min-width: 320px !important;
        width: 320px !important;
        border-right: 1px solid #e6e6e6;
    }

    section[data-testid="stSidebar"] > div {
        width: 320px !important;
    }

    /* Better spacing for sidebar widgets */
    section[data-testid="stSidebar"] .stMultiSelect {
        margin-bottom: 0.8rem;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ======================================================
# LOAD DATA
# ======================================================

@st.cache_data
def load_data():

    base_dir = Path(__file__).resolve().parent.parent
    data_path = base_dir / "data" / "SuperMarket Analysis.csv"

    df = pd.read_csv(data_path)

    # Clean column names
    df.columns = df.columns.str.strip()

    # Convert Date safely
    df["Date"] = pd.to_datetime(
        df["Date"],
        format="mixed",
        errors="coerce"
    )

    # Convert Time safely
    df["Time"] = pd.to_datetime(
        df["Time"],
        format="mixed",
        errors="coerce"
    )

    # Create derived columns
    df["Month"] = df["Date"].dt.month_name()
    df["Day"] = df["Date"].dt.day_name()
    df["Hour"] = df["Time"].dt.hour

    return df


try:
    df = load_data()
except Exception as e:
    st.error("Could not load the dataset.")
    st.exception(e)
    st.stop()


# ======================================================
# HEADER
# ======================================================

st.title("🛒 Supermarket Sales Dashboard")

st.write(
    """
    Interactive business intelligence dashboard for analysing
    supermarket sales performance, customer behaviour,
    product demand and profitability.
    """
)

st.divider()


# ======================================================
# SIDEBAR FILTERS
# ======================================================

st.sidebar.title("🎛️ Dashboard Filters")

# ------------------------------------------------------
# Date Filter
# ------------------------------------------------------

min_date = df["Date"].min().date()
max_date = df["Date"].max().date()

date_range = st.sidebar.date_input(
    "Date Range",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date
)

if isinstance(date_range, (tuple, list)) and len(date_range) == 2:
    start_date, end_date = date_range
elif isinstance(date_range, (tuple, list)) and len(date_range) == 1:
    start_date = date_range[0]
    end_date = date_range[0]
else:
    start_date = date_range
    end_date = date_range


# ------------------------------------------------------
# Branch
# ------------------------------------------------------

branch_options = sorted(df["Branch"].dropna().unique())

branch = st.sidebar.multiselect(
    "Branch",
    options=branch_options,
    default=branch_options
)


# ------------------------------------------------------
# City
# ------------------------------------------------------

city_options = sorted(df["City"].dropna().unique())

city = st.sidebar.multiselect(
    "City",
    options=city_options,
    default=city_options
)


# ------------------------------------------------------
# Customer Type
# ------------------------------------------------------

customer_options = sorted(df["Customer type"].dropna().unique())

customer = st.sidebar.multiselect(
    "Customer Type",
    options=customer_options,
    default=customer_options
)


# ------------------------------------------------------
# Product Line
# ------------------------------------------------------

product_options = sorted(df["Product line"].dropna().unique())

product = st.sidebar.multiselect(
    "Product Line",
    options=product_options,
    default=product_options
)


# ------------------------------------------------------
# Payment
# ------------------------------------------------------

payment_options = sorted(df["Payment"].dropna().unique())

payment = st.sidebar.multiselect(
    "Payment Method",
    options=payment_options,
    default=payment_options
)


# ------------------------------------------------------
# Gender
# ------------------------------------------------------

gender_options = sorted(df["Gender"].dropna().unique())

gender = st.sidebar.multiselect(
    "Gender",
    options=gender_options,
    default=gender_options
)


# ======================================================
# APPLY FILTERS
# ======================================================

filtered_df = df[
    (df["Date"].dt.date >= start_date)
    &
    (df["Date"].dt.date <= end_date)
    &
    (df["Branch"].isin(branch))
    &
    (df["City"].isin(city))
    &
    (df["Customer type"].isin(customer))
    &
    (df["Product line"].isin(product))
    &
    (df["Payment"].isin(payment))
    &
    (df["Gender"].isin(gender))
].copy()


if filtered_df.empty:
    st.warning(
        "No records match the selected filters. "
        "Please adjust your sidebar selections."
    )
    st.stop()


# ======================================================
# KPI SECTION
# ======================================================

st.subheader("📌 Key Performance Indicators")

total_sales = filtered_df["Sales"].sum()
total_profit = filtered_df["gross income"].sum()
transactions = len(filtered_df)
average_rating = filtered_df["Rating"].mean()
items_sold = filtered_df["Quantity"].sum()

k1, k2, k3, k4, k5 = st.columns(5)

k1.metric(
    "💷 Total Sales",
    f"£{total_sales:,.2f}"
)

k2.metric(
    "💰 Gross Income",
    f"£{total_profit:,.2f}"
)

k3.metric(
    "🧾 Transactions",
    f"{transactions:,}"
)

k4.metric(
    "⭐ Average Rating",
    f"{average_rating:.2f}"
)

k5.metric(
    "📦 Items Sold",
    f"{items_sold:,.0f}"
)

st.divider()


# ======================================================
# QUICK INSIGHTS
# ======================================================

top_product = (
    filtered_df.groupby("Product line")["Sales"]
    .sum()
    .idxmax()
)

top_branch = (
    filtered_df.groupby("Branch")["Sales"]
    .sum()
    .idxmax()
)

top_city = (
    filtered_df.groupby("City")["Sales"]
    .sum()
    .idxmax()
)

top_payment = (
    filtered_df["Payment"]
    .value_counts()
    .idxmax()
)

insight1, insight2 = st.columns(2)

with insight1:
    st.info(
        f"""
        ### 🏆 Sales Leaders

        **Top Product Line:** {top_product}

        **Top Branch:** {top_branch}
        """
    )

with insight2:
    st.info(
        f"""
        ### 📍 Customer Insights

        **Top City:** {top_city}

        **Most Used Payment Method:** {top_payment}
        """
    )

st.divider()


# ======================================================
# SALES ANALYSIS
# ======================================================

st.header("📊 Sales Analysis")


# ------------------------------------------------------
# Chart 1 - Sales by Product Line
# ------------------------------------------------------

sales_product = (
    filtered_df.groupby("Product line")["Sales"]
    .sum()
    .reset_index()
    .sort_values("Sales", ascending=False)
)

fig1 = px.bar(
    sales_product,
    x="Product line",
    y="Sales",
    color="Sales",
    text_auto=".2s",
    title="Sales by Product Line",
    template="plotly_white"
)

fig1.update_layout(
    title_x=0.5,
    xaxis_title="Product Line",
    yaxis_title="Sales"
)

st.plotly_chart(fig1, use_container_width=True)

st.info(
    """
    **Insight:** Product lines with the highest sales contribute the largest
    share of total revenue and should receive priority in stock planning
    and promotional campaigns.
    """
)

st.divider()


# ------------------------------------------------------
# Chart 2 - Sales by Branch
# ------------------------------------------------------

sales_branch = (
    filtered_df.groupby("Branch")["Sales"]
    .sum()
    .reset_index()
    .sort_values("Sales", ascending=False)
)

fig2 = px.bar(
    sales_branch,
    x="Branch",
    y="Sales",
    color="Branch",
    text_auto=".2s",
    title="Sales by Branch",
    template="plotly_white"
)

fig2.update_layout(
    title_x=0.5,
    xaxis_title="Branch",
    yaxis_title="Sales"
)

st.plotly_chart(fig2, use_container_width=True)

st.info(
    """
    **Insight:** Comparing branch performance helps identify the strongest
    locations and branches that may need operational or marketing improvements.
    """
)

st.divider()


# ------------------------------------------------------
# Chart 3 - Sales by City
# ------------------------------------------------------

sales_city = (
    filtered_df.groupby("City")["Sales"]
    .sum()
    .reset_index()
    .sort_values("Sales", ascending=False)
)

fig3 = px.bar(
    sales_city,
    x="City",
    y="Sales",
    color="Sales",
    text_auto=".2s",
    title="Sales by City",
    template="plotly_white"
)

fig3.update_layout(
    title_x=0.5,
    xaxis_title="City",
    yaxis_title="Sales"
)

st.plotly_chart(fig3, use_container_width=True)

st.info(
    """
    **Insight:** City-level sales performance reveals regional demand
    and can support better marketing and resource allocation.
    """
)

st.divider()


# ======================================================
# SALES TREND & CUSTOMER ANALYSIS
# ======================================================

st.header("📈 Sales Trend & Customer Analysis")


# ------------------------------------------------------
# Chart 4 - Daily Sales Trend
# ------------------------------------------------------

daily_sales = (
    filtered_df.groupby("Date")["Sales"]
    .sum()
    .reset_index()
    .sort_values("Date")
)

fig4 = px.line(
    daily_sales,
    x="Date",
    y="Sales",
    markers=True,
    title="Daily Sales Trend",
    template="plotly_white"
)

fig4.update_layout(
    title_x=0.5,
    xaxis_title="Date",
    yaxis_title="Sales"
)

st.plotly_chart(fig4, use_container_width=True)

st.info(
    """
    **Insight:** Daily sales trends show busy and quiet periods,
    helping with staffing, promotions and demand forecasting.
    """
)

st.divider()


# ------------------------------------------------------
# Chart 5 - Payment Method Distribution
# ------------------------------------------------------

payment_sales = (
    filtered_df.groupby("Payment")["Sales"]
    .sum()
    .reset_index()
)

fig5 = px.pie(
    payment_sales,
    names="Payment",
    values="Sales",
    hole=0.45,
    title="Payment Method Distribution"
)

fig5.update_layout(
    title_x=0.5
)

st.plotly_chart(fig5, use_container_width=True)

st.info(
    """
    **Insight:** Payment method preferences help the business understand
    customer checkout behaviour and optimise payment options.
    """
)

st.divider()


# ------------------------------------------------------
# Chart 6 - Sales by Customer Type
# ------------------------------------------------------

customer_sales = (
    filtered_df.groupby("Customer type")["Sales"]
    .sum()
    .reset_index()
)

fig6 = px.bar(
    customer_sales,
    x="Customer type",
    y="Sales",
    color="Customer type",
    text_auto=".2s",
    title="Sales by Customer Type",
    template="plotly_white"
)

fig6.update_layout(
    title_x=0.5,
    xaxis_title="Customer Type",
    yaxis_title="Sales"
)

st.plotly_chart(fig6, use_container_width=True)

st.info(
    """
    **Insight:** Comparing member and normal customers shows which segment
    contributes more revenue and where loyalty programmes may add value.
    """
)

st.divider()


# ======================================================
# PRODUCT & CUSTOMER INSIGHTS
# ======================================================

st.header("📦 Product & Customer Insights")


# ------------------------------------------------------
# Chart 7 - Sales by Gender
# ------------------------------------------------------

gender_sales = (
    filtered_df.groupby("Gender")["Sales"]
    .sum()
    .reset_index()
)

fig7 = px.bar(
    gender_sales,
    x="Gender",
    y="Sales",
    color="Gender",
    text_auto=".2s",
    title="Sales by Gender",
    template="plotly_white"
)

fig7.update_layout(
    title_x=0.5,
    xaxis_title="Gender",
    yaxis_title="Sales"
)

st.plotly_chart(fig7, use_container_width=True)

st.info(
    """
    **Insight:** Gender-based sales analysis helps identify differences
    in purchasing patterns across customer groups.
    """
)

st.divider()


# ------------------------------------------------------
# Chart 8 - Quantity Sold by Product Line
# ------------------------------------------------------

quantity_product = (
    filtered_df.groupby("Product line")["Quantity"]
    .sum()
    .reset_index()
    .sort_values("Quantity", ascending=False)
)

fig8 = px.bar(
    quantity_product,
    x="Product line",
    y="Quantity",
    color="Quantity",
    text_auto=True,
    title="Quantity Sold by Product Line",
    template="plotly_white"
)

fig8.update_layout(
    title_x=0.5,
    xaxis_title="Product Line",
    yaxis_title="Quantity Sold"
)

st.plotly_chart(fig8, use_container_width=True)

st.info(
    """
    **Insight:** Product lines with the highest quantity sold indicate
    stronger customer demand and should be prioritised in stock planning.
    """
)

st.divider()


# ------------------------------------------------------
# Chart 9 - Average Rating by Product Line
# ------------------------------------------------------

rating_product = (
    filtered_df.groupby("Product line")["Rating"]
    .mean()
    .reset_index()
    .sort_values("Rating", ascending=False)
)

fig9 = px.bar(
    rating_product,
    x="Product line",
    y="Rating",
    color="Rating",
    text_auto=".2f",
    title="Average Customer Rating by Product Line",
    template="plotly_white"
)

fig9.update_layout(
    title_x=0.5,
    xaxis_title="Product Line",
    yaxis_title="Average Rating"
)

st.plotly_chart(fig9, use_container_width=True)

st.info(
    """
    **Insight:** Higher product ratings suggest stronger customer satisfaction,
    while lower-rated categories may need quality or service improvements.
    """
)

st.divider()


# ======================================================
# PROFIT & TIME ANALYSIS
# ======================================================

st.header("💰 Profit & Time Analysis")


# ------------------------------------------------------
# Chart 10 - Gross Income by Product Line
# ------------------------------------------------------

profit_product = (
    filtered_df.groupby("Product line")["gross income"]
    .sum()
    .reset_index()
    .sort_values("gross income", ascending=False)
)

fig10 = px.bar(
    profit_product,
    x="Product line",
    y="gross income",
    color="gross income",
    text_auto=".2s",
    title="Gross Income by Product Line",
    template="plotly_white"
)

fig10.update_layout(
    title_x=0.5,
    xaxis_title="Product Line",
    yaxis_title="Gross Income"
)

st.plotly_chart(fig10, use_container_width=True)

st.info(
    """
    **Insight:** Product lines generating the most gross income make the
    largest contribution to profitability and should remain a strategic focus.
    """
)

st.divider()


# ------------------------------------------------------
# Chart 11 - Sales by Hour
# ------------------------------------------------------

hour_sales = (
    filtered_df.dropna(subset=["Hour"])
    .groupby("Hour")["Sales"]
    .sum()
    .reset_index()
    .sort_values("Hour")
)

fig11 = px.line(
    hour_sales,
    x="Hour",
    y="Sales",
    markers=True,
    title="Sales by Hour of the Day",
    template="plotly_white"
)

fig11.update_layout(
    title_x=0.5,
    xaxis_title="Hour",
    yaxis_title="Sales"
)

st.plotly_chart(fig11, use_container_width=True)

st.info(
    """
    **Insight:** Peak shopping hours can help management plan staffing
    levels and schedule promotions at the most valuable times.
    """
)

st.divider()


# ------------------------------------------------------
# Chart 12 - Monthly Sales
# ------------------------------------------------------

month_order = [
    "January",
    "February",
    "March",
    "April",
    "May",
    "June",
    "July",
    "August",
    "September",
    "October",
    "November",
    "December"
]

monthly_sales = (
    filtered_df.groupby("Month")["Sales"]
    .sum()
    .reset_index()
)

monthly_sales["Month"] = pd.Categorical(
    monthly_sales["Month"],
    categories=month_order,
    ordered=True
)

monthly_sales = monthly_sales.sort_values("Month")

fig12 = px.line(
    monthly_sales,
    x="Month",
    y="Sales",
    markers=True,
    title="Monthly Sales Trend",
    template="plotly_white"
)

fig12.update_layout(
    title_x=0.5,
    xaxis_title="Month",
    yaxis_title="Sales"
)

st.plotly_chart(fig12, use_container_width=True)

st.info(
    """
    **Insight:** Monthly sales trends reveal seasonal patterns and help
    improve forecasting, inventory planning and promotion scheduling.
    """
)

st.divider()


# ======================================================
# DATA EXPLORER
# ======================================================

st.header("📋 Data Explorer")

with st.expander("View Filtered Dataset"):

    st.dataframe(
        filtered_df,
        use_container_width=True
    )


with st.expander("View Summary Statistics"):

    numeric_columns = [
        "Unit price",
        "Quantity",
        "Sales",
        "gross income",
        "Rating"
    ]

    available_numeric_columns = [
        col for col in numeric_columns
        if col in filtered_df.columns
    ]

    st.dataframe(
        filtered_df[available_numeric_columns].describe(),
        use_container_width=True
    )


# ======================================================
# DOWNLOAD DATA
# ======================================================

csv_data = filtered_df.to_csv(index=False).encode("utf-8")

st.download_button(
    label="📥 Download Filtered Data",
    data=csv_data,
    file_name="filtered_supermarket_sales.csv",
    mime="text/csv"
)

st.divider()


# ======================================================
# BUSINESS RECOMMENDATIONS
# ======================================================

st.header("🎯 Business Recommendations")

best_product = (
    filtered_df.groupby("Product line")["Sales"]
    .sum()
    .idxmax()
)

best_branch = (
    filtered_df.groupby("Branch")["Sales"]
    .sum()
    .idxmax()
)

best_city = (
    filtered_df.groupby("City")["Sales"]
    .sum()
    .idxmax()
)

best_payment = (
    filtered_df["Payment"]
    .value_counts()
    .idxmax()
)

best_profit_product = (
    filtered_df.groupby("Product line")["gross income"]
    .sum()
    .idxmax()
)

st.success(
    f"""
    **Key Recommendations**

    - Prioritise inventory and promotions for **{best_product}** because it currently generates the highest sales.
    - Review practices at **Branch {best_branch}** and consider applying successful strategies to other branches.
    - Focus marketing activity in **{best_city}**, the strongest-performing city under the current filters.
    - Ensure strong support for **{best_payment}**, the most commonly used payment method.
    - Maintain availability and visibility of **{best_profit_product}**, which currently generates the highest gross income.
    """
)

st.divider()


# ======================================================
# FILTER SUMMARY
# ======================================================

st.subheader("🔎 Current Filter Summary")

f1, f2, f3 = st.columns(3)

f1.metric(
    "Selected Branches",
    len(branch)
)

f2.metric(
    "Selected Cities",
    len(city)
)

f3.metric(
    "Selected Product Lines",
    len(product)
)

st.caption(
    f"Dashboard currently contains {len(filtered_df):,} transactions after filtering."
)

st.divider()


# ======================================================
# FOOTER
# ======================================================

st.markdown(
    """
    ### 🛒 Supermarket Sales Dashboard

    Built with **Python, Pandas, Plotly and Streamlit**.

    This dashboard provides interactive analysis of supermarket
    sales performance, customer behaviour, product demand and profitability.
    """
)