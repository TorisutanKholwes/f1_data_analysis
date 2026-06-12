from dash import Dash, html, dcc, Input, Output

app = Dash(__name__,
           meta_tags=[{
               "name": "viewport",
               "content": "width=device-width, initial-scale=1, shrink-to-fit=no"
           }],
           suppress_callback_exceptions=True
           )

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.H1('F1 Dashboard'),
    html.Nav(
        html.Ul([
            html.Li(html.A('Home', href='#')),
            html.Li(html.A('Track', href='/track')),
            html.Li(html.A('Driver', href='/driver')),
            html.Li(html.A('Team', href='/team')),
        ])
    ),
    html.Div(
        className="main-content",
        children=html.Div(id="page-content")
    )
])