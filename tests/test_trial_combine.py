import pytest
from unittest.mock import patch, MagicMock
import pandas as pd



def test_filter_to_new_excel():
    """Test the filter_to_new_excel function without real file or folder operations."""
    # Mock arguments
    folder_path = "mock_folder_path"
    selected_columns = ["col1", "col2", "col3"]
    final_data_path = "mock_final_data_path"

    # Mock data for CSV/Excel files
    mock_data_1 = pd.DataFrame({
        "col1": [1, 2, 3],
        "col2": [4, 5, 6],
        "col3": [7, 8, 9],
    })

    mock_data_2 = pd.DataFrame({
        "col1": [10, 20],
        "col2": [30, 40],
        "col3": [50, 60],
    })

    # Mock files in the folder
    mock_file_list = ["file1.csv", "file2.xlsx", "file3.txt"]  # Includes a non-relevant file

    # Patch dependencies
    with patch("os.listdir", return_value=mock_file_list) as mock_listdir, \
         patch("pandas.read_csv", return_value=mock_data_1) as mock_read_csv, \
         patch("pandas.read_excel", return_value=mock_data_2) as mock_read_excel, \
         patch("pandas.DataFrame.to_excel") as mock_to_excel:

        # Import the function under test
        from functions.clearing_data.trial_combined import filter_to_new_excel

        # Run the function
        filter_to_new_excel(folder_path, selected_columns, final_data_path)

        # Assertions
        mock_listdir.assert_called_once_with(folder_path)  # Check if listdir is called with the correct folder
        assert mock_read_csv.call_count == 1  # Check CSV files were read once
        assert mock_read_excel.call_count == 1  # Check Excel files were read once
        assert mock_to_excel.call_count == 1  # Ensure the final DataFrame was saved

        # Check that the final data path includes the expected file name, using `Path` to match the type
        output_file_path = Path(final_data_path) / "combined_data_trial.xlsx"
        mock_to_excel.assert_called_once_with(output_file_path, index=False)

if __name__ == "__main__":
    test_filter_to_new_excel()
