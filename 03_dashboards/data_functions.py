# data_functions.py

import plotly.express as px
import pandas as pd

def get_filtered_df(df, selected_region):
    """Filters the dataframe based on the selected region."""
    if(selected_region == 'all'):
        filtered_df = df.copy()
    else:
        filtered_df = df[df['SR_Name_Eng'] == selected_region] if selected_region else df
    filtered_df = filtered_df[~filtered_df['Deceased'].isna()]
    return filtered_df

def create_deceased_bar_chart(filtered_df):
    """Creates a bar chart for the number of deceased by township."""
    fig = px.bar(
        filtered_df.groupby('Township_Name_Eng')['Deceased'].count().reset_index(),
        x='Township_Name_Eng',
        y='Deceased',
        color='Deceased',
        title='Number of Deceased by Townships as of March 28',
        labels={'Deceased': 'Number of Deceased as of March 28', 'Township_Name_Eng': 'Name of Township'}
    )
    fig.update_layout(
        height=600,
        width=1200,
    )
    return fig

def create_impact_map(filtered_df):
    """Creates a scatter map showing earthquake impact."""
    fig = px.scatter_map(
        filtered_df.groupby('Township_Name_Eng').agg(
            Deceased_sum=('Deceased', 'count'),
            Latitude_avg=('Latitude', 'mean'),
            Longitude_avg=('Longitude', 'mean')).reset_index(),
        lat='Latitude_avg',
        lon='Longitude_avg',
        hover_name='Township_Name_Eng',
        color='Deceased_sum',
        size='Deceased_sum',
        zoom=6,
        height=800,
        title='Earthquake Impact Map: Number of Deceased by Townships as of March 28'
    )
    return fig
