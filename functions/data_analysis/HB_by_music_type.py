import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from scipy.stats import f_oneway


def plot_hr_by_music_type(R_peak_data_path, combined_data_file):
    """Plots the distribution of heart rate (HR) by music type and performs ANOVA.

    Args:
        r_peaks_file (str): Path to the R-peaks file.
        combined_data_file (str): Path to the combined data file.
    """
    # Load data
    hr_data = pd.read_excel(R_peak_data_path)
    combined_data = pd.read_excel(combined_data_file)

    # Merge HR data with music type
    merged_data = hr_data.merge(
        combined_data, how="inner", left_on=["participant_id", "session_id"], right_on=["participant_id", "session"]
    )

    # Plotting HR by music type
    plt.figure(figsize=(8, 6))
    sns.boxplot(x="music_type", y="HR", data=merged_data)
    plt.title("Heart Rate by Music Type", fontsize=14)
    plt.xlabel("Music Type", fontsize=12)
    plt.ylabel("Heart Rate (bpm)", fontsize=12)
    plt.grid(alpha=0.3)
    plt.tight_layout()
    plt.show()

    # ANOVA test for HR by music type
    tonal = merged_data[merged_data["music_type"] == "tonal"]["HR"]
    atonal = merged_data[merged_data["music_type"] == "atonal"]["HR"]
    discord = merged_data[merged_data["music_type"] == "discord"]["HR"]
    f_stat, p_value = f_oneway(tonal, atonal, discord)

    # Print ANOVA results
    print(f"ANOVA Test Results: F-statistic = {f_stat:.2f}, p-value = {p_value:.3e}")
    if p_value < 0.05:
        print("There is a significant effect of music type on heart rate.")
    else:
        print("No significant effect of music type on heart rate.")
