"""This script is the main code with all the functions neede to filter the data.

It uses the combine_ppg_averages function to calculate PPG averages and the filter_to_new_excel function
to filter the trial data based on selected columns.
"""

# Import the functions for clearing data
from functions.clearing_data.adding_ppg_to_trial_comb import match_ppg_data
from functions.clearing_data.is_to_excel import calculate_is
from functions.clearing_data.trial_combined import filter_to_new_excel

# Import the functions for data analyze


# Path to data folder
base_path = r"C:\Users\Home\Desktop\Studies\Phyton\projects 2024-2025\Final_project\data"
# Path to the folder with trial data
trial_data_path = r"C:\Users\Home\Desktop\Studies\Phyton\projects 2024-2025\Final_project\data\trial_data"
# Path to the folder with PPG file
PPG_data_path = r"C:\Users\Home\Desktop\Studies\Phyton\projects 2024-2025\Final_project\data\PPG_data"
# Path to the final data folder
final_data_path = r"C:\Users\Home\Desktop\Studies\Phyton\projects 2024-2025\Final_project\data"
# Path to the trial_combined
combined_data_file = (
    r"C:\Users\Home\Desktop\Studies\Phyton\projects 2024-2025\Final_project\data\combined_data_trial.xlsx"
)
selected_columns = ["session", "music_type", "valence_rating", "RT", "PPG_response_start"]


# Call the function from functions.py
filter_to_new_excel(trial_data_path, selected_columns, final_data_path)
match_ppg_data(combined_data_file, PPG_data_path)
calculate_is(base_path, combined_data_file)  # analyze_music_type_vs_IS(trial_combined_path)
