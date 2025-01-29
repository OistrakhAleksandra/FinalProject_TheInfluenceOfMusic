from unittest.mock import patch

import numpy as np
import pandas as pd
import pytest
from functions.clearing_data.adding_ppg_to_trial_comb import match_ppg_data
from functions.clearing_data.calc_r_peaks_from_ppg import process_ppg_folder
from functions.clearing_data.is_to_excel import calculate_is
from functions.clearing_data.trial_combined import filter_to_new_excel


@pytest.fixture
def mock_trial_data():
    """Mock trial data for matching PPG."""
    return pd.DataFrame(
        {
            "session": [1, 2],
            "participant_id": [101, 102],
            "PPG_response_start": [1.5, 3.0],
        }
    )


@pytest.fixture
def mock_ppg_data():
    """Mock PPG data."""
    return pd.DataFrame(
        {
            "time": [1.4, 1.5, 1.6],
            "PPG": [0.8, 0.9, 1.0],
        }
    )


@patch("pandas.read_excel")
@patch("pandas.read_csv")
@patch("os.listdir")
@patch("pandas.DataFrame.to_excel")
def test_match_ppg_data(mock_to_excel, mock_listdir, mock_read_csv, mock_read_excel, mock_trial_data, mock_ppg_data):
    """Test PPG data matching function."""
    mock_read_excel.return_value = mock_trial_data
    mock_listdir.return_value = ["sub-101_sess1_PPG.csv", "sub-102_sess2_PPG.csv"]
    mock_read_csv.return_value = mock_ppg_data

    match_ppg_data("mock_trial_combined.xlsx", "mock_input_folder")

    mock_to_excel.assert_called_once()


@patch("os.listdir")
@patch("pandas.read_csv")
@patch("pandas.DataFrame.to_excel")
def test_process_ppg_folder(mock_to_excel, mock_read_csv, mock_listdir):
    """Test processing PPG folder."""
    mock_listdir.return_value = ["sub-101_sess1_PPG.csv"]
    mock_read_csv.return_value = pd.DataFrame({"PPG": np.random.randn(1000)})

    process_ppg_folder("mock_PPG_data", "mock_output.xlsx")

    mock_to_excel.assert_called_once()


@patch("pandas.read_excel")
@patch("pandas.DataFrame.to_excel")
def test_calculate_is(mock_to_excel, mock_read_excel):
    """Test calculating IS values."""
    mock_read_excel.return_value = pd.DataFrame({"participant_id": [1, 2], "IS": [None, None]})

    calculate_is("mock_HBD_data", "mock_combined_data.xlsx")

    mock_to_excel.assert_called_once()


@patch("os.listdir")
@patch("pandas.read_csv")
@patch("pandas.DataFrame.to_excel")
def test_filter_to_new_excel(mock_to_excel, mock_read_csv, mock_listdir):
    """Test filtering and saving new Excel file."""
    mock_listdir.return_value = ["data1.csv", "data2.xlsx"]
    mock_read_csv.return_value = pd.DataFrame({"col1": [1, 2, 3], "col2": [4, 5, 6]})

    filter_to_new_excel("mock_trial_data", ["col1", "col2"], "mock_output.xlsx")

    mock_to_excel.assert_called_once()


if __name__ == "__main__":
    pytest.main()
