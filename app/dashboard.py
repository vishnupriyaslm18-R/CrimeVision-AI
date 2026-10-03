import streamlit as st
import pandas as pd
import sys
import os
import plotly.express as px


# =========================================================
# PROJECT PATH
# =========================================================

PROJECT_ROOT = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..")
)

sys.path.append(PROJECT_ROOT)


# =========================================================
# IMPORT PROJECT MODULES
# =========================================================

from utils.analysis import (
    get_summary,
    get_yearly_analysis,
    get_state_analysis,
    get_district_analysis,
    get_crime_category_analysis
)

from utils.prediction import predict_future_year

from database.database import (
    create_database,
    add_crime_record,
    get_all_records,
    update_crime_record,
    delete_record
)


# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="CrimeVision AI",
    page_icon="🔎",
    layout="wide",
    initial_sidebar_state="expanded"
)


# =========================================================
# DATABASE
# =========================================================

create_database()


# =========================================================
# COLOR PALETTE
# =========================================================

CHART_COLORS = [
    "#2563EB",
    "#7C3AED",
    "#E11D48",
    "#F97316",
    "#0891B2",
    "#059669",
    "#D97706",
    "#DB2777",
    "#4F46E5",
    "#0F766E"
]


# =========================================================
# CUSTOM CSS
# =========================================================

st.markdown(
    """
<style>

.stApp {
    background:
        linear-gradient(
            135deg,
            #f8fbff 0%,
            #eef2ff 48%,
            #fff7ed 100%
        );
}


/* SIDEBAR */

[data-testid="stSidebar"] {
    background:
        linear-gradient(
            180deg,
            #0f172a 0%,
            #172554 45%,
            #4c1d95 100%
        );
}

[data-testid="stSidebar"] * {
    color: white !important;
}


/* HEADINGS */

h1 {
    color: #172554 !important;
    font-weight: 850 !important;
}

h2 {
    color: #1e3a8a !important;
    font-weight: 800 !important;
}

h3 {
    color: #312e81 !important;
    font-weight: 750 !important;
}


/* COLORFUL CARDS */

.crime-cards {
    display: grid;
    grid-template-columns: repeat(5, 1fr);
    gap: 18px;
    width: 100%;
    margin-top: 18px;
    margin-bottom: 35px;
}

.crime-card {
    min-height: 155px;
    padding: 22px 19px;
    border-radius: 22px;
    position: relative;
    overflow: hidden;
    color: white;

    box-shadow:
        0 10px 28px rgba(15, 23, 42, 0.18);

    transition:
        transform 0.25s ease,
        box-shadow 0.25s ease;
}

.crime-card:hover {
    transform: translateY(-8px);

    box-shadow:
        0 20px 40px rgba(15, 23, 42, 0.28);
}


.crime-card-blue {
    background:
        linear-gradient(
            135deg,
            #1d4ed8,
            #2563eb,
            #38bdf8
        );
}


.crime-card-purple {
    background:
        linear-gradient(
            135deg,
            #4c1d95,
            #7c3aed,
            #c084fc
        );
}


.crime-card-red {
    background:
        linear-gradient(
            135deg,
            #881337,
            #e11d48,
            #fb7185
        );
}


.crime-card-orange {
    background:
        linear-gradient(
            135deg,
            #9a3412,
            #ea580c,
            #f59e0b
        );
}


.crime-card-teal {
    background:
        linear-gradient(
            135deg,
            #115e59,
            #0891b2,
            #22d3ee
        );
}


.crime-icon {
    font-size: 30px;
    margin-bottom: 7px;
    position: relative;
    z-index: 2;
}

.crime-title {
    font-size: 15px;
    font-weight: 750;
    position: relative;
    z-index: 2;
}

.crime-number {
    font-size: 31px;
    font-weight: 900;
    line-height: 1.15;
    margin-top: 8px;
    position: relative;
    z-index: 2;
}

.crime-description {
    font-size: 12px;
    margin-top: 9px;
    opacity: 0.90;
    position: relative;
    z-index: 2;
}


.crime-card::before {
    content: "";
    position: absolute;

    width: 125px;
    height: 125px;

    right: -50px;
    top: -50px;

    border-radius: 50%;

    background: rgba(255,255,255,0.13);
}

.crime-card::after {
    content: "";
    position: absolute;

    width: 95px;
    height: 95px;

    right: -30px;
    bottom: -40px;

    border-radius: 50%;

    background: rgba(255,255,255,0.10);
}


/* BUTTONS */

.stButton > button {
    border-radius: 12px !important;
    min-height: 45px !important;
    font-weight: 750 !important;
}


/* RESPONSIVE */

@media (max-width: 1200px) {

    .crime-cards {
        grid-template-columns: repeat(3, 1fr);
    }

}

@media (max-width: 750px) {

    .crime-cards {
        grid-template-columns: repeat(2, 1fr);
    }

}

</style>
""",
    unsafe_allow_html=True
)


# =========================================================
# SIDEBAR
# =========================================================

st.sidebar.title("🔎 CrimeVision AI")

st.sidebar.caption(
    "Crime Pattern Analysis & Prediction"
)

st.sidebar.markdown("---")

page = st.sidebar.radio(
    "Navigation",
    [
        "🏠 Dashboard",
        "📊 Crime Analysis",
        "🔮 Future Prediction",
        "📁 Crime Records"
    ]
)

st.sidebar.markdown("---")

st.sidebar.info(
    "🇮🇳 India-based crime data analysis using "
    "historical data and Machine Learning."
)


# =========================================================
# LOAD DATA
# =========================================================

summary = get_summary()

yearly = get_yearly_analysis()

states = get_state_analysis()

districts = get_district_analysis()

categories = get_crime_category_analysis()

latest_year = int(
    yearly["Year"].max()
)


# =========================================================
# HOME DASHBOARD
# =========================================================

if page == "🏠 Dashboard":

    st.title("🔎 CrimeVision AI")

    st.write(
        "Crime Pattern Analysis • "
        "Future Trend Prediction • "
        "Crime Records"
    )

    st.markdown("---")


    # =====================================================
    # OVERVIEW CARDS
    # =====================================================

    st.subheader("📌 CrimeVision Overview")

    cards_html = f"""
<div class="crime-cards">

<div class="crime-card crime-card-blue">

<div class="crime-icon">📋</div>

<div class="crime-title">
Crime Records
</div>

<div class="crime-number">
{summary['Total_Records']:,}
</div>

<div class="crime-description">
Available dataset records
</div>

</div>


<div class="crime-card crime-card-purple">

<div class="crime-icon">🇮🇳</div>

<div class="crime-title">
States / UTs
</div>

<div class="crime-number">
{summary['Total_States']}
</div>

<div class="crime-description">
Geographical coverage
</div>

</div>


<div class="crime-card crime-card-red">

<div class="crime-icon">📍</div>

<div class="crime-title">
Districts
</div>

<div class="crime-number">
{summary['Total_Districts']}
</div>

<div class="crime-description">
District-level coverage
</div>

</div>


<div class="crime-card crime-card-orange">

<div class="crime-icon">⚠️</div>

<div class="crime-title">
Crime Categories
</div>

<div class="crime-number">
{len(categories)}
</div>

<div class="crime-description">
Crime categories
</div>

</div>


<div class="crime-card crime-card-teal">

<div class="crime-icon">📅</div>

<div class="crime-title">
Data Period
</div>

<div class="crime-number">
{summary['Years'][0]}–{summary['Years'][-1]}
</div>

<div class="crime-description">
Historical coverage
</div>

</div>

</div>
"""

    st.markdown(
        cards_html,
        unsafe_allow_html=True
    )

    st.markdown("---")


    # =====================================================
    # HISTORICAL TREND
    # =====================================================

    st.subheader(
        "📈 Historical Crime Trend"
    )

    fig = px.line(
        yearly,
        x="Year",
        y="Crime_Count",
        markers=True,
        title="2017–2022 Recorded Crime Trend",
        color_discrete_sequence=["#2563EB"]
    )

    fig.update_traces(
        line_width=5,
        marker_size=12
    )

    fig.update_layout(
        height=450,
        template="plotly_white",
        hovermode="x unified"
    )

    st.plotly_chart(
        fig,
        width="stretch"
    )

    st.caption(
        "Historical values represent aggregated recorded "
        "crime-category counts in the dataset."
    )

    st.markdown("---")


    # =====================================================
    # PIE + STATE BAR
    # =====================================================

    left, right = st.columns(2)


    with left:

        st.subheader(
            "🍩 Crime Category Distribution"
        )

        top_categories = categories.head(8).copy()

        other_count = categories.iloc[8:][
            "Crime_Count"
        ].sum()

        if other_count > 0:

            other = pd.DataFrame(
                {
                    "Crime_Category": [
                        "Other Categories"
                    ],
                    "Crime_Count": [
                        other_count
                    ]
                }
            )

            pie_data = pd.concat(
                [
                    top_categories,
                    other
                ],
                ignore_index=True
            )

        else:

            pie_data = top_categories


        fig = px.pie(
            pie_data,
            names="Crime_Category",
            values="Crime_Count",
            hole=0.48,
            title="Crime Category Share",
            color_discrete_sequence=CHART_COLORS
        )

        fig.update_traces(
            textposition="inside",
            textinfo="percent"
        )

        fig.update_layout(
            height=500,
            template="plotly_white"
        )

        st.plotly_chart(
            fig,
            width="stretch"
        )


    with right:

        st.subheader(
            "🇮🇳 State-wise Comparison"
        )

        top_states = (
            states
            .head(10)
            .sort_values("Crime_Count")
        )

        fig = px.bar(
            top_states,
            x="Crime_Count",
            y="State",
            orientation="h",
            title="Top 10 States / UTs",
            color="Crime_Count",
            color_continuous_scale="Turbo"
        )

        fig.update_layout(
            height=500,
            template="plotly_white",
            coloraxis_showscale=False
        )

        st.plotly_chart(
            fig,
            width="stretch"
        )


    # =====================================================
    # DISTRICT
    # =====================================================

    st.markdown("---")

    st.subheader(
        "📍 District-wise Comparison"
    )

    top_districts = (
        districts
        .head(10)
        .sort_values("Crime_Count")
    )

    fig = px.bar(
        top_districts,
        x="Crime_Count",
        y="District",
        orientation="h",
        title="Top 10 Districts",
        color="Crime_Count",
        color_continuous_scale="Plasma"
    )

    fig.update_layout(
        height=500,
        template="plotly_white",
        coloraxis_showscale=False
    )

    st.plotly_chart(
        fig,
        width="stretch"
    )


    # =====================================================
    # FUTURE PREVIEW
    # =====================================================

    st.markdown("---")

    st.subheader(
        "🔮 Future Trend Preview"
    )

    preview_year = latest_year + 1

    preview = predict_future_year(
        preview_year
    )

    p1, p2, p3, p4 = st.columns(4)

    with p1:

        st.metric(
            "📅 Next Year",
            preview["future_year"]
        )

    with p2:

        st.metric(
            "🔮 Estimated Count",
            f"{preview['predicted_crime_count']:,}"
        )

    with p3:

        st.metric(
            "📈 Trend",
            preview["trend"]
        )

    with p4:

        st.metric(
            "📊 Change",
            f"{preview['change_percentage']}%"
        )

    st.caption(
        "Future values are ML-based estimates, "
        "not actual future data."
    )


    # =====================================================
    # KEY INSIGHTS
    # =====================================================

    st.markdown("---")

    st.subheader(
        "💡 Key Project Insights"
    )

    highest_state = states.iloc[0]

    highest_district = districts.iloc[0]

    highest_category = categories.iloc[0]

    peak_year = yearly.loc[
        yearly["Crime_Count"].idxmax()
    ]

    i1, i2 = st.columns(2)


    with i1:

        st.info(
            f"🇮🇳 Highest state-level count: "
            f"{highest_state['State']} — "
            f"{int(highest_state['Crime_Count']):,}"
        )

        st.info(
            f"📍 Highest district-level count: "
            f"{highest_district['District']} — "
            f"{int(highest_district['Crime_Count']):,}"
        )


    with i2:

        st.info(
            f"⚠️ Largest crime category: "
            f"{highest_category['Crime_Category']} — "
            f"{int(highest_category['Crime_Count']):,}"
        )

        st.info(
            f"📅 Peak historical year: "
            f"{int(peak_year['Year'])} — "
            f"{int(peak_year['Crime_Count']):,}"
        )


# =========================================================
# CRIME ANALYSIS
# =========================================================

elif page == "📊 Crime Analysis":

    st.title(
        "📊 Crime Pattern Analysis"
    )

    st.write(
        "Explore historical crime patterns across "
        "years, states, districts and crime categories."
    )

    st.markdown("---")


    # =====================================================
    # FILTERS
    # =====================================================

    st.subheader(
        "🔎 Crime Data Filters"
    )

    filter_col1, filter_col2, filter_col3 = st.columns(3)


    with filter_col1:

        filter_year = st.selectbox(
            "📅 Select Year",
            [
                "All Years"
            ] + yearly["Year"].astype(str).tolist(),
            key="filter_year"
        )


    with filter_col2:

        filter_state = st.selectbox(
            "🇮🇳 Select State / UT",
            [
                "All States / UTs"
            ] + states["State"].tolist(),
            key="filter_state"
        )


    with filter_col3:

        filter_category = st.selectbox(
            "⚠️ Select Crime Category",
            [
                "All Categories"
            ] + categories["Crime_Category"].tolist(),
            key="filter_category"
        )


    # =====================================================
    # FILTERED DATA
    # =====================================================

    filtered_df = pd.read_csv(
        "data/processed/crime_analysis_clean.csv"
    )

    filtered_df.columns = (
        filtered_df.columns
        .str.strip()
        .str.lower()
    )


    crime_columns = [
        col
        for col in filtered_df.columns
        if col not in [
            "year",
            "state_name",
            "state_code",
            "district_name",
            "district_code",
            "registration_circles"
        ]
    ]


    if filter_year != "All Years":

        filtered_df = filtered_df[
            filtered_df["year"] == int(filter_year)
        ]


    if filter_state != "All States / UTs":

        filtered_df = filtered_df[
            filtered_df["state_name"] == filter_state
        ]


    if filter_category != "All Categories":

        filtered_count = pd.to_numeric(
            filtered_df[filter_category],
            errors="coerce"
        ).sum()

    else:

        filtered_count = (
            filtered_df[crime_columns]
            .apply(
                pd.to_numeric,
                errors="coerce"
            )
            .sum()
            .sum()
        )


    filtered_count = int(
        filtered_count
    )


    # =====================================================
    # FILTERED SUMMARY
    # =====================================================

    st.subheader(
        "📌 Filtered Crime Summary"
    )

    f1, f2, f3 = st.columns(3)


    with f1:

        st.metric(
            "📊 Filtered Crime Count",
            f"{filtered_count:,}"
        )


    with f2:

        st.metric(
            "📋 Matching Records",
            f"{len(filtered_df):,}"
        )


    with f3:

        st.metric(
            "🔎 Selected Year",
            filter_year
        )


    # =====================================================
    # FILTERED DISTRICT
    # =====================================================

    st.markdown("---")

    st.subheader(
        "📍 Filtered District Analysis"
    )


    if len(filtered_df) > 0:

        district_filtered = (
            filtered_df.copy()
        )


        if filter_category != "All Categories":

            district_filtered[
                "Filtered_Crimes"
            ] = pd.to_numeric(
                district_filtered[
                    filter_category
                ],
                errors="coerce"
            ).fillna(0)

        else:

            district_filtered[
                "Filtered_Crimes"
            ] = (
                district_filtered[
                    crime_columns
                ]
                .apply(
                    pd.to_numeric,
                    errors="coerce"
                )
                .fillna(0)
                .sum(axis=1)
            )


        district_summary = (
            district_filtered
            .groupby(
                "district_name"
            )["Filtered_Crimes"]
            .sum()
            .reset_index()
            .sort_values(
                "Filtered_Crimes",
                ascending=False
            )
            .head(10)
        )


        district_summary = (
            district_summary
            .sort_values(
                "Filtered_Crimes"
            )
        )


        fig = px.bar(
            district_summary,
            x="Filtered_Crimes",
            y="district_name",
            orientation="h",
            title="📍 Top Districts for Selected Filters",
            color="Filtered_Crimes",
            color_continuous_scale="Turbo"
        )


        fig.update_layout(
            height=500,
            template="plotly_white",
            coloraxis_showscale=False
        )


        st.plotly_chart(
            fig,
            width="stretch"
        )


    else:

        st.warning(
            "No records found for the selected filters."
        )


    st.markdown("---")


    # =====================================================
    # ANALYSIS TABS
    # =====================================================

    tab1, tab2, tab3, tab4 = st.tabs(
        [
            "📅 Year Analysis",
            "🇮🇳 State Analysis",
            "📍 District Analysis",
            "⚠️ Crime Categories"
        ]
    )


    # =====================================================
    # YEAR ANALYSIS
    # =====================================================

    with tab1:

        st.subheader(
            "📅 Year-wise Crime Analysis"
        )

        selected_year = st.selectbox(
            "Select Year",
            yearly["Year"].tolist(),
            key="analysis_year"
        )


        year_value = yearly[
            yearly["Year"] == selected_year
        ]["Crime_Count"].iloc[0]


        y1, y2, y3 = st.columns(3)


        with y1:

            st.metric(
                "📅 Selected Year",
                selected_year
            )


        with y2:

            st.metric(
                "📊 Recorded Count",
                f"{int(year_value):,}"
            )


        with y3:

            max_year = int(
                yearly.loc[
                    yearly["Crime_Count"].idxmax(),
                    "Year"
                ]
            )

            st.metric(
                "📈 Peak Year",
                max_year
            )


        st.markdown("---")


        fig = px.line(
            yearly,
            x="Year",
            y="Crime_Count",
            markers=True,
            title="📈 Historical Crime Trend",
            color_discrete_sequence=["#2563EB"]
        )


        fig.update_traces(
            line_width=5,
            marker_size=12
        )


        fig.update_layout(
            height=450,
            template="plotly_white"
        )


        st.plotly_chart(
            fig,
            width="stretch"
        )


        fig = px.bar(
            yearly,
            x="Year",
            y="Crime_Count",
            title="📊 Year-wise Crime Comparison",
            color="Crime_Count",
            color_continuous_scale="Turbo"
        )


        fig.update_layout(
            height=450,
            template="plotly_white",
            coloraxis_showscale=False
        )


        st.plotly_chart(
            fig,
            width="stretch"
        )


        st.dataframe(
            yearly,
            width="stretch",
            hide_index=True
        )


    # =====================================================
    # STATE ANALYSIS
    # =====================================================

    with tab2:

        st.subheader(
            "🇮🇳 State-wise Crime Analysis"
        )


        selected_state = st.selectbox(
            "🔎 Select State / UT",
            states["State"].tolist(),
            key="analysis_state"
        )


        selected_state_data = states[
            states["State"] == selected_state
        ].iloc[0]


        selected_state_count = int(
            selected_state_data[
                "Crime_Count"
            ]
        )


        s1, s2, s3 = st.columns(3)


        with s1:

            st.metric(
                "🇮🇳 Selected State",
                selected_state
            )


        with s2:

            st.metric(
                "📊 Recorded Count",
                f"{selected_state_count:,}"
            )


        with s3:

            st.metric(
                "🏆 Highest State",
                states.iloc[0]["State"]
            )


        st.markdown("---")


        top_states_analysis = (
            states
            .head(15)
            .sort_values("Crime_Count")
        )


        fig = px.bar(
            top_states_analysis,
            x="Crime_Count",
            y="State",
            orientation="h",
            title="🇮🇳 Top 15 States / UTs",
            color="Crime_Count",
            color_continuous_scale="Viridis"
        )


        fig.update_layout(
            height=600,
            template="plotly_white",
            coloraxis_showscale=False
        )


        st.plotly_chart(
            fig,
            width="stretch"
        )


        state_pie = states.head(8).copy()

        other_state_count = states.iloc[8:][
            "Crime_Count"
        ].sum()


        if other_state_count > 0:

            other_state = pd.DataFrame(
                {
                    "State": [
                        "Other States / UTs"
                    ],
                    "Crime_Count": [
                        other_state_count
                    ]
                }
            )


            state_pie = pd.concat(
                [
                    state_pie,
                    other_state
                ],
                ignore_index=True
            )


        fig = px.pie(
            state_pie,
            names="State",
            values="Crime_Count",
            hole=0.45,
            title="🍩 State-wise Crime Distribution",
            color_discrete_sequence=CHART_COLORS
        )


        fig.update_traces(
            textposition="inside",
            textinfo="percent"
        )


        fig.update_layout(
            height=550,
            template="plotly_white"
        )


        st.plotly_chart(
            fig,
            width="stretch"
        )


        st.dataframe(
            states,
            width="stretch",
            hide_index=True
        )


    # =====================================================
    # DISTRICT ANALYSIS
    # =====================================================

    with tab3:

        st.subheader(
            "📍 District-wise Crime Analysis"
        )


        selected_district = st.selectbox(
            "🔎 Select District",
            districts["District"].tolist(),
            key="analysis_district"
        )


        selected_district_data = districts[
            districts["District"] == selected_district
        ].iloc[0]


        selected_district_count = int(
            selected_district_data[
                "Crime_Count"
            ]
        )


        d1, d2, d3 = st.columns(3)


        with d1:

            st.metric(
                "📍 Selected District",
                selected_district
            )


        with d2:

            st.metric(
                "📊 Recorded Count",
                f"{selected_district_count:,}"
            )


        with d3:

            st.metric(
                "🏆 Highest District",
                districts.iloc[0]["District"]
            )


        st.markdown("---")


        top_districts_analysis = (
            districts
            .head(15)
            .sort_values("Crime_Count")
        )


        fig = px.bar(
            top_districts_analysis,
            x="Crime_Count",
            y="District",
            orientation="h",
            title="📍 Top 15 Districts",
            color="Crime_Count",
            color_continuous_scale="Plasma"
        )


        fig.update_layout(
            height=600,
            template="plotly_white",
            coloraxis_showscale=False
        )


        st.plotly_chart(
            fig,
            width="stretch"
        )


        st.dataframe(
            districts,
            width="stretch",
            hide_index=True
        )


    # =====================================================
    # CATEGORY ANALYSIS
    # =====================================================

    with tab4:

        st.subheader(
            "⚠️ Crime Category Analysis"
        )


        selected_category = st.selectbox(
            "🔎 Select Crime Category",
            categories["Crime_Category"].tolist(),
            key="analysis_category"
        )


        selected_category_data = categories[
            categories["Crime_Category"]
            == selected_category
        ].iloc[0]


        selected_category_count = int(
            selected_category_data[
                "Crime_Count"
            ]
        )


        c1, c2, c3 = st.columns(3)


        with c1:

            st.metric(
                "⚠️ Selected Category",
                selected_category
            )


        with c2:

            st.metric(
                "📊 Recorded Count",
                f"{selected_category_count:,}"
            )


        with c3:

            st.metric(
                "🏆 Largest Category",
                categories.iloc[0][
                    "Crime_Category"
                ]
            )


        st.markdown("---")


        top_categories_analysis = (
            categories
            .head(15)
            .sort_values("Crime_Count")
        )


        fig = px.bar(
            top_categories_analysis,
            x="Crime_Count",
            y="Crime_Category",
            orientation="h",
            title="⚠️ Top 15 Crime Categories",
            color="Crime_Count",
            color_continuous_scale="Turbo"
        )


        fig.update_layout(
            height=650,
            template="plotly_white",
            coloraxis_showscale=False
        )


        st.plotly_chart(
            fig,
            width="stretch"
        )


        category_pie = categories.head(10).copy()


        fig = px.pie(
            category_pie,
            names="Crime_Category",
            values="Crime_Count",
            hole=0.50,
            title="🍩 Crime Category Distribution",
            color_discrete_sequence=CHART_COLORS
        )


        fig.update_traces(
            textposition="inside",
            textinfo="percent"
        )


        fig.update_layout(
            height=600,
            template="plotly_white"
        )


        st.plotly_chart(
            fig,
            width="stretch"
        )


        st.dataframe(
            categories,
            width="stretch",
            hide_index=True
        )


# =========================================================
# FUTURE PREDICTION
# =========================================================

elif page == "🔮 Future Prediction":

    st.title(
        "🔮 Future Crime Trend Prediction"
    )


    st.write(
        "Estimate future crime trends using historical "
        "crime data and Machine Learning."
    )


    st.markdown("---")


    st.info(
        f"📅 Historical data is available from "
        f"{int(yearly['Year'].min())} to {latest_year}. "
        f"You can enter any future year after {latest_year}."
    )


    # =====================================================
    # YEAR INPUT
    # =====================================================

    st.subheader(
        "📅 Select Future Year"
    )


    future_year = st.number_input(
        "Enter the year you want to predict",
        min_value=latest_year + 1,
        max_value=2100,
        value=latest_year + 1,
        step=1
    )


    if st.button(
        "🔮 Generate Future Prediction",
        width="stretch"
    ):

        result = predict_future_year(
            int(future_year)
        )


        st.markdown("---")


        # =================================================
        # PREDICTION VALUES
        # =================================================

        st.subheader(
            "✨ Prediction Result"
        )


        p1, p2, p3, p4 = st.columns(4)


        with p1:

            st.metric(
                "📅 Future Year",
                result["future_year"]
            )


        with p2:

            st.metric(
                "🔮 Estimated Count",
                f"{result['predicted_crime_count']:,}"
            )


        with p3:

            st.metric(
                "📈 Trend",
                result["trend"]
            )


        with p4:

            st.metric(
                "📊 Change",
                f"{result['change_percentage']}%"
            )


        st.markdown("---")


        # =================================================
        # TREND MESSAGE
        # =================================================

        if result["trend"] == "Increasing":

            st.warning(
                f"📈 Estimated trend for "
                f"{future_year}: Increasing"
            )

        elif result["trend"] == "Decreasing":

            st.info(
                f"📉 Estimated trend for "
                f"{future_year}: Decreasing"
            )

        else:

            st.success(
                f"➡️ Estimated trend for "
                f"{future_year}: Stable"
            )


        if result["trend_level"] == "High":

            st.error(
                f"🔴 Trend Level: "
                f"{result['trend_level']}"
            )

        elif result["trend_level"] == "Moderate":

            st.warning(
                f"🟠 Trend Level: "
                f"{result['trend_level']}"
            )

        else:

            st.success(
                f"🟢 Trend Level: "
                f"{result['trend_level']}"
            )


        st.markdown("---")


        # =================================================
        # HISTORICAL VS FUTURE GRAPH
        # =================================================

        st.subheader(
            "📈 Historical vs Future Estimate"
        )


        historical = result[
            "historical_data"
        ].copy()


        historical["Type"] = "Historical"


        future_row = pd.DataFrame(
            {
                "Year": [
                    result["future_year"]
                ],
                "Crime_Count": [
                    result["predicted_crime_count"]
                ],
                "Type": [
                    "Future Estimate"
                ]
            }
        )


        combined = pd.concat(
            [
                historical,
                future_row
            ],
            ignore_index=True
        )


        fig = px.line(
            combined,
            x="Year",
            y="Crime_Count",
            color="Type",
            markers=True,
            title=(
                "📈 Historical Crime Pattern "
                "+ Future Estimate"
            ),
            color_discrete_map={
                "Historical": "#2563EB",
                "Future Estimate": "#E11D48"
            }
        )


        fig.update_traces(
            marker_size=12,
            line_width=4
        )


        fig.update_layout(
            height=500,
            template="plotly_white",
            hovermode="x unified"
        )


        st.plotly_chart(
            fig,
            width="stretch"
        )


        st.markdown("---")


        # =================================================
        # PREDICTION DETAILS
        # =================================================

        st.subheader(
            "🧠 Prediction Details"
        )


        d1, d2 = st.columns(2)


        with d1:

            st.markdown(
                f"""
### 🔮 Estimated {future_year}

**Estimated Crime Count**

# {result['predicted_crime_count']:,}

**Trend:** {result['trend']}

**Trend Level:** {result['trend_level']}
"""
            )


        with d2:

            st.markdown(
                f"""
### 📊 Change from Latest Data

**Latest Historical Year**

# {latest_year}

**Estimated Change**

# {result['change_percentage']}%

The estimate is calculated using the
historical yearly crime pattern.
"""
            )


        st.markdown("---")


        # =================================================
        # CRIME PREVENTION SECTION
        # =================================================

        st.subheader(
            "🔐 Crime Prevention & Action Suggestions"
        )


        st.write(
            "Based on the historical crime pattern and "
            "future trend estimate, CrimeVision AI provides "
            "the following preventive action areas."
        )


        st.markdown("---")


        prevention_col1, prevention_col2 = st.columns(2)


        # =================================================
        # LEFT COLUMN
        # =================================================

        with prevention_col1:

            st.markdown(
                """
### 📍 1. Identify High-Risk Areas

Districts and areas showing higher recorded
crime counts can be identified for increased
preventive monitoring and resource planning.


### 👮 2. Preventive Monitoring

Historical crime patterns and estimated trends
can help authorities plan preventive monitoring
for areas or periods showing increased activity.


### 🛡️ 3. Improve Cyber Crime Awareness

When cybercrime-related categories show
significant activity, awareness programmes
can focus on online fraud prevention,
phishing awareness and digital safety.
"""
            )


        # =================================================
        # RIGHT COLUMN
        # =================================================

        with prevention_col2:

            st.markdown(
                """
### 👥 4. Community Awareness

Public awareness programmes can help people
understand safety practices, reporting methods
and crime-prevention measures.


### 📊 5. Data-Driven Resource Planning

Historical and predicted crime patterns can
support better planning of available resources
and preventive activities.


### 🚨 6. Early Warning & Reporting

When an increasing trend is detected, the
system can act as an analytical indicator for
planning preventive measures and timely
reporting.
"""
            )


        st.markdown("---")


        st.info(
            "💡 CrimeVision AI does not predict a specific "
            "crime event. It analyzes historical patterns "
            "and provides future trend estimates that can "
            "support preventive planning."
        )


        st.markdown("---")


        # =================================================
        # DISCLAIMER
        # =================================================

        st.warning(
            "⚠️ This is a Machine Learning-based estimate "
            "using historical data. It is not actual future "
            "crime data and should not be interpreted as a "
            "guaranteed future event."
        )


# =========================================================
# CRIME RECORD MANAGEMENT
# =========================================================

elif page == "📁 Crime Records":

    st.title(
        "📁 Crime Record Management"
    )


    st.write(
        "Add, view, search, edit, download and delete "
        "crime records using the local SQLite database."
    )


    st.markdown("---")


    tab1, tab2 = st.tabs(
        [
            "➕ Add Record",
            "📋 View Records"
        ]
    )


    # =====================================================
    # ADD RECORD
    # =====================================================

    with tab1:

        st.subheader(
            "➕ Add New Crime Record"
        )


        with st.form(
            "crime_record_form"
        ):

            date = st.date_input(
                "Date"
            )


            state = st.text_input(
                "State"
            )


            city = st.text_input(
                "City / District"
            )


            crime_type = st.text_input(
                "Crime Type"
            )


            description = st.text_area(
                "Description"
            )


            status = st.selectbox(
                "Status",
                [
                    "Reported",
                    "Under Review",
                    "Closed"
                ]
            )


            submitted = st.form_submit_button(
                "💾 Save Record"
            )


            if submitted:

                if (
                    not state
                    or not city
                    or not crime_type
                ):

                    st.error(
                        "Please fill State, City/District "
                        "and Crime Type."
                    )

                else:

                    add_crime_record(
                        str(date),
                        state,
                        city,
                        crime_type,
                        description,
                        status
                    )


                    st.success(
                        "✅ Crime record saved successfully!"
                    )


    # =====================================================
    # VIEW RECORDS
    # =====================================================

    with tab2:

        st.subheader(
            "📋 Stored Crime Records"
        )


        records = get_all_records()


        if records:

            columns = [
                "ID",
                "Date",
                "State",
                "City",
                "Crime Type",
                "Description",
                "Status"
            ]


            records_df = pd.DataFrame(
                records,
                columns=columns
            )


            record_ids = [
                record[0]
                for record in records
            ]


            # =================================================
            # TOTAL RECORDS
            # =================================================

            st.metric(
                "📋 Total Stored Records",
                len(records_df)
            )


            # =================================================
            # SEARCH
            # =================================================

            st.markdown(
                "### 🔎 Search Crime Records"
            )


            search_text = st.text_input(
                "Search by State, City, Crime Type or Status",
                placeholder="Type something to search..."
            )


            if search_text:

                search_mask = (
                    records_df.astype(str)
                    .apply(
                        lambda row: row.str.contains(
                            search_text,
                            case=False,
                            na=False
                        ).any(),
                        axis=1
                    )
                )


                display_records = records_df[
                    search_mask
                ]

            else:

                display_records = records_df


            st.caption(
                f"Showing {len(display_records)} "
                f"of {len(records_df)} records"
            )


            st.dataframe(
                display_records,
                width="stretch",
                hide_index=True
            )


            # =================================================
            # DOWNLOAD
            # =================================================

            st.download_button(
                "⬇️ Download Crime Records CSV",

                data=display_records.to_csv(
                    index=False
                ).encode("utf-8"),

                file_name="crimevision_crime_records.csv",

                mime="text/csv",

                width="stretch"
            )


            # =================================================
            # EDIT
            # =================================================

            st.markdown("---")


            st.subheader(
                "✏️ Edit Crime Record"
            )


            edit_id = st.selectbox(
                "Select Record ID to Edit",
                record_ids,
                key="edit_record_id"
            )


            selected_record = next(
                record
                for record in records
                if record[0] == edit_id
            )


            edit_date = st.date_input(
                "Date",
                value=pd.to_datetime(
                    selected_record[1]
                ).date(),
                key="edit_date"
            )


            edit_state = st.text_input(
                "State",
                value=selected_record[2],
                key="edit_state"
            )


            edit_city = st.text_input(
                "City / District",
                value=selected_record[3],
                key="edit_city"
            )


            edit_crime_type = st.text_input(
                "Crime Type",
                value=selected_record[4],
                key="edit_crime_type"
            )


            edit_description = st.text_area(
                "Description",
                value=selected_record[5],
                key="edit_description"
            )


            status_options = [
                "Reported",
                "Under Review",
                "Closed"
            ]


            current_status = selected_record[6]


            if current_status in status_options:

                status_index = (
                    status_options.index(
                        current_status
                    )
                )

            else:

                status_index = 0


            edit_status = st.selectbox(
                "Status",
                status_options,
                index=status_index,
                key="edit_status"
            )


            if st.button(
                "✏️ Update Crime Record",
                width="stretch"
            ):

                if (
                    not edit_state
                    or not edit_city
                    or not edit_crime_type
                ):

                    st.error(
                        "Please fill State, City/District "
                        "and Crime Type."
                    )

                else:

                    update_crime_record(
                        edit_id,
                        str(edit_date),
                        edit_state,
                        edit_city,
                        edit_crime_type,
                        edit_description,
                        edit_status
                    )


                    st.success(
                        "✅ Crime record updated successfully!"
                    )


                    st.rerun()


            # =================================================
            # DELETE
            # =================================================

            st.markdown("---")


            st.subheader(
                "🗑️ Delete Record"
            )


            selected_id = st.selectbox(
                "Select Record ID",
                record_ids,
                key="delete_record_id"
            )


            if st.button(
                "🗑️ Delete Selected Record",
                width="stretch"
            ):

                delete_record(
                    selected_id
                )


                st.success(
                    "✅ Record deleted successfully!"
                )


                st.rerun()


        else:

            st.info(
                "📭 No crime records have been added yet."
            )