import pandas as pd
import numpy as np
from scipy.stats import spearmanr
from functions.data_analysis.ppg_to_valence import calculate_spearman_correlation  

def test_calculate_spearman_correlation():
    # Create a test dataset
    data = {
        "valence_rating": np.random.uniform(1, 5, 50),  # Random values between 1 and 5
        "PPG_data": np.random.uniform(50, 100, 50)  # Random values between 50 and 100
    }
    df = pd.DataFrame(data)

    # Test with valid input
    try:
        calculate_spearman_correlation(df)
        print("Test Passed: Function ran successfully with valid input.")
    except Exception as e:
        print(f"Test Failed: Function raised an error with valid input: {e}")

    # Test with missing values
    df_with_nan = df.copy()
    df_with_nan.loc[0:4, "valence_rating"] = np.nan  # Introduce NaN values
    try:
        calculate_spearman_correlation(df_with_nan)
        print("Test Passed: Function handled missing values correctly.")
    except Exception as e:
        print(f"Test Failed: Function raised an error with missing values: {e}")

    # Test with missing required columns
    df_missing_col = df.drop(columns=["valence_rating"])
    try:
        calculate_spearman_correlation(df_missing_col)
        print("Test Failed: Function did not raise an error for missing column 'valence_rating'.")
    except KeyError:
        print("Test Passed: Function correctly raised KeyError for missing column 'valence_rating'.")
    except Exception as e:
        print(f"Test Failed: Unexpected error for missing column test: {e}")

if __name__ == "__main__":
    test_calculate_spearman_correlation()
