import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import statsmodels.api as sm
from statsmodels.formula.api import ols


def analyze_music_type_vs_IS(combined_data_file: str):
    """Analyze the relationship between 'music_type' and 'IS' using correlation, ANOVA, and visualization.

    Parameters:
        combined_data_file (str): Path to the combined data file.

    Returns:
        None
    """
    # Reading the file
    df = pd.read_excel(combined_data_file)

    # Ensure required columns exist
    required_columns = ["music_type", "IS"]
    for col in required_columns:
        if col not in df.columns:
            raise ValueError(f"Column '{col}' is missing in the input data.")

    # Drop rows with missing IS values
    df = df.dropna(subset=["IS"])

    # 1. Correlation between 'music_type' and 'IS'
    df["music_type_numeric"] = df["music_type"].astype("category").cat.codes  # Convert music_type to numeric
    correlation = df["music_type_numeric"].corr(df["IS"])
    print(f"Correlation between music type and Introspective sensitivity (IS): {correlation:.3f}")

    # Interpret correlation result
    if abs(correlation) < 0.1:
        print("The correlation between music type and IS is very weak or nonexistent.")
    elif abs(correlation) < 0.3:
        print("There is a weak correlation between music type and IS.")
    elif abs(correlation) < 0.5:
        print("There is a moderate correlation between music type and IS.")
    else:
        print("There is a strong correlation between music type and IS.")

    # 2. ANOVA test for 'music_type' and 'IS'
    model = ols("IS ~ C(music_type)", data=df).fit()  # Fit the model
    p_value = sm.stats.anova_lm(model, typ=2)["PR(>F)"].iloc[0]  # Get the p-value

    # Interpret ANOVA result
    print(f"ANOVA p-value: {p_value:.3e}")
    if p_value < 0.05:
        print("The ANOVA test indicates that music type has a significant effect on IS.")
    else:
        print("The ANOVA test indicates that music type does not have a significant effect on IS.")

    # 3. Graph of IS vs music_type
    plt.figure(figsize=(10, 6))
    sns.boxplot(x="music_type", y="IS", data=df, hue="music_type", palette="Set2", dodge=False, legend=False)
    plt.title("Interoceptive Sensitivity (IS) by Music Type", fontsize=14)
    plt.xlabel("Music Type", fontsize=12)
    plt.ylabel("Interoceptive Sensitivity (IS)", fontsize=12)
    plt.grid(alpha=0.3)
    plt.tight_layout()
    plt.show()
