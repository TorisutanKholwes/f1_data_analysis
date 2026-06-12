from dash import Dash, html, dcc, Input, Output
from components.elements import card, static

def get_home_dashboard():
    return html.Div([
        html.Div([
            html.H2("Driver with the most wins :"),
            card(title="Niki Lauda", id="most-wins")
        ]),

        html.Div([
            html.H2("Victory count per driver"),
            static(id="victory-drivers")
        ]),

        html.Div([
            html.H2("Fastest track"),
            card(title="", id="fastest-track")
        ]),

        html.Div([
            html.H2("Fatest lap per track"),
            static(id="fatest-laps")
        ]),

        html.Div([
            html.H2("Track map"),
            static(id='track-map')
        ]),
    ])