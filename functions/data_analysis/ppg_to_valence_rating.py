import pandas as pd
from scipy.stats import spearmanr


def calculate_spearman_correlation(combined_data_file=str) -> None:
    # Reading the excel file
    data = pd.read_excel(combined_data_file)

    # Clean column names (strip any extra spaces)
    data.columns = data.columns.str.strip()

    # Remove NaN values from the specific columns
    data_clean = data.dropna(subset=["valence_rating", "PPG_data"])

    # Calculate Spearman's correlation coefficient and p-value
    corr, p_value = spearmanr(data_clean["valence_rating"], data_clean["PPG_data"])

    # Print Spearman's correlation coefficient and p-value
    print(f"Spearman's correlation coefficient: {corr:.3f}, p-value: {p_value:.3f}")

    # Print conclusion about statistical dependency
    if p_value > 0.05:
        print("No statistically significant relationship between the variables.")
    else:
        print("There is a statistically significant relationship between the variables.")
