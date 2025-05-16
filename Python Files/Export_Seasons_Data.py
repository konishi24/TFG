import csv
from Extract_Player_Data import seasons_data

def export_seasons_data_to_csv(output_file):
    with open(output_file, mode='w', newline='') as file:
        writer = csv.writer(file)
        
        # Write the header
        headers = ['Season', 'Player', 'Chosen Fighter', 'Opponent', 'Odds', 'W_L', 'Fight Length', 'Result',
                   'Weight Class', 'Fight Location', 'M_F', 'Ref']
        writer.writerow(headers)
        
        for season, data in seasons_data.items():
            season_number = int(season.split()[-1])  # Extract number from "Season X"
            formatted_season = f"Season {season_number:02d}"  # Add "Season" prefix and leading zero
            for player, stats in data.items():
                max_length = max(len(stats[key]) for key in stats.keys())
                for i in range(max_length):
                    row = [formatted_season, player]
                    for key in headers[2:]:
                        value = stats.get(key, [''])[i] if i < len(stats.get(key, [])) else ''
                        row.append('' if value == "Not Applicable" else value)
                    writer.writerow(row)

if __name__ == "__main__":
    export_seasons_data_to_csv('Seasons_Data.csv')
