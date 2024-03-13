
import csv

# Open the CSV file
import pandas as pd

# Read the CSV file into a DataFrame
df = pd.read_csv(r'C:\Semester 6\Semester 6\Sistem Pendukung Keputusan\final_project\database\dataset\SPK Final Project 2024 - python.csv')

# Create an empty dictionary to store the columns
columns_dict = {}

# Iterate over each column in the DataFrame
for column in df.columns:
    # Add the column data to the dictionary
    columns_dict[column] = df[column].tolist()
