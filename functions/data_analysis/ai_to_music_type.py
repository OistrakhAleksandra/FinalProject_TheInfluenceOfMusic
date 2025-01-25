import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import statsmodels.api as sm
from statsmodels.formula.api import ols


def analyze_music_type_vs_IS(trial_combined_path=str):
    """Analyze the relationship between 'music_type' and 'IS'.

    Parameters:
        df (pd.DataFrame): The input DataFrame containing 'music_type' and 'IS' columns.

    Returns:
        tuple: Correlation value and ANOVA table.
    """
    # Reading the file
    df = pd.read_excel(trial_combined_path)

    # 1. Correlation between 'music_type' and 'IS'
    df["music_type_numeric"] = df["music_type"].astype("category").cat.codes  # Convert music_type to numeric
    correlation = df["music_type_numeric"].corr(df["IS"])
    print(f"Correlation between music type and Introspective sensitivity: {correlation:.3f}")

    # 2. ANOVA test for 'music_type' and 'IS'
    model = ols("IS ~ C(music_type)", data=df).fit()  # Fit the model
    anova_table = sm.stats.anova_lm(model, typ=2)  # Perform ANOVA
    print(anova_table)

    # 3. Graph of IS vs music_type
    plt.figure(figsize=(10, 6))
    sns.boxplot(x="music_type", y="IS", data=df, palette="Set2", hue="music_type")
    plt.title("IS by Music Type")
    plt.xlabel("Music Type")
    plt.ylabel("Introspective sensitivity (IS)")
    # plt.savefig('graph.png')
    plt.show()
