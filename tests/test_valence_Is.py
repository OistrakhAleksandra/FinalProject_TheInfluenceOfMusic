import pandas as pd
import numpy as np
from functions.data_analysis.valence_to_IS import plot_valence_vs_interoception  # Replace with the correct module name

def test_plot_valence_vs_interoception():
    # Create a simple test dataset
    data = {
        'participant_id': ['P1', 'P2', 'P3', 'P4', 'P5'],
        'valence_rating': np.random.uniform(1, 5, 5),
        'IS': np.random.uniform(0, 100, 5)
    }
    df = pd.DataFrame(data)
    
    # Save to a temporary Excel file for testing
    file_path = 'test_data.xlsx'
    with pd.ExcelWriter(file_path) as writer:
        df.to_excel(writer, index=False, sheet_name='Sheet1')

    # Test the function with the test data
    try:
        plot_valence_vs_interoception(file_path, 'Sheet1')
        print("Test Passed: Function ran successfully with valid input.")
    except Exception as e:
        print(f"Test Failed: {e}")

if __name__ == "__main__":
    test_plot_valence_vs_interoception()
