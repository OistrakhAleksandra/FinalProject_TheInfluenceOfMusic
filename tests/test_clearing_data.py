from unittest.mock import patch

import numpy as np
import pandas as pd
from functions.clearing_data.adding_ppg_to_trial_comb import match_ppg_data
from functions.clearing_data.calc_r_peaks_from_ppg import process_ppg_folder

# Importing functions from clearing_data module
from functions.clearing_data.is_to_excel import calculate_is
from functions.clearing_data.trial_combined import filter_to_new_excel


@patch("os.listdir", return_value=["sub-1_sess1_HBD.csv", "sub-2_sess1_HBD.csv"])
@patch("pandas.read_csv")
@patch("pandas.read_excel")
@patch("pandas.DataFrame.to_excel")
def test_calculate_is(mock_to_excel, mock_read_excel, mock_read_csv, mock_listdir):
    """Test calculating IS values without requiring actual files."""
    mock_read_excel.return_value = pd.DataFrame({"participant_id": [1, 2], "IS": [None, None]})

    # Ensure all columns have the same length
    mock_read_csv.return_value = pd.DataFrame(
        {
            "resting_RRI": [0.8, 0.8, 0.85, 0.85],
            "delay": [0.1, 0.2, 0.3, 0.4],
            "response": ["Sync", "Sync", "Async", "Async"],
        }
    )

    calculate_is("mock_HBD_data", "mock_combined_data.xlsx")

    mock_to_excel.assert_called_once()


@patch("pandas.read_excel")
@patch("os.listdir", return_value=["data1.csv", "data2.xlsx"])
@patch("pandas.read_csv")
@patch("pandas.DataFrame.to_excel")
def test_filter_to_new_excel(mock_to_excel, mock_read_csv, mock_listdir, mock_read_excel):
    """Test filtering and saving selected data columns to an Excel file."""
    mock_read_csv.return_value = pd.DataFrame({"col1": [1, 2, 3], "col2": [4, 5, 6]})
    mock_read_excel.return_value = pd.DataFrame({"col1": [10, 20, 30], "col2": [40, 50, 60]})

    filter_to_new_excel("mock_trial_data", ["col1", "col2"], "mock_output.xlsx")

    mock_to_excel.assert_called_once()


@patch("pandas.read_excel")
@patch("pandas.read_csv")
@patch("os.listdir", return_value=["sub-1_sess1_PPG.csv"])
@patch("pandas.DataFrame.to_excel")
def test_match_ppg_data(mock_to_excel, mock_listdir, mock_read_csv, mock_read_excel):
    """Test matching PPG data to trial records."""
    mock_read_excel.return_value = pd.DataFrame({"session": [1], "participant_id": [1], "PPG_response_start": [100]})

    mock_read_csv.side_effect = [
        pd.DataFrame({"session": [1], "participant_id": [1], "PPG_response_start": [100]}),
        pd.DataFrame({"time": [90, 100, 110], "PPG": [0.5, 0.6, 0.7]}),
    ]

    match_ppg_data("mock_combined.xlsx", "mock_PPG_folder")

    mock_to_excel.assert_called_once()


@patch("pandas.read_csv")
@patch("os.listdir", return_value=["sub-1_sess1_PPG.csv"])
@patch("pandas.DataFrame.to_excel")
def test_process_ppg_folder(mock_to_excel, mock_listdir, mock_read_csv):
    """Test processing PPG data and extracting R-peaks."""
    # Simulated PPG signal with periodic peaks
    ppg_signal = np.sin(np.linspace(0, 10, 100))

    mock_read_csv.return_value = pd.DataFrame({"PPG": ppg_signal})

    process_ppg_folder("mock_PPG_folder", "mock_output.xlsx")

    mock_to_excel.assert_called_once()
