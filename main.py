"""This script is the main code with all the functions neede to filter the data.

It uses the combine_ppg_averages function to calculate PPG averages and the filter_to_new_excel function
to filter the trial data based on selected columns.
"""

# Import the functions
# from functions.clearing_data.ppg_combined import combine_ppg_averages
# from functions.clearing_data.trial_mean_values import calculate_average_rt
from functions.clearing_data.adding_ppg_to_trial_comb import match_ppg_data
from functions.clearing_data.is_from_ppg import process_ppg_and_trial_data_to_excel
from functions.clearing_data.trial_combined import filter_to_new_excel
from functions.data_analysis.ai_to_music_type import analyze_music_type_vs_IS

# Path to the folder with trial data
folder_path = r"C:\Users\Home\Desktop\Studies\Phyton\projects 2024-2025\Final_project\data\trial_data"
# Path to the folder with PPG file
input_folder = r"C:\Users\Home\Desktop\Studies\Phyton\projects 2024-2025\Final_project\data\PPG_data"
# Columns for combined_trial
selected_columns = ["session", "music_type", "valence_rating", "RT", "PPG_response_start"]
# Path to the final data folder
final_data_path = r"C:\Users\Home\Desktop\Studies\Phyton\projects 2024-2025\Final_project\data"
# Columns for PPG_combined data
needed_columns = ["valence_rating", "RT"]
# Path to the trial_combined
trial_combined_path = (
    r"C:\Users\Home\Desktop\Studies\Phyton\projects 2024-2025\Final_project\data\combined_data_trial.xlsx"
)

# Call the function from functions.py
filter_to_new_excel(folder_path, selected_columns, final_data_path)
# combine_ppg_averages(input_folder, final_data_path)
# calculate_average_rt(trial_combined_path, final_data_path)
match_ppg_data(trial_combined_path, input_folder)
process_ppg_and_trial_data_to_excel(input_folder, folder_path, trial_combined_path)
analyze_music_type_vs_IS(trial_combined_path)
