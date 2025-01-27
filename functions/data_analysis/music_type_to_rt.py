import logging

import matplotlib.pyplot as plt
import pandas as pd
from scipy.stats import f_oneway

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")


def analyze_rt_by_music_type(combined_data_file: str) -> str:
    """Analyzes reaction time (RT) differences between music types and performs ANOVA.

    Parameters:
        trial_combined_path (str): Path to the Excel file containing the data.

    Returns:
        str: Conclusion based on the ANOVA test result.
    """
    # Read the Excel file
    data = pd.read_excel(combined_data_file)

    # Ensure the required columns are present
    required_columns = ["participant_id", "music_type", "RT"]
    if not all(col in data.columns for col in required_columns):
        raise ValueError(f"The input file must contain the following columns: {required_columns}")

    # Perform ANOVA to check for significant differences between music types
    tonal = data[data["music_type"] == "tonal"]["RT"]
    atonal = data[data["music_type"] == "atonal"]["RT"]
    discord = data[data["music_type"] == "discord"]["RT"]

    f_stat, p_value = f_oneway(tonal, atonal, discord)
    logging.info(f"ANOVA F-statistic: {f_stat:.2f}, p-value: {p_value:.4f}")

    # Interpret the results
    if p_value < 0.05:
        conclusion = "Music type has a significant effect on reaction time (RT)."
    else:
        conclusion = "Music type does not have a significant effect on reaction time (RT)."

    # Calculate mean and standard deviation of RT for each music type
    summary_stats = data.groupby("music_type")["RT"].agg(["mean", "std"]).reset_index()

    # Plot the bar chart with error bars
    plt.figure(figsize=(6, 4))
    plt.bar(
        summary_stats["music_type"],
        summary_stats["mean"],
        yerr=summary_stats["std"],
        capsize=5,
        color=["skyblue", "lightgreen", "salmon"],
    )

    # Add labels, title, and grid
    plt.xlabel("Music Type")
    plt.ylabel("Average RT (Mean ± SD)")
    plt.title("Average RT by Music Type with Standard Deviation")
    plt.grid(axis="y", linestyle="--", alpha=0.7)

    # Show the plot
    plt.tight_layout()
    plt.show()

    return conclusion
