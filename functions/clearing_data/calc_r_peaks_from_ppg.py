import os
import re
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.signal import cheby2, find_peaks, sosfiltfilt


def process_ppg_folder(PPG_data_path: str, final_data_path: str) -> None:
    """Processes all PPG files in the specified folder, extracts R-peaks, calculates HR,
    and saves the results in a single Excel file.

    Args:
        PPG_data_path (str): Path to the folder containing PPG files.
        final_data_path (str): Path to save the resulting Excel file with R-peaks and HR.
    """
    all_results = []

    def rpeaks_from_ppg(ppg_signal, sample_rate):
        """Extracts R-peaks from a PPG signal."""
        filter_range = [0.5, 5]
        sos = cheby2(4, 20, filter_range, btype="bandpass", fs=sample_rate, output="sos")
        filtered_data = sosfiltfilt(sos, ppg_signal)

        prominence_threshold = max(filtered_data) * 0.15
        min_distance = int(sample_rate * 0.6)

        r_peaks, _ = find_peaks(filtered_data, prominence=prominence_threshold, distance=min_distance)
        return r_peaks

    def calculate_hr(r_peaks, sample_rate):
        """Calculates Heart Rate (HR) from R-peaks."""
        rr_intervals = np.diff(r_peaks) / sample_rate
        valid_rr_intervals = [rr for rr in rr_intervals if 0.3 <= rr <= 1.5]
        hr_values = 60 / np.array(valid_rr_intervals)
        return [hr for hr in hr_values if 40 <= hr <= 200]

    for file_name in os.listdir(PPG_data_path):
        if file_name.endswith(".csv"):
            file_path = os.path.join(PPG_data_path, file_name)

            try:
                match = re.match(r"sub-(\d+)_sess(\d+)_PPG.csv", file_name)
                if not match:
                    print(f"File name does not match expected pattern: {file_name}")
                    continue

                participant_id = match.group(1)
                session_id = match.group(2)

                data = pd.read_csv(file_path)
                if "PPG" not in data.columns:
                    print(f"File {file_name} is missing the required 'PPG' column.")
                    continue

                ppg_signal = data["PPG"].values
                sample_rate = 100

                r_peaks = rpeaks_from_ppg(ppg_signal, sample_rate)
                if len(r_peaks) == 0:
                    print(f"No R-peaks detected in {file_name}.")
                    continue

                hr_values = calculate_hr(r_peaks, sample_rate)
                if len(hr_values) == 0:
                    print(f"No valid HR values calculated for {file_name}.")
                    continue

                for i, hr in enumerate(hr_values):
                    if i < len(r_peaks) - 1:
                        all_results.append(
                            {
                                "participant_id": participant_id,
                                "session_id": session_id,
                                "r_peak_index": r_peaks[i],
                                "HR": hr,
                            }
                        )

            except Exception as e:
                print(f"Failed to process {file_name}: {e}")

    if all_results:
        results_df = pd.DataFrame(all_results)
        output_path = Path(final_data_path) / "R-peaks_and_HR.xlsx"
        results_df.to_excel(output_path, index=False)
        print("R-peaks and HR saved to R-peaks_and_HR excel file.")
    else:
        print("No R-peaks or HR were extracted.")
