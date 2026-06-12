from app import app
from dash import html, Input, Output

from pages.driver.elements import get_driver_dashboard
from pages.track.elements import get_track_dashboard
from pages.home.elements import get_home_dashboard

import os

import pages.driver.graph
import pages.track.graph
import pages.home.graph

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
    return html.Div([html.H1("404 Not Found")])



if __name__ == '__main__':
    dash_host=os.getenv("DASH_HOST", "localhost")
    dash_port=os.getenv("DASH_PORT", "8050")
    debugging=os.getenv("DEBUGGING", "True")
    print("Launching app with the following configuration:")
    print(f"DASH_HOST: {dash_host}")
    print(f"DASH_PORT: {dash_port}")
    print(f"DEBUGGING: {debugging}")
    app.run(jupyter_mode='external', debug=debugging.lower()=="true", host=dash_host, port=dash_port)