# scripts/download_dataset.py

import os
from kaggle.api.kaggle_api_extended import KaggleApi

def download_dataset(dataset_name, output_dir):
    # Initialize the Kaggle API
    api = KaggleApi()
    api.authenticate()

    # Create the output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)

    # Download the dataset
    print(f"Downloading dataset: {dataset_name}")
    api.dataset_download_files(dataset_name, path=output_dir, unzip=True)
    print(f"Dataset downloaded to {output_dir}")

if __name__ == "__main__":
    dataset_name = "mlg-ulb/creditcardfraud"  # Kaggle dataset name
    output_dir = "data"                       # Output directory
    download_dataset(dataset_name, output_dir)