from dash import Dash, html, dcc, Input, Output
from components.elements import static
from data import track_list


def get_track_dashboard():
    return html.Div([
        dcc.Dropdown(
            id='track-dropdown',
            options=track_list,
            value=track_list[0]
        ),

        html.Div([
            html.H3('Choose a specific lap'),
            dcc.Slider(1, 1, 1,
                       id='track-slider',
                       ),
        ]),

        html.Div([
            html.H2('Position of drivers'),
            static(id='final-position'),
        ]),

        html.Div([
            html.H2("Best section time per lap"),
            static(id='best-section-time'),
        ]),

        html.Div([
            html.H2("Tyres used by drivers"),
            static(id='track-tyres')
        ]),

        html.Div([
            html.H2("Max speed"),
            dcc.RadioItems(
                id='track-speed-radio',
                options={
                    'all': 'All laps',
                    'one': 'One lap',
                },
                value='all',
                inline=True,
            ),
            static(id='max-speed')
        ])
    ])