import pandas as pd
import pytest
from functions.data_analysis.IS_ti_music_type import analyze_music_type_vs_IS

def test_analyze_music_type_vs_IS():
    # Create a sample DataFrame
    data = {
        'music_type': ['Classical', 'Pop', 'Rock', 'Jazz', 'Classical', 'Pop', 'Rock', 'Jazz', 'Classical', 'Rock'],
        'IS': [85, 90, 78, 88, 92, 95, 70, 82, 88, 75]
    }
    df = pd.DataFrame(data)
    
    # Run the function
    correlation, anova_table = analyze_music_type_vs_IS(df)
    
    # Assertions to validate results
    assert isinstance(correlation, (float, int)), "Correlation must be a numeric value."
    assert not anova_table.empty, "ANOVA table must not be empty."

# Run tests only when executed directly
if __name__ == "__main__":
    pytest.main()
