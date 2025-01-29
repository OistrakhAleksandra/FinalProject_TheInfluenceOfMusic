from unittest.mock import patch

import pandas as pd
from functions.clearing_data.is_to_excel import calculate_is
from functions.clearing_data.trial_combined import filter_to_new_excel


@patch("os.listdir", return_value=["sub-1_sess1_HBD.csv", "sub-2_sess1_HBD.csv"])
@patch("pandas.read_csv")
@patch("pandas.read_excel")
@patch("pandas.DataFrame.to_excel")
def test_calculate_is(mock_to_excel, mock_read_excel, mock_read_csv, mock_listdir):
    """Test calculating IS values without needing actual files."""
    # Mock the combined data Excel file
    mock_read_excel.return_value = pd.DataFrame({"participant_id": [1, 2], "IS": [None, None]})

    # Mock HBD data (simulating heartbeat discrimination task results)
    mock_read_csv.return_value = pd.DataFrame(
        {
            "resting_RRI": [0.8, 0.85],  # Simulated resting RRI values
            "delay": [0.2, 0.25],
            "response": ["Sync", "Async"],
        }
    )

    # Call the function with mock paths
    calculate_is("mock_HBD_data", "mock_combined_data.xlsx")

    # Ensure the function attempts to write the result to an Excel file
    mock_to_excel.assert_called_once()


@patch("pandas.read_excel")
@patch("os.listdir", return_value=["data1.csv", "data2.xlsx"])
@patch("pandas.read_csv")
@patch("pandas.DataFrame.to_excel")
def test_filter_to_new_excel(mock_to_excel, mock_read_csv, mock_listdir, mock_read_excel):
    """Test filtering and saving new Excel file without actual file system."""
    # Mock CSV file reading
    mock_read_csv.return_value = pd.DataFrame({"col1": [1, 2, 3], "col2": [4, 5, 6]})

    # Mock Excel file reading
    mock_read_excel.return_value = pd.DataFrame({"col1": [10, 20, 30], "col2": [40, 50, 60]})

    # Call the function with mock paths
    filter_to_new_excel("mock_trial_data", ["col1", "col2"], "mock_output.xlsx")

    # Ensure the function attempts to write filtered data to an Excel file
    mock_to_excel.assert_called_once()
