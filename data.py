import pandas as pd
from glob import glob

drivers_map = {
    'VER': ('Max Verstappen', 'Red Bull'),
    'GAS': ('Pierre Gasly', 'Alpine'),
    'PER': ('Sergio Perez', 'Red Bull'),
    'ALO': ('Fernando Alonso', 'Aston Martin'),
    'LEC': ('Charles Leclerc', 'Ferrari'),
    'STR': ('Lance Stroll', 'Aston Martin'),
    'MAG': ('Kevin Magnussen', 'Haas'),
    'TSU': ('Yuki Tsunoda', 'Racing Bulls'),
    'ALB': ('Alexander Albon', 'Williams'),
    'ZHO': ('Zhou Guanyu', 'Kick Sauber'),
    'HUL': ('Nico Hulkenberg', 'Haas'),
    'LAW': ('Liam Lawson', 'Racing Bulls'),
    'NOR': ('Lando Norris', 'McLaren'),
    'COL': ('Franco Colapinto', 'Williams'),
    'HAM': ('Lewis Hamilton', 'Mercedes'),
    'SAI': ('Carlos Sainz', 'Ferrari'),
    'DOO': ('Jack Doohan', 'Alpine'),
    'RUS': ('George Russel', 'Mercedes'),
    'BOT': ('Valtteri Bottas', 'Kick Sauber'),
    'PIA': ('Oscar Piastri', 'McLaren'),
    'OCO': ('Esteban Ocon', 'Alpine'),
    'RIC': ('Daniel Ricciardo', 'Racing Bulls'),
    'SAR': ('Logan Sargeant', 'Williams'),
    'BEA': ('Oliver Bearman', 'Haas')
}

teams_list = []
drivers_list = []
for prefix, info in drivers_map.items():
    if info[1] not in teams_list:
        teams_list.append(info[1])
    if info[0] not in drivers_list:
        drivers_list.append(info[0])


f1_data = (
    pd.concat(
        ((pd.read_csv(x)
        .assign(
            track=x.split('/')[1].split('2')[0].replace('_', ' ')
        ) for x in glob('data/*.csv'))),
        ignore_index=True, )
    .rename(columns=str.lower)
    .rename(
        columns={
            'sector1time': 'sector1',
            'sector2time': 'sector2',
            'sector3time': 'sector3',
        }
    )
    .query('laptime < 500 or laptime.isna()')
    .assign(
        full_name=lambda df: df['driver'].apply(lambda x: drivers_map[x][0]),
        team=lambda df: df['driver'].apply(lambda x: drivers_map[x][1]),
    )
)

track_list = f1_data['track'].unique().tolist()