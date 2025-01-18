import os
from pathlib import Path

import pandas as pd


def combine_ppg_averages(input_folder: str, final_data_path: str) -> None:
    # Create an empty list to store data for all files
    combined_data_list = []

    # Iterate through all files in the folder
    for file_name in os.listdir(input_folder):
        # Check if the file is a CSV or Excel file and contains "_PPG" in its name
        if file_name.endswith((".csv", ".xlsx")) and "_PPG" in file_name:
            # Extract participant_id and session from the file name
            try:
                participant_id = file_name.split("_")[0].replace("sub-", "")
                session = file_name.split("_")[1].replace("sess", "")
            except IndexError:
                continue  # Skip files with invalid naming format

            # Read the data from the file
            file_path = os.path.join(input_folder, file_name)  # Fixed file path assignment
            if file_name.endswith(".csv"):
                df = pd.read_csv(file_path)
            elif file_name.endswith(".xlsx"):
                df = pd.read_excel(file_path)

            # Check if the "PPG" column exists in the file
            if "PPG" not in df.columns:
                continue  # Skip files without "PPG" column

            # Calculate the average of the "PPG" column
            average_ppg = df["PPG"].mean()

            # Append the participant_id, session, and average_PPG to the list
            combined_data_list.append(
                {"participant_id": participant_id, "session": session, "average_PPG": average_ppg}
            )

    # Check if any data was added to the combined data list
    if not combined_data_list:
        print("No valid data found.")
        return  # If no valid data was found, exit the function

    # Create a DataFrame from the combined data list
    combined_data = pd.DataFrame(combined_data_list)

    # Save the combined data to an Excel file
    output_path = Path(final_data_path) / "combined_PPG_averages.xlsx"
    combined_data.to_excel(output_path, index=False)
