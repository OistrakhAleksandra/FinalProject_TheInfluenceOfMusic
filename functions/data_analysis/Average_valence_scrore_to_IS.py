import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from scipy.stats import pearsonr


def analyze_valence_vs_IS(combined_data_file: str):
    """Analyzes and visualizes the relationship between the average valence score and IS for each participant.

    Parameters:
        combined_data_file (str): Path to the combined data file containing valence scores and IS.

    Returns:
        None
    """
    # Load data
    df = pd.read_excel(combined_data_file)

    # Ensure required columns exist
    required_columns = ["participant_id", "valence_rating", "IS"]
    for col in required_columns:
        if col not in df.columns:
            raise ValueError(f"Column '{col}' is missing in the input data.")

    # Calculate mean valence rating per participant
    grouped_data = (
        df.groupby("participant_id")
        .agg(
            mean_valence=("valence_rating", "mean"),
            IS=("IS", "first"),  # Assuming IS is the same for each participant
        )
        .reset_index()
    )

    # Scatter plot with regression line
    plt.figure(figsize=(8, 6))
    sns.scatterplot(x="mean_valence", y="IS", data=grouped_data, alpha=0.7)
    sns.regplot(x="mean_valence", y="IS", data=grouped_data, scatter=False, color="red", ci=None)
    plt.title("Relationship Between Mean Valence Score and IS", fontsize=14)
    plt.xlabel("Mean Valence Score", fontsize=12)
    plt.ylabel("Interoceptive Sensitivity (IS)", fontsize=12)
    plt.grid(alpha=0.3)
    plt.tight_layout()
    plt.show()

    # Pearson correlation
    correlation, p_value = pearsonr(grouped_data["mean_valence"], grouped_data["IS"])
    print(f"Pearson Correlation: r = {correlation:.2f}, p-value = {p_value:.3e}")

    # Interpret correlation result
    if p_value < 0.05:
        print("There is a significant correlation between mean valence score and IS.")
    else:
        print("There is no significant correlation between mean valence score and IS.")


# Example usage
combined_data_file = (
    r"C:\Users\Home\Desktop\Studies\Phyton\projects 2024-2025\Final_project\data\combined_data_trial.xlsx"
)
analyze_valence_vs_IS(combined_data_file)
