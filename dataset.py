import pandas as pd
import plotly.express as px
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
df=pd.read_csv('Visadataset.csv')

st.set_page_config(page_title="Visa Dashboard",layout="wide")


st.sidebar.header("Please Filter here:")
region=st.sidebar.multiselect(
    "Select the Region:",
    options=df['region_of_employment'].unique(),
    default=df['region_of_employment'].unique()
)
education=st.sidebar.multiselect(
    "Select the Education:",
    options=df['education_of_employee'].unique(),
    default=df['education_of_employee'].unique()
)
employment_type = st.sidebar.multiselect("Employment Type", options=df['unit_of_wage'].unique(), default=df['unit_of_wage'].unique())
application_status = st.sidebar.multiselect("Application Status", options=df['case_status'].unique(), default=df['case_status'].unique())
year_range = st.sidebar.slider("Year Range", min_value=int(df['yr_of_estab'].min()), max_value=int(df['yr_of_estab'].max()), value=(int(df['yr_of_estab'].min()), int(df['yr_of_estab'].max())))
Salary = st.sidebar.slider("Salary Range", min_value=int(df['prevailing_wage'].min()), max_value=int(df['prevailing_wage'].max()), value=(int(df['prevailing_wage'].min()), int(df['prevailing_wage'].max())))



filtered_df=df[(df['region_of_employment'].isin(region)) &
                (df['education_of_employee'].isin(education))&
                (df['unit_of_wage'].isin(employment_type))&
                (df['case_status'].isin(application_status))&
                (df['yr_of_estab'].between(year_range[0], year_range[1]))&
                (df['prevailing_wage'].between(Salary[0],Salary[1]))]

# MainPage
st.title("Visa Application Dashboard")
st.write(f"### Showing {len(filtered_df)} out of {len(df)} records")
st.write(filtered_df)

region_certification = filtered_df.groupby('region_of_employment')['case_status'].value_counts(normalize=True).unstack().fillna(0) * 100
st.subheader("Certification Rate by Region")
st.bar_chart(region_certification)


education_certification=filtered_df.groupby('education_of_employee')['case_status'].value_counts(normalize=True).unstack().fillna(0)*100
st.subheader("Certification Rate by Education")
st.bar_chart(education_certification)

employment_certification = filtered_df.groupby('unit_of_wage')['case_status'].value_counts(normalize=True).unstack().fillna(0) * 100
st.subheader("Certification Rate by Employment Type")
st.bar_chart(employment_certification)

#Salary Analysis

certified_salaries=filtered_df[filtered_df['case_status']=='Certified']['prevailing_wage']
denied_salaries = filtered_df[filtered_df['case_status'] == 'Denied']['prevailing_wage']

st.subheader("Salary Analysis")

# Plot histograms using matplotlib
fig, ax = plt.subplots(1, 2, figsize=(14, 6))

ax[0].hist(certified_salaries, bins=20, color='green', alpha=0.7)
ax[0].set_title('Certified Applications - Salary Distribution')
ax[0].set_xlabel('Salary')
ax[0].set_ylabel('Frequency')

ax[1].hist(denied_salaries, bins=20, color='red', alpha=0.7)
ax[1].set_title('Denied Applications - Salary Distribution')
ax[1].set_xlabel('Salary')
ax[1].set_ylabel('Frequency')

st.pyplot(fig)

fig, ax = plt.subplots(figsize=(10, 6))
sns.countplot(data=filtered_df,x='yr_of_estab',hue='case_status',ax=ax)
ax.set_title('Yearly Certification Countplot')
ax.set_xlabel('Year')
ax.set_ylabel('Count')
st.pyplot(fig)