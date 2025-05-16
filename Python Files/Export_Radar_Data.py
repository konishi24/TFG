import csv
from Extract_Player_Data import seasons_data

def get_total_average_odds():
    odds_dict = {}
    with open('Total_Average_Data.csv', mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            odds_dict[row['Player']] = float(row['Total Average Odds'])
    return odds_dict

def export_seasons_data_to_csv(output_file):
    # Get total average odds for each player
    total_avg_odds = get_total_average_odds()
    
    # Get unique players from all seasons
    all_players = set()
    for season in seasons_data.values():
        all_players.update(season.keys())

    with open(output_file, mode='w', newline='') as file:
        writer = csv.writer(file)
        headers = ['Player', 'Underdog', 'Heavy Favorite (-300)', 'Season Win', 'Picks Made', 'Seasons Played',  
                   'Finish Rate', 'Redemption', 'Longest Season', 'Odds']
        writer.writerow(headers)

        for player in all_players:
            total_picks = 0
            underdog_picks = 0
            heavy_fav_picks = 0
            total_odds = 0
            finishes = 0
            redemptions = 0
            longest_season = 0
            seasons_won = 0
            
            # Calculate stats across all seasons for this player
            for season_data in seasons_data.values():
                if player in season_data:
                    player_season = season_data[player]
                    
                    # Count picks and calculate odds-based stats
                    picks_this_season = len(player_season['Odds'])
                    total_picks += picks_this_season
                    longest_season = max(longest_season, picks_this_season)
                    
                    for odds in player_season['Odds']:
                        if "Not Applicable" in odds:
                            continue
                        if odds and float(odds) > 0:
                            underdog_picks += 1
                        if odds and float(odds) <= -300:
                            heavy_fav_picks += 1
                        if odds:
                            total_odds += float(odds)
                    
                    # Count finishes (KO/TKO or Submission)
                    finishes += sum(1 for x in player_season['Result'] 
                                  if 'TKO' in x or 'Sub' in x)
                    
                    # Count redemptions
                    redemptions += sum(1 for x in player_season['Redemption'] 
                                     if x == 'Y')
                    
                    # Check for season victory
                    if 'Y' in player_season['Season Victory']:
                        seasons_won += 1

            seasons_played = len([s for s in seasons_data.values() if player in s])
            
            # Calculate final stats
            stats = [
                player,
                round(underdog_picks, 2) if total_picks > 0 else 0,
                round(heavy_fav_picks, 2) if total_picks > 0 else 0,
                round(seasons_won, 2) if seasons_played > 0 else 0,
                total_picks,
                seasons_played,
                round(finishes, 2) if total_picks > 0 else 0,
                round(redemptions, 2) if seasons_played > 0 else 0,
                longest_season,
                total_avg_odds.get(player, 0)  # Get total average odds from CSV
            ]
            
            writer.writerow(stats)

if __name__ == "__main__":
    export_seasons_data_to_csv('Radar_Data.csv')
