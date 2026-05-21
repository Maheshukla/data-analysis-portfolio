import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import r2_score, mean_absolute_error
from xgboost import XGBRegressor
from fpdf import FPDF
from datetime import datetime
from fpdf import FPDF
from prophet import Prophet
from sklearn.ensemble import IsolationForest
import sqlite3
import math

# Page Config
st.set_page_config(
    page_title="Superstore Sales Dashboard",
    layout="wide"
)

# =========================
# AUTHENTICATION CONFIG
# =========================

names = ["Admin User"]
usernames = ["admin"]
passwords = ["admin123"]

# Simple authentication fallback if streamlit_authenticator isn't installed
# =========================
# SIMPLE LOGIN SYSTEM
# =========================

if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

# LOGIN PAGE
if not st.session_state.logged_in:

    st.title("🔐 Login")

    username = st.text_input("Username")

    password = st.text_input(
        "Password",
        type="password"
    )

    if st.button("Login"):

        if username == "admin" and password == "admin123":

            st.session_state.logged_in = True

            st.rerun()

        else:

            st.error("Incorrect Username or Password")

# DASHBOARD
else:

    st.sidebar.success("Welcome Admin User")

    if st.sidebar.button("Logout"):

        st.session_state.logged_in = False

        st.rerun()

    # Title
    st.title("📊 Superstore Sales Dashboard")

    st.markdown("""
    <div class="sticky-tabs-wrapper">
    """, unsafe_allow_html=True)

    st.markdown("""
    <style>

    /* SIDEBAR FULL FIX */

    section[data-testid="stSidebar"] {
        background-color: #111827 !important;
        color: white !important;
    }

    section[data-testid="stSidebar"] * {
        color: white !important;
    }

    /* Sidebar Selectbox */

    section[data-testid="stSidebar"] .stMultiSelect {
        background-color: #1f2937 !important;
        border-radius: 10px;
        padding: 5px;
    }

    /* Sidebar Buttons */

    section[data-testid="stSidebar"] button {
        background-color: #374151 !important;
        color: white !important;
        border-radius: 10px;
    }

    /* Sidebar Header */

    section[data-testid="stSidebar"] h1,
    section[data-testid="stSidebar"] h2,
    section[data-testid="stSidebar"] h3 {
        color: white !important;
    }

    /* =========================
    REAL STICKY TABS FIX
    ========================= */

    .stTabs {
        position: sticky;
        top: 0;
        z-index: 9999;
        background-color: #0E1117;
        padding-top: 10px;
        padding-bottom: 10px;
    }

    div[data-baseweb="tab-list"] {
        gap: 10px;
        overflow-x: auto;
        white-space: nowrap;
        scrollbar-width: none;
    }

    div[data-baseweb="tab"] {
        background-color: #111827;
        border-radius: 10px;
        padding: 10px 18px;
    }

    </style>
    """, unsafe_allow_html=True)

    # =========================
    # SQLITE DATABASE SETUP
    # =========================

    conn = sqlite3.connect(':memory:')

    cursor = conn.cursor()

    # =========================
    # FILE UPLOAD SYSTEM
    # =========================

    uploaded_file = st.sidebar.file_uploader(
        "📂 Upload CSV File",
        type=["csv"]
    )

    # Required Columns
    required_columns = [
        'Sales',
        'Profit',
        'Category',
        'Region',
        'State',
        'Segment',
        'Sub-Category',
        'City',
        'Ship Mode'
    ]

    if uploaded_file is not None:

        try:

            uploaded_df = pd.read_csv(uploaded_file)

            # Check Required Columns
            if all(
                col in uploaded_df.columns
                for col in required_columns
            ):

                csv_df = uploaded_df

                st.sidebar.success(
                    "✅ Compatible dataset uploaded!"
                )

            else:

                st.sidebar.warning(
                    "⚠ Invalid dataset format. "
                    "Loading default Superstore dataset."
                )

                csv_df = pd.read_csv(
                    "project1_sales_analysis/data/SampleSuperstore.csv"
                )

        except:

            st.sidebar.error(
                "❌ Error reading file. "
                "Loading default dataset."
            )

            csv_df = pd.read_csv(
                "project1_sales_analysis/data/SampleSuperstore.csv"
            )

    else:

        # Default Dataset
        csv_df = pd.read_csv(
            "project1_sales_analysis/data/SampleSuperstore.csv"
        )

    # Save Dataset to SQL
    csv_df.to_sql(
        'superstore',
        conn,
        if_exists='replace',
        index=False
    )

    # Load Dataset
    filtered_df = pd.read_sql_query(
        "SELECT * FROM superstore",
        conn
    )

    # Clean Columns
    filtered_df.columns = filtered_df.columns.str.strip()

    # ======================
    # SIDEBAR FILTERS
    # ======================

    st.sidebar.header("Filter Data")

    selected_region = st.sidebar.multiselect(
        "Select Region",
        options=filtered_df['Region'].unique(),
        default=filtered_df['Region'].unique()
    )

    if not selected_region:
        selected_region = filtered_df['Region'].unique()

    selected_category = st.sidebar.multiselect(
        "Select Category",
        options=filtered_df['Category'].unique(),
        default=filtered_df['Category'].unique()
    )

    if not selected_category:
        selected_category = filtered_df['Category'].unique()

    selected_segment = st.sidebar.multiselect(
        "Select Segment",
        options=filtered_df['Segment'].unique(),
        default=filtered_df['Segment'].unique()
    )

    if not selected_segment:
        selected_segment = filtered_df['Segment'].unique()

    # Dynamic Sub-Category Filter

    filtered_subcategories = filtered_df[
        filtered_df['Category'].isin(selected_category)
    ]['Sub-Category'].unique()

    selected_subcategory = st.sidebar.multiselect(
        "Select Sub-Category",
        options=filtered_subcategories,
        default=filtered_subcategories
    )

    if not selected_subcategory:
        selected_subcategory = filtered_subcategories

    # Dynamic State Filter

    filtered_states = filtered_df[
        filtered_df['Region'].isin(selected_region)
    ]['State'].unique()

    selected_state = st.sidebar.multiselect(
        "Select State",
        options=filtered_states,
        default=filtered_states
    )

    if not selected_state:
        selected_state = filtered_states
    
    # Dynamic City Filter

    filtered_cities = filtered_df[
        filtered_df['State'].isin(selected_state)
    ]['City'].unique()

    selected_city = st.sidebar.multiselect(
        "Select City",
        options=filtered_cities,
        default=filtered_cities
    )

    if not selected_city:
        selected_city = filtered_cities

    selected_shipmode = st.sidebar.multiselect(
        "Select Ship Mode",
        options=filtered_df['Ship Mode'].unique(),
        default=filtered_df['Ship Mode'].unique()
    )

    if not selected_shipmode:
        selected_shipmode = filtered_df['Ship Mode'].unique()

    sales_range = st.sidebar.slider(
        "Select Sales Range",
        float(filtered_df['Sales'].min()),
        float(filtered_df['Sales'].max()),
        (
            float(filtered_df['Sales'].min()),
            float(filtered_df['Sales'].max())
        )
    )

    

    profit_range = st.sidebar.slider(
        "Select Profit Range",
        float(filtered_df['Profit'].min()),
        float(filtered_df['Profit'].max()),
        (
            float(filtered_df['Profit'].min()),
            float(filtered_df['Profit'].max())
        )
    )
    

    # Filter Dataset
    if not selected_subcategory:
        selected_subcategory = filtered_df['Sub-Category'].unique()

    filtered_data = filtered_df[

        (filtered_df['Region'].isin(selected_region)) &

        (filtered_df['Category'].isin(selected_category)) &

        (filtered_df['Segment'].isin(selected_segment)) &

        (filtered_df['Sub-Category'].isin(selected_subcategory)) &

        (filtered_df['State'].isin(selected_state)) &

        (filtered_df['City'].isin(selected_city)) &

        (filtered_df['Ship Mode'].isin(selected_shipmode)) &

        (filtered_df['Sales'] >= sales_range[0]) &

        (filtered_df['Sales'] <= sales_range[1]) &

        (filtered_df['Profit'] >= profit_range[0]) &

        (filtered_df['Profit'] <= profit_range[1])

    ]

    st.sidebar.subheader("🚨 Anomaly Detection")

    numeric_cols = filtered_data.select_dtypes(include=['number']).columns.tolist()

    selected_anomaly_col = st.sidebar.selectbox(
        "Select Column for Anomaly Detection",
        numeric_cols
    )

    contamination = st.sidebar.slider(
        "Anomaly Sensitivity",
        0.01,
        0.20,
        0.05
    )

    # Download Button
    st.sidebar.download_button(
        label="Download Filtered Data",
        data=filtered_data.to_csv(index=False),
        file_name='filtered_superstore_data.csv',
        mime='text/csv'
    )

    st.markdown("## 📈 Business Performance Overview")

    # ======================
    # KPI SECTION
    # ======================

    total_sales = filtered_data['Sales'].sum()
    total_profit = filtered_data['Profit'].sum()
    avg_discount = filtered_data['Discount'].mean()
    total_orders = len(filtered_data)

    profit_margin = (
        total_profit / total_sales
    ) * 100

    col1, col2, col3, col4, col5 = st.columns(5)

    col1.metric("Total Sales", f"${total_sales:,.0f}")
    col2.metric("Total Profit", f"${total_profit:,.0f}")
    col3.metric("Average Discount", f"{avg_discount:.2f}")
    col4.metric("Total Orders", total_orders)
    col5.metric("Profit Margin", f"{profit_margin:.2f}%")

    st.divider()

    # ======================
    # TABS
    # ======================

    tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8, tab9, tab10, tab11, tab12, tab13, tab14 = st.tabs([
        "Overview",
        "Regional Analysis",
        "Product Analysis",
        "Profit Analysis",
        "Correlation Analysis",
        "Sub-Category Analysis",
        "Data Table",
        "Advanced Analytics",
        "ML Prediction",
        "ML Insights",
        "Reports",
        "Forecasting",
        "SQL Analytics",
        "Benford Analysis"
    ])

    # ======================
    # SALES BY CATEGORY
    # ======================

    with tab1:

        st.subheader("Sales by Category")

        category_sales = (
            filtered_data.groupby('Category')['Sales']
            .sum()
        )

        fig = px.bar(
            category_sales,
            x=category_sales.index,
            y='Sales',
            title="Sales by Category",
            color=category_sales.index
        )

        st.plotly_chart(fig, use_container_width=True)

    with tab2:

        # ======================
        # PROFIT BY REGION
        # ======================

        st.subheader("Profit by Region")

        region_profit = (
            filtered_data.groupby('Region')['Profit']
            .sum()
        )

        fig2 = px.bar(
            region_profit,
            x=region_profit.index,
            y='Profit',
            title="Profit by Region",
            color=region_profit.index
        )

        st.plotly_chart(fig2, use_container_width=True)

        # ======================
        # TOP STATES
        # ======================

        st.subheader("Top 10 Profitable States")

        top_states = (
            filtered_data.groupby('State')['Profit']
            .sum()
            .sort_values(ascending=False)
            .head(10)
        )

        fig3, ax3 = plt.subplots(figsize=(10,5))

        top_states.plot(
            kind='bar',
            color='green',
            ax=ax3
        )

        ax3.set_ylabel("Profit")
        ax3.set_xlabel("State")

        st.pyplot(fig3)

    with tab3:

        # ======================
        # SALES DISTRIBUTION
        # ======================

        st.subheader("Sales Distribution by Category")

        category_sales_pie = (
            filtered_data.groupby('Category')['Sales']
            .sum()
        )

        fig4, ax4 = plt.subplots(figsize=(6,6))

        ax4.pie(
            category_sales_pie,
            labels=category_sales_pie.index,
            autopct='%1.1f%%'
        )

        st.pyplot(fig4)

    with tab4:

        # ======================
        # LOSS MAKING STATES
        # ======================

        st.subheader("Top Loss Making States")

        loss_states = (
            filtered_data.groupby('State')['Profit']
            .sum()
            .sort_values()
            .head(10)
        )

        fig5, ax5 = plt.subplots(figsize=(10,5))

        loss_states.plot(
            kind='bar',
            color='red',
            ax=ax5
        )

        ax5.set_ylabel("Profit")
        ax5.set_xlabel("State")

        st.pyplot(fig5)

    with tab5:

        st.subheader("Correlation Heatmap")

        correlation_matrix = filtered_data.corr(numeric_only=True)

        fig6, ax6 = plt.subplots(figsize=(8,6))

        sns.heatmap(
            correlation_matrix,
            annot=True,
            cmap='coolwarm',
            ax=ax6
        )

        st.pyplot(fig6)

    with tab6:

        st.subheader("Top 10 Sub-Categories by Sales")

        top_sub_sales = (
            filtered_data.groupby('Sub-Category')['Sales']
            .sum()
            .sort_values(ascending=False)
            .head(10)
        )

        fig7 = px.bar(
            top_sub_sales,
            x=top_sub_sales.index,
            y='Sales',
            title="Top Sub-Categories by Sales",
            color=top_sub_sales.index
        )

        st.plotly_chart(fig7, use_container_width=True)

        # ======================

        st.subheader("Top 10 Sub-Categories by Profit")

        top_sub_profit = (
            filtered_data.groupby('Sub-Category')['Profit']
            .sum()
            .sort_values(ascending=False)
            .head(10)
        )

        fig8 = px.bar(
            top_sub_profit,
            x=top_sub_profit.index,
            y='Profit',
            title="Top Sub-Categories by Profit",
            color=top_sub_profit.index
        )

        st.plotly_chart(fig8, use_container_width=True)

        # ======================

        st.subheader("Top Loss Making Sub-Categories")

        loss_sub = (
            filtered_data.groupby('Sub-Category')['Profit']
            .sum()
            .sort_values()
            .head(10)
        )

        fig9 = px.bar(
            loss_sub,
            x=loss_sub.index,
            y='Profit',
            title="Loss Making Sub-Categories",
            color=loss_sub.index
        )

        st.plotly_chart(fig9, use_container_width=True)

    with tab7:

        st.subheader("Filtered Dataset")

        st.dataframe(
            filtered_data,
            use_container_width=True
        )

        # ======================

        st.subheader("Dataset Summary")

        st.write(filtered_data.describe())

    with tab8:

        st.subheader("Sales vs Profit Analysis")

        fig10 = px.scatter(
            filtered_data,
            x='Sales',
            y='Profit',
            color='Category',
            size='Quantity',
            hover_data=['Sub-Category'],
            title="Sales vs Profit by Category"
        )

        st.plotly_chart(fig10, use_container_width=True)

        # ======================

        st.subheader("Discount Impact on Profit")

        fig11 = px.scatter(
            filtered_data,
            x='Discount',
            y='Profit',
            color='Category',
            size='Sales',
            hover_data=['Sub-Category'],
            title="Discount vs Profit"
        )

        st.plotly_chart(fig11, use_container_width=True)

        st.divider()

        st.subheader("🚨 Anomaly Detection")

        if selected_anomaly_col:

            anomaly_df = filtered_data[[selected_anomaly_col]].dropna()

            model = IsolationForest(
                contamination=contamination,
                random_state=42
            )

            anomaly_df['Anomaly'] = model.fit_predict(
                anomaly_df[[selected_anomaly_col]]
            )

            anomaly_df['Anomaly'] = anomaly_df['Anomaly'].map({
                1: 'Normal',
                -1: 'Anomaly'
            })

            anomaly_count = (
                anomaly_df['Anomaly'] == 'Anomaly'
            ).sum()

            st.metric(
                "Detected Anomalies",
                anomaly_count
            )

            fig_anomaly = px.scatter(
                anomaly_df,
                y=selected_anomaly_col,
                color='Anomaly',
                title=f'Anomaly Detection - {selected_anomaly_col}'
            )

            st.plotly_chart(
                fig_anomaly,
                use_container_width=True
            )

            csv = anomaly_df.to_csv(index=False)

            st.download_button(
                "⬇ Download Anomaly Report",
                csv,
                "anomaly_report.csv",
                "text/csv"
            )

        @st.cache_resource
        def train_model(data):

            ml_df = data.copy()

            required_cols = [
                'Sales',
                'Quantity',
                'Discount',
                'Profit',
                'Category',
                'Region',
                'Segment',
                'Ship Mode',
                'Sub-Category',
                'State'
            ]

            ml_df = ml_df[required_cols].dropna()

            label_encoders = {}

            categorical_cols = [
                'Category',
                'Region',
                'Segment',
                'Ship Mode',
                'Sub-Category',
                'State'
            ]

            for col in categorical_cols:

                le = LabelEncoder()

                ml_df[col] = le.fit_transform(
                    ml_df[col]
                )

                label_encoders[col] = le

            X = ml_df.drop('Profit', axis=1)

            y = ml_df['Profit']

            X_train, X_test, y_train, y_test = train_test_split(
                X,
                y,
                test_size=0.2,
                random_state=42
            )

            model = XGBRegressor(
                n_estimators=300,
                learning_rate=0.05,
                max_depth=6,
                random_state=42
            )

            model.fit(X_train, y_train)

            y_pred = model.predict(X_test)

            r2 = r2_score(y_test, y_pred)

            mae = mean_absolute_error(y_test, y_pred)

            return (
                model,
                label_encoders,
                X,
                y_test,
                y_pred,
                r2,
                mae
            )


    # =========================
    # ML PREDICTION TAB
    # =========================

    with tab9:

        st.subheader("🤖 Advanced Profit Prediction")

        model, label_encoders, X, y_test, y_pred, r2, mae = train_model(filtered_df)

        # =========================
        # USER INPUTS
        # =========================

        sales_input = st.number_input(
            "Enter Sales Amount",
            min_value=0.0,
            value=500.0
        )

        quantity_input = st.number_input(
            "Enter Quantity",
            min_value=1,
            value=2
        )

        discount_input = st.slider(
            "Select Discount",
            0.0,
            1.0,
            0.2
        )

        pred_category = st.selectbox(
            "Select Category",
            filtered_df['Category'].unique()
        )

        pred_region = st.selectbox(
            "Select Region",
            filtered_df['Region'].unique()
        )

        pred_segment = st.selectbox(
            "Select Segment",
            filtered_df['Segment'].unique()
        )

        pred_ship = st.selectbox(
            "Select Ship Mode",
            filtered_df['Ship Mode'].unique()
        )

        pred_sub = st.selectbox(
            "Select Sub-Category",
            filtered_df['Sub-Category'].unique()
        )

        pred_state = st.selectbox(
            "Select State",
            filtered_df['State'].unique()
        )

        # =========================
        # PREPARE INPUT DATA
        # =========================

        input_data = pd.DataFrame({

            'Sales': [sales_input],

            'Quantity': [quantity_input],

            'Discount': [discount_input],

            'Category': [
                label_encoders['Category']
                .transform([pred_category])[0]
            ],

            'Region': [
                label_encoders['Region']
                .transform([pred_region])[0]
            ],

            'Segment': [
                label_encoders['Segment']
                .transform([pred_segment])[0]
            ],

            'Ship Mode': [
                label_encoders['Ship Mode']
                .transform([pred_ship])[0]
            ],

            'Sub-Category': [
                label_encoders['Sub-Category']
                .transform([pred_sub])[0]
            ],

            'State': [
                label_encoders['State']
                .transform([pred_state])[0]
            ]

        })

        # =========================
        # PREDICTION
        # =========================

        prediction = model.predict(input_data)

        # =========================
        # DISPLAY RESULTS
        # =========================

        st.info(
            f"Model Accuracy (R² Score): {r2:.2f}"
        )

        st.info(
            f"Mean Absolute Error: {mae:.2f}"
        )

        st.success(
            f"Predicted Profit: ${prediction[0]:,.2f}"
        )


    # =========================
    # ML INSIGHTS TAB
    # =========================

    with tab10:

        model, label_encoders, X, y_test, y_pred, r2, mae = train_model(filtered_df)

        st.subheader("📊 Feature Importance Analysis")

        importance_df = pd.DataFrame({

            'Feature': X.columns,

            'Importance': model.feature_importances_

        })

        importance_df = importance_df.sort_values(
            by='Importance',
            ascending=False
        )

        fig_importance = px.bar(
            importance_df,
            x='Importance',
            y='Feature',
            orientation='h',
            color='Importance',
            title='Feature Importance for Profit Prediction'
        )

        st.plotly_chart(
            fig_importance,
            use_container_width=True
        )

        st.dataframe(
            importance_df,
            use_container_width=True
        )

        # =========================
        # ACTUAL VS PREDICTED
        # =========================

        st.divider()

        st.subheader("📈 Actual vs Predicted Profit")

        comparison_df = pd.DataFrame({

            'Actual Profit': y_test,

            'Predicted Profit': y_pred

        })

        fig_compare = px.scatter(

            comparison_df,

            x='Actual Profit',

            y='Predicted Profit',

            title='Actual vs Predicted Profit',

            opacity=0.7

        )

        st.plotly_chart(
            fig_compare,
            use_container_width=True
        )

        st.dataframe(
            comparison_df.head(20),
            use_container_width=True
        )

        # =========================
        # BUSINESS INSIGHTS
        # =========================

        st.divider()

            # =========================
        # BUSINESS INSIGHTS
        # =========================

        st.divider()

        top_category = (
            filtered_data.groupby('Category')['Profit']
            .sum()
            .idxmax()
        )

        worst_region = (
            filtered_data.groupby('Region')['Profit']
            .sum()
            .idxmin()
        )

        best_subcategory = (
            filtered_data.groupby('Sub-Category')['Profit']
            .sum()
            .idxmax()
        )

        avg_discount = filtered_data['Discount'].mean()

        with st.expander(
            "💡 AI Business Insights",
            expanded=True
        ):

            st.success(
                f"🏆 Most Profitable Category: {top_category}"
            )

            st.warning(
                f"⚠️ Lowest Performing Region: {worst_region}"
            )

            st.info(
                f"📈 Best Sub-Category: {best_subcategory}"
            )

            if avg_discount > 0.3:

                st.error(
                    "🚨 High average discount detected. "
                    "Profit margins may decrease."
                )

            else:

                st.success(
                    "✅ Discount levels are under control."
                )

    # =========================
    # REPORTS TAB
    # =========================

    with tab11:

        st.subheader("📄 Business Report Generator")

        st.write(
            "Generate and download an executive business report."
        )

        if st.button("📥 Generate PDF Report"):

            # =========================
            # CREATE PDF
            # =========================

            pdf = FPDF()

            pdf.add_page()

            pdf.set_font("Arial", "B", 18)

            pdf.cell(
                200,
                10,
                txt="Superstore Analytics Report",
                ln=True,
                align='C'
            )

            pdf.ln(10)

            pdf.set_font("Arial", size=12)

            # =========================
            # KPI SUMMARY
            # =========================

            pdf.cell(
                200,
                10,
                txt=f"Total Sales: ${total_sales:,.2f}",
                ln=True
            )

            pdf.cell(
                200,
                10,
                txt=f"Total Profit: ${total_profit:,.2f}",
                ln=True
            )

            pdf.cell(
                200,
                10,
                txt=f"Profit Margin: {profit_margin:.2f}%",
                ln=True
            )

            pdf.cell(
                200,
                10,
                txt=f"ML Model Accuracy (R²): {r2:.2f}",
                ln=True
            )

            pdf.ln(10)

            # =========================
            # AI INSIGHTS
            # =========================

            pdf.set_font("Arial", "B", 14)

            pdf.cell(
                200,
                10,
                txt="AI Business Insights",
                ln=True
            )

            pdf.set_font("Arial", size=12)

            pdf.cell(
                200,
                10,
                txt=f"Most Profitable Category: {top_category}",
                ln=True
            )

            pdf.cell(
                200,
                10,
                txt=f"Lowest Performing Region: {worst_region}",
                ln=True
            )

            pdf.cell(
                200,
                10,
                txt=f"Best Sub-Category: {best_subcategory}",
                ln=True
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
            # SAVE PDF
            # =========================

            pdf.output("business_report.pdf")

            # =========================
            # DOWNLOAD BUTTON
            # =========================

            with open(
                "business_report.pdf",
                "rb"
            ) as file:

                st.download_button(

                    label="📄 Download Report",

                    data=file,

                    file_name="business_report.pdf",

                    mime="application/pdf"

                )

            st.success(
                "✅ PDF report generated successfully!"
            )

        st.write(filtered_df.columns)

    # =========================
    # FORECASTING TAB
    # =========================

    with tab12:

        st.subheader("📈 Sales Forecasting")

        st.write(
            "Predict future sales trends using Prophet."
        )

        # =========================
        # LOAD DATA
        # =========================

        forecast_df = filtered_df.copy()

        forecast_df = pd.read_csv(
            "project1_sales_analysis/data/Sample - Superstore.csv",
            encoding='latin1'
        )

        forecast_df.columns = (
            forecast_df.columns.str.strip()
        )


        # =========================
        # AUTO DETECT DATE COLUMN
        # =========================

        possible_date_cols = [
            col for col in forecast_df.columns
            if 'date' in col.lower()
        ]

        if len(possible_date_cols) == 0:

            st.error(
                "❌ No date column found in dataset."
            )

        else:

            date_col = possible_date_cols[0]

            st.success(
                f"✅ Using Date Column: {date_col}"
            )

            # =========================
            # DATE CONVERSION
            # =========================

            forecast_df[date_col] = pd.to_datetime(
                forecast_df[date_col],
                errors='coerce'
            )

            forecast_df = forecast_df.dropna(
                subset=[date_col]
            )

            # =========================
            # DAILY SALES
            # =========================

            sales_forecast = (
                forecast_df.groupby(date_col)['Sales']
                .sum()
                .reset_index()
            )

            sales_forecast.columns = ['ds', 'y']

            # =========================
            # FORECAST PERIOD
            # =========================

            periods = st.slider(
                "Select Forecast Period (Days)",
                min_value=30,
                max_value=365,
                value=90
            )

            # =========================
            # TRAIN MODEL
            # =========================

            model = Prophet()

            model.fit(sales_forecast)

            # =========================
            # FUTURE DATES
            # =========================

            future = model.make_future_dataframe(
                periods=periods
            )

            forecast = model.predict(future)

            # =========================
            # FORECAST CHART
            # =========================

            st.subheader("📊 Forecasted Sales Trend")

            fig_forecast = px.line(
                forecast,
                x='ds',
                y='yhat',
                title='Future Sales Forecast'
            )

            st.plotly_chart(
                fig_forecast,
                use_container_width=True
            )

            # =========================
            # FORECAST TABLE
            # =========================

            st.subheader("📋 Forecast Data")

            st.dataframe(
                forecast[
                    ['ds', 'yhat', 'yhat_lower', 'yhat_upper']
                ].tail(20),
                use_container_width=True
            )

            # =========================
            # BUSINESS INSIGHTS
            # =========================

            future_sales = (
                forecast['yhat']
                .tail(periods)
                .mean()
            )

            current_sales = (
                sales_forecast['y']
                .mean()
            )

            st.divider()

            with st.expander(
                "💡 Forecast Insights",
                expanded=True
            ):

                if future_sales > current_sales:

                    st.success(
                        "📈 Forecast predicts future sales growth."
                    )

                else:

                    st.warning(
                        "⚠️ Forecast predicts slower sales trends."
                    )

                st.info(
                    f"Average Forecasted Sales: ${future_sales:,.2f}"
                )

    # =========================
    # SQL ANALYTICS TAB
    # =========================

    with tab13:

        st.subheader("🗄 SQL Analytics Dashboard")

        st.write(
            "Live business insights using SQL queries."
        )

        # =========================
        # REGION SALES
        # =========================

        query1 = """
        SELECT Region,
            SUM(Sales) AS Total_Sales
        FROM superstore
        GROUP BY Region
        ORDER BY Total_Sales DESC
        """

        region_sales_sql = pd.read_sql_query(
            query1,
            conn
        )

        st.subheader("📈 Sales by Region (SQL)")

        fig_sql1 = px.bar(
            region_sales_sql,
            x='Region',
            y='Total_Sales',
            color='Region',
            title='Regional Sales using SQL'
        )

        st.plotly_chart(
            fig_sql1,
            use_container_width=True
        )

        # =========================
        # TOP PROFIT STATES
        # =========================

        query2 = """
        SELECT State,
            SUM(Profit) AS Total_Profit
        FROM superstore
        GROUP BY State
        ORDER BY Total_Profit DESC
        LIMIT 10
        """

        top_profit_states = pd.read_sql_query(
            query2,
            conn
        )

        st.subheader("🏆 Top Profit States (SQL)")

        fig_sql2 = px.bar(
            top_profit_states,
            x='State',
            y='Total_Profit',
            color='State',
            title='Top Profit States using SQL'
        )

        st.plotly_chart(
            fig_sql2,
            use_container_width=True
        )

        # =========================
        # CATEGORY PERFORMANCE
        # =========================

        query3 = """
        SELECT Category,
            SUM(Sales) AS Total_Sales,
            SUM(Profit) AS Total_Profit
        FROM superstore
        GROUP BY Category
        """

        category_sql = pd.read_sql_query(
            query3,
            conn
        )

        st.subheader("📊 Category Performance (SQL)")

        st.dataframe(
            category_sql,
            use_container_width=True
        )

        # =========================
    # BENFORD LAW ANALYSIS
    # =========================

    with tab14:

        st.subheader("🔍 Benford Law Analysis")

        st.write(
            "Analyze numerical patterns for potential anomalies or fraud detection."
        )

        # Select Column
        benford_column = st.selectbox(
            "Select Numeric Column",
            ['Sales', 'Profit', 'Quantity']
        )

        # Prepare Data
        benford_data = filtered_data[
            benford_column
        ].dropna()

        benford_data = benford_data[
            benford_data > 0
        ]

        # Extract First Digits
        first_digits = benford_data.astype(str).str[0].astype(int)

        actual_counts = (
            first_digits
            .value_counts(normalize=True)
            .sort_index()
        )

        # Expected Benford Distribution
        benford_distribution = {
            d: math.log10(1 + 1/d)
            for d in range(1, 10)
        }

        expected_df = pd.DataFrame({
            'Digit': list(benford_distribution.keys()),
            'Expected': list(benford_distribution.values())
        })

        actual_df = pd.DataFrame({
            'Digit': actual_counts.index,
            'Actual': actual_counts.values
        })

        benford_compare = pd.merge(
            expected_df,
            actual_df,
            on='Digit',
            how='left'
        )

        benford_compare['Actual'] = (
            benford_compare['Actual']
            .fillna(0)
        )

        # Chart
        fig_benford = px.bar(
            benford_compare,
            x='Digit',
            y=['Expected', 'Actual'],
            barmode='group',
            title=f'Benford Analysis - {benford_column}'
        )

        st.plotly_chart(
            fig_benford,
            use_container_width=True
        )

        # Difference Score
        benford_compare['Difference'] = abs(
            benford_compare['Expected']
            - benford_compare['Actual']
        )

        anomaly_score = benford_compare[
            'Difference'
        ].sum()

        st.metric(
            "Benford Deviation Score",
            round(anomaly_score, 4)
        )

        # Insight
        if anomaly_score > 0.3:

            st.error(
                "⚠ Significant deviation detected. "
                "Possible suspicious pattern."
            )

        else:

            st.success(
                "✅ Distribution appears reasonably normal."
            )

        # Show Data
        st.dataframe(
            benford_compare,
            use_container_width=True
        )

        # =========================
        # SUSPICIOUS RECORDS DETECTOR
        # =========================

        st.subheader("🚨 Suspicious Transactions")

        # Add First Digit Column
        suspicious_df = filtered_data.copy()

        suspicious_df['First_Digit'] = (
            suspicious_df[benford_column]
            .astype(str)
            .str[0]
        )

        # High Sales Threshold
        sales_threshold = (
            suspicious_df['Sales']
            .mean()
            + 2 * suspicious_df['Sales'].std()
        )

        # High Quantity Threshold
        quantity_threshold = (
            suspicious_df['Quantity']
            .mean()
            + 2 * suspicious_df['Quantity'].std()
        )

        # Suspicious Conditions
        suspicious_records = suspicious_df[
            (
                suspicious_df['Sales']
                > sales_threshold
            )
            |
            (
                suspicious_df['Quantity']
                > quantity_threshold
            )
            |
            (
                suspicious_df['Profit']
                < 0
            )
        ]

        # Show Count
        st.metric(
            "Suspicious Records Found",
            len(suspicious_records)
        )

        # Show Table
        # Safe Columns Display

        display_columns = [
            col for col in [
                'Order ID',
                'Category',
                'Sub-Category',
                'Region',
                'Sales',
                'Profit',
                'Quantity',
                'First_Digit'
            ]
            if col in suspicious_records.columns
        ]

        st.dataframe(
            suspicious_records[
                display_columns
            ],
            use_container_width=True
        )

        # Optional Download
        csv_download = suspicious_records.to_csv(
            index=False
        )

        st.download_button(
            "📥 Download Suspicious Records",
            csv_download,
            file_name="suspicious_records.csv",
            mime="text/csv"
        )

    st.markdown("""
    </div>
    """, unsafe_allow_html=True)