"""Import necessary libraries for file handling and data processing"""

import matplotlib.pyplot as plt
import pandas as pd

# Define the file path
file_path = r"C:\Users\Home\Desktop\Studies\Phyton\projects 2024-2025\Project_2\data\combined_data_trial.xlsx"

# Read the Excel file
data = pd.read_excel(file_path)

# Ensure the required columns are present
required_columns = ["participant_id", "music_type", "RT"]
if not all(col in data.columns for col in required_columns):
    raise ValueError(f"The input file must contain the following columns: {required_columns}")

# Plot the data
plt.figure(figsize=(10, 6))
for music_type in data["music_type"].unique():
    music_data = data[data["music_type"] == music_type]
    plt.plot(music_data["participant_id"], music_data["RT"], label=music_type)

plt.xlabel("Participant ID")
plt.ylabel("Average RT")
plt.title("Average RT for Each Music Type")
plt.legend(title="Music Type")
plt.grid(True)
plt.xticks(rotation=45)
plt.tight_layout()

# Ensure the graph is displayed
plt.show()
