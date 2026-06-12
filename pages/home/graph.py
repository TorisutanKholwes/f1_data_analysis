from app import app
from data import f1_data
from dash import Input, Output

import plotly.express as px

@app.callback(
    Output("most-wins-title", "children"),
    Output("most-wins-subtitle", "children"),
    Output("most-wins-text", "children"),
)
def update_text():
    df = (
        f1_data
        .sort_values(['track', 'driver', 'lapnumber'])
        .groupby(['track', 'driver'], as_index=False)
        .tail(1)
    )

    wins = df[df['position'] == 1]

    wins_by_driver = (
        wins.groupby("full_name")
        .size()
        .reset_index(name="victories")
        .sort_values("victories", ascending=False)
    )

    best_driver = wins_by_driver.iloc[0]

    tracks = wins.query(f'full_name=="{best_driver["full_name"]}"')["track"].values

    return best_driver["full_name"], f"{best_driver["victories"]} victories", "Tracks: " + ", ".join(tracks)

@app.callback(
    Output("victory-drivers", "figure"),
)
def update_graph():
    df = (
        f1_data
        .sort_values(['track', 'driver', 'lapnumber'])
        .groupby(['track', 'driver'], as_index=False)
        .tail(1)
    )

    wins = df[df['position'] == 1]

    wins_by_driver = (
        wins.groupby("full_name")
        .size()
        .reset_index(name="victories")
        .sort_values("victories", ascending=False)
    )

    fig = px.bar(
        wins_by_driver,
        x="full_name",
        y="victories",
        labels={
            "victories": "Wins",
            "full_name": "Driver"
        }
    )

    return fig

@app.callback(
    Output("fastest-track-title", "children"),
    Output("fastest-track-subtitle", "children"),
    Output("fastest-track-text", "children"),
)
def update_text():
    df = (
        f1_data
        .sort_values(['track', 'driver', 'lapnumber'])
        .groupby(['track', 'driver'], as_index=False)
        .tail(1)
    )

    idx = f1_data.groupby("track")["maxspeed"].idxmax()
    fastest_by_track = f1_data.loc[idx, ["track", "full_name", "maxspeed", "lapnumber"]].sort_values("maxspeed", ascending=False)

    result = fastest_by_track.iloc[0]

    track_name = result["track"]
    max_speed = result["maxspeed"]
    driver_name = result["full_name"]
    lap_number = result["lapnumber"]

    return track_name, f"Max speed is {max_speed} km/h", f"Achieved by {driver_name} on lap {int(lap_number)}"

@app.callback(
    Output("fatest-laps", "figure"),
)
def update_graph():
    df = (
        f1_data
        .sort_values(['track', 'driver', 'lapnumber'])
        .groupby(['track', 'driver'], as_index=False)
        .tail(1)
    )

    idx = f1_data.groupby("track")["maxspeed"].idxmax()
    fastest_by_track = f1_data.loc[idx, ["track", "full_name", "maxspeed"]]

    fig = px.bar(
        fastest_by_track,
        x="track",
        y="maxspeed",
        labels={
            "maxspeed": "Speed (in km/h)",
            "track": "Track",
        },
        custom_data=["full_name"],
    )

    fig.update_traces(
        hovertemplate="Track : %{x}<br>Speed : %{y} km/h<br>Achieved by %{customdata[0]}<extra></extra>",
    )

    return fig