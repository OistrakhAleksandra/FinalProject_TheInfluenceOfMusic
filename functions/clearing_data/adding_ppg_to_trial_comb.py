import os
import re
from pathlib import Path

import pandas as pd


def match_ppg_data(combined_data_file: str, PPG_data_path: str) -> None:
    """This function matches PPG data to the trial data by comparing participant IDs and session numbers.

    Args:
    combined_data_file (str): Path to the Excel file containing combined data.
    input_folder (str): Path to the folder containing the PPG CSV files.

    Raises:
    ValueError: If the required columns are not found in the trial data.
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

    # Get all filenames in the input folder
    available_files = os.listdir(PPG_data_path)

    # Compile a regular expression pattern to extract participant_id and session from file names
    pattern = re.compile(r"sub-(\d+)_sess(\d+)_PPG.csv")

    # Iterate over each row in the DataFrame
    for index, row in trial_data.iterrows():
        session = row["session"]
        participant_id = row["participant_id"]
        ppg_response_start = row["PPG_response_start"]

        # Try to find the matching file using the regular expression
        matched_file = None
        for file_name in available_files:
            match = pattern.search(file_name)
            if match:
                file_participant_id = int(match.group(1))  # Get participant id from file name
                file_session = int(match.group(2))  # Get session from file name

                # Check if the participant_id and session from the file match those in the row
                if file_participant_id == participant_id and file_session == session:
                    matched_file = file_name
                    break

        if matched_file:
            file_path = Path(PPG_data_path) / matched_file  # Using Path with '/' operator

            try:
                ppg_data = pd.read_csv(file_path)

                # Check if the 'time' and 'PPG' columns exist
                if "time" not in ppg_data.columns or "PPG" not in ppg_data.columns:
                    error_message = f"Required columns 'time' or 'PPG' missing in {matched_file}"
                    raise ValueError(error_message)

                # Find the row where the time is closest to the PPG_response_start value
                closest_time_row = ppg_data.iloc[(ppg_data["time"] - ppg_response_start).abs().argmin()]

                # Extract the PPG value corresponding to the closest time
                ppg_value = closest_time_row["PPG"]

                # Ensure PPG value is a number and within the expected range [-1, 1]
                try:
                    ppg_value = float(ppg_value)  # Try to convert to float
                    if -2 <= ppg_value <= 2:
                        trial_data.loc[index, "PPG_data"] = ppg_value  # Using .loc for assignment
                    else:
                        trial_data.loc[index, "PPG_data"] = None  # Set to None if outside range
                except (ValueError, TypeError):
                    print(f"Invalid PPG value {ppg_value} for {matched_file}. Deleting.")
                    trial_data.loc[index, "PPG_data"] = None  # Set to None if it's not a valid number

            except ValueError as e:
                print(f"Error: {e}")  # Print specific error message for missing columns
            except (FileNotFoundError, pd.errors.EmptyDataError) as e:
                print(f"Error reading file {matched_file}: {e!s}")
            except Exception as e:
                print(f"Unexpected error processing file {matched_file}: {e!s}")

        else:
            pass
    # Save the updated Excel file
    try:
        trial_data.to_excel(combined_data_file, index=False)
        print("PPG is added to the final excel")
    except PermissionError as e:
        print(f"Error saving the updated file due to permission issue: {e!s}")
    except Exception as e:
        print(f"Unexpected error saving the file: {e!s}")
