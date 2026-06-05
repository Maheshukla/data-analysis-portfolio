import streamlit as st

from utils.theme import apply_theme
from utils.data_loader import load_data
from components.sidebar import render_sidebar
from components.kpi_cards import render_kpis
from models.anomaly_detection import detect_anomalies
from utils.database import create_connection
import pandas as pd
from models.prediction_model import train_model
from utils.preprocessing import preprocess_data
import plotly.express as px
from utils.helpers import (
    column_exists,
    safe_category_values,
    safe_filter,
    safe_mean,
    safe_max,
    safe_min
)
from components.charts import (
    gender_distribution_chart,
    age_distribution_chart,
    department_chart,
    wait_time_chart,
    billing_chart,
    billing_by_condition_chart,
    race_distribution_chart,
    satisfaction_chart,
    gender_satisfaction_chart
)

# =========================
#PAGE CONFIG
#=========================

st.set_page_config(
    page_title="Healthcare Analytics",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =========================
#APPLY THEME
#=========================

apply_theme()


# =========================
# FILE UPLOAD
# =========================

uploaded_file = st.sidebar.file_uploader(

    "📤 Upload Healthcare CSV",

    type=["csv"]
)

# =========================
#LOAD DATA
#=========================

df = load_data(uploaded_file)
df = preprocess_data(df)

# =========================
#SIDEBAR
#=========================

filters = render_sidebar(df)

# =========================
# FILTER LOGIC
# =========================

filtered_df = df.copy()

# =========================
# GENDER FILTER
# =========================

if column_exists(
    filtered_df,
    "Patient Gender"
):

    filtered_df = safe_filter(
        filtered_df,
        "Patient Gender",
        filters["gender"]
    )

# =========================
# RACE FILTER
# =========================

if column_exists(
    filtered_df,
    "Patient Race"
):

    filtered_df = safe_filter(
        filtered_df,
        "Patient Race",
        filters["race"]
    )

# =========================
# DEPARTMENT FILTER
# =========================

if column_exists(
    filtered_df,
    "Department Referral"
):

    filtered_df = safe_filter(
        filtered_df,
        "Department Referral",
        filters["department"]
    )

# =========================
# DATABASE CONNECTION
# =========================

conn = create_connection(filtered_df)

# =========================
#HEADER
#=========================

# =========================
# HEADER
# =========================

st.container()

st.markdown(
    """
<div style="background: linear-gradient(135deg,#111827,#1e293b);
padding:30px;
border-radius:18px;
text-align:center;
margin-bottom:20px;
border:1px solid #374151;">

<h1 style="color:white;font-size:42px;margin-bottom:10px;">
🏥 Healthcare Analytics Dashboard
</h1>

<p style="color:#d1d5db;font-size:18px;">
Advanced Hospital Intelligence System
</p>

</div>
""",
    unsafe_allow_html=True
)

# =========================
#KPIs
#=========================

# =========================
# DATASET SUMMARY
# =========================

with st.expander(
    "📊 Dataset Quality Summary",
    expanded=False
):

    total_rows = filtered_df.shape[0]

    total_columns = filtered_df.shape[1]

    missing_values = (
        filtered_df.isnull()
        .sum()
        .sum()
    )

    duplicate_rows = (
        filtered_df.duplicated()
        .sum()
    )

    numeric_columns = (
        filtered_df
        .select_dtypes(
            include=["number"]
        )
        .columns
        .tolist()
    )

    categorical_columns = (
        filtered_df
        .select_dtypes(
            exclude=["number"]
        )
        .columns
        .tolist()
    )

    col1, col2, col3 = st.columns(3)

    with col1:

        st.metric(
            "Total Rows",
            f"{total_rows:,}"
        )

        st.metric(
            "Numeric Columns",
            len(numeric_columns)
        )

    with col2:

        st.metric(
            "Total Columns",
            total_columns
        )

        st.metric(
            "Categorical Columns",
            len(categorical_columns)
        )

    with col3:

        st.metric(
            "Missing Values",
            missing_values
        )

        st.metric(
            "Duplicate Rows",
            duplicate_rows
        )

    st.info(
        """
        ✅ Dataset preprocessing
        and validation completed.
        """
    )

render_kpis(filtered_df)

st.divider()

# =========================
#OVERVIEW SECTION
#=========================

tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8, tab9 = st.tabs([

    "Overview",

    "Patient Analysis",

    "Cost Analysis",

    "AI Insights",

    "Anomaly Detection",

    "SQL Analytics",

    "Forecasting",

    "Reports",

    "ML Prediction"

])

# =========================
#TAB 1
#=========================

with tab1:

    st.subheader(
        "📋 Healthcare Dataset Overview"
    )

    st.dataframe(
        filtered_df.head(20),
        use_container_width=True
    )

    st.divider()

    row1_col1, row1_col2 = st.columns(2)

    with row1_col1:

        try:

            race_distribution_chart(
                filtered_df
            )

        except Exception as e:

            st.warning(
                f"""
                ⚠️ Unable to render race chart.

                {str(e)}
                """
            )

    with row1_col2:

        try:

            satisfaction_chart(
                filtered_df
            )

        except Exception as e:

            st.warning(
                f"""
                ⚠️ Unable to render satisfaction chart.

                {str(e)}
                """
            )

    st.divider()

    try:

        gender_satisfaction_chart(
            filtered_df
        )

    except Exception as e:

        st.warning(
            f"""
            ⚠️ Unable to render gender satisfaction chart.

            {str(e)}
            """
        )

# =========================
#TAB 2
#=========================

with tab2:

    st.subheader(
        "👨‍⚕️ Patient Demographics"
    )

    row1_col1, row1_col2 = st.columns(2)

    with row1_col1:

        try:

            gender_distribution_chart(
                filtered_df
            )

        except Exception as e:

            st.warning(
                f"""
                ⚠️ Unable to render chart.

                {str(e)}
                """
            )

    with row1_col2:

        try:

            age_distribution_chart(
                filtered_df
            )

        except Exception as e:

            st.warning(
                f"""
                ⚠️ Unable to render age chart.

                {str(e)}
                """
            )

    st.divider()

    row2_col1, row2_col2 = st.columns(2)

    with row2_col1:

        try:

            department_chart(
                filtered_df
            )

        except Exception as e:

            st.warning(
                f"""
                ⚠️ Unable to render department chart.

                {str(e)}
                """
            )

    with row2_col2:

        try:

            wait_time_chart(
                filtered_df
            )

        except Exception as e:

            st.warning(
                f"""
                ⚠️ Unable to render wait time chart.

                {str(e)}
                """
            )

# =========================
#TAB 3
#=========================

with tab3:

    st.subheader(
        "💰 Healthcare Cost Analytics"
    )

    row1_col1, row1_col2 = st.columns(2)

    with row1_col1:

        try:

            billing_chart(
                filtered_df
            )

        except Exception as e:

            st.warning(
                f"""
                ⚠️ Unable to render billing chart.

                {str(e)}
                """
            )

    with row1_col2:

        try:

            billing_by_condition_chart(
                filtered_df
            )

        except Exception as e:

            st.warning(
                f"""
                ⚠️ Unable to render billing condition chart.

                {str(e)}
                """
            )

# =========================
#TAB 4
#=========================

with tab4:

    st.subheader(
        "🤖 AI Healthcare Insights"
    )

    # =========================
    # SAFE AI INSIGHTS
    # =========================

    if column_exists(
        filtered_df,
        "Department Referral"
    ):

        if not filtered_df[
            "Department Referral"
        ].dropna().empty:

            top_department = (
                filtered_df[
                    "Department Referral"
                ]
                .value_counts()
                .idxmax()
            )

        else:

            top_department = "No Data"

    else:

        top_department = "Column Missing"

    # =========================
    # SAFE WAIT TIME
    # =========================

    avg_wait = safe_mean(
        filtered_df,
        "Patient Waittime"
    )

    max_wait = safe_max(
        filtered_df,
        "Patient Waittime"
    )

    with st.expander(
        "💡 Executive Healthcare Insights",
        expanded=True
    ):

        st.success(
            f"""
            🏥 Most visited department:
            {top_department}
            """
        )

        st.info(
            f"""
            ⏳ Average patient wait time:
            {avg_wait:.1f} minutes
            """
        )

        st.warning(
            f"""
            🚨 Maximum patient wait time:
            {max_wait:.1f} minutes
            """
        )

        if avg_wait > 35:

            st.error(
                """
                ⚠️ High average wait time detected.
                Operational optimization recommended.
                """
            )

        else:

            st.success(
                """
                ✅ Patient wait times are under control.
                """
            )

    # =========================
# TAB 5
# =========================

with tab5:

    st.subheader(
        "🚨 Healthcare Anomaly Detection"
    )

    anomaly_column = st.selectbox(
        "Select Column",
        [
            "Patient Waittime",
            "Patient Satisfaction Score",
            "Patient Age"
        ]
    )

    anomaly_df = detect_anomalies(
        filtered_df,
        anomaly_column
    )

    anomaly_count = (
        anomaly_df["Anomaly"]
        == "Anomaly"
    ).sum()

    st.metric(
        "Detected Anomalies",
        anomaly_count
    )

    import plotly.express as px

    fig = px.scatter(
        anomaly_df,
        y=anomaly_column,
        color="Anomaly",
        title=f"Anomaly Detection - {anomaly_column}"
    )

    fig.update_layout(
        template="plotly_dark",
        height=600
    )

    st.plotly_chart(
        fig,
        use_container_width=True,
        key="anomaly_chart"
    )

    csv = anomaly_df.to_csv(index=False)

    st.download_button(
        "📥 Download Anomaly Report",
        csv,
        file_name="healthcare_anomalies.csv",
        mime="text/csv"
    )

    # =========================
# TAB 6
# =========================

with tab6:

    st.subheader(
        "🗄 Healthcare SQL Analytics"
    )

    # =========================
    # QUERY 1
    # =========================

    query1 = """
    SELECT
        [Department Referral],
        COUNT(*) AS Total_Patients
    FROM healthcare
    GROUP BY [Department Referral]
    ORDER BY Total_Patients DESC
    """

    department_sql = pd.read_sql_query(
        query1,
        conn
    )

    st.subheader(
        "🏥 Patients by Department"
    )

    fig1 = px.bar(
        department_sql,
        x="Department Referral",
        y="Total_Patients",
        color="Department Referral",
        title="Department Patient Volume"
    )

    fig1.update_layout(
        template="plotly_dark",
        height=500
    )

    st.plotly_chart(
        fig1,
        use_container_width=True,
        key="sql_department_chart"
    )

    # =========================
    # QUERY 2
    # =========================

    query2 = """
    SELECT
        [Patient Gender],
        AVG([Patient Waittime]) AS Avg_Wait
    FROM healthcare
    GROUP BY [Patient Gender]
    """

    wait_sql = pd.read_sql_query(
        query2,
        conn
    )

    st.subheader(
        "⏳ Average Wait Time by Gender"
    )

    fig2 = px.bar(
        wait_sql,
        x="Patient Gender",
        y="Avg_Wait",
        color="Patient Gender",
        title="Average Wait Time Analysis"
    )

    fig2.update_layout(
        template="plotly_dark",
        height=500
    )

    st.plotly_chart(
        fig2,
        use_container_width=True,
        key="sql_wait_chart"
    )

    # =========================
    # QUERY 3
    # =========================

    query3 = """
    SELECT
        [Patient Race],
        AVG([Patient Satisfaction Score]) AS Avg_Satisfaction
    FROM healthcare
    GROUP BY [Patient Race]
    """

    satisfaction_sql = pd.read_sql_query(
        query3,
        conn
    )

    st.subheader(
        "⭐ Satisfaction by Race"
    )

    st.dataframe(
        satisfaction_sql,
        use_container_width=True
    )

    # =========================
# TAB 7
# =========================

with tab7:

    st.subheader(
        "📈 Patient Volume Forecasting"
    )

    from prophet import Prophet

    forecast_df = filtered_df.copy()

    # =========================
    # DATE CONVERSION
    # =========================

    # =========================
    # SAFE DATE COLUMN CHECK
    # =========================

    if column_exists(
        forecast_df,
        "Patient Admission Date"
    ):

        forecast_df[
            "Patient Admission Date"
        ] = pd.to_datetime(

            forecast_df[
                "Patient Admission Date"
            ],

            dayfirst=True,
            errors="coerce"
        )

        forecast_df = forecast_df.dropna(
            subset=["Patient Admission Date"]
        )

    else:

        st.warning(
            """
            ⚠️ Patient Admission Date column not found.
            Forecasting unavailable.
            """
        )

        st.info(
            "Forecasting skipped safely."
        )

        st.stop()

    # =========================
    # DAILY PATIENT COUNT
    # =========================

    # =========================
    # SAFE FORECAST DATA
    # =========================

    if not forecast_df.empty:

        patient_forecast = (

            forecast_df.groupby(
                "Patient Admission Date"
            )

            .size()

            .reset_index(
                name="Patient_Count"
            )
        )

    else:

        st.warning(
            """
            ⚠️ No valid forecasting data available.
            """
        )

        st.info(
            "Forecasting skipped safely."
        )

        st.stop()

    patient_forecast.columns = [
        "ds",
        "y"
    ]

    # =========================
    # FORECAST PERIOD
    # =========================

    forecast_days = st.slider(
        "Forecast Days",
        30,
        365,
        90
    )

    # =========================
    # MODEL
    # =========================

    model = Prophet()

    model.fit(patient_forecast)

    # =========================
    # FUTURE DATA
    # =========================

    future = model.make_future_dataframe(
        periods=forecast_days
    )

    forecast = model.predict(future)

    # =========================
    # CHART
    # =========================

    fig = px.line(
        forecast,
        x="ds",
        y="yhat",
        title="Future Patient Volume Forecast"
    )

    fig.update_layout(
        template="plotly_dark",
        height=600
    )

    st.plotly_chart(
        fig,
        use_container_width=True,
        key="forecast_chart"
    )

    # =========================
    # FORECAST TABLE
    # =========================

    st.subheader(
        "📋 Forecast Data"
    )

    st.dataframe(
        forecast[
            [
                "ds",
                "yhat",
                "yhat_lower",
                "yhat_upper"
            ]
        ].tail(20),
        use_container_width=True
    )

    # =========================
    # AI INSIGHTS
    # =========================

    avg_future = (
        forecast["yhat"]
        .tail(forecast_days)
        .mean()
    )

    current_avg = (
        patient_forecast["y"]
        .mean()
    )

    with st.expander(
        "💡 Forecast Insights",
        expanded=True
    ):

        if avg_future > current_avg:

            st.success(
                """
                📈 Forecast predicts increasing patient load.
                """
            )

        else:

            st.warning(
                """
                📉 Forecast predicts stable/decreasing patient load.
                """
            )

        st.info(
            f"""
            Predicted average future patients:
            {avg_future:.1f}
            """
        )

        # =========================
# TAB 8
# =========================

with tab8:

    st.subheader(
        "📄 Healthcare Executive Report"
    )

    st.write(
        """
        Generate professional healthcare analytics reports.
        """
    )

    if st.button(
        "📥 Generate PDF Report"
    ):

        from fpdf import FPDF
        from datetime import datetime

        pdf = FPDF()

        pdf.add_page()

        # =========================
        # TITLE
        # =========================

        pdf.set_font(
            "Arial",
            "B",
            20
        )

        pdf.cell(
            200,
            10,
            txt="Healthcare Analytics Report",
            ln=True,
            align="C"
        )

        pdf.ln(10)

        # =========================
        # KPIs
        # =========================

        pdf.set_font(
            "Arial",
            size=12
        )

        pdf.cell(
            200,
            10,
            txt=f"Total Patients: {len(filtered_df)}",
            ln=True
        )

        pdf.cell(
            200,
            10,
            txt=f"Average Wait Time: {avg_wait:.1f}",
            ln=True
        )

        pdf.cell(
            200,
            10,
            txt=f"Maximum Wait Time: {max_wait:.1f}",
            ln=True
        )

        pdf.cell(
            200,
            10,
            txt=f"Top Department: {top_department}",
            ln=True
        )

        pdf.ln(10)

        # =========================
        # INSIGHTS
        # =========================

        pdf.set_font(
            "Arial",
            "B",
            16
        )

        pdf.cell(
            200,
            10,
            txt="Executive Insights",
            ln=True
        )

        pdf.set_font(
            "Arial",
            size=12
        )

        pdf.multi_cell(
            0,
            10,
            txt="""
Healthcare analytics indicates operational trends,
patient wait-time patterns, and department activity.

AI-driven insights suggest optimizing high-load
departments to improve patient satisfaction.
"""
        )

        pdf.ln(10)

        # =========================
        # DATE
        # =========================

        current_date = datetime.now().strftime(
            "%d-%m-%Y %H:%M:%S"
        )

        pdf.cell(
            200,
            10,
            txt=f"Generated On: {current_date}",
            ln=True
        )

        # =========================
        # SAVE FILE
        # =========================

        pdf.output(
            "healthcare_report.pdf"
        )

        # =========================
        # DOWNLOAD
        # =========================

        with open(
            "healthcare_report.pdf",
            "rb"
        ) as file:

            st.download_button(
                label="📄 Download PDF Report",
                data=file,
                file_name="healthcare_report.pdf",
                mime="application/pdf"
            )

        st.success(
            "✅ PDF report generated successfully!"
        )

        # =========================
# TAB 9
# =========================

with tab9:

    st.subheader(
        "🤖 Patient Wait Time Prediction"
    )

    # =========================
    # SAFE ML COLUMN CHECK
    # =========================

    required_ml_columns = [

        "Patient Age",

        "Patient Gender",

        "Patient Race",

        "Department Referral",

        "Patient Satisfaction Score",

        "Patient Waittime"
    ]

    missing_ml_columns = [

        col for col in required_ml_columns

        if col not in filtered_df.columns
    ]

    if missing_ml_columns:

        st.warning(
            f"""
            ⚠️ ML Prediction unavailable.

            Missing columns:
            {', '.join(missing_ml_columns)}
            """
        )

        st.info(
            "ML Prediction skipped safely."
        )

    # =========================
    # EMPTY DATAFRAME CHECK
    # =========================

    if filtered_df.empty:

        st.warning(
            """
            ⚠️ No data available for ML prediction.
            """
        )

        st.info(
            "ML Prediction skipped safely."
        )

    model, label_encoders, X, r2, mae = train_model(
        filtered_df
    )

    # =========================
    # USER INPUTS
    # =========================

    age_input = st.slider(
        "Patient Age",
        1,
        100,
        35,
        key="ml_age_slider"
    )

    gender_input = st.selectbox(
        "Patient Gender",
        filtered_df[
            "Patient Gender"
        ].dropna().unique(),
        key="ml_gender_input"
    )

    race_input = st.selectbox(
        "Patient Race",
        filtered_df[
            "Patient Race"
        ].dropna().unique(),
        key="ml_race_input"
    )

    department_options = (
        filtered_df[
            "Department Referral"
        ]
        .dropna()
        .unique()
    )

    department_input = st.selectbox(
        "Department Referral",
        department_options,
        key="ml_department_input"
    )

    satisfaction_input = st.slider(
        "Patient Satisfaction Score",
        1,
        10,
        5,
        key="ml_satisfaction_input"
    )

    # =========================
    # INPUT DATA
    # =========================

    input_df = pd.DataFrame({

        "Patient Age": [
            age_input
        ],

        "Patient Gender": [

            label_encoders[
                "Patient Gender"
            ].transform([
                gender_input
            ])[0]

        ],

        "Patient Race": [

            label_encoders[
                "Patient Race"
            ].transform([
                race_input
            ])[0]

        ],

        "Department Referral": [

            label_encoders[
                "Department Referral"
            ].transform([
                department_input
            ])[0]

        ],

        "Patient Satisfaction Score": [
            satisfaction_input
        ]

    })

    # =========================
    # PREDICTION
    # =========================

    # =========================
    # SAFE PREDICTION
    # =========================

    try:

        prediction = model.predict(
            input_df
        )

        st.metric(
            "Predicted Wait Time",
            f"{prediction[0]:.1f} min"
        )

        st.info(
            f"Model Accuracy (R²): {r2:.2f}"
        )

        st.info(
            f"Mean Absolute Error: {mae:.2f}"
        )

    except Exception as e:

        st.error(
            f"""
            ❌ Prediction Error:

            {str(e)}
            """
        )