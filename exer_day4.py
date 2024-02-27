import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from urllib.request import urlopen
import json
from copy import deepcopy
import streamlit as st

@st.cache_data
def load_data(path):
    df = pd.read_csv(path)
    return df

df_ch_raw=load_data(path='./data/raw/renewable_power_plants_CH.csv')
df_ch=deepcopy(df_ch_raw)

st.title("Clean Energy Sources in Switzerland")
st.header("Are you interested in which canton in Switzerland boasts the most clean energy sources?")

if st.checkbox("Show dataset"):
    st.subheader("This is my dataset:")
    st.dataframe(data=df_ch_raw)

df_ch_canton = pd.read_csv('canton.csv')

geojson_ch = json.load(open('./data/raw/georef-switzerland-kanton.geojson'))



st.header("Map of Switzerland")

# Sample Streamlit Map
st.subheader("Production per energy source")

sources = sorted(pd.unique(df_ch['energy_source_level_2']))
source = st.selectbox("Choose a energy source", sources)

x = df_ch_canton[df_ch_canton['energy_source_level_2']==source]

fig = px.choropleth_mapbox(x, geojson=geojson_ch, locations='canton_name',color='production', featureidkey='properties.kan_name',mapbox_style='open-street-map',
                           hover_data={"canton_name": True,
                           "production":True,
                            },                     
                          ) 
fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0},mapbox_style="carto-positron",
                  mapbox_zoom=5, mapbox_center = {"lat": 46.5653, "lon": 7.2650})

st.plotly_chart(fig)

yy=[]
for s in sources:
 y=df_ch_canton[df_ch_canton['energy_source_level_2']==s].energy_source_level_2.count()
 yy.append(y)

st.header("Distribution of renewable energies in Switzerland")

fig1=go.Figure()
fig1.add_bar(x=sources,y=yy)

st.plotly_chart(fig1)

cantons=df_ch.canton.unique()

n_sources=[]

for s in sources:
    my_list=[]
    for c in cantons:
        my_list.append(df_ch_canton[(df_ch_canton['canton']==c) & (df_ch_canton['energy_source_level_2']==s)].energy_source_level_2.count())
    n_sources.append(my_list)


st.header("Distribution of renewable energies per canton")

for c in cantons:
 fig2=go.Figure(data=[
        go.Bar(x=cantons,y=n_sources[0], name='Bioenergy'),
        go.Bar(x=cantons,y=n_sources[1], name='Hydro'),
        go.Bar(x=cantons,y=n_sources[2], name='Solar'),
        go.Bar(x=cantons,y=n_sources[3], name='Wind'),
    ],
    layout={
        'barmode': 'stack'
    }
 )

st.plotly_chart(fig2)

df_x=df_ch_canton.groupby(['canton','canton_name']).electrical_capacity.mean().sort_values(ascending=False).reset_index()

st.header("Mean energy capacity per canton")

fig3 = px.choropleth_mapbox(df_x, geojson=geojson_ch, locations='canton_name',color='electrical_capacity', featureidkey='properties.kan_name',mapbox_style='open-street-map',
                           hover_data={"canton_name": True,
                           "electrical_capacity":True,
                           },                        
                          ) 
fig3.update_layout(margin={"r":0,"t":0,"l":0,"b":0},mapbox_style="carto-positron",
                  mapbox_zoom=5, mapbox_center = {"lat": 46.5653, "lon": 7.2650})

st.plotly_chart(fig3)

#st.subheader("Mean value of the electrical capacity")

fig4=go.Figure(data=[
        go.Bar(x=df_x.canton.values,y=df_x.electrical_capacity.values),
    ],
)

fig4.update_layout(
    title={"text": "Electrical capacity", "font": {"size": 24}},
    xaxis={"title": {"text": "Canton", "font": {"size": 18}}},
    yaxis={"title": {"text": "Capacity", "font": {"size": 18}}},
    #paper_bgcolor='rgb(254, 246, 224)',
    #plot_bgcolor='rgb(254, 246, 224)',
)
st.plotly_chart(fig4)

st.header("Violin plot of the tariff for different energy source")

sources1 = ["All"]+ sorted(pd.unique(df_ch['energy_source_level_2']))
source1 = st.selectbox("Choose a energy source", sources1)

fig5 = go.Figure()

if source1=='All':
 for s in sources:
  y=df_ch_canton[df_ch_canton['energy_source_level_2']==s].tariff
  fig5.add_box(y=y,name=s)
else:
  y=df_ch_canton[df_ch_canton['energy_source_level_2']==source1].tariff
  fig5.add_box(y=y,name=s)

st.plotly_chart(fig5)

df_x_t=df_ch_canton.groupby(['energy_source_level_2']).tariff.mean().sort_values(ascending=False).reset_index()

st.header("Distribution of the mean value of the tariff for energy source")

fig_x = go.Figure()
fig_x.add_pie(labels = df_x_t.energy_source_level_2.values, values = df_x_t.tariff.values)

st.plotly_chart(fig_x)