import os
import glob

# Specify the folder path
folder_path = r'C:\Users\kanta\OneDrive\Desktop\TFG'

# Use glob to match all CSV files in the folder
csv_files = glob.glob(os.path.join(folder_path, 'Fight Game*.csv'))

# Count the number of CSV files
num_csv_files = len(csv_files)

# print(f'There are {num_csv_files} CSV files in the folder.')
