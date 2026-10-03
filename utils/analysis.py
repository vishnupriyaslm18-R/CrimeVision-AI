import pandas as pd

DATA_PATH = "data/processed/crime_analysis_clean.csv"


def load_data():
    df = pd.read_csv(DATA_PATH)

    # Clean column names
    df.columns = df.columns.str.strip().str.lower()

    return df


# 1. Year-wise crime analysis
def get_yearly_analysis():
    df = load_data()

    crime_columns = [
        col for col in df.columns
        if col not in [
            "year",
            "state_name",
            "state_code",
            "district_name",
            "district_code",
            "registration_circles"
        ]
    ]

    yearly = []

    for year in sorted(df["year"].unique()):

        year_data = df[df["year"] == year]

        total_crimes = year_data[crime_columns].sum().sum()

        yearly.append({
            "Year": int(year),
            "Crime_Count": int(total_crimes)
        })

    return pd.DataFrame(yearly)


# 2. State-wise crime analysis
def get_state_analysis():
    df = load_data()

    crime_columns = [
        col for col in df.columns
        if col not in [
            "year",
            "state_name",
            "state_code",
            "district_name",
            "district_code",
            "registration_circles"
        ]
    ]

    df["Total_Crimes"] = df[crime_columns].sum(axis=1)

    state_data = (
        df.groupby("state_name")["Total_Crimes"]
        .sum()
        .reset_index()
    )

    state_data.columns = [
        "State",
        "Crime_Count"
    ]

    return state_data.sort_values(
        "Crime_Count",
        ascending=False
    )


# 3. District-wise crime analysis
def get_district_analysis():
    df = load_data()

    crime_columns = [
        col for col in df.columns
        if col not in [
            "year",
            "state_name",
            "state_code",
            "district_name",
            "district_code",
            "registration_circles"
        ]
    ]

    df["Total_Crimes"] = df[crime_columns].sum(axis=1)

    district_data = (
        df.groupby("district_name")["Total_Crimes"]
        .sum()
        .reset_index()
    )

    district_data.columns = [
        "District",
        "Crime_Count"
    ]

    return district_data.sort_values(
        "Crime_Count",
        ascending=False
    )


# 4. Crime category analysis
def get_crime_category_analysis():
    df = load_data()

    crime_columns = [
        col for col in df.columns
        if col not in [
            "year",
            "state_name",
            "state_code",
            "district_name",
            "district_code",
            "registration_circles"
        ]
    ]

    results = []

    for col in crime_columns:

        total = pd.to_numeric(
            df[col],
            errors="coerce"
        ).sum()

        results.append({
            "Crime_Category": col,
            "Crime_Count": int(total)
        })

    result_df = pd.DataFrame(results)

    return result_df.sort_values(
        "Crime_Count",
        ascending=False
    )


# 5. Summary
def get_summary():
    df = load_data()

    crime_columns = [
        col for col in df.columns
        if col not in [
            "year",
            "state_name",
            "state_code",
            "district_name",
            "district_code",
            "registration_circles"
        ]
    ]

    total_crimes = int(
        df[crime_columns].sum().sum()
    )

    return {
        "Total_Records": len(df),
        "Total_States": df["state_name"].nunique(),
        "Total_Districts": df["district_name"].nunique(),
        "Total_Crimes": total_crimes,
        "Years": sorted(df["year"].unique())
    }


if __name__ == "__main__":

    print("\n===== CRIMEVISION AI ANALYSIS =====")

    summary = get_summary()

    print("\nTotal Records:", summary["Total_Records"])
    print("Total States:", summary["Total_States"])
    print("Total Districts:", summary["Total_Districts"])
    print("Total Crimes:", summary["Total_Crimes"])
    print("Years:", summary["Years"])

    print("\n===== YEAR-WISE ANALYSIS =====")
    print(get_yearly_analysis())

    print("\n===== TOP STATES =====")
    print(get_state_analysis().head(10))

    print("\n===== TOP DISTRICTS =====")
    print(get_district_analysis().head(10))

    print("\n===== TOP CRIME CATEGORIES =====")
    print(get_crime_category_analysis().head(10))