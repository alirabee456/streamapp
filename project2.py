import numpy as np
import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go

data = pd.read_csv('pandas28.csv')
branch_list = ["All"] + data['Branch'].unique().tolist()

selected_branch = st.sidebar.selectbox("Select Branch", options=branch_list)
image=st.sidebar.image('profit.gif')
data_new = data.copy()
if selected_branch != "All":
    data_new = data_new[data_new["Branch"] == selected_branch]
KPIS, Quantity, Total,targets = st.tabs(['KPIS', 'Quantity', 'Total','targets'])
with KPIS:
    total_sales = data_new['Total'].sum()
    total_quantity = data_new['Quantity'].sum()
    total_tax = data_new['Tax 5%'].sum()
    orders = data_new['Invoice ID'].count()
    avg_rating = data_new['Rating'].mean()

    col1, col2, col3, col4, col5 = st.columns([2, 2, 2, 2, 2])
    col1.metric(label='Total Sales', value=f"{round(total_sales / 1000, 2)}K")
    col2.metric(label='Total Quantity', value=total_quantity)
    col3.metric(label='Total Tax', value=f"{round(total_tax / 1000, 2)}K")
    col4.metric(label='Orders', value=orders)
    col5.metric(label='Rating', value=round(avg_rating, 2))

with Quantity:
    s = data_new.groupby('Product line')['Quantity'].sum().reset_index().sort_values(by='Quantity', ascending=True)
    s1 = data_new.groupby('Gender')['Quantity'].sum().reset_index()
    s2 = data_new.groupby('Customer type')['Quantity'].sum().reset_index()

    bar1 = px.bar(s, y='Product line', x='Quantity', title='Sum of Quantity by Product Line', text_auto='.2s')
    pie1 = px.pie(s1, values='Quantity', names='Gender', title='Sum of Quantity by Gender',hole=.6)
    pie2 = px.pie(s2, values='Quantity', names='Customer type', title='Sum of Quantity by Customer Type',hole=.6)

    st.plotly_chart(bar1)
    st.plotly_chart(pie1)
    st.plotly_chart(pie2)
with Total:
    s = data_new.groupby('Product line')['Total'].sum().reset_index().sort_values(by='Total', ascending=True)
    s1 = data_new.groupby('Gender')['Total'].sum().reset_index()
    s2 = data_new.groupby('Customer type')['Total'].sum().reset_index()

    bar1 = px.bar(s, y='Product line', x='Total', title='Sum of Total by Product Line', text_auto='.2s')
    pie1 = px.pie(s1, values='Total', names='Gender', title='Sum of Total by Gender',hole=.6)
    pie2 = px.pie(s2, values='Total', names='Customer type', title='Sum of Total by Customer Type',hole=.6)

    st.plotly_chart(bar1)
    st.plotly_chart(pie1)
    st.plotly_chart(pie2)
with targets:
    target_sales=110000
    fig = go.Figure(
        go.Indicator(mode='number+gauge+delta', value=data_new['Total'].sum(), domain={'x': [0, 1], 'y': [0, 1]},
                     title={'text': 'Sales'}, delta={'reference': target_sales}, gauge={'axis': {'range': [0, target_sales]}}))
    target_Quantity=1000
    fig1 = go.Figure(
        go.Indicator(mode='number+gauge+delta', value=data_new['Quantity'].sum(), domain={'x': [0, 1], 'y': [0, 1]},
                     title={'text': 'Quantity'}, delta={'reference': target_Quantity}, gauge={'axis': {'range': [0, target_Quantity]}}))
    target_Rating=8

    fig2 = go.Figure(
        go.Indicator(mode='number+gauge+delta', value=data_new['Rating'].mean(), domain={'x': [0, 1], 'y': [0, 1]},
                     title={'text': 'Rating'}, delta={'reference': target_Rating}, gauge={'axis': {'range': [0, target_Rating]}}))
    st.plotly_chart(fig)
    st.plotly_chart(fig1)
    st.plotly_chart(fig2)
