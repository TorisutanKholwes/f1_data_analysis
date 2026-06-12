import plotly.express as px
from dash import Input, Output

from app import app
from data import f1_data
import plotly.graph_objects as go

def get_best_time_on_sector(track, lap, sector):
    return float(f1_data.query(f"track == '{track}' and lapnumber == {lap}")[sector].min())

def format_time(seconds):
    minutes = int(seconds // 60)
    sec = seconds % 60
    return f"{minutes}:{sec:05.2f}"


@app.callback(
    Output('position-graph', 'figure'),
    Input('driver-dropdown', 'value'),
)
def update_graph(name):
    updated = (
        f1_data
        .query(f'full_name == "{name}"')
        .groupby('track')
        .agg(
            position=('position', 'last')
        )
        .reset_index()
    )

    fig = px.line(
        updated,
        x='track',
        y='position',
        title=f"{name} position on each track",
        labels={
            'track': 'Track',
            'position': 'Position'
        },
    )
    fig.update_yaxes(
        autorange=False,
        dtick=1,
        tickmode='linear',
        tickvals=list(range(1, 21)),
        range=[20.5, 0.5],
    )

    return fig

@app.callback(
    Output('driver-best-lap-graph', 'figure'),
    Input('driver-dropdown', 'value'),
)
def update_graph(name):
    updated = (
        f1_data
        .query(f'full_name == "{name}"')
        .groupby('track')
        .agg(
            best_lap=('laptime', 'min'),
            avg_lap=('laptime', 'mean'),
        )
        .reset_index()
    )

    updated["best_lap_str"]=updated["best_lap"].apply(format_time)
    updated["avg_lap_str"]=updated["avg_lap"].apply(format_time)

    fig = px.bar(
        updated,
        x='track',
        y=['best_lap', 'avg_lap'],
        barmode='group',
        title=f"{name} best lap and average lap time on each track",
        labels={
            'track': 'Track',
            'best_lap': 'Best Lap',
            'avg_lap': 'Average Lap',
        },
    )

    fig.update_layout(
        yaxis_title='Lap time (in seconds)',
    )

    for trace in fig.data:
        if trace.name == "best_lap":
            trace.customdata = updated[["best_lap_str"]]
            trace.hovertemplate= (
                "Track: %{x}<br>"
                "Best Lap: %{customdata[0]}<extra></extra>"
            )
        elif trace.name == "avg_lap":
            trace.customdata = updated[["avg_lap_str"]]
            trace.hovertemplate= (
                "Track: %{x}<br>"
                "Average Lap: %{customdata[0]}<extra></extra>"
            )

    fig.update_layout(showlegend=False)

    return fig

@app.callback(
    Output('time-per-lap-graph', 'figure'),
    Input('driver-dropdown', 'value'),
    Input('time-per-lap-track', 'value'),
)
def update_graph(name, track):
    updated = (
        f1_data
        .query(f"full_name == '{name}' and track == '{track}'")
    )

    fig = px.line(
        updated,
        x='lapnumber',
        y='laptime',

    )

    fig.update_xaxes(minor=dict(showgrid=True))
    fig.update_yaxes(minor=dict(showgrid=True))

    return fig

@app.callback(
    Output("sector-graph", "figure"),
    Input('driver-dropdown', 'value'),
    Input('time-per-lap-track', 'value'),
)
def update_graph(name, track):
    updated = (
        f1_data
        .query(f"full_name == '{name}' and track == '{track}'")
    )
    updated['sector1_color'] = 'green'
    updated['sector2_color'] = 'blue'
    updated['sector3_color'] = 'red'

    best_lap = [500, 500, 500]
    laps_count = updated['lapnumber'].max()
    for lap in range(1, int(laps_count)+1):
        i = 0
        for sector in ['sector1', 'sector2', 'sector3']:
            current = updated.query(f"lapnumber == {lap}")
            if current.empty:
                i+=1
                continue
            time = float(current[sector].values[0])
            if time < best_lap[i]:
                if time <= get_best_time_on_sector(track, lap, sector):
                    updated.loc[current.index, f"{sector}_color"] = 'purple'
                else:
                    updated.loc[current.index, f"{sector}_color"] = 'green'
                best_lap[i] = time
            else:
                updated.loc[current.index, f"{sector}_color"] = 'red'
            updated.loc[current.index, f"{sector}_best"] = get_best_time_on_sector(track, lap, sector)
            updated.loc[current.index, f"{sector}_personal_best"] = best_lap[i]
            i += 1


    fig = go.Figure()

    fig.add_bar(
        x=updated["lapnumber"],
        y=updated["sector1"],
        name="sector1",
        marker_color=updated["sector1_color"],
        customdata=updated[["sector1_best", "sector1_personal_best"]].to_numpy(),
        hovertemplate="Sector 1 <br>Lap %{x}<br>Time : %{y}<br>Personal best: %{customdata[1]}<br>Best : %{customdata[0]}<extra></extra>",
    )

    fig.add_bar(
        x=updated["lapnumber"],
        y=updated["sector2"],
        name="sector2",
        marker_color=updated["sector2_color"],
        customdata=updated[["sector2_best", "sector2_personal_best"]].to_numpy(),
        hovertemplate="Sector 2 <br>Lap %{x}<br>Time : %{y}<br>Personal best: %{customdata[1]}<br>Best : %{customdata[0]}<extra></extra>",
    )

    fig.add_bar(
        x=updated["lapnumber"],
        y=updated["sector3"],
        name="sector3",
        marker_color=updated["sector3_color"],
        customdata=updated[["sector3_best", "sector3_personal_best"]].to_numpy(),
        hovertemplate="Sector 3 <br>Lap %{x}<br>Time : %{y}<br>Personal best: %{customdata[1]}<br>Best : %{customdata[0]}<extra></extra>",
    )

    fig.update_layout(barmode="stack", showlegend=False)

    return fig