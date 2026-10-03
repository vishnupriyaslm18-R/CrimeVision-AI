import pandas as pd
from sklearn.linear_model import LinearRegression

DATA_PATH = "data/processed/crime_analysis_clean.csv"


# =========================================================
# LOAD DATA
# =========================================================

def load_data():

    df = pd.read_csv(DATA_PATH)

    df.columns = (
        df.columns
        .str.strip()
        .str.lower()
    )

    return df


# =========================================================
# YEAR-WISE CRIME DATA
# =========================================================

def get_yearly_crime_data():

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

    # Convert crime columns to numeric
    df[crime_columns] = df[crime_columns].apply(
        pd.to_numeric,
        errors="coerce"
    )

    # Total recorded crime-category counts
    df["total_crimes"] = (
        df[crime_columns]
        .sum(axis=1)
    )

    # Year-wise total
    yearly = (
        df.groupby("year")["total_crimes"]
        .sum()
        .reset_index()
    )

    yearly.columns = [
        "Year",
        "Crime_Count"
    ]

    yearly = yearly.sort_values(
        "Year"
    )

    return yearly


# =========================================================
# FUTURE CRIME PREDICTION
# =========================================================

def predict_future_year(future_year):

    yearly = get_yearly_crime_data()

    # -----------------------------------------------------
    # Historical data
    # -----------------------------------------------------

    X = yearly[["Year"]]
    y = yearly["Crime_Count"]

    # -----------------------------------------------------
    # Machine Learning Model
    # -----------------------------------------------------

    model = LinearRegression()

    model.fit(
        X,
        y
    )

    # -----------------------------------------------------
    # Future prediction
    # -----------------------------------------------------

    future_data = pd.DataFrame(
        [[future_year]],
        columns=["Year"]
    )

    predicted_value = model.predict(
        future_data
    )[0]

    # Prevent negative prediction
    predicted_value = max(
        0,
        predicted_value
    )

    # -----------------------------------------------------
    # Latest historical year
    # -----------------------------------------------------

    latest_year = int(
        yearly["Year"].max()
    )

    latest_count = float(
        yearly.loc[
            yearly["Year"] == latest_year,
            "Crime_Count"
        ].iloc[0]
    )

    # -----------------------------------------------------
    # Trend
    # -----------------------------------------------------

    if predicted_value > latest_count:

        trend = "Increasing"

    elif predicted_value < latest_count:

        trend = "Decreasing"

    else:

        trend = "Stable"

    # -----------------------------------------------------
    # Percentage change
    # -----------------------------------------------------

    change_percentage = (
        (
            predicted_value
            - latest_count
        )
        / latest_count
    ) * 100

    # -----------------------------------------------------
    # Trend level
    # -----------------------------------------------------

    if abs(change_percentage) < 5:

        trend_level = "Low"

    elif abs(change_percentage) < 15:

        trend_level = "Moderate"

    else:

        trend_level = "High"

    # -----------------------------------------------------
    # Return result
    # -----------------------------------------------------

    return {

        "future_year":
            int(future_year),

        "predicted_crime_count":
            round(predicted_value),

        "trend":
            trend,

        "trend_level":
            trend_level,

        "change_percentage":
            round(
                change_percentage,
                2
            ),

        "latest_year":
            latest_year,

        "latest_count":
            round(latest_count),

        "historical_data":
            yearly
    }


# =========================================================
# TEST FROM TERMINAL
# =========================================================

if __name__ == "__main__":

    print(
        "\n======================================"
    )

    print(
        " CRIMEVISION AI FUTURE PREDICTION"
    )

    print(
        "======================================"
    )

    print(
        "\nHistorical Crime Data:"
    )

    print(
        get_yearly_crime_data()
    )

    # Ask future year
    future_year = int(
        input(
            "\nEnter future year: "
        )
    )

    # Prediction
    result = predict_future_year(
        future_year
    )

    print(
        "\n--------------------------------------"
    )

    print(
        "Future Year:",
        result["future_year"]
    )

    print(
        "Estimated Crime Count:",
        f"{result['predicted_crime_count']:,}"
    )

    print(
        "Trend:",
        result["trend"]
    )

    print(
        "Trend Level:",
        result["trend_level"]
    )

    print(
        "Change:",
        str(
            result["change_percentage"]
        ) + "%"
    )

    print(
        "--------------------------------------"
    )