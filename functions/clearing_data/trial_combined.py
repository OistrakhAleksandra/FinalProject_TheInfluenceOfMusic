"""Import necessary libraries for file handling and data processing"""

import os
from pathlib import Path

import pandas as pd


# Function to convert CSV and Excel files to a single Excel file with selected columns
def filter_to_new_excel(trial_data_path: str, selected_columns: list[str], combined_data_file: str) -> None:
    # Create an empty DataFrame to store the combined data
    combined_data = pd.DataFrame()

    for index, file_name in enumerate(os.listdir(trial_data_path), start=1):  # Loop through all files in the folder
        # Check if the file is a CSV or Excel file
        if file_name.endswith((".csv", ".xlsx")):
            file_path = os.path.join(trial_data_path, file_name)

            # Read the data based on the file type
            if file_name.endswith(".csv"):
                data = pd.read_csv(file_path)
            elif file_name.endswith(".xlsx"):
                data = pd.read_excel(file_path)

            # Check if the file contains all the required columns
            if all(col in data.columns for col in selected_columns):
                # Select only the required columns
                data_filtered = data.loc[:, selected_columns].copy()  # Explicitly make a copy of the slice

                # Add a column to indicate the file number or file name
                data_filtered.loc[:, "participant_id"] = f"{index}"

                # Append the data to the combined DataFrame
                combined_data = pd.concat([combined_data, data_filtered], ignore_index=True)

            else:
                print(f"File {file_name} is missing one or more required columns: {selected_columns}")

    # Path to save the final combined Excel file
    output_path = Path(combined_data_file) / "combined_data_trial.xlsx"
    print("Data from trial_data folder is added to the final excel")

    # Remove all rows where there is at least one NaN (missing value) in any column
    df_cleaned = combined_data.dropna()  # dropna removes rows with NaN values

    # Save the cleaned data back to the same file
    df_cleaned.to_excel(output_path, index=False)

    selected_columns = ["session", "music_type", "valence_rating", "RT", "PPG_response_start"]
