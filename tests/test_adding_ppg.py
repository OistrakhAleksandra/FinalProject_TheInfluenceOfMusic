from unittest.mock import patch
import pandas as pd


# Test the function
def test_match_ppg_data() -> None:
    """Test the match_ppg_data function without real file interactions."""
    # Mock arguments
    trial_combined_path = "mock_trial_combined.xlsx"
    input_folder = "mock_input_folder"

    # Mock trial data (Excel content)
    mock_trial_data = pd.DataFrame(
        {
            "session": [1, 2],
            "participant_id": [101, 102],
            "PPG_response_start": [1.5, 3.0],
        }
    )

    # Mock PPG CSV content
    mock_ppg_data = pd.DataFrame(
        {
            "time": [1.4, 1.5, 1.6],
            "PPG": [0.8, 0.9, 1.0],
        }
    )

    # Mock file list in input folder
    mock_file_list = ["sub-101_sess1_PPG.csv", "sub-102_sess2_PPG.csv"]

    # Patch dependencies
    with (
        patch("pandas.read_excel", return_value=mock_trial_data) as mock_read_excel,
        patch("pandas.DataFrame.to_excel") as mock_to_excel,
        patch("os.listdir", return_value=mock_file_list) as mock_listdir,
        patch("pandas.read_csv", return_value=mock_ppg_data) as mock_read_csv,
    ):
        from functions.clearing_data.adding_ppg_to_trial_comb import match_ppg_data

        # Run the function
        match_ppg_data(trial_combined_path, input_folder)

        # Assertions
        mock_read_excel.assert_called_once_with(trial_combined_path)
        mock_listdir.assert_called_once_with(input_folder)
        assert mock_read_csv.call_count == 2  # Should read two CSV files
        assert mock_to_excel.call_count == 1  # Should save the updated DataFrame


if __name__ == "__main__":
    test_match_ppg_data()
