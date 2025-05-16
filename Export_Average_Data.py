import csv
from Extract_Player_Data import seasons_data

def american_to_decimal(american_odds):
    if american_odds > 0:
        return (american_odds / 100) + 1
    else:
        return (100 / abs(american_odds)) + 1

def decimal_to_american(decimal_odds):
    if decimal_odds >= 2.0:
        return int((decimal_odds - 1) * 100)
    else:
        return int(-100 / (decimal_odds - 1))

def calculate_total_average_decimal_odds(seasons_data):
    total_decimal_odds = {}
    count_odds = {}

    for season, players in seasons_data.items():
        for player, data in players.items():
            odds_list = data.get('Odds', [])
            for odds in odds_list:
                try:
                    american_odds = int(odds)
                    decimal_odds = american_to_decimal(american_odds)
                    if player in total_decimal_odds:
                        total_decimal_odds[player] += decimal_odds
                        count_odds[player] += 1
                    else:
                        total_decimal_odds[player] = decimal_odds
                        count_odds[player] = 1
                except ValueError:
                    # Handle cases where odds are not integers
                    continue

    average_decimal_odds = {player: total_decimal_odds[player] / count_odds[player] for player in total_decimal_odds}
    return average_decimal_odds

def calculate_picks_per_season(seasons_data):
    total_wins = {}
    seasons_played = {}

    for season, players in seasons_data.items():
        for player, data in players.items():
            w_l_list = data.get('W_L', [])
            wins_this_season = sum(1 for result in w_l_list if result.upper() == 'W')
            
            if player in total_wins:
                total_wins[player] += wins_this_season
                seasons_played[player] += 1
            else:
                total_wins[player] = wins_this_season
                seasons_played[player] = 1

    # Calculate average wins per season
    average_wins = {
        player: total_wins[player] / seasons_played[player] 
        for player in total_wins
    }
    
    return average_wins

def calculate_na_picks_per_season(seasons_data):
    total_na = {}

    for season, players in seasons_data.items():
        for player, data in players.items():
            fighter_list = data.get('Chosen Fighter', [])
            
            # Count NAs from both Result and Chosen Fighter fields
            na_this_season = sum(1 for fighter in fighter_list if fighter == 'Not Applicable')
            
            if player in total_na:
                total_na[player] += na_this_season
            else:
                total_na[player] = na_this_season

    return total_na

def calculate_average_fight_length(seasons_data):
    total_time = {}
    fights_count = {}

    for season, players in seasons_data.items():
        for player, data in players.items():
            time_list = data.get('Fight Length', [])
            for time in time_list:
                if time != 'Not Applicable':
                    try:
                        # Convert time string (MM:SS) to seconds
                        total_seconds, excess = map(int, time.split(':'))                        
                        if player in total_time:
                            total_time[player] += total_seconds
                            fights_count[player] += 1
                        else:
                            total_time[player] = total_seconds
                            fights_count[player] = 1
                    except (ValueError, AttributeError):
                        continue

    # Calculate average time in seconds and convert back to MM:SS format
    average_time = {}
    for player in total_time:
        avg_seconds = total_time[player] / fights_count[player]
        minutes = int(avg_seconds // 60)
        seconds = int(avg_seconds % 60)
        average_time[player] = f"{minutes:02d}:{seconds:02d}"
    return average_time

def calculate_total_TFG_wins(seasons_data):
    TFG_win = {}

    for season, players in seasons_data.items():
        for player, data in players.items():
            w_l_list = data.get('Season Victory', [])
            TFG_win_this_season = sum(1 for result in w_l_list if result == 'Y')
            
            if player in TFG_win:
                TFG_win[player] += TFG_win_this_season
            else:
                TFG_win[player] = TFG_win_this_season

    return TFG_win

def export_total_data_to_csv(output_file):
    average_decimal_odds = calculate_total_average_decimal_odds(seasons_data)
    average_american_odds = {player: decimal_to_american(avg_decimal_odds) for player, avg_decimal_odds in average_decimal_odds.items()}
    average_picks_per_season = calculate_picks_per_season(seasons_data)
    total_na = calculate_na_picks_per_season(seasons_data)
    average_fight_time = calculate_average_fight_length(seasons_data)
    TFG_WINS = calculate_total_TFG_wins(seasons_data)
    average_picks_per_season = {player: round(avg, 1) for player, avg in average_picks_per_season.items()}

    # Sort players by their average American odds and picks
    sorted_players = sorted(average_american_odds.items(), key=lambda x: x[1], reverse=True)
    sorted_picks = sorted(average_picks_per_season.items(), key=lambda x: x[1], reverse=True)
    
    # Sort players by fight time (convert MM:SS to seconds for sorting)
    def time_to_seconds(time_str):
        try:
            minutes, seconds = map(int, time_str.split(':'))
            return minutes * 60 + seconds
        except:
            return 0
    
    
    # Create dictionaries for ranks
    sorted_times = sorted(average_fight_time.items(), key=lambda x: time_to_seconds(x[1]), reverse=False)
    picks_rank = {player: rank for rank, (player, _) in enumerate(sorted_picks, start=1)}
    time_rank = {player: rank for rank, (player, _) in enumerate(sorted_times, start=1)}

    with open(output_file, mode='w', newline='') as file:
        writer = csv.writer(file)
        headers = ['Player', 'Total Average Odds', 'Total Average Odds Rank', 
                  'Average Correct Picks', 'Average Correct Picks Rank', 
                  'Total NA Picks', 'Average Fight Time', 'Fight Time Rank', 
                  'Total TFG Wins']
        writer.writerow(headers)

        for odds_rank, (player, avg_american_odds) in enumerate(sorted_players, start=1):
            avg_picks = average_picks_per_season.get(player, 0)
            picks_ranking = picks_rank.get(player, '')
            na_count = total_na.get(player, 0)
            avg_time = average_fight_time.get(player, '00:00')
            time_ranking = time_rank.get(player, '')
            wins = TFG_WINS.get(player, 0)
            row = [player, avg_american_odds, odds_rank, avg_picks, 
                  picks_ranking, na_count, avg_time, time_ranking,
                  wins]
            writer.writerow(row)

if __name__ == "__main__":
    export_total_data_to_csv('Total_Average_Data.csv')