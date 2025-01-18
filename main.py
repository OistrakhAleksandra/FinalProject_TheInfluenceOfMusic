from data_filter import filter_to_new_excel  # Import the function

# Define folder path and selected columns
folder_path = r"C:\Users\Home\Desktop\Studies\Phyton\projects 2024-2025\Project_2\data\trial_data"
selected_columns = ["session", "music_type", "valence_rating", "RT"]  # Specify the columns you need
final_folder_path = r"C:\Users\Home\Desktop\Studies\Phyton\projects 2024-2025\Project_2\data"

# Call the function from functions.py
filter_to_new_excel(folder_path, selected_columns, final_folder_path)
