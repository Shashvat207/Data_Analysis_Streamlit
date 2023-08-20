import matplotlib.pyplot as plt
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import seaborn as sns
st.sidebar.title("Olympics Analysis")
user_menu=st.sidebar.radio(
    "Select an Option",('Medal Tally','Overall Analysis','Country-wise Analysis')
)
df=pd.read_csv(r"C:\Users\shash\Downloads\Datasets\athlete_events.csv")
region=pd.read_csv(r"C:\Users\shash\Downloads\Datasets\noc_regions.csv")

def preprocess():
    global df,region
    df=df[df["Season"]=='Summer']
    df=df.merge(region,on='NOC',how='left')
    df.drop_duplicates(inplace=True)
    df=pd.concat([df,pd.get_dummies(df['Medal'])],axis=1)
    return df
df=preprocess()
def most_successfull(df,country):
    temp_df=df.dropna(subset=["Medal"])
    temp_df=temp_df[temp_df["region"]==country]
    x = temp_df["Name"].value_counts().reset_index()
    #x.rename(columns={"count":"index"},inplace=True)
    #x= x.head(15).merge(df,left_on='index',right_on='Name',how='left')[["index","Name_x","Sport","region"]].drop_duplicates("index")
    #x.rename(columns={'index':'Name',"Name_x":"Medals"},inplace=True)
    x=x.drop_duplicates('Name')
    return x.head(15)
def yearwisemedal(df,country):
    temp_df = df.dropna(subset=["Medal"])
    temp_df.drop_duplicates(subset=["Team", 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'], inplace=True)
    new_df=temp_df[temp_df['region']==country]
    final_df=new_df.groupby('Year').count()['Medal'].reset_index()
    return final_df
def medal_tally(df):
    medal_tally = df.drop_duplicates(subset=["Team", 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'])
    medal_tally = medal_tally.groupby("region").sum()[['Gold', 'Silver', 'Bronze']].sort_values('Gold', ascending=False).reset_index()
    medal_tally['Total']=medal_tally['Gold']+medal_tally["Silver"]+medal_tally["Bronze"]

    return medal_tally
medal_df=df.drop_duplicates(subset=["Team",'NOC','Games','Year','City','Sport','Event','Medal'])
def fetch_medal_tally(year,country,df):
    medal_df=df.drop_duplicates(subset=["Team",'NOC','Games','Year','City','Sport','Event','Medal'])
    flag=0
    if year=="overall" and country=="overall":
        temp_df=medal_df
    if year=="overall" and country!="overall":
        flag=1
        temp_df=medal_df[medal_df["region"]==country]
    if year!="overall" and country=="overall":
        temp_df=medal_df[medal_df["Year"]==int(year)]
    if year!="overall" and country!="overall":
        temp_df=medal_df[(medal_df["Year"]==year) & (medal_df["region"]==country)]
    if flag==1:
        x=temp_df.groupby("Year").sum()[['Gold','Silver','Bronze']].sort_values('Year').reset_index()
    else:
        x=temp_df.groupby("region").sum()[['Gold','Silver','Bronze']].sort_values('Gold',ascending=False).reset_index()
    x['Total']=x['Gold']+x["Silver"]+x["Bronze"]
    return x
def country_year(df):
    years = df["Year"].unique().tolist()
    years.sort()
    years.insert(0, "overall")
    country = np.unique(df['region'].dropna().values).tolist()
    country.sort()
    country.insert(0, "overall")
    return years,country
def country_heatmap(df,country):
    temp_df=df.dropna(subset=["Medal"])
    temp_df.drop_duplicates(subset=["Team", 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'], inplace=True)
    new_df = temp_df[temp_df['region'] == country]
    pt=new_df.pivot_table(index="Sport",columns="Year",values='Medal',aggfunc='count').fillna(0)
    return pt


if user_menu=='Medal Tally':
    st.sidebar.header("Medal Tally")
    years,country=country_year(df)
    year=st.sidebar.selectbox("Select Year",years)
    countryy=st.sidebar.selectbox("Select Country",country)
    medal_tally=fetch_medal_tally(year,countryy,df)
    if year=="overall" and countryy=="overall":
        st.title("Overall Analysis")
    if year!="overall" and countryy=="overall":
        st.title("Medal Tally in "+str(year)+" Olympics")
    if year=="overall" and countryy!="overall":
        st.title(countryy+" Overall Performance")
    if year!="overall" and countryy!="overall":
        st.title(countryy+" performance in "+str(year)+" Olympics")
    st.table(medal_tally)
if user_menu=="Overall Analysis":
    st.header("Top Statistics")
    editions=df['Year'].unique().shape[0]-1
    cities = df['City'].unique().shape[0]
    sports = df['Sport'].unique().shape[0]
    events = df['Event'].unique().shape[0]
    names = df['Name'].unique().shape[0]
    nations = df['region'].unique().shape[0]
    col1 , col2 ,col3=st.columns(3)
    with col1:
        st.header("Editions")
        st.title(editions)
    with col2:
        st.header("Hosts")
        st.title(cities)
    with col3:
        st.header("Sports")
        st.title(sports)
    col1, col2, col3 = st.columns(3)
    with col1:
        st.header("Events")
        st.title(events)
    with col2:
        st.header("Athletes")
        st.title(names)
    with col3:
        st.header("Nation")
        st.title(nations)
    st.title("Nations Over Time")
    nations_over_time=df.drop_duplicates(['Year','region'])['Year'].value_counts().reset_index().sort_values('Year')
    fig = px.line(nations_over_time, y='count', x='Year')
    st.plotly_chart(fig)
    st.title("Athletes over Time")
    athletes_over_time = df.drop_duplicates(['Name', 'region'])['Year'].value_counts().reset_index().sort_values('Year')
    fig = px.line(athletes_over_time, y='count', x='Year')
    st.plotly_chart(fig)

    st.title("Events over Time")
    athletes_over_time = df.drop_duplicates(['Event', 'region'])['Year'].value_counts().reset_index().sort_values('Year')
    fig = px.line(athletes_over_time, y='count', x='Year')
    st.plotly_chart(fig)

    st.title("Cities over Time")
    athletes_over_time = df.drop_duplicates(['City', 'region'])['Year'].value_counts().reset_index().sort_values('Year')
    fig = px.line(athletes_over_time, y='count', x='Year')
    st.plotly_chart(fig)

if user_menu=='Country-wise Analysis':
    st.sidebar.title("Country Wise Analysis")
    year,country_list=country_year(df)
    count=st.sidebar.selectbox("Select a Country",country_list)

    country=yearwisemedal(df,count)
    fig = px.line(country, y='Medal', x='Year')
    st.title(count+" Medals over the years")
    st.plotly_chart(fig)
    pt=country_heatmap(df,count);
    st.title(count+" Excel in the Sports")
    try:
        fig,ax=plt.subplots(figsize=(20,20))
        ax=sns.heatmap(pt,annot=True)
        st.pyplot(fig)
    except:
        st.subheader("No Data Found")
    st.title("Most Success full players")
    st.table(most_successfull(df,count))