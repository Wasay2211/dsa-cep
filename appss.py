import pandas as pd
import streamlit as st
import plotly.express as px


st.set_page_config(page_title='Wild dogs in the frame ')
st.header('Dogs Caught')
st.subheader('We Have caught dogs from different areas of Karachi. Becasue these dogs are being wild')

### --- LOAD DATAFRAME
excel_file = 'Total Caught.xlsx'
sheet_name = 'DATADOG'

df = pd.read_excel(excel_file,
                   sheet_name=sheet_name,
                   usecols='B:D',
                   header=3)

df_dogs = pd.read_excel(excel_file,
                                sheet_name= sheet_name,
                                usecols='F:G',
                                header=3)
df_dogs.dropna(inplace=True)

# --- STREAMLIT SELECTION
Areas = df['Areas'].unique().tolist()
types = df['types'].unique().tolist()

types_selection = st.slider('tpyes :',
                        min_value= min(types),
                        max_value= max(types),
                        value=(min(types),max(types)))

Areas_selection = st.multiselect('Areas:',
                                    Areas,
                                    default=Areas)

# --- FILTER DATAFRAME BASED ON SELECTION
mask = (df['types'].between(*types_selection)) & (df['Areas'].isin(Areas_selection))
number_of_result = df[mask].shape[0]
st.markdown(f'*Available Results: {number_of_result}*')

# --- GROUP DATAFRAME AFTER SELECTION
df_grouped = df[mask].groupby(by=['Rating']).count()[['types']]
df_grouped = df_grouped.rename(columns={'types': 'Dogs'})
df_grouped = df_grouped.reset_index()

# --- PLOT BAR CHART
bar_chart = px.bar(df_grouped,
                   x='Rating',
                   y='Dogs',
                   text='Dogs',
                   color_discrete_sequence = ['#F63366']*len(df_grouped),
                   template= 'plotly_black')
st.plotly_chart(bar_chart)

# --- PLOT PIE CHART
pie_chart = px.pie(df_dogs,
                title='Total No. of Dogs',
                values='Dogs',
                names='Areas')
st.plotly_chart(pie_chart)
