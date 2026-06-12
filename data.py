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

circuits_coords = {
    'Abu Dhabi': {'lat': 24.4539, 'lon': 54.3530, 'link': 'https://en.wikipedia.org/wiki/Yas_Marina_Circuit'},
    'Austin': {'lat': 30.1328, 'lon': -97.6411, 'link': 'https://en.wikipedia.org/wiki/Circuit_of_the_Americas'},
    'Australia': {'lat': -37.8150, 'lon': 144.9680, 'link': 'https://en.wikipedia.org/wiki/Albert_Park_Circuit'},
    'Austria': {'lat': 47.2127, 'lon': 14.7675, 'link': 'https://en.wikipedia.org/wiki/Red_Bull_Ring'},
    'Azerbaijan': {'lat': 40.3769, 'lon': 49.8671, 'link': 'https://en.wikipedia.org/wiki/Baku_City_Circuit'},
    'Barhain': {'lat': 26.1351, 'lon': 50.5108, 'link': 'https://en.wikipedia.org/wiki/Bahrain_International_Circuit'},
    'Belgium': {'lat': 50.4372, 'lon': 5.9714, 'link': 'https://en.wikipedia.org/wiki/Circuit_de_Spa-Francorchamps'},
    'Brazil': {'lat': -23.5505, 'lon': -46.2361, 'link': 'https://en.wikipedia.org/wiki/Interlagos'},
    'Canada': {'lat': 45.5017, 'lon': -73.5673, 'link': 'https://en.wikipedia.org/wiki/Gilles_Villeneuve_Circuit'},
    'China': {'lat': 31.3989, 'lon': 121.4565, 'link': 'https://en.wikipedia.org/wiki/Shanghai_International_Circuit'},
    'Emilia Romagna': {'lat': 44.3519, 'lon': 12.0412, 'link': 'https://en.wikipedia.org/wiki/Autodromo_Enzo_e_Dino_Ferrari'},
    'Great Britain': {'lat': 51.8042, 'lon': -0.3370, 'link': 'https://en.wikipedia.org/wiki/Silverstone_Circuit'},
    'Hungary': {'lat': 47.5811, 'lon': 19.2486, 'link': 'https://en.wikipedia.org/wiki/Hungaroring'},
    'Italy': {'lat': 45.6205, 'lon': 8.5874, 'link': 'https://en.wikipedia.org/wiki/Autodromo_Nazionale_Monza'},
    'Japan': {'lat': 34.8431, 'lon': 135.7662, 'link': 'https://en.wikipedia.org/wiki/Suzuka_International_Racing_Course'},
    'Las Vegas': {'lat': 36.2744, 'lon': -115.1769, 'link': 'https://en.wikipedia.org/wiki/Las_Vegas_Grand_Prix'},
    'Mexico': {'lat': 19.4042, 'lon': -99.0955, 'link': 'https://en.wikipedia.org/wiki/Mexico_City_Grand_Prix'},
    'Miami': {'lat': 25.9506, 'lon': -80.2389, 'link': 'https://en.wikipedia.org/wiki/Miami_Grand_Prix'},
    'Monaco': {'lat': 43.7384, 'lon': 7.4246, 'link': 'https://en.wikipedia.org/wiki/Monaco_Grand_Prix'},
    'Netherland': {'lat': 52.3888, 'lon': 4.5411, 'link': 'https://en.wikipedia.org/wiki/Zandvoort_Circuit'},
    'Qatar': {'lat': 25.3548, 'lon': 51.4544, 'link': 'https://en.wikipedia.org/wiki/Lusail_International_Circuit'},
    'Saudi Arabia': {'lat': 26.4159, 'lon': 50.0877, 'link': 'https://en.wikipedia.org/wiki/Jeddah_Corniche_Circuit'},
    'Singapore': {'lat': 1.2914, 'lon': 103.8622, 'link': 'https://en.wikipedia.org/wiki/Marina_Bay_Street_Circuit'},
    'Spain': {'lat': 41.5699, 'lon': 1.8951, 'link': 'https://en.wikipedia.org/wiki/Circuit_de_Barcelona-Catalunya'},
}

tracks_coord = pd.DataFrame(circuits_coords).T.reset_index(names='track')

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