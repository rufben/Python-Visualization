from pathlib import Path  # Python Standard Library
import pandas as pd  # pip install pandas openpyxl
import plotly.express as px
import streamlit as st
import matplotlib.pyplot as plt
import plotly.figure_factory as ff

st.set_page_config(page_title = "Bike Purchase dashboard",
                   layout ="wide"
                  )

@st.cache_data()
def first_task():
    df = pd.read_csv("C:/Users/14709/Desktop/data analytics/bike_buyers_clean.csv")
    df.head(5)
    return df 

df = first_task()
#st.dataframe(df)

# sidebars#
st.sidebar.header("Helpful Filters:" )
gender = st.sidebar.multiselect('Gender',
                                options= df['Gender'].unique(),
                                default=df['Gender'].unique()
                                )



education = st.sidebar.multiselect('Education',
                                options= df['Education'].unique(),
                                default=df['Education'].unique()
                                )


occupation = st.sidebar.multiselect('Occupation',
                                options= df['Occupation'].unique(),
                                default=df['Occupation'].unique()
                                )


df_filter= df.query(
    "Gender ==@gender & Occupation == @occupation & Education == @education "
    )

#st.dataframe(df_filter)


#--Mainpage--#

st.title('Bike Buyer Data')
st.markdown('##')

#--KPI's--

total_income = int(df_filter['Income'].sum())
#total_cars = int(df_filter['Cars'].sum())
no_of_id = df_filter['ID'].nunique()
no_of_bikes = df_filter.loc[df['Purchased Bike'] == 'Yes', 'ID'].nunique()

left_column,middle_column,right_column = st.columns(3)
with left_column:
    st.subheader("Total Income")
    st.subheader(f"US $ {total_income:,}")
with middle_column:
    st.subheader("Total Users")
    st.subheader(f" {no_of_id:}")
with right_column:
    st.subheader("Total Bikes Bought")
    st.subheader(no_of_bikes)
    
st.markdown("---")



income_by_region = (
    df_filter.groupby(by=['Region']).sum()[['Income']].sort_values(by='Income')
    )
bike_purchased = (
    df_filter.groupby(by=['Purchased Bike']).nunique()[['ID']]
    )

fig_income = px.bar(
    income_by_region,
    x = 'Income',
    y = income_by_region.index,
    orientation = 'h',
    title = "<b>Income by Region</b>",
    template = 'plotly_white',
    )

#st.plotly_chart(fig_income)


tt_pie =px.pie(
    bike_purchased ,
    names=bike_purchased .index,
    values='ID',
    title ="<b>Bikes purchased</b>"
    )

line_check=px.scatter(
    df_filter ,
    x='Income',
    y='Age',
    color='Purchased Bike',
    title='Distribution of Income by Age'
    )


#st.plotly_chart(line_check)

df_filter['no_of_id'] = no_of_id
#df_filter['no_of_bikes']= no_of_bikes

fig_line =px.bar(
    df_filter,
    x= 'Commute Distance',
    y= 'no_of_id',
    color='Purchased Bike',
    title='Distribution of Distance traveled'
    
    )

#st.plotly_chart(fig_line)
#st.plotly_chart(tt_pie)

left_column,right_column = st.columns(2)
left_column.plotly_chart(fig_income, use_container_width=True)
right_column.plotly_chart(tt_pie, use_container_width=True)

st.markdown("##")
#st.plotly_chart(fig_line)
left_column,right_column = st.columns(2)
left_column.plotly_chart(fig_line, use_container_width=True)
right_column.plotly_chart(line_check, use_container_width=True)


hide_st_style = """
                <style>
                #MainMenu {visibility:hidden;}
                footer {visibility:hidden;}
                header {visibility:hidden;}
                </style>
                """
st.markdown(hide_st_style, unsafe_allow_html=True)


















