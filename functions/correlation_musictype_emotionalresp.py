import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy.stats import pearsonr


# Function to calculate Pearson correlation for each music type
def calculate_pearson_correlation(average_valence):
    correlations = []
    for music_type in average_valence["music_type"].unique():
        subset = average_valence[average_valence["music_type"] == music_type]
        if len(subset) > 1:  # ensures that there is sufficient data to make calculations
            r, p_value = pearsonr(subset["Subject"].rank(), subset["valence_rating"])
            correlations.append({"music_type": music_type, "pearson_r": r, "p_value": p_value})

            #  visualize the correlation
            plot_correlation_graph(subset, music_type, r, p_value)

            # Check the correlation significance and strength
            check_correlation(music_type, p_value, r)

    return correlations


#  plot the correlation graph with the correlation line
def plot_correlation_graph(subset, music_type, r, p_value):
    # Scatter plot
    plt.figure()
    plt.scatter(subset["Subject"].rank(), subset["valence_rating"], label=f"r = {r:.2f}, p = {p_value:.2g}")

    # Calculate the correlation line
    m, b = np.polyfit(subset["Subject"].rank(), subset["valence_rating"], 1)
    plt.plot(subset["Subject"].rank(), m * subset["Subject"].rank() + b, color="green")

    # Title and labels
    plt.title(f"Correlation for {music_type}")
    plt.xlabel("Subject Rank")
    plt.ylabel("Emotional Response")
    plt.legend()
    plt.show()


# Function to check the significance of the correlation and the strength of the correlation
def check_correlation(music_type, p_value, r):
    if p_value <= 0.05:
        print(f"Correlation was found between {music_type} and Emotional response.")
        # Categorizing the strength of the correlation
        if abs(r) <= 0.3:
            print(f"Strength of correlation for {music_type}: Weak correlation")
        elif abs(r) <= 0.5:
            print(f"Strength of correlation for {music_type}: Moderate correlation")
        else:
            print(f"Strength of correlation for {music_type}: Strong correlation")
    else:
        print(f"No correlation was found between {music_type} and Emotional response.")


#  correlations to DataFrame
def correlations_to_dataframe(correlations):
    return pd.DataFrame(correlations)
