
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import plotly.express as px

st.set_page_config(layout='wide')
st.title("Mental Health Analysis based on One Online Community")
st.header("Mental Health Analysis Dashboard")

df=pd.read_csv('Mental Health Dataset.csv')
df.head()

# change to timestamp
df['Timestamp'] = pd.to_datetime(df['Timestamp'])

# extract year and month from timestamp
df['Year'] = df['Timestamp'].dt.year
df['Month_No'] = df['Timestamp'].dt.month
df['Month'] = df['Timestamp'].dt.month_name()

st.sidebar.header("Filter information")

years = sorted(df.Year.unique().tolist())
years_choices = st.sidebar.selectbox("Select Year", ["All"]+years, index=0)

countries = sorted(df.Country.unique().tolist())
countries_choices = st.sidebar.selectbox("Select Country", ["All"]+countries, index=0)

occupations = sorted(df.Occupation.unique().tolist())
occupations_choices = st.sidebar.selectbox("Select Occupation", ["All"]+occupations, index=0)


if years_choices != "All":
    df = df[ df['Year']== years_choices]
if countries_choices != "All":
    df = df[ df['Country'] == countries_choices]
if occupations_choices != "All":
    df = df[ df['Occupation']==occupations_choices ]

#---------- row 1
col1, col2, col3 = st.columns(3)
taking_treatment_rate =round( (len(df[ df['treatment']=='Yes'] )/len(df['treatment'])) *100 ,2)
col1.metric("Taking Treatment Rate", taking_treatment_rate,'%')

support_awareness_rate = round((len(df[ df['care_options']=='Yes'])/ len(df['care_options']))*100,2)
col2.metric("Support Awareness Rate", support_awareness_rate,"%")

growing_stress_rate = round((len(df[ df['Growing_Stress']=='Yes'])/ len(df['Growing_Stress']))*100,2)
col3.metric("Growing Stress Rate", growing_stress_rate,"%")

#----------row 2
col1,col2=st.columns(2)
with col1:
    # treatment analysis
    treatment_analysis = df['treatment'].value_counts().reset_index(name='Count')
    fig =px.pie(
        treatment_analysis,
        names='treatment',
        values='Count',
        title='Contribution of Treatment'
    )
    st.plotly_chart(fig)

with col2:
    taking_treatment = df[ df['treatment']=='Yes' ]
    taking_treatment_by_year =  taking_treatment.groupby('Year')['treatment'].size().reset_index(name='Count')
    fig= px.line(
        taking_treatment_by_year,
        x='Year',
        y='Count',
        title='Taking Treatment over Years'
    )
    st.plotly_chart(fig)


# ---------------- row 2
col1, col2 = st.columns(2)
with col1:
    # Top 10 of countries with treatment
    top_10_list = df[ df['treatment']=='Yes' ]['Country'].value_counts().nlargest(10).index
    df_top10 =df[ df['Country'].isin(top_10_list) ]
    top_10_treatment_by_countries = df_top10.groupby( ['Country', 'treatment'] ).size().reset_index(name='Count').sort_values(by='Count', ascending=False)
    fig = px.bar(top_10_treatment_by_countries,
       x='Country',
       y='Count',
       title='Top 10 Countries of Treatment',
       color='treatment'
       )
    st.plotly_chart(fig)

with col2:
    # top 10 countries of taking treatment by Gender
    top_10_countries_of_taking_treatment = df_top10[ df_top10['treatment']=='Yes' ]
    top_10_countries_of_taking_treatment_by_gender = top_10_countries_of_taking_treatment.groupby( ['Country', 'Gender']).size().reset_index(name='Count').sort_values(by='Count',ascending=False)
    fig =px.bar(
        top_10_countries_of_taking_treatment_by_gender,
        x='Country',
        y='Count',
        color='Gender',
        title='Top 10 Countries for taking Treatment by Gender'
    )
    st.plotly_chart(fig)

# ------------ row 3
col1, = st.columns(1)
with col1:
    #top 10 countries of taking treatment by Occupation
    top_10_countries_of_taking_treatment_by_occupation = top_10_countries_of_taking_treatment.groupby( ['Country', 'Occupation']).size().reset_index(name='Count').sort_values(by='Count', ascending=False)
    fig =px.bar(
        top_10_countries_of_taking_treatment_by_occupation,
        x='Country',
        y='Count',
        color='Occupation',
        title='Top 10 Countries for taking Treatment by Occupation'
    )
    st.plotly_chart(fig)


col1, = st.columns(1)
with col1:
    df_numerics = df.copy()
    # convert categorical data to numeric
    df_numerics = df_numerics.apply(lambda x: x.str.strip() if x.dtype == "object" else x)
    # df_numerics = df_numerics.map({'Yes': 1, 'No':0, 'unknown':2, 'Maybe':2, 'Low':0, 'Medium':1, 'High':2, 'Not sure':2, '1-14 days':0, '15-30 days':1, '31-60 days':2, 'Go out Every day':3, 'More than 2 months':4})
    binary_map = {'Yes': 1, 'No': 0, 'Maybe': 0.5, 'Not sure': 0.5, 'unknown': 0.5}
    scale_map = {'Low': 0, 'Medium': 1, 'High': 2}
    days_map = {'Go out Every day': 0, '1-14 days': 1, '15-30 days': 2, '31-60 days': 3, 'More than 2 months': 4}

    df_numerics = df_numerics.replace(binary_map)
    df_numerics = df_numerics.replace(scale_map)
    df_numerics = df_numerics.replace(days_map)

    col_to_plot = ['self_employed', 'family_history', 'treatment', 'Days_Indoors', 'Growing_Stress', 'Changes_Habits', 'Mental_Health_History', 'Mood_Swings', 'Coping_Struggles', 'Work_Interest', 'Social_Weakness', 'mental_health_interview', 'care_options']
    corr_matrix = df_numerics[col_to_plot].corr()
    plt.figure(figsize=(10,5))
    sns.heatmap(corr_matrix)
    plt.title('Correlation Heatmap',fontsize=16,fontweight='bold', pad=20)
    st.pyplot(plt)


st.write ("""
    1. Focus on Care Option Awareness Improvement
          - Declare available care options in main events, social media or send direct emails to those community members

    2. Target on People who has Family History
          - Make counselling sessions and follow up them

    3. Target on Men and HouseWife
          - Make appropriate outdoor social activities in every once a week. It can improve high-stress rate.
 """)
