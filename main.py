"""This script is the main code with all the functions neede to filter the data.

It uses the combine_ppg_averages function to calculate PPG averages and the filter_to_new_excel function
to filter the trial data based on selected columns.
"""

# Import the functions
from functions.clearing_data.adding_ppg_to_trial_comb import match_ppg_data
from functions.clearing_data.calc_r_peaks_from_ppg import process_ppg_folder
from functions.clearing_data.is_to_excel import calculate_is
from functions.clearing_data.trial_combined import filter_to_new_excel
from functions.data_analysis.Average_valence_scrore_to_IS import analyze_valence_vs_IS
from functions.data_analysis.HB_by_music_type import plot_hr_by_music_type
from functions.data_analysis.is_to_music_type import analyze_music_type_vs_IS
from functions.data_analysis.music_type_to_rt import analyze_rt_by_music_type
from functions.data_analysis.valence_rating_by_music_type import plot_valence_by_music_type

# Path to the final data folder
final_data_path = r"C:\Users\Home\Desktop\Studies\Phyton\projects 2024-2025\Final_project\data"
# Path to the folder with trial data
trial_data_path = r"C:\Users\Home\Desktop\Studies\Phyton\projects 2024-2025\Final_project\data\trial_data"
# Path to the folder with PPG files
PPG_data_path = r"C:\Users\Home\Desktop\Studies\Phyton\projects 2024-2025\Final_project\data\PPG_data"
# Path to the folder with HBD data
HBD_data_path = r"C:\Users\Home\Desktop\Studies\Phyton\projects 2024-2025\Final_project\data\HBD_data"
# Path to R-peaks data
R_peak_data_path = r"C:\Users\Home\Desktop\Studies\Phyton\projects 2024-2025\Final_project\data\R-peaks.xlsx"
# Path to the trial_combined
combined_data_file = (
    r"C:\Users\Home\Desktop\Studies\Phyton\projects 2024-2025\Final_project\data\combined_data_trial.xlsx"
)
selected_columns = ["session", "music_type", "valence_rating", "RT", "PPG_music_start", "PPG_response_start"]


# Call the clearing and calculating data functions
filter_to_new_excel(trial_data_path, selected_columns, final_data_path)
match_ppg_data(combined_data_file, PPG_data_path)
process_ppg_folder(PPG_data_path, final_data_path)
calculate_is(HBD_data_path, combined_data_file)

# Call the analyzing functions
plot_valence_by_music_type(combined_data_file)
plot_hr_by_music_type(R_peak_data_path, combined_data_file)
analyze_music_type_vs_IS(combined_data_file)
analyze_rt_by_music_type(combined_data_file)
analyze_valence_vs_IS(combined_data_file)
