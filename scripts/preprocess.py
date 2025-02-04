# scripts/preprocess.py

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import os

def preprocess_data(input_file, output_file):
    # Load raw data
    df = pd.read_csv(input_file)

    # Separate features and target
    X = df.drop(columns=["Class"])
    y = df["Class"]

    # Scale the 'Amount' feature
    scaler = StandardScaler()
    X["Amount"] = scaler.fit_transform(X[["Amount"]])

    # Drop the 'Time' feature (optional, based on analysis)
    X = X.drop(columns=["Time"])

    # Save processed data
    processed_df = pd.concat([X, y], axis=1)
    processed_df.to_csv(output_file, index=False)
    print(f"Processed data saved to {output_file}")

if __name__ == "__main__":
    input_file = "data/creditcard.csv"
    output_file = "data/processed_data.csv"
    preprocess_data(input_file, output_file)