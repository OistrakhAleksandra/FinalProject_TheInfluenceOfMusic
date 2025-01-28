import os
import pytest
import pandas as pd
import numpy as np
from unittest.mock import MagicMock, patch
from functions.clearing_data.calc_r_peaks_from_ppg import process_ppg_folder  

def create_test_csv(ppg_data):
    """Helper function to create a mock DataFrame with PPG data."""
    return pd.DataFrame({"PPG": ppg_data})

@pytest.fixture
@patch("your_module.os.listdir")
@patch("your_module.pd.read_csv")
def test_process_ppg_folder(mock_read_csv, mock_listdir):
    # Arrange
    PPG_data_path = "mock/PPG_data"
    final_data_path = "mock/final_data"

    # Mock files in PPG_data_path
    test_files = ["sub-01_sess01_PPG.csv", "sub-02_sess02_PPG.csv"]
    mock_listdir.return_value = test_files

    # Mock PPG data
    sample_rate = 100
    ppg_signal = np.sin(np.linspace(0, 2 * np.pi * 5, sample_rate * 10))  # Simulated PPG signal
    mock_read_csv.side_effect = [
        create_test_csv(ppg_signal),
        create_test_csv(ppg_signal),
    ]

    # Capture results
    results = []

    def mock_save_results(_, results_list):
        nonlocal results
        results = results_list

    # Patch the part of the function that writes to Excel
    with patch("your_module.pd.DataFrame.to_excel", new=mock_save_results):
        # Act
        process_ppg_folder(PPG_data_path, final_data_path)

    # Assert
    assert len(results) > 0, "No results were generated."
    for result in results:
        assert "participant_id" in result, "Expected 'participant_id' key not found in result."
        assert "session_id" in result, "Expected 'session_id' key not found in result."
        assert "r_peak_index" in result, "Expected 'r_peak_index' key not found in result."
        assert "HR" in result, "Expected 'HR' key not found in result."
        assert 40 <= result["HR"] <= 200, "HR values should be within physiological range."


if __name__ == "__main__":
    pytest.main()
