import pandas as pd
import streamlit as st
import numpy as np
import plotly.express as px
import os
import warnings
warnings.filterwarnings('ignore')



st.set_page_config(page_title="Viz Superstore", page_icon="📈", layout="wide")

st.title("📈Superstore Visualization")
st.markdown('<style>div.block-container{padding-top:3rem;}</style>',unsafe_allow_html=True)

fl = st.file_uploader(":file_folder: Upload a File", type=(['csv', 'txt', 'xlxs', 'xlx']))
if fl is not None:
    filename = fl.name
    st.write(filename)
    df = pd.read_csv(filename, encoding = "latin1")
else:
    url = ("C:/Users/Sandra/Desktop/DA Projects/Kaggle/Test.csv")
    df = pd.read_csv(url, encoding = "latin1")



# convert date column to datetime
df['Order Date'] = pd.to_datetime(df['Order Date'])
df['Ship Date'] = pd.to_datetime(df['Ship Date'])

# create a column totalsales
df['Total Sales'] = df['Sales'] * df['Quantity']

# get the year, month and quater
date = pd.DatetimeIndex(df['Order Date'])
df['Order Year'] = date.year
df['Order Month'] = date.month
df['Order Quarter'] = date.quarter


#change dypye of year, month and quater
df["Order Year"] = df["Order Year"].astype("str")
df["Order Month"] = df["Order Month"].astype("str")
df["Order Quarter"] = df['Order Quarter'].astype("str")



result = []
for value in df["Order Month"]:
    if value == '1':
      result.append("January") # January
    elif value == '2':
      result.append("Febuary") # Febuary
    elif value == '3':
      result.append("March") # March
    elif value == '4':
      result.append("April") # April
    elif value == '5':
      result.append("May") # May
    elif value == '6':
      result.append("June") # Jun
    elif value == '7':
      result.append("July") # Jul
    elif value == '8':
      result.append("August") # August
    elif value == '9':
      result.append("September") # September
    elif value == '10':
      result.append("October") # October
    elif value == '11':
      result.append("November") # November
    elif value == '12':
      result.append("December") # December

df['Month_Name'] = result


# create side filter pane for region

st.sidebar.header("Choose Filter: ")
region = st.sidebar.multiselect("Pick Region", df['Region'].unique())
if not region:
    df2 = df.copy()
else:
    df2 = df[df['Region'].isin(region)]


# create side filter pane for state
state = st.sidebar.multiselect("Pick State", df2['State'].unique())
if not state:
    df3 = df2.copy()
else:
    df3 = df2[df2['State'].isin(state)]



# create side filter pane for city
city = st.sidebar.multiselect('Pick City', df3['City'].unique())


# Apply filter based on State, City and Region
if not region and not state and not city:
    filtered_df = df
elif not state and not region:
    filtered_df = df[df['City'].isin(city)]
elif not state and not city:
    filtered_df = df[df['Region'].isin(region)]
elif not region and not city:
    filtered_df = df[df['State'].isin(state)]
elif state and city:
    filtered_df = df3[df3['State'].isin(state) & df3['City'].isin(city)]
elif state and region:
    filtered_df = df3[df3['State'].isin(state) & df3['Region'].isin(region)]
elif region and city:
    filtered_df = df3[df3['Region'].isin(region) & df3['City'].isin(city)]
elif city:
    filtered_df = df3[df3['City'].isin(city)]
else:
    filtered_df = df3[df3['Region'].isin(region) & df3['Region'].isin(region) & df3['Region'].isin(region)]

D1, D2, D3 = st.columns(3)

# FOR YEAR
with D1:
   opt_year = filtered_df['Order Year'].unique()
   year = D1.multiselect('Select Year ', sorted(opt_year), key='year')

# FOR MONTH NAME
with D2:
   opt_mth = filtered_df['Month_Name'].unique()
   month = D2.multiselect('Select Month', opt_mth, key='months')

# FOR QUARTER
with D3:
   opt_quar = filtered_df['Order Quarter'].unique()
   quarter = D3.multiselect("Select Quarter", sorted(opt_quar), key="quarter")

amount = filtered_df['Total Sales'].sum()
curr = "${:,.2f}".format(amount)



year_op = filtered_df[filtered_df['Order Year'].isin(year)]
month_op = filtered_df[filtered_df['Month_Name'].isin(month)]
quater_op = filtered_df[filtered_df['Order Quarter'].isin(quarter)]



M1, M2, M3 = st.columns(3)
with M1:
  # from streamlit_extras.metric_cards import style_metric_cards
  if year:
    cus_id = year_op['Customer ID'].nunique()
  elif month:
    cus_id = month_op['Customer ID'].nunique()
  elif quarter:
    cus_id = quater_op['Customer ID'].nunique()
  else:
     cus_id = filtered_df['Customer ID'].nunique()
  M1.metric('Total Customers', cus_id)
  # style_metric_cards(background_color="#596073",border_left_color="#F71938",border_color="#1f66bd",box_shadow="#F71938")
with M2:
  if year:
    ord_id = year_op['Order ID'].count()
  elif month:
     ord_id = month_op['Order ID'].count()
  elif quarter:
     ord_id = quater_op['Order ID'].count()
  else:
     cus_id = filtered_df['Order ID'].count()
  M2.metric('Total Orders', cus_id)

with M3:
  if year:
    prod_id = year_op['Product ID'].count()
  elif month:
    prod_id = month_op['Product ID'].count()
  elif quarter:
    prod_id = quater_op['Product ID'].count()
  else:
    prod_id = filtered_df['Product ID'].count()
  M3.metric('Total Products', prod_id)


# TOTAL CUSTOMERS AND DISCOUNT AND PROFIT
C1, C2, C3 = st.columns(3)

with C1:
  if year:
    amount = year_op['Total Sales'].sum()
  elif month:
    amount = month_op['Total Sales'].sum()
  elif quarter:
    amount = quater_op['Total Sales'].sum()
  elif year and month:
    amount = year_op['Total Sales'].sum() & month_op['Total Sales'].sum()
  elif year and quarter:
    amount = year_op['Total Sales'].sum() & quater_op['Total Sales'].sum()
  else:
    amount = filtered_df['Total Sales'].sum()
  C1.metric("Total Sales", "${:,.2f}".format(amount))

with C2:
  if year:
    discount = year_op['Discount'].sum()
  elif month:
    discount = month_op['Discount'].sum()
  elif quarter:
    discount = quater_op['Discount'].sum()
  elif year and month:
    discount = year_op['Discount'] & month_op['Discount']
  elif year and month and quarter:
    discount = year_op['Discount'] & quater_op['Discount']
  else:
    discount = filtered_df['Discount'].sum()

  C2.metric("Total Discount", "${:,.2f}".format(discount))


with C3:
  if year:
    profit = year_op['Profit'].sum()
  elif month:
    profit = month_op['Profit'].sum()
  elif quarter:
    profit = quater_op['Profit'].sum()
  elif year and month:
    profit = year_op['Profit'].sum() & month_op['Profit'].sum()
  elif year and quarter:
    profit = year_op['Profit'].sum() & quater_op['Profit'].sum()
  else:
    profit = filtered_df['Profit'].sum()
  C3.metric("Total Profit", "${:,.2f}".format(profit))
   

# CHARTS
Char1, Char2 = st.columns(2)
with Char1:
   st.subheader("Region Sales")
   if year:
      fig = px.pie(year_op, values = 'Total Sales', names = "Region")
      fig.update_traces(text=year_op['Region'], textposition = 'outside')
   elif month:
      fig = px.pie(month_op, values = 'Total Sales', names = "Region")
      fig.update_traces(text=month_op['Region'], textposition = 'outside')
   elif quarter:
      fig = fig = px.pie(quater_op, values = 'Total Sales', names = "Region")
      fig.update_traces(text=quater_op['Region'], textposition = 'outside')
   else:
      fig = px.pie(filtered_df, values = 'Total Sales', names = "Region")
      fig.update_traces(text=filtered_df['Region'], textposition = 'outside')
   st.plotly_chart(fig, use_container_width= True)


with Char2:
   st.subheader("Segment Sales")
   if year:
      fig = px.bar(year_op, x=year_op['Segment'].value_counts().index, y=year_op['Segment'].value_counts().values,
                   labels={'x': 'Segment',
                           'y': "Counts"})
      fig.update_traces(text=year_op['Segment'].value_counts().values)
     
   elif month:
      fig = px.bar(month_op, x = month_op['Segment'].value_counts().index, y=month_op['Segment'].value_counts().values,
                   labels={
                      'x': 'Segment',
                      'y' : 'Counts'
                   })
      fig.update_traces(text=year_op['Segment'].value_counts().values)
     
   elif quarter:
      fig = px.bar(quater_op, x = quater_op['Segment'].value_counts().index, y=quater_op['Segment'].value_counts().values,
                   labels={
                      'x': 'Segment',
                      'y': 'Counts'
                   })
      fig.update_traces(text=year_op['Segment'].value_counts().values)
   else:
      fig = px.bar(filtered_df, x = filtered_df['Segment'].value_counts().index, y=filtered_df['Segment'].value_counts().values,
                   labels={
                      'x': 'Segment',
                      'y': 'Counts'
                   })
      fig.update_traces(text=filtered_df['Segment'].value_counts().values)
    
   st.plotly_chart(fig, use_container_width= True)



# SECOND CHARTS

   # # group by year
lin_yr = year_op.groupby(['Region', 'Category'])[['Total Sales', 'Profit']].sum().reset_index()
year_met = year_op.groupby(['Region', 'Category', 'State'])[['Total Sales', 'Profit']].sum().reset_index()

# group by month
lin_mnth = month_op.groupby(['Region', 'Category'])[['Total Sales', 'Profit']].sum().reset_index()
month_met = month_op.groupby(['Region', 'Category', 'State'])[['Total Sales', 'Profit']].sum().reset_index()

# group by quater
lin_qua = quater_op.groupby(['Region', 'Category'])['Total Sales'].sum().reset_index()
quater_met = quater_op.groupby(['Region', 'Category', 'State'])[['Total Sales', 'Profit']].sum().reset_index()

# group by df
lin_filt = filtered_df.groupby(['Region', 'Category'])['Total Sales'].sum().reset_index()
filtered_met = filtered_df.groupby(['Region', 'Category', 'State'])[['Total Sales', 'Profit']].sum().reset_index()


V1, V2 = st.columns(2)

with V1:
   if year:
      fig = px.line(lin_yr, x= 'Region', y='Total Sales', markers=True, color ='Category',
             title = "Total Sales by Region and Category")
   elif month:
      fig = px.line(lin_mnth, x= 'Region', y='Total Sales', markers=True, color = 'Category',
             title = "Total Sales by Region and Category")
   elif quarter:
       fig = px.line(lin_qua, x= 'Region', y='Total Sales', markers=True, color = 'Category',
             title = "Total Sales by Region and Category")
   else:
       fig = px.line(lin_filt, x= 'Region', y='Total Sales', markers=True, color = 'Category',
             title = "Total Sales by Region and Category")
   st.plotly_chart(fig, use_container_width= True)


with V2:
   if year:
      fig = px.scatter(year_met, x="Total Sales", y="Profit", color = 'State',
                title = "Yearly Total Sales and Profit by State")
   elif month:
      fig = px.scatter(month_met, x="Total Sales", y="Profit", color = 'State',
                title = "Yearly Total Sales and Profit by State")
   elif quarter:
       fig = px.scatter(quater_met, x="Total Sales", y="Profit", color = 'State',
                title = "Yearly Total Sales and Profit by State")
   else:
       fig = px.scatter(filtered_met, x="Total Sales", y="Profit", color = 'State',
                title = "Yearly Total Sales and Profit by State")
   st.plotly_chart(fig, use_container_width= True)