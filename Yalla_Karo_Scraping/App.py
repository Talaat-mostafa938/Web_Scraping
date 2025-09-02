import pandas as pd
import streamlit as st
import requests
from bs4 import BeautifulSoup
import csv

st.set_page_config("Web Scraping Yalla Kora")

st.title("Web Scraping App")

col1 , col2 , col3 = st.columns(3)

with col1:
    day = st.number_input("Enter Day", min_value=1, max_value=31, step=1 )

with col2:
    month = st.number_input("Enter Month", min_value=1, max_value=12, step=1)

with col3:
    year = st.number_input("Enter Year", min_value=2010, max_value=2100, step=1)

data_entry = f"{month}/{day}/{year}"

url = f"https://www.yallakora.com/match-center?date={data_entry}#days"
page = requests.get(url)
soup = BeautifulSoup(page.content , "html.parser")

data = [] 

championships = soup.find_all('div' , class_="matchCard")
for i in range(len(championships)):
    championship_name = championships[i].contents[1].find("h2").text.strip()
    matchs = championships[i].find_all('div' , class_="teamCntnr")

    for match in matchs:
        teamA = match.find("div" , class_="teams teamA").text.strip()
        teamB = match.find("div" , class_="teams teamB").text.strip()
        result = match.find("div" , class_="MResult").text.strip()
        time = match.find("div" , class_="MResult").find("span", class_="time").text.strip()
        resultA = result[0]
        resultB = result[4]

        result = resultA + " - " + resultB

        data.append({
              "Championship": championship_name,
              "Team A": teamA,
              "Result": result,
              "Team B": teamB,
              "Time": time
          })

df = pd.DataFrame(data)

st.title("🏆 Match results")
st.markdown("""
    <style>
    div.stButton > button:first-child {
        background-color: #799EFF; /* احمر */
        color: black;
        font-weight: bold;
        border-radius: 8px;
        height: 40px;
        width: 200px;
    }
    div.stButton > button:hover {
        background-color: #F3F2EC;
        color: black;
    }
    </style>
""", unsafe_allow_html=True)



if st.button("Get Matches"):
    st.write(f"{day}/{month}/{year}")
    st.dataframe(df)
    
if st.button("Download as CSV"):
    safe_date = f"{day}-{month}-{year}"
    df.to_csv(f"Matches {safe_date}.csv", index=False, encoding="utf-8-sig")
    st.success("File downloaded successfully as Matchs_info.csv")