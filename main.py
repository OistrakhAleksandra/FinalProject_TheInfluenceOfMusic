# Import the functions
from .functions.clearing_data.ppg_combined import combine_ppg_averages
from .functions.clearing_data.trial_combined import filter_to_new_excel

# Define folder path and selected columns
folder_path = r"C:\Users\Home\Desktop\Studies\Phyton\projects 2024-2025\Project_2\data\trial_data"
input_folder = r"C:\Users\Home\Desktop\Studies\Phyton\projects 2024-2025\Project_2\data\PPG_data"  # Path to the folder with PPG files
selected_columns = ["session", "music_type", "valence_rating", "RT"]  # Specify the columns you need
final_data_path = r"C:\Users\Home\Desktop\Studies\Phyton\projects 2024-2025\Project_2\data"
combined_data_path = r"C:\Users\Home\Desktop\Studies\Phyton\projects 2024-2025\Project_2\data\combined_data.xlsx"
needed_columns = ["valence_rating", "RT"]

# Call the function from functions.py
filter_to_new_excel(folder_path, selected_columns, final_data_path)
combine_ppg_averages(input_folder, final_data_path)
