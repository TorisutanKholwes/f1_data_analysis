from dash import Dash, html, dcc, Input, Output

from data import track_list


def get_track_dashboard():
    return html.Div([
        dcc.Dropdown(
            id='track-dropdown',
            options=track_list,
        )
    ])