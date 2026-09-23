import folium
import pandas as pd
from folium.plugins import MarkerCluster


def create_launch_map(processed_csv='data/processed/spacex_processed.csv', save_html='figures/map/spacex_launch_map.html'):
    df = pd.read_csv(processed_csv)
    # Expect columns: latitude, longitude
    map_center = [0, 0]
    if 'Latitude' in df.columns and 'Longitude' in df.columns:
        lat_mean = df['Latitude'].mean()
        lon_mean = df['Longitude'].mean()
        map_center = [lat_mean, lon_mean]
    else:
        # try to infer from launch site names using coords_lookup
        from src.coords_lookup import lookup
        coords = df['Launch Site'].map(lambda s: lookup(s) if isinstance(s, str) else None)
        coords = coords.dropna()
        if not coords.empty:
            lat_mean = sum(c[0] for c in coords) / len(coords)
            lon_mean = sum(c[1] for c in coords) / len(coords)
            map_center = [lat_mean, lon_mean]

    m = folium.Map(location=map_center, zoom_start=2)
    marker_cluster = MarkerCluster().add_to(m)

    for _, row in df.iterrows():
        lat = None
        lon = None
        if 'Latitude' in row and 'Longitude' in row:
            lat = row.get('Latitude')
            lon = row.get('Longitude')
        if pd.isna(lat) or pd.isna(lon):
            # try lookup by launch site text
            from src.coords_lookup import lookup
            coords = lookup(row.get('Launch Site'))
            if coords:
                lat, lon = coords
        if lat is None or lon is None or pd.isna(lat) or pd.isna(lon):
            continue
        popup = folium.Popup(str(row.get('Flight Number', 'Launch')) + ' - ' + str(row.get('Launch Site','')), max_width=300)
        folium.Marker(location=[lat, lon], popup=popup).add_to(marker_cluster)

    m.save(save_html)
    return save_html


if __name__ == '__main__':
    print('Create folium map from processed CSV')
