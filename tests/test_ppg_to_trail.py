import pytest
from unittest.mock import patch, MagicMock
import pandas as pd
from pathlib import Path

# Import the function to be tested
from functions.clearing_data.adding_ppg_to_trial_comb import match_ppg_data

def test_match_ppg_data():
    # Mock input data for the Excel file
    mock_excel_data = pd.DataFrame({
        "session": [1, 2],
        "participant_id": [101, 102],
        "PPG_response_start": [0.5, 1.0]
    })

    # Mock PPG CSV data
    mock_ppg_data_101 = pd.DataFrame({
        "time": [0.3, 0.5, 0.7],
        "PPG": [10, 20, 30]
    })

    mock_ppg_data_102 = pd.DataFrame({
        "time": [0.8, 1.0, 1.2],
        "PPG": [40, 50, 60]
    })

    # Mock os.listdir to return mock PPG files
    mock_file_list = ["sub-101_sess1_PPG.csv", "sub-102_sess2_PPG.csv"]

    # Mock pandas.read_excel to return the mock Excel data
    with patch("pandas.read_excel", return_value=mock_excel_data):
        # Mock pandas.to_excel to capture the written data
        with patch("pandas.DataFrame.to_excel") as mock_to_excel:
            # Mock os.listdir to return the mocked file list
            with patch("os.listdir", return_value=mock_file_list):
                # Mock pandas.read_csv to return different mock PPG data depending on the file path
                def mock_read_csv(file_path, *args, **kwargs):
                    if "sub-101_sess1_PPG.csv" in str(file_path):
                        return mock_ppg_data_101
                    elif "sub-102_sess2_PPG.csv" in str(file_path):
                        return mock_ppg_data_102
                    raise FileNotFoundError

                with patch("pandas.read_csv", side_effect=mock_read_csv):
                    # Call the function to test
                    match_ppg_data("mock_combined_data.xlsx", "mock_ppg_data_path")

                    # Check if to_excel was called once
                    assert mock_to_excel.call_count == 1

                    # Capture the DataFrame written to the Excel file
                    written_df = mock_to_excel.call_args[0][0]

                    # Validate the results
                    assert "PPG_data" in written_df.columns
                    assert written_df.loc[0, "PPG_data"] == 20  # Closest PPG value for participant 101, session 1
                    assert written_df.loc[1, "PPG_data"] == 50  # Closest PPG value for participant 102, session 2

if __name__ == "__main__":
    pytest.main()


