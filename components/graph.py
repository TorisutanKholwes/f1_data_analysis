from dash import dcc

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