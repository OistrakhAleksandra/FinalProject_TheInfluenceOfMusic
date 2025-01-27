import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from scipy.stats import linregress


def plot_valence_vs_interoception(combined_data_file):
    """Plots the relationship between average valence rating and interoceptive sensitivity (IS).

    Parameters:
        file_path (str): Path to the Excel file containing the data.

    Returns:
        None
    """
    # Load data (no need for sheet_name)
    data = pd.read_excel(combined_data_file)

    # Group by participant_id to calculate the average valence_rating and IS for each participant
    grouped_data = data.groupby("participant_id").agg({"valence_rating": "mean", "IS": "mean"}).reset_index()

    # Perform linear regression
    slope, intercept, r_value, p_value, std_err = linregress(grouped_data["IS"], grouped_data["valence_rating"])

    # Plotting the scatter plot with regression line
    plt.figure(figsize=(10, 6))
    sns.scatterplot(x="IS", y="valence_rating", data=grouped_data, label="Participant Data")
    plt.plot(
        grouped_data["IS"],
        slope * grouped_data["IS"] + intercept,
        color="red",
        label=f"Linear Regression (R²={r_value**2:.2f})",
    )

    # Customize the plot
    plt.title("Relationship Between Average Valence Rating and Interoceptive Sensitivity", fontsize=14)
    plt.xlabel("Interoceptive Sensitivity (IS)", fontsize=12)
    plt.ylabel("Average Valence Rating", fontsize=12)
    plt.legend()
    plt.grid(alpha=0.3)
    plt.tight_layout()

    # Show the plot
    plt.show()
