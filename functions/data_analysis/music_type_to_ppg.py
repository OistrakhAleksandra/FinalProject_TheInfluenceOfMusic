"""Import necessary libraries for file handling and data processing"""

import matplotlib.pyplot as plt
import pandas as pd

# Define the file path
combined_data_file = r"C:\Users\Home\Desktop\Studies\Phyton\projects 2024-2025\Project_2\data\combined_data_trial.xlsx"

# Read the Excel file
data = pd.read_excel(combined_data_file)

# Ensure the required columns are present
required_columns = ["participant_id", "music_type", "PPG_data"]
if not all(col in data.columns for col in required_columns):
    raise ValueError(f"The input file must contain the following columns: {required_columns}")

# Group data by participant_id and music_type, then calculate the mean PPG_data for each group
average_ppg = data.groupby(["participant_id", "music_type"])["PPG_data"].mean().reset_index()

# Pivot the data to create columns for each music_type
pivot_data = average_ppg.pivot(index="participant_id", columns="music_type", values="PPG_data")

# Check if all required music types are present, fill missing values with NaN
music_types = ["tonal", "atonal", "discord"]
for music_type in music_types:
    if music_type not in pivot_data.columns:
        pivot_data[music_type] = None

# Sort the pivoted data by participant_id for consistent plotting
pivot_data = pivot_data.sort_index()

# Plot the data
plt.figure(figsize=(10, 6))
for music_type in music_types:
    if music_type in pivot_data:
        plt.plot(pivot_data.index, pivot_data[music_type], label=music_type, marker="o")

# Add labels, title, and legend
plt.xlabel("Participant ID")
plt.ylabel("Average PPG")
plt.title("Average PPG Data for Different Music Types")
plt.legend(title="Music Type")
plt.grid(True)

# Show the plot
plt.tight_layout()
plt.show()
