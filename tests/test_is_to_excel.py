import pytest
from unittest.mock import patch, MagicMock
import numpy as np
import pandas as pd
from functions.clearing_data.is_to_excel import calculate_is

# Test data setup
@pytest.fixture
def mock_hbd_data():
    """Fixture to mock Heartbeat Discrimination data."""
    return pd.DataFrame({
        'resting_RRI': [1.0],
        'response': ['Sync', 'Async', 'Sync', 'Async', 'Sync'],
        'delay': [0.2, 0.3, 0.4, 0.5, 0.6]
    })

@pytest.fixture
def mock_combined_data():
    """Fixture to mock combined data."""
    return pd.DataFrame({
        'participant_id': [1, 2],
        'IS': [None, None]
    })

# Test for IS calculation (excluding file I/O)
def test_calculate_is(mock_hbd_data, mock_combined_data):
    # Mocking the reading and writing of files
    with patch('pandas.read_excel', return_value=mock_combined_data) as mock_read_excel, \
         patch('pandas.read_csv', return_value=mock_hbd_data) as mock_read_csv, \
         patch('pandas.DataFrame.to_excel') as mock_to_excel:
        
        # Mocking the file paths
        HBD_data_path = "mock/path"
        combined_data_file = "mock/combined_data.xlsx"

        # Call the function
        calculate_is(HBD_data_path, combined_data_file)

        # Assert read_excel was called to load the combined data
        mock_read_excel.assert_called_with(combined_data_file)
        
        # Assert read_csv was called with the correct file paths
        mock_read_csv.assert_called()

        # Check if the IS column is updated correctly (assuming the Gaussian fitting is successful)
        assert mock_combined_data.loc[0, 'IS'] is not None
        assert isinstance(mock_combined_data.loc[0, 'IS'], float)

        # If the Gaussian fitting failed or IS could not be calculated, IS should be NaN
        assert pd.isna(mock_combined_data.loc[1, 'IS'])

        # Ensure to_excel was called to save the updated data
        mock_to_excel.assert_called_once_with(mock_combined_data, index=False)

# Test case where Gaussian fitting fails
def test_calculate_is_with_invalid_data(mock_combined_data):
    """Test when Gaussian fitting fails and IS is set to NaN."""
    invalid_hbd_data = pd.DataFrame({
        'resting_RRI': [1.0],
        'response': ['Sync', 'Sync', 'Sync'],
        'delay': [0.2, 0.3, 0.4]
    })

    with patch('pandas.read_excel', return_value=mock_combined_data) as mock_read_excel, \
         patch('pandas.read_csv', return_value=invalid_hbd_data) as mock_read_csv, \
         patch('pandas.DataFrame.to_excel') as mock_to_excel:

        # Call the function with invalid sync ratio data
        calculate_is("mock/path", "mock/combined_data.xlsx")

        # Check that the IS value is set to NaN due to invalid sync ratios
        assert pd.isna(mock_combined_data.loc[0, 'IS'])

        # Ensure to_excel was called to save the updated data
        mock_to_excel.assert_called_once_with(mock_combined_data, index=False)
