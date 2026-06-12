from dash import html
from components.elements import *
from data import drivers_list, track_list

def get_driver_dashboard():
    return html.Div([
        dcc.Dropdown(
            id='driver-dropdown',
            className='elt-dropdown',
            options=drivers_list,
            value=drivers_list[0],
        ),

        html.Div([
            html.H2('Position by Track'),
            static(id='position-graph')
        ]),

        html.Div([
           html.H2("Best Lap Time by Track"),
           static(
               id='driver-best-lap-graph',
           )
        ]),

        html.H3("Choose a track"),
        dcc.Dropdown(
            id='time-per-lap-track',
            options=track_list,
            value=track_list[0],
        ),

        html.Div([
            html.H2("Lap Time in a track"),
            static(
                id='time-per-lap-graph',
            )
        ]),

        html.Div([
            html.H2("Sector"),
            static(
                id='sector-graph',
            )
        ])
    ])