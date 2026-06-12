import plotly.express as px
from dash import Input, Output

from app import app
from data import f1_data

@app.callback(
    Output("track-slider", "max"),
    Output("track-slider", "marks"),
    Output("track-slider", "value"),
    Input("track-dropdown", "value"),
    prevent_initial_call=False,
)
def update_slider_range(track):
    if not track:
        return 1, {}, 1

    df = (
        f1_data
        .query(f"track == '{track}'")
        .groupby('full_name')
        .agg(
            max_lap=('lapnumber', 'max'),
        )
        .reset_index()
    )

    new_max = int(df['max_lap'].max())

    marks = {i: str(i) for i in range(1, new_max+1, max(1, new_max // 10))}

    new_value = max(1, new_max)

    return new_max, marks, new_value

@app.callback(
    Output('final-position', 'figure'),
    Input('track-dropdown', 'value'),
    Input("track-slider", "value"),
)
def update_graph(track, lap):
    final_positions = (
        f1_data
        .query(f"track == '{track}' and lapnumber == {lap}")
        .sort_values(by='position')
    )

    if final_positions.empty:
        return px.bar(title=f"No data for {track}")

    fig = px.bar(
        final_positions,
        x='position',
        y='full_name',
        orientation='h',
        #color='team',
        title=f'Final positions — {track}',
        labels={"position": "Final position", "full_name": "Driver", "team": "Team"},
    )

    fig.update_yaxes(autorange="reversed")

    fig.update_xaxes(dtick=1, autorange="reversed" if False else True)

    fig.update_layout(margin={"l": 200, "r": 20, "t": 40, "b": 40})  # laisser de la place aux noms


    return fig

@app.callback(
    Output('best-section-time', 'figure'),
    Input('track-dropdown', 'value'),
)
def update_graph(track):
    df = (
        f1_data
        .query(f"track == '{track}'")
        .groupby('lapnumber')
        .agg(
            best_sector1=('sector1', 'min'),
            best_sector2=('sector2', 'min'),
            best_sector3=('sector3', 'min'),
        )
        .reset_index()
    )

    fig = px.line(
        df,
        x='lapnumber',
        y=['best_sector1', 'best_sector2', 'best_sector3'],
        labels = {
            'lapnumber': 'Lap',
            'best_sector1': 'Sector 1',
            'best_sector2': 'Sector 2',
            'best_sector3': 'Sector 3',
        },
    )

    fig.for_each_trace(lambda t: t.update(name=t.name.replace('best_sector1', 'Sector 1')
                                          .replace('best_sector2', 'Sector 2')
                                          .replace('best_sector3', 'Sector 3')))

    fig.update_layout(
        legend_title=f"Sectors - {track}",
        yaxis_title="Time (in seconds)",
    )

    fig.update_traces(
        hovertemplate='Lap %{x}<br>%{y:.3f} seconds<br>%{fullData.name}<extra></extra>',
    )

    return fig

@app.callback(
    Output('track-tyres', 'figure'),
    Input('track-dropdown', 'value'),
    Input("track-slider", "value"),
)
def update_graph(track, lap):
    df = (
        f1_data
        .query(f"track == '{track}' and lapnumber == {lap}")
        .groupby('compound')
        .size()
        .reset_index(name='count')
    )

    fig = px.pie(
        df,
        values='count',
        names='compound',
    )

    return fig

@app.callback(
    Output('max-speed', 'figure'),
    Input('track-dropdown', 'value'),
    Input("track-slider", "value"),
    Input('track-speed-radio', 'value')
)
def update_graph(track, lap, lap_type):
    query = f"track == '{track}'"
    if lap_type == 'one':
        query += f" and lapnumber == {lap}"

    df = (
        f1_data
        .query(query)
    )
    if lap_type == 'all':
        df = (
            df
            .groupby('full_name')
            .agg(maxspeed=('maxspeed', 'max'))
            .reset_index()
        )

    fig = px.bar(
        df,
        x='full_name',
        y='maxspeed',
    )

    return fig