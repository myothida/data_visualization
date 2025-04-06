# app.py

import dash
from dash import dcc, html
import plotly.graph_objects as go
import pandas as pd
from dash.dependencies import Input, Output
from data_functions import get_filtered_df, create_deceased_bar_chart, create_impact_map


df = pd.read_csv('./data/MM_earthquake_2025_unverified_data.csv')
dropdown_options = [{'label': region, 'value': region} for region in df['SR_Name_Eng'].dropna().unique()]
dropdown_options.append({'label': 'All region', 'value': 'all'})

app = dash.Dash(__name__)

app.layout = html.Div([   
    html.H1("Earthquake Impact Dashboard", style={'text-align': 'center'}),    
    
    html.Div([
        dcc.Dropdown(
            id='region-dropdown',
            options=dropdown_options,
            value="all",  
            placeholder="Select Region",
            style={'width': '50%', 'padding': '20px', 'margin': '20px auto'}
        )
    ]),    

    html.Div([
            # Left graph (Bar chart)
            html.Div([
                dcc.Graph(id='deceased-bar-chart')
            ], style={'width': '48%', 'display': 'inline-block', 'padding': '20px'}),
            
            # Right graph (Impact map)
            html.Div([
                dcc.Graph(id='impact-map')
            ], style={'width': '48%', 'display': 'inline-block', 'padding': '20px'}),
        ], style={'display': 'flex', 'justify-content': 'space-between'}),
])


@app.callback(
    [Output('deceased-bar-chart', 'figure'),
     Output('impact-map', 'figure')],
    [Input('region-dropdown', 'value')]
)

def update_dashboard(selected_region):
    filtered_df = get_filtered_df(df, selected_region)
    
    deceased_bar_chart = create_deceased_bar_chart(filtered_df)
    impact_map = create_impact_map(filtered_df)
    
    return deceased_bar_chart, impact_map

if __name__ == '__main__':
    app.run(debug=True)
