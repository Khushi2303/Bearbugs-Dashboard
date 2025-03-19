import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Load the data
file_path = "Bearbugs_assig.xlsx"
xls = pd.ExcelFile(file_path)
data_df = xls.parse('Data')
data_df.columns = data_df.columns.str.strip()

data_df['Sales'] = pd.to_numeric(data_df['Sales'], errors='coerce')
data_df['Quantity'] = pd.to_numeric(data_df['Quantity'], errors='coerce')
data_df['Discount'] = pd.to_numeric(data_df['Discount'], errors='coerce')
data_df['Profit'] = pd.to_numeric(data_df['Profit'], errors='coerce')

data_df['Order Date'] = pd.to_datetime(data_df['Order Date'], errors='coerce')
data_df['Year'] = data_df['Order Date'].dt.year

# Compute Average Order Value (AOV) per year
aov_per_year = data_df.groupby('Year')['Sales'].sum() / data_df.groupby('Year')['Order ID'].nunique()

# Top 3 states with highest discounts
top_discount_states = data_df.groupby('State')['Discount'].mean().nlargest(3)

# Streamlit UI
st.title("📊 Bearbugs Assignment Dashboard")

st.sidebar.title("🔍 Filters")
year_filter = st.sidebar.selectbox("Select Year", sorted(data_df['Year'].unique(), reverse=True))
state_filter = st.sidebar.multiselect("Select State(s)", data_df['State'].unique(), default=data_df['State'].unique()[:5])
category_filter = st.sidebar.multiselect("Select Category(s)", data_df['Category'].unique(), default=data_df['Category'].unique())

filtered_data = data_df[(data_df['Year'] == year_filter) & (data_df['State'].isin(state_filter)) & (data_df['Category'].isin(category_filter))]

st.header(f"📅 Data for Year {year_filter}")
st.write(filtered_data.head())

st.header("1️⃣ Average Order Value (AOV) Per Year")
st.bar_chart(aov_per_year)

st.header("2️⃣ Top 3 States Offering Highest Discounts")
st.bar_chart(top_discount_states)

st.header("📌 Sales & Profit Analysis")
fig, ax = plt.subplots(figsize=(8, 5))
sns.lineplot(x='Order Date', y='Sales', data=filtered_data, ax=ax)
st.pyplot(fig)

st.header("📉 Profit Trend Over Time")
fig2, ax2 = plt.subplots(figsize=(8, 5))
sns.lineplot(x='Order Date', y='Profit', data=filtered_data, ax=ax2, color='green')
st.pyplot(fig2)

st.header("💰 Sales Distribution by Category")
fig3, ax3 = plt.subplots(figsize=(8, 5))
sns.boxplot(x='Category', y='Sales', data=filtered_data, ax=ax3)
st.pyplot(fig3)

st.write("### 🚀 More insights coming soon!")

# Deployment Guide
st.sidebar.header("🚀 Deployment Steps")
st.sidebar.markdown("1️⃣ Install Streamlit: `pip install streamlit pandas seaborn matplotlib`\n" "2️⃣ Run: `streamlit run dashboard.py`\n" "3️⃣ Deploy on Streamlit Cloud or Render!")
