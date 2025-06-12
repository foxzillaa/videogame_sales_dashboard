import streamlit as st
import pandas as pd
import datetime
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from PIL import Image



df = pd.read_csv('vgsales.csv')

st.set_page_config(layout="wide")
st.markdown('<style>div.block-container{padding-top: 1rem;}</style>', unsafe_allow_html=True)
image = Image.open('vg.jpg')
image = image.resize((500, 400))
col1, col2 = st.columns([0.1, 0.9])
with col1:
    st.image(image, use_container_width=False)

html_title = """
    <style>
    .title-test{
    font-weight:bold;
    padding:5px;
    border-radius:6px
    }
    </style>
    <center><h1 class = "title-test">Videogame Global Sales Interactive Dashboard</h1></center>"""
with col2:
    st.markdown(html_title, unsafe_allow_html=True)

col3, col4, col5 = st.columns([0.1, 0.45, 0.45])

with col3: 
    box_date = str(datetime.datetime.now().strftime("%Y %B %d"))
    st.write(f"Last updated:\n {box_date}")

with col4:
   fig = px.bar(df.head(100), x='Name', y='Global_Sales', labels = {"Global_Sales" : "Global Sales {$}" },
                title = "Global Video Games Sales", hover_data = ["Global_Sales"],
                 template = "gridon", height = 700 )
   st.plotly_chart(fig, use_container_width=True)
_, view1, dwn1, view2, dwn2 = st.columns([0.15,0.20,0.20,0.20,0.20])
with view1:
    expander = st.expander("Global sales by Name")
    data = df [["Name", "Global_Sales"]].groupby(by="Name")["Global_Sales"].sum().reset_index().sort_values(by= "Global_Sales", ascending=False).head(100)
    expander.write(data)
with dwn1:
    st.download_button("Get Complete Data", data = data.to_csv().encode('utf-8'), 
                       file_name = "Videogame_Global_Sales.csv", mime = "text/csv")
    

region_totals = df[["NA_Sales", "EU_Sales", "JP_Sales", "Other_Sales"]].sum().reset_index()
region_totals.columns = ["Region", "Sales"]

with col5:
    fig1 = px.pie(region_totals, names="Region", values="Sales", labels = {"Sales": "Total Sales {$}"}, title="Sales by Region", template="plotly_white")
    st.plotly_chart(fig1, use_container_width=True)
with view2:
    expander1 = st.expander("Sales by Region")
    region_data = df[["NA_Sales", "EU_Sales", "JP_Sales", "Other_Sales"]].sum().reset_index()
    region_data.columns = ["Region", "Sales"]
    expander1.write(region_data)
with dwn2:
    st.download_button("Get Region Data", data = region_data.to_csv().encode('utf-8'), 
                       file_name = "Region_Sales_Data.csv", mime = "text/csv")
st.divider()

genre_options = df["Genre"].unique()
selected_genre = st.multiselect("Want to filter by genre? Leave unselected to see all", genre_options, default = genre_options[:0])

if not selected_genre:
    selected_genre = genre_options


filtered_df = df[df["Genre"].isin(selected_genre)]
result1 = (
    filtered_df[["Platform", "Genre", "Global_Sales"]]
    .groupby(["Platform", "Genre"])["Global_Sales"]
    .sum()
    .reset_index()
    .pivot(index="Platform", columns="Genre", values="Global_Sales")
    .fillna(0)
)

fig3 = go.Figure()

for genre in result1.columns:
    fig3.add_trace(go.Bar(
        x=result1.index,
        y=result1[genre],
        name=genre
    ))
    if len(selected_genre) == 1:
        graph_title = f"Global Sales by Platform for Genre: {selected_genre[0]}"
    else:
        graph_title = "Global Sales by Platform and Genre"


fig3.update_layout(
    title = graph_title,
    xaxis = dict(title="Platform"),
    yaxis = dict(title="Global Sales"),
    barmode = "stack", 
    template = "plotly_white",
    legend = dict(x=1, y=1)
)

_, col6 = st.columns([0.1, 0.9])
with col6:
    st.plotly_chart(fig3, use_container_width=True)