import os

import numpy as np
import pandas as pd
from scipy.optimize import curve_fit


def calculate_is(HBD_data_path, combined_data_file):
    """Calculates Interoceptive Sensitivity (IS) for each participant using the Heartbeat Discrimination Test data
    and updates the combined Excel file.

    Args:
        HBD_data_path (str): Path to the folder containing Heartbeat Discrimination Test CSV files.
        combined_data_file (str): Path to the combined Excel file to update.
    """

    def gaussian(x, A, mu, sigma, b):
        """Gaussian function for curve fitting."""
        return A * np.exp(-((x - mu) ** 2) / (2 * sigma**2)) + b

    # Load combined data
    combined_data = pd.read_excel(combined_data_file)

    # List all HBD files
    hbd_files = [file for file in os.listdir(HBD_data_path) if file.endswith(".csv")]

    for file in hbd_files:
        print(f"Processing file: {file}")

        # Extract participant ID from file name
        try:
            participant_id = int(file.split("_")[0].split("-")[1])
        except ValueError:
            print(f"Could not extract participant ID from file name: {file}. Skipping.")
            continue

        # Load HBD data
        hbd_data = pd.read_csv(os.path.join(HBD_data_path, file))

        # Extract resting RRI
        resting_rri = hbd_data["resting_RRI"].dropna().iloc[0] if not hbd_data["resting_RRI"].isna().all() else None
        if resting_rri is None or resting_rri <= 0:
            print(f"Invalid or missing resting RRI for participant {participant_id}. Skipping.")
            continue

        # Convert resting RRI to milliseconds
        resting_rri_ms = resting_rri * 1000
        hbd_data["response"] = hbd_data["response"].map({"Sync": 1, "Async": 0})

        if hbd_data["response"].isnull().any():
            print(f"Invalid responses for participant {participant_id}. Skipping.")
            continue

        # Calculate normalized delays
        hbd_data["normalized_delay"] = hbd_data["delay"] / resting_rri_ms

        # Calculate sync ratios for each normalized delay
        normalized_delays = hbd_data["normalized_delay"].unique()
        sync_ratios = [
            hbd_data[hbd_data["normalized_delay"] == delay]["response"].mean() for delay in normalized_delays
        ]

        print(f"Normalized delays for participant {participant_id}: {normalized_delays}")
        print(f"Sync ratios for participant {participant_id}: {sync_ratios}")

        # Skip if no valid sync_ratios or all values are identical
        if not sync_ratios or len(set(sync_ratios)) == 1:
            print(f"No valid or varying sync_ratios for participant {participant_id}. Skipping.")
            combined_data.loc[combined_data["participant_id"] == participant_id, "IS"] = np.nan
            continue

        # Fit Gaussian function to calculate IS
        try:
            bounds = ([0, 0, 0, -1], [1, 1, 1, 1])
            popt, _ = curve_fit(
                gaussian, normalized_delays[: len(sync_ratios)], sync_ratios, p0=[0.5, 0.5, 0.1, 0], bounds=bounds
            )
            A, mu, sigma, b = popt
            IS_value = 1 - A if 0 < A < 1 else np.nan
            print(f"Calculated IS for participant {participant_id}: {IS_value}")
        except RuntimeError:
            IS_value = np.nan
            print(f"Gaussian fitting failed for participant {participant_id}. Setting IS to NaN.")

        # Update IS value in the combined data
        combined_data.loc[combined_data["participant_id"] == participant_id, "IS"] = IS_value

    # Save updated combined data
    combined_data.to_excel(combined_data_file, index=False)
    print(f"Calculation complete. IS values have been added to {combined_data_file}.")
