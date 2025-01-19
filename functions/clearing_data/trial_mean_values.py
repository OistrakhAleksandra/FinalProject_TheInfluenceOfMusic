"""Import necessary libraries for file handling and data processing"""

from pathlib import Path

import pandas as pd


def calculate_average_rt(trial_combined_path: str, final_data_directory: str) -> None:
    """Calculates the average RT for each music type for each participant and saves it to the new Excel file.

    Parameters:
    - trial_combined_path (str): The path to the input Excel file.
    - final_data_directory (str): The path to the directory where the output Excel file will be saved.
    """
    # Validate the input file extension
    if not trial_combined_path.endswith(".xlsx"):
        error_message = "Input path must end with '.xlsx'."
        raise ValueError(error_message)

    # Ensure the output directory exists
    final_data_dir = Path(final_data_directory)
    if not final_data_dir.is_dir():
        error_message = f"The specified path is not a directory: {final_data_directory}"
        raise ValueError(error_message)

    # Read the input Excel file
    data = pd.read_excel(trial_combined_path)

    # Ensure column names are as expected
    required_columns = ["participant_id", "music_type", "RT"]
    if not all(col in data.columns for col in required_columns):
        error_message = f"The input file must contain the following columns: {required_columns}"
        raise ValueError(error_message)

    # Group by participant_id and music_type, calculate the mean RT
    avg_rt = data.groupby(["participant_id", "music_type"])["RT"].mean().reset_index()

    # Construct the full path for the output Excel file
    output_file_path = final_data_dir / "trial_mean_values.xlsx"

    # Save the resulting DataFrame to the output file
    avg_rt.to_excel(output_file_path, index=False, engine="openpyxl")
