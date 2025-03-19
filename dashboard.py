import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Load the dataset
file_path = "Bearbugs_assig.xlsx"
xls = pd.ExcelFile(file_path)
data_df = xls.parse('Data')
data_df.columns = data_df.columns.str.strip()

# Convert data types
data_df['Sales'] = pd.to_numeric(data_df['Sales'], errors='coerce')
data_df['Quantity'] = pd.to_numeric(data_df['Quantity'], errors='coerce')
data_df['Discount'] = pd.to_numeric(data_df['Discount'], errors='coerce')
data_df['Profit'] = pd.to_numeric(data_df['Profit'], errors='coerce')

data_df['Order Date'] = pd.to_datetime(data_df['Order Date'], errors='coerce')
data_df['Year'] = data_df['Order Date'].dt.year

# 📊 Streamlit UI
st.set_page_config(page_title="Bearbugs Dashboard", layout="wide")
st.markdown("<h1 style='text-align: center; color: cyan;'>📊 Bearbugs Dashboard</h1>", unsafe_allow_html=True)

# Sidebar Filters
st.sidebar.title("🔍 Filters")
year_filter = st.sidebar.selectbox("Select Year", sorted(data_df['Year'].dropna().unique(), reverse=True))
state_filter = st.sidebar.multiselect("Select State(s)", data_df['State'].dropna().unique(), default=data_df['State'].dropna().unique()[:5])
category_filter = st.sidebar.multiselect("Select Category(s)", data_df['Category'].dropna().unique(), default=data_df['Category'].dropna().unique())

filtered_data = data_df[(data_df['Year'] == year_filter) & 
                        (data_df['State'].isin(state_filter)) & 
                        (data_df['Category'].isin(category_filter))]


# 🏆 **Filtered Data**
filtered_data = data_df[(data_df['Year'] == year_filter) & 
                        (data_df['State'].isin(state_filter)) & 
                        (data_df['Category'].isin(category_filter))]

# 🏆 **KPIs (Key Business Metrics)**
st.markdown("<h1>📊 Bearbugs Assignment Dashboard</h1>", unsafe_allow_html=True)
st.markdown("## 🏆 Key Business Metrics")

col1, col2, col3 = st.columns(3)
col1.metric("💰 Total Sales", f"${filtered_data['Sales'].sum():,.2f}")
col2.metric("📦 Total Orders", f"{filtered_data['Order ID'].nunique()}")
col3.metric("💹 Total Profit", f"${filtered_data['Profit'].sum():,.2f}")

# 📊 **Visualizations**
st.markdown("## 📊 Sales & Profit Trends")

# 🏛 Bar Charts (Sales & Profit per Category)
col4, col5 = st.columns(2)
with col4:
    st.markdown("### 🔹 Sales by Category")
    fig, ax = plt.subplots()
    sns.barplot(x='Category', y='Sales', data=filtered_data, palette='coolwarm', ax=ax)
    ax.set_xticklabels(ax.get_xticklabels(), rotation=45)
    st.pyplot(fig)

with col5:
    st.markdown("### 🔹 Profit by Category")
    fig2, ax2 = plt.subplots()
    sns.barplot(x='Category', y='Profit', data=filtered_data, palette='Blues', ax=ax2)
    ax2.set_xticklabels(ax2.get_xticklabels(), rotation=45)
    st.pyplot(fig2)

# 📈 **Line Chart for Sales Trend Over Time**
st.markdown("### 📈 Sales Trend Over Time")
fig3, ax3 = plt.subplots(figsize=(12, 5))
sns.lineplot(x='Order Date', y='Sales', data=filtered_data, color='cyan', marker="o", ax=ax3)
st.pyplot(fig3)

# 🎯 **Heatmap for Discount & Sales Relation**
st.markdown("### 🔥 Discount vs Sales Heatmap")
fig4, ax4 = plt.subplots(figsize=(10, 5))
sns.heatmap(filtered_data.pivot_table(values='Sales', index='Category', columns='Discount', aggfunc='sum'), cmap='coolwarm', annot=True)
st.pyplot(fig4)


# 🏆 **Q1: AOV for 2017 where Ship mode is Second Class**
aov_2017 = data_df[(data_df['Year'] == 2017) & (data_df['Ship Mode'] == 'Second Class')]
aov_value = aov_2017['Sales'].sum() / aov_2017['Order ID'].nunique()

# 📍 **Q2: Top 3 states with highest discounts in 2015**
top_discount_states = data_df[data_df['Year'] == 2015].groupby('State')['Discount'].mean().nlargest(3)

# 🛒 **Q3: Highest-Selling Category for California in "Home Office"**
california_sales = data_df[(data_df['State'] == 'California') & (data_df['Segment'] == 'Home Office')]
top_category = california_sales.groupby('Category')['Sales'].sum().idxmax()

# 📈 **Q4: Sales % increase/decrease in Kentucky (2016-2017)**
kentucky_sales = data_df[data_df['State'] == 'Kentucky'].groupby('Year')['Sales'].sum()
kentucky_change = ((kentucky_sales.get(2017, 0) - kentucky_sales.get(2016, 0)) / kentucky_sales.get(2016, 1)) * 100

# 🔄 **Q5: Customer Retention for 2015**
repeat_customers_2015 = data_df[data_df['Year'] == 2015].groupby('Customer ID')['Order ID'].nunique()
retention_rate = (repeat_customers_2015[repeat_customers_2015 > 1].count() / repeat_customers_2015.count()) * 100

# 📌 **Q6: Repeat % of customers buying furniture in South Region (2016)**
south_furniture = data_df[(data_df['Year'] == 2016) & (data_df['Region'] == 'South') & (data_df['Category'] == 'Furniture')]
repeat_customers_south = south_furniture.groupby('Customer ID')['Order ID'].nunique()
repeat_percent = (repeat_customers_south[repeat_customers_south > 1].count() / repeat_customers_south.count()) * 100

# 🚫 **Q7: Identify the Least Profitable Product**
least_profitable_product = data_df.groupby('Product Name')['Profit'].sum().idxmin()

# 📊 **Dashboard Layout**
st.subheader("📅 Data for Year 2017")
st.dataframe(aov_2017[['Order ID', 'Order Date', 'Sales', 'Ship Mode', 'Customer ID']].head())

# 🏆 **Metrics Row**
col1, col2, col3 = st.columns(3)
col1.metric("📊 AOV for 2017", f"${aov_value:.2f}")
col2.metric("📍 Sales Change in Kentucky (2016-2017)", f"{kentucky_change:.2f}%")
col3.metric("🔁 Customer Retention (2015)", f"{retention_rate:.2f}%")

col4, col5 = st.columns(2)
col4.metric("🔄 Repeat Customers Buying Furniture (2016, South)", f"{repeat_percent:.2f}%")
col5.metric("💰 Least Profitable Product", least_profitable_product)


## Q6: Repeat % of customers buying furniture in South Region (2016)
south_furniture = data_df[(data_df['Year'] == 2016) & (data_df['Region'] == 'South') & (data_df['Category'] == 'Furniture')]
repeat_customers_south = south_furniture.groupby('Customer ID')['Order ID'].nunique()
repeat_percent = (repeat_customers_south[repeat_customers_south > 1].count() / repeat_customers_south.count()) * 100

## Q7: Least Profitable Product
least_profitable_product = data_df.groupby('Product Name')['Profit'].sum().idxmin()

# 📌 **Charts Section**
st.markdown("### 📊 Key Insights")
col6, col7 = st.columns(2)

with col6:
    st.markdown("### 1️⃣ Average Order Value (AOV) Per Year")
    st.bar_chart(data_df.groupby('Year')['Sales'].mean())

with col7:
    st.markdown("### 2️⃣ Top 3 States Offering Highest Discounts")
    st.bar_chart(top_discount_states)

# 📈 **Sales & Profit Analysis**
st.markdown("### 📌 Sales & Profit Analysis")

col8, col9 = st.columns(2)

with col8:
    st.markdown("#### 📈 Sales Trend Over Time")
    fig, ax = plt.subplots(figsize=(10, 5))
    sns.lineplot(x='Order Date', y='Sales', data=filtered_data, ax=ax)
    st.pyplot(fig)

with col9:
    st.markdown("#### 💰 Profit Trend Over Time")
    fig2, ax2 = plt.subplots(figsize=(10, 5))
    sns.lineplot(x='Order Date', y='Profit', data=filtered_data, ax=ax2, color='green')
    st.pyplot(fig2)

# 📌 **Sales Distribution by Category**
st.markdown("### 📊 Sales Distribution by Category")
fig3, ax3 = plt.subplots(figsize=(5, 2))
sns.boxplot(x='Category', y='Sales', data=filtered_data, ax=ax3)
st.pyplot(fig3)

