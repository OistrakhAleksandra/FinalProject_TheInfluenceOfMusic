import os
import re
import warnings

import numpy as np
import pandas as pd
from scipy.optimize import curve_fit
from scipy.signal import cheby2, filtfilt, find_peaks


def calculate_is(base_path, combined_data_file):
    """Calculate IS (Integration Score) and update the existing Excel file.

    Parameters:
        base_path (str): Path to the base folder containing "PPG_data" and "HBD_data".
        trial_combined_path (str): Path to the Excel file where results will be saved.
    """

    def gaussian(x, A, mu, sigma, b):
        """Gaussian function for curve fitting."""
        return A * np.exp(-((x - mu) ** 2) / (2 * sigma**2)) + b

    def filter_ppg(ppg_data):
        """Filter PPG data using a Chebyshev Type II filter."""
        fs = 1000  # Sampling frequency in Hz
        low_cutoff, high_cutoff = 0.5, 5  # Frequency range in Hz
        order = 4
        sos = cheby2(order, 20, [low_cutoff / (fs / 2), high_cutoff / (fs / 2)], btype="band", output="sos")
        return filtfilt(sos, np.zeros(sos.shape[1]), ppg_data)

    def process_hbd(hbd_file, participant_rri):
        """Process HBD data and calculate IS."""
        hbd_data = pd.read_csv(hbd_file)
        hbd_data["response"] = hbd_data["response"].map({"Sync": 1, "Async": 0})
        grouped = hbd_data.groupby("delay")["response"].mean()

        x, y = grouped.index.values, grouped.values

        # Check if data is valid
        if len(x) == 0 or len(y) == 0:
            print(f"Warning: No valid data in file {hbd_file}")
            return np.nan, np.nan

        # Adjust for heartbeat periodicity
        if not np.isnan(participant_rri):
            adjusted_x = np.concatenate([x, x + participant_rri])
            adjusted_y = np.tile(y, 2)
        else:
            adjusted_x, adjusted_y = x, y

        # Check for NaN or invalid values
        if np.any(np.isnan(adjusted_x)) or np.any(np.isnan(adjusted_y)):
            print(f"Warning: NaN values detected in file {hbd_file}")
            return np.nan, np.nan

        try:
            with warnings.catch_warnings():
                warnings.simplefilter("ignore")
                popt, _ = curve_fit(
                    gaussian,
                    adjusted_x,
                    adjusted_y,
                    p0=[max(adjusted_y), np.median(adjusted_x), np.std(adjusted_x), min(adjusted_y)],
                )
            A, sigma = popt[0], popt[2]
        except (RuntimeError, ValueError) as e:
            print(f"Warning: Curve fit failed for file {hbd_file}: {e}")
            A, sigma = np.nan, np.nan

        return A, sigma

    # Paths to data folders
    ppg_path = os.path.join(base_path, "PPG_data")
    hbd_path = os.path.join(base_path, "HBD_data")

    # Load existing Excel file
    if not os.path.exists(combined_data_file):
        print("File does not exist.")
        return
    df = pd.read_excel(combined_data_file)
    df["participant_id"] = df["participant_id"].astype(str)

    # Store results
    results = []

    # Iterate over HBD files
    for hbd_file in os.listdir(hbd_path):
        if hbd_file.endswith(".csv"):
            match = re.search(r"sub-(\d+)", hbd_file)
            if not match:
                print(f"Warning: Could not extract participant ID from {hbd_file}")
                continue

            participant_id = match.group(1).lstrip("0")
            hbd_full_path = os.path.join(hbd_path, hbd_file)
            ppg_file = os.path.join(ppg_path, f"{participant_id}.csv")

            # Process PPG data
            if os.path.exists(ppg_file):
                ppg_data = pd.read_csv(ppg_file)["PPG"].values
                ppg_filtered = filter_ppg(ppg_data)
                peaks, _ = find_peaks(ppg_filtered, distance=300)
                avg_rri = np.mean(np.diff(peaks)) / 1000 if len(peaks) > 1 else np.nan
            else:
                avg_rri = np.nan

            # Calculate IS
            A, sigma = process_hbd(hbd_full_path, avg_rri)
            results.append(
                {"participant_id": participant_id, "Amplitude (A)": A, "Variance (σ)": sigma, "Average RRI": avg_rri}
            )

    # Create results DataFrame and normalize IS values
    results_df = pd.DataFrame(results)
    if not results_df.empty:
        A_values = results_df["Amplitude (A)"].dropna()
        min_A, max_A = A_values.min(), A_values.max()
        results_df["Normalized IS"] = results_df["Amplitude (A)"].apply(
            lambda x: np.nan
            if x == min_A
            else (max(0, min((x - min_A) / (max_A - min_A), 1)) if pd.notna(x) else np.nan)
        )
    else:
        results_df["Normalized IS"] = np.nan

    # Merge results into original DataFrame
    df["IS"] = df["participant_id"].map(results_df.set_index("participant_id")["Normalized IS"].to_dict())

    # Save updated Excel file
    df.to_excel(combined_data_file, index=False)
    print("IS calculations have been added to the combined data file.")
