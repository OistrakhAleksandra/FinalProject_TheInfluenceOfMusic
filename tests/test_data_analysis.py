from unittest.mock import patch

import pandas as pd

# Importing functions from data_analysis module
from functions.data_analysis.is_to_music_type import analyze_music_type_vs_IS
from functions.data_analysis.music_type_to_rt import analyze_rt_by_music_type


@patch("pandas.read_excel")
def test_analyze_music_type_vs_IS(mock_read_excel):
    """Test analyzing relationship between music type and IS using ANOVA (excluding graphing)."""
    mock_read_excel.return_value = pd.DataFrame(
        {
            "music_type": ["tonal", "tonal", "atonal", "atonal", "discord", "discord"],
            "IS": [0.5, 0.6, 0.7, 0.8, 0.6, 0.7],  # At least two values per music type
        }
    )

    analyze_music_type_vs_IS("mock_combined.xlsx")

    assert True  # Ensuring the function runs without errors


@patch("pandas.read_excel")
def test_analyze_rt_by_music_type(mock_read_excel):
    """Test analyzing reaction time differences by music type using ANOVA (excluding graphing)."""
    mock_read_excel.return_value = pd.DataFrame(
        {
            "participant_id": [1, 1, 2, 2, 3, 3, 4, 4, 5, 5],
            "music_type": [
                "tonal",
                "tonal",
                "atonal",
                "atonal",
                "discord",
                "discord",
                "tonal",
                "atonal",
                "discord",
                "tonal",
            ],
            "RT": [0.4, 0.5, 0.6, 0.7, 0.5, 0.6, 0.3, 0.8, 0.4, 0.6],  # Ensure two values per category
        }
    )

    result = analyze_rt_by_music_type("mock_combined.xlsx")

    assert "significant effect" in result or "does not have a significant effect" in result
