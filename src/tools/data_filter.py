import os
import pandas as pd
from typing import List

# Function to convert CSV and Excel files to a single Excel file with selected columns
def filter_to_new_excel(folder_path: str, selected_columns: List[str], final_folder_path: str) -> None:
    # Create an empty DataFrame to store the combined data
    combined_data = pd.DataFrame()

    for file_name in os.listdir(folder_path):  # Loop through all files in the folder
        # Check if the file is a CSV or Excel file
        if file_name.endswith(".csv") or file_name.endswith(".xlsx"):
            file_path = os.path.join(folder_path, file_name)
            
            # Read the data based on the file type
            if file_name.endswith(".csv"):
                data = pd.read_csv(file_path)
            elif file_name.endswith(".xlsx"):
                data = pd.read_excel(file_path)
            
            # Check if the file contains all the required columns
            if all(col in data.columns for col in selected_columns):
                # Select only the required columns
                data_filtered = data[selected_columns]
                
                # Append the data to the combined DataFrame
                combined_data = pd.concat([combined_data, data_filtered], ignore_index=True)
            else:
                print(f"File {file_name} is missing one or more required columns: {selected_columns}")
    
    # Path to save the final combined Excel file
    output_path = os.path.join(final_folder_path, "combined_data.xlsx")
    
    # Save the combined data to a new Excel file
    combined_data.to_excel(output_path, index=False)
  
