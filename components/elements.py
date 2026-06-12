from dash import dcc, html

def static(*args, **kwargs):
    return dcc.Graph(
        *args,
        config={
            'displayModeBar': False,
            'scrollZoom': False,
            'doubleClick': False,
            'showTips': True,
            'staticPlot': False,
        }
        , **kwargs)

def card(title, subtitle="", text="", id=""):
    titleId = "" if id == "" else f"{id}-title"
    subtitleId = "" if id == "" else f"{id}-subtitle"
    textId = "" if id == "" else f"{id}-text"
    return html.Div(className="dash-card", id=id, children=[
        html.H2(title, id=titleId),
        html.H3(subtitle, id=subtitleId),
        html.P(text, id=textId),
    ])