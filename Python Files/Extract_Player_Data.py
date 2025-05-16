import pandas as pd
from pprint import pprint
from CSV_Counter import num_csv_files

keys = ['Chosen Fighter', 'Opponent', 'Odds', 'W_L', 'Result', 'Fight Length',
        'Weight Class', 'Fight Location', 'M_F', 'Ref', 'Season Victory']
parlay_keys = ['Parlay Result', 'Redemption']

player_data = {}

seasons_data = {}

def set_up_keys(player):
    """
    Initialize the keys for a new player in the player_data dictionary.
    
    Args:
        player (str): The name of the player.
    """
    for key in keys:
        player_data[player][key] = []
    for p_key in parlay_keys:
        player_data[player][p_key] = []

def parlay_data(data, player):
    """
    Add parlay data to the player_data dictionary for a given player.
    
    Args:
        data (pd.Series): The data row containing parlay information.
        player (str): The name of the player.
    """
    if player in player_data:
        for index, item in enumerate(data):
            if index in [8, 9]:
                player_data[player][parlay_keys[index-8]].append(data.iloc[index])


def add_data(data, player):
    """
    Add fight data to the player_data dictionary for a given player.
    
    Args:
        data (pd.Series): The data row containing fight information.
        player (str): The name of the player.
    """
    for key in keys:
        # if key == 'Fight Length' and data[key] == '25;00':
        #     player_data[player][key].append('25:00')
        #     continue

        # if key == 'FOTN' or key == 'Streak':
        #     player_data[player][key].append(int(data[key]))
        #     continue

        if key == 'Season Victory': continue

        player_data[player][key].append(data[key])

def season_V(player):
    """
    Mark a player as having a season victory.
    
    Args:
        player (str): The name of the player.
    """
    player_data[player]['Season Victory'].append('Y')

def ufc300(data, player):
    """
    Add UFC 300 data to the player_data dictionary for a given player.
    
    Args:
        data (pd.Series): The data row containing UFC 300 information.
        player (str): The name of the player.
    """
    if player in player_data:
        for index, item in enumerate(data):
            if index in [19,20]:
                player_data[player][parlay_keys[index-19]].append(data.iloc[index])

def nested_dict(file_path):
    """
    Populate the player_data dictionary with data from a CSV file.
    
    Args:
        file_path (str): The path to the CSV file.
    """
    global player_data
    df = pd.read_csv(file_path)

    for index, row in df.iterrows():
        player = row['Player']

        if player == 'Parlay':
            continue 
        
        if row.iloc[12] == 'Y':
            season_V(player)
            continue

        if row.iloc[0] == 'UFC 300':
            ufc300(row, player)
            continue

        #checks if the row contains parlay data
        if "/" in row.iloc[8]:
            parlay_data(row, player)
            continue

        if player not in player_data:
            player_data[player] = {}
            set_up_keys(player)

        if player in player_data:
            add_data(row, player)


while True:
    season_number = input('Enter the season number(s): ').strip().split()

    if not season_number:
        break

    if "0" in season_number:
        for i in range(num_csv_files):
            file_path = 'Fight Game - Selected per Season - Season ' + str(i+1) + '.csv'
            print(file_path)
            nested_dict(file_path)
            seasons_data['Season ' + str(i+1)] = player_data
            player_data = {}
    else:
        for season in season_number:
            file_path = 'Fight Game - Selected per Season - Season ' + season + '.csv'
            print(file_path)
            nested_dict(file_path)
            seasons_data['Season ' + season] = player_data
            player_data = {}


# pprint(seasons_data)