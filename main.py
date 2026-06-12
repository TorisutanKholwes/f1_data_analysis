from app import app
from dash import html, Input, Output

from pages.driver.elements import get_driver_dashboard
from pages.home import get_home_dashboard
from pages.team import get_team_dashboard
from pages.track import get_track_dashboard

import os

import pages.driver.graph


@app.callback(
    Output("page-content", "children"),
    Input("url", "pathname"),
)
def display_page(pathname):
    if pathname == "/":
        return get_home_dashboard()
    elif pathname == "/track":
        return get_track_dashboard()
    elif pathname == "/driver":
        return get_driver_dashboard()
    elif pathname == "/team":
        return get_team_dashboard()
    return html.Div("404 Not Found")



if __name__ == '__main__':
    dash_host=os.getenv("DASH_HOST", "localhost")
    dash_port=os.getenv("DASH_PORT", "8050")
    debugging=os.getenv("DEBUGGING", "False")
    app.run(jupyter_mode='external', debug=debugging.lower()=="true", host=dash_host, port=dash_port)