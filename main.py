"""This script is the main code with all the functions neede to filter the data.

It uses the combine_ppg_averages function to calculate PPG averages and the filter_to_new_excel function
to filter the trial data based on selected columns.
"""

# Import the functions
from functions.clearing_data.ppg_combined import combine_ppg_averages
from functions.clearing_data.trial_combined import filter_to_new_excel

# Path to the folder with trial data
folder_path = r"C:\Users\Home\Desktop\Studies\Phyton\projects 2024-2025\Project_2\data\trial_data"
# Path to the folder with PPG file
input_folder = r"C:\Users\Home\Desktop\Studies\Phyton\projects 2024-2025\Project_2\data\PPG_data"
# Columns for combined_trial
selected_columns = ["session", "music_type", "valence_rating", "RT"]
# Path to the final data folder
final_data_path = r"C:\Users\Home\Desktop\Studies\Phyton\projects 2024-2025\Project_2\data"
# Columns for PPG_combined data
needed_columns = ["valence_rating", "RT"]

# Call the function from functions.py
filter_to_new_excel(folder_path, selected_columns, final_data_path)
combine_ppg_averages(input_folder, final_data_path)
