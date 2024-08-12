import streamlit as st
import leafmap.foliumap as leafmap
import pandas as pd

st.set_page_config(layout="wide")

st.sidebar.title("About")
st.sidebar.info("Marker Cluster")

st.title("NYC Firehouse Listing")

facilities = "/Users/hanhhieudao/demo-map-/pages/data/FDNY_Firehouse_Listing_20240807.csv"
regions = "/Users/hanhhieudao/demo-map-/pages/data/Borough Boundaries.geojson"

df = pd.read_csv(facilities)

firehouse_names = df['FacilityName'].unique()

selected_firehouse = st.selectbox("Select a Firehouse", firehouse_names)

selected_location = df[df['FacilityName'] == selected_firehouse][['Latitude', 'Longitude']].iloc[0]
latitude, longitude = selected_location['Latitude'], selected_location['Longitude']

lat_diff = 0.002
lon_diff = 0.002

bounds = [[latitude - lat_diff, longitude - lon_diff], [latitude + lat_diff, longitude + lon_diff]]

m = leafmap.Map(center=[40.7128, -74.0060], zoom=10)

m.add_geojson(regions, layer_name="NYC Boroughs")

m.add_points_from_xy(
    df,
    x="Longitude",
    y="Latitude",
    popup=["FacilityName", "FacilityAddress", "Borough", "Postcode"]
)

m.fit_bounds(bounds)

m.to_streamlit(height=700)

firehouse_info = df[df['FacilityName'] == selected_firehouse].T
st.dataframe(firehouse_info, use_container_width=True)