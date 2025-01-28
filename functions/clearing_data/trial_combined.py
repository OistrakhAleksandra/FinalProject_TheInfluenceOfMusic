import os
from pathlib import Path

import pandas as pd


def filter_to_new_excel(trial_data_path: str, selected_columns: list[str], combined_data_file: str) -> None:
    """Reads CSV and Excel files from a folder, extracts selected columns,
    and saves cleaned data to an Excel file without averaging valence ratings.

    Args:
        trial_data_path (str): Path to the folder containing trial data files.
        selected_columns (list[str]): List of column names to extract.
        combined_data_file (str): Path to save the final combined Excel file.
    """
    combined_data = pd.DataFrame()

    for index, file_name in enumerate(os.listdir(trial_data_path), start=1):
        if file_name.endswith((".csv", ".xlsx")):
            file_path = os.path.join(trial_data_path, file_name)

            if file_name.endswith(".csv"):
                data = pd.read_csv(file_path)
            elif file_name.endswith(".xlsx"):
                data = pd.read_excel(file_path)

            if all(col in data.columns for col in selected_columns):
                data_filtered = data.loc[:, selected_columns].copy()
                data_filtered["participant_id"] = index  # Add participant ID
                combined_data = pd.concat([combined_data, data_filtered], ignore_index=True)
            else:
                print(f"File {file_name} is missing one or more required columns: {selected_columns}")

    # Remove NaN values
    df_cleaned = combined_data.dropna()

    # Save final dataset
    output_path = Path(combined_data_file) / "combined_data_trial.xlsx"
    df_cleaned.to_excel(output_path, index=False)
    print(f"Final cleaned data saved to {output_path}.")
