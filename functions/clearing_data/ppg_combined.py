"""Import necessary libraries for file handling and data processing"""

import logging
import os
from pathlib import Path

import pandas as pd

# Set up logging configuration
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")


def combine_ppg_averages(input_folder: str, final_data_path: str) -> None:
    """This function combines the PPG data and calculates the averages for each participant.

    Parameters:
    - input_folder (str): Path to the folder containing PPG data files.
    - final_data_path (str): Path to save the combined data as an Excel file.
    """
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
            file_path = Path(input_folder) / file_name  # Corrected the path creation
            if file_name.endswith(".csv"):
                ppg_data = pd.read_csv(file_path)
            elif file_name.endswith(".xlsx"):
                ppg_data = pd.read_excel(file_path)

            # Check if the "PPG" column exists in the file
            if "PPG" not in ppg_data.columns:
                continue  # Skip files without "PPG" column

            # Calculate the average of the "PPG" column
            average_ppg = ppg_data["PPG"].mean()

            # Append the participant_id, session, and average_PPG to the list
            combined_data_list.append(
                {"participant_id": participant_id, "session": session, "average_PPG": average_ppg}
            )

    # Check if any data was added to the combined data list
    if not combined_data_list:
        logging.warning("No valid data found.")
        return  # If no valid data was found, exit the function

    # Create a DataFrame from the combined data list
    combined_data = pd.DataFrame(combined_data_list)

    # Calculate the overall average for each participant
    overall_averages = combined_data.groupby("participant_id")["average_PPG"].mean().reset_index()
    overall_averages = overall_averages.rename(columns={"average_PPG": "overall_average_PPG"})

    # Merge the overall averages with the original data using the DataFrame method
    combined_data = combined_data.merge(overall_averages, on="participant_id", how="left")

    # Set overall_average_PPG to NaN for all sessions except the first session of each participant
    combined_data["overall_average_PPG"] = combined_data.groupby("participant_id")["overall_average_PPG"].transform(
        lambda x: x.where(x.index == x.index.min(), None)
    )

    # Save the combined data to an Excel file
    output_path = Path(final_data_path) / "combined_PPG_averages.xlsx"
    combined_data.to_excel(output_path, index=False)
