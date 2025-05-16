import csv
from Extract_Player_Data import seasons_data

def american_to_decimal(american_odds):
    if american_odds == 0:
        return 1.0
    if american_odds > 0:
        return (american_odds / 100) + 1
    else:
        return (100 / abs(american_odds)) + 1

def decimal_to_american(decimal_odds):
    if decimal_odds <= 1:
        return 0
    if decimal_odds >= 2:
        return (decimal_odds - 1) * 100
    else:
        return -100 / (decimal_odds - 1)

def calculate_data(stats, count=0, season_odds=0, season_time=0.0):
    for odd in stats['Odds']:
        try:
            if odd != 'Not Applicable':
                count += 1
                odd_value = float(odd)
                season_odds += american_to_decimal(odd_value)
        except (ValueError, TypeError):
            continue
    
    for time in stats['Fight Length']:
        try:
            if time != 'Not Applicable':
                # Split the time string into minutes and seconds
                minutes, seconds = map(int, time.split(':'))
                # Convert to total seconds or minutes
                total_time = minutes + (seconds/60)  # This will give you time in minutes
                season_time += total_time
        except (ValueError, TypeError):
            continue
    return season_odds, season_time, count

def rank_data(data, season_rankings):
        for season in season_rankings:
        # Sort by odds in descending order (higher odds = better rank)
            if data == 'odds':
                season_rankings[season].sort(key=lambda x: x[data], reverse=True)
            elif data == 'time':
                season_rankings[season].sort(key=lambda x: x[data], reverse=False)
            # Add rank to each player
            for rank, player_data in enumerate(season_rankings[season], 1):
                player_data['rank' + data] = rank


def export_parlay_data_to_csv(output_file):
    # First, calculate all season odds and store them by season
    season_rankings = {}
    
    # Calculate season odds for all players
    for season, data in seasons_data.items():
        season_rankings[season] = []

        for player, stats in data.items():
            season_odds, season_time, count = calculate_data(stats)
            if 'Y' in stats['Redemption']:
                red = 'Y'
            else:
                red = 'N'
            #Average Odds Per Season
            if count != 0:
                season_odds = season_odds / count
                season_time = season_time / count
                season_rankings[season].append({
                    'player': player,
                    'odds': season_odds,
                    'time': season_time,
                    'redemption': red
                })

    rank_data('odds', season_rankings)
    rank_data('time', season_rankings)
    
    # Write to CSV
    with open(output_file, mode='w', newline='') as file:
        writer = csv.writer(file)
        headers = ['Seasons', 'Player', 'Season Odds', 'Season Odds Rank', 'Season Fight Length', 'Season Fight Length Rank', 'Redemption']
        writer.writerow(headers)

        # Write data with rankings
        for season in season_rankings:
            season_number = int(season.split()[-1])  # Extract number from "Season X"
            formatted_season = f"Season {season_number:02d}"  # Add "Season" prefix and leading zero
            for player_data in season_rankings[season]:
                row = [
                    formatted_season,  # Use formatted season number
                    player_data['player'],
                    f"{int(decimal_to_american(player_data['odds']))}",
                    player_data['rankodds'],
                    f"{int(player_data['time'])}",
                    player_data['ranktime'],
                    player_data['redemption']
                ]
                writer.writerow(row)

if __name__ == "__main__":
    export_parlay_data_to_csv('Season_Average_Data.csv')