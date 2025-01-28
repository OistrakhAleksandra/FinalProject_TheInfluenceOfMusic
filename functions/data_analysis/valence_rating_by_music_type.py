import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns


def plot_valence_by_music_type(combined_data_file):
    from scipy.stats import f_oneway

    """
    Plots the distribution of valence rating by music type.

    Args:
        combined_data_file (str): Path to the combined data file.
    """
    data = pd.read_excel(combined_data_file)

    plt.figure(figsize=(8, 6))
    sns.boxplot(x="music_type", y="valence_rating", hue="music_type", palette="pastel", data=data)

    # ANOVA test to check if music type affects valence rating
    tonal = data[data["music_type"] == "tonal"]["valence_rating"]
    atonal = data[data["music_type"] == "atonal"]["valence_rating"]
    discord = data[data["music_type"] == "discord"]["valence_rating"]
    f_stat, p_value = f_oneway(tonal, atonal, discord)

    print(f"ANOVA Test Results: F-statistic = {f_stat:.2f}, p-value = {p_value:.3e}")
    if p_value < 0.05:
        print("There is a significant effect of music type on valence rating.")
    else:
        print("No significant effect of music type on valence rating.")
    plt.title("Valence Rating by Music Type", fontsize=14)
    plt.xlabel("Music Type", fontsize=12)
    plt.ylabel("Valence Rating", fontsize=12)
    plt.grid(alpha=0.3)
    plt.tight_layout()
    plt.show()
