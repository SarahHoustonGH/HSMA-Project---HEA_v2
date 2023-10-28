import streamlit as st
import pandas as pd
import numpy as np
import csv
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
import seaborn as sns
import geopandas as gpd
from geopy.geocoders import Nominatim
import folium
from folium.plugins import MarkerCluster
from folium import plugins
import pandas as pd
import json
import requests
import geopandas as gpd
import streamlit_folium
from streamlit_folium import st_folium

### Mapping ------------------------------------------------

st.markdown("## Referral Sources - Maps")

#Create buttons in sidebar


with st.sidebar:
    add_radio = modality = st.radio(
    "What modality would you like to view?",
    ["X", "U"],
    captions = ["X ray", "Ultrasound"])


local_authority = st.text_input('Local authority', 'Haringey')
st.write('Selection:', local_authority )


# Create a Folium map
#this is slow and note if this is 2011 or 2021 geojson data
df2 = gpd.read_file("Data\lsoa.geojson")

IMD = pd.read_csv("Data\IMD_LSOA_Lookup.csv")

IMD = IMD.rename(columns={'LSOA11': 'LSOA11CD'})
combineddf  = df2.merge(IMD, on='LSOA11CD', how='left')


#User adds Local authority name for mapping of LSOAs within the LA
#print("Enter name of local authority")
LA = local_authority

# Uses centre of chosen local authority to centre map 
# Location of centroids from  https://nihr.opendatasoft.com/explore/dataset/local_authority_districts/table/
location_data = pd.read_csv("Data\LA_locations.csv")
LA_location = location_data[location_data['LAD23NMW'].str.startswith(LA)]
LA_location_lat= LA_location[["LAT"]].values
LA_location_long= LA_location[["LONG"]].values


# Create base map
m = folium.Map(location=[LA_location_lat,LA_location_long],
                        zoom_start=12,
                        tiles='cartodbpositron')



#Return all LSOA names with a substring of the LA name
df3 = combineddf[combineddf['LSOA11NM'].str.startswith(LA)]

#Read in the data to be displayed on the LSOA map
df_lsoa_imd =  pd.read_csv("Stage1Outputs\GPSummaryReferralData_U_Map.csv")

#df2["LSOA21CDtxt"] = df2["LSOA21CD"].astype(str)
folium.Choropleth(
                geo_data = df3,      
                  data=df3,
                  columns=['LSOA11CD', 'IMD2019 Decile'],
                  key_on="properties.LSOA11CD",
                  fill_color ='YlGnBu',      
                  fill_opacity = 0.5,
                  legend_name='IMD',
                  highlight=True).add_to(m)


#Read in the GP location data to be displayed on the LSOA map
df_gp =  pd.read_csv("Stage1Outputs\GPSummaryReferralData_U_Map.csv")

for (index, row) in df_gp.iterrows():
    pop_up_text = f"The postcode for {row.loc['GP practice name']} " #+ \
                     #is {row.loc['Postcode']}"
    folium.Circle(location=[row.loc['Latitude'], row.loc['Longitude']],
                  #radius=1000,  # Adjust the radius as needed,
                  radius = row.loc["CountReferrals_Baseline"],
                  fill = True,
                  fill_opacity = 0.9,
                  color = 'black',
                  popup=pop_up_text, 
                  tooltip=f"{row.loc['GP practice name']} sent {row.loc['CountReferrals_Baseline']} referrals").add_to(m)
    


st_data = st_folium(m, width=725)