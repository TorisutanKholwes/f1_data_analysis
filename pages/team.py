from data import teams_list
from dash import Dash, html, dcc, Input, Output

def get_team_dashboard():
    return html.Div([
        dcc.Dropdown(
            id='team-dropdown',
            options=teams_list,
        )
    ])