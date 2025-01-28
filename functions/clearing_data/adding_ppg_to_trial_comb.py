import os
import re
from pathlib import Path

import pandas as pd


def match_ppg_data(combined_data_file: str, PPG_data_path: str) -> None:
    """Matches PPG data to the trial data by comparing participant IDs and session numbers.

    Args:
        combined_data_file (str): Path to the Excel file containing combined data.
        PPG_data_path (str): Path to the folder containing the PPG CSV files.

    Returns:
        None
    """
    # Load the data from the Excel file
    trial_data = pd.read_excel(combined_data_file)

    # Check if required columns exist in the DataFrame
    required_columns = ["session", "participant_id", "PPG_response_start"]
    missing_columns = [col for col in required_columns if col not in trial_data.columns]
    if missing_columns:
        raise ValueError(f"Missing required columns: {', '.join(missing_columns)}")

    # Create a new column for PPG values
    trial_data["PPG_data"] = None

    # Pre-index available files by participant_id and session for faster lookup
    file_index = {}
    for file_name in os.listdir(PPG_data_path):
        match = re.match(r"sub-(\d+)_sess(\d+)_PPG.csv", file_name)
        if match:
            file_participant_id = int(match.group(1))
            file_session = int(match.group(2))
            file_index[(file_participant_id, file_session)] = file_name

    # Iterate over each row in the DataFrame
    for index, row in trial_data.iterrows():
        session = row["session"]
        participant_id = row["participant_id"]
        ppg_response_start = row["PPG_response_start"]

        # Check if the corresponding PPG file exists
        matched_file = file_index.get((participant_id, session))
        if matched_file:
            file_path = Path(PPG_data_path) / matched_file

            try:
                ppg_data = pd.read_csv(file_path)

                # Check if the 'time' and 'PPG' columns exist
                if "time" not in ppg_data.columns or "PPG" not in ppg_data.columns:
                    print(f"Required columns 'time' or 'PPG' missing in {matched_file}")
                    continue

                # Find the row where the time is closest to the PPG_response_start value
                closest_time_row = ppg_data.iloc[(ppg_data["time"] - ppg_response_start).abs().argmin()]

                # Extract the PPG value corresponding to the closest time
                ppg_value = closest_time_row["PPG"]

                # Ensure PPG value is numeric
                try:
                    ppg_value = float(ppg_value)
                    trial_data.loc[index, "PPG_data"] = ppg_value
                except ValueError:
                    print(f"Invalid PPG value {ppg_value} in {matched_file}. Skipping row.")
            except Exception as e:
                print(f"Error processing file {matched_file}: {e}")

    # Save the updated Excel file
    trial_data.to_excel(combined_data_file, index=False)
    print("PPG is added to the final excel.")
