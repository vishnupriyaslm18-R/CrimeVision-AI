import pandas as pd
import os

INPUT_PATH = "data/raw/NCRB_Crime_Analysis_2017_2022_with_25Crime_categories_Districtwise.csv"
OUTPUT_PATH = "data/processed/crime_analysis_clean.csv"


def preprocess_data():

    # Load dataset
    df = pd.read_csv(INPUT_PATH)

    print("Original Dataset Shape:", df.shape)
    print("\nColumns:")
    print(df.columns.tolist())

    # Remove completely empty columns
    df = df.dropna(axis=1, how="all")

    # Remove duplicate rows
    df = df.drop_duplicates()

    # Clean column names
    df.columns = (
        df.columns
        .str.strip()
        .str.replace(" ", "_")
        .str.replace("/", "_")
    )

    # Create processed folder
    os.makedirs("data/processed", exist_ok=True)

    # Save cleaned dataset
    df.to_csv(OUTPUT_PATH, index=False)

    print("\nProcessed Dataset Shape:", df.shape)
    print("\nProcessed dataset saved successfully!")
    print(OUTPUT_PATH)


if __name__ == "__main__":
    preprocess_data()