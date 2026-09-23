import dash
from dash import dcc, html
import plotly.express as px
import pandas as pd

app = dash.Dash(__name__)

try:
    df = pd.read_csv('../data/processed/spacex_processed.csv')
except Exception:
    df = pd.DataFrame()

site_options = [{'label': 'All Sites', 'value': 'ALL'}]
if not df.empty and 'launch_site.site_name_long' in df.columns:
    sites = df['launch_site.site_name_long'].unique()
    site_options.extend([{'label': s, 'value': s} for s in sites])

app.layout = html.Div([
    html.H1('SpaceX Falcon 9 Launch Dashboard'),
    dcc.Dropdown(id='site-dropdown', options=site_options, value='ALL'),
    dcc.Graph(id='success-pie-chart'),
    dcc.RangeSlider(id='payload-slider', min=0, max=10000, step=100, value=[0, 10000]),
    dcc.Graph(id='payload-scatter')
])


from dash.dependencies import Input, Output


@app.callback(
    Output('success-pie-chart', 'figure'),
    Input('site-dropdown', 'value')
)
def update_pie(selected_site):
    if df.empty:
        return {}
    dff = df.copy()
    if selected_site != 'ALL':
        dff = dff[dff['launch_site.site_name_long'] == selected_site]
    if 'class' not in dff.columns:
        return {}
    fig = px.pie(dff, names='class', title='Launch Success Distribution')
    return fig


@app.callback(
    Output('payload-scatter', 'figure'),
    [Input('site-dropdown', 'value'), Input('payload-slider', 'value')]
)
def update_scatter(selected_site, payload_range):
    if df.empty:
        return {}
    dff = df.copy()
    low, high = payload_range
    if 'payload.mass_kg' in dff.columns:
        dff = dff[(dff['payload.mass_kg'] >= low) & (dff['payload.mass_kg'] <= high)]
    if selected_site != 'ALL':
        dff = dff[dff['launch_site.site_name_long'] == selected_site]
    if 'payload.mass_kg' not in dff.columns or 'class' not in dff.columns:
        return {}
    fig = px.scatter(dff, x='payload.mass_kg', y='class', color='orbit', title='Payload vs Outcome')
    return fig


if __name__ == '__main__':
    app.run_server(debug=True)
