import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score

from sklearn.linear_model import LinearRegression
import numpy as np

from itertools import combinations
from collections import Counter

from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer
)

from reportlab.lib.styles import getSampleStyleSheet

from io import BytesIO

st.set_page_config(
    page_title="E-Commerce Analytics",
    page_icon="🛒",
    layout="wide"
)


@st.cache_data
def load_data():

    base_path = (
        Path(__file__)
        .resolve()
        .parent.parent
        / "data"
    )

    customers = pd.read_csv(
        base_path / "olist_customers_dataset.csv"
    )

    orders = pd.read_csv(
        base_path / "olist_orders_dataset.csv"
    )

    order_items = pd.read_csv(
        base_path / "olist_order_items_dataset.csv"
    )

    payments = pd.read_csv(
        base_path / "olist_order_payments_dataset.csv"
    )

    reviews = pd.read_csv(
        base_path / "olist_order_reviews_dataset.csv"
    )

    products = pd.read_csv(
        base_path / "olist_products_dataset.csv"
    )

    sellers = pd.read_csv(
        base_path / "olist_sellers_dataset.csv"
    )

    category_translation = pd.read_csv(
        base_path / "product_category_name_translation.csv"
    )

    # =========================
    # Product Category Translation
    # =========================

    products = products.merge(
        category_translation,
        on="product_category_name",
        how="left"
    )

    # =========================
    # Orders + Customers
    # =========================

    master_df = orders.merge(
        customers,
        on="customer_id",
        how="left"
    )

    # =========================
    # Order Items
    # =========================

    master_df = master_df.merge(
        order_items,
        on="order_id",
        how="left"
    )

    # =========================
    # Products
    # =========================

    master_df = master_df.merge(
        products,
        on="product_id",
        how="left"
    )

    # =========================
    # Sellers
    # =========================

    master_df = master_df.merge(
        sellers,
        on="seller_id",
        how="left"
    )

    # =========================
    # Payments
    # =========================

    master_df = master_df.merge(
        payments,
        on="order_id",
        how="left"
    )

    # =========================
    # Reviews
    # =========================

    master_df = master_df.merge(
        reviews,
        on="order_id",
        how="left"
    )

    return master_df


def ecommerce_dashboard():

    st.title(
        "🛒 E-Commerce Analytics Dashboard"
    )

    df = load_data()

    # =====================
    # SIDEBAR FILTERS
    # =====================

    st.sidebar.title("Filters")

    # Order Status

    selected_status = st.sidebar.multiselect(
        "Order Status",
        options=df["order_status"].dropna().unique()
    )

    if selected_status:

        df = df[
            df["order_status"].isin(
                selected_status
            )
        ]

    # Customer State

    selected_state = st.sidebar.selectbox(
        "Customer State",
        ["All"] +
        sorted(
            df["customer_state"]
            .dropna()
            .unique()
            .tolist()
        )
    )

    if selected_state != "All":

        df = df[
            df["customer_state"]
            == selected_state
        ]

    # Payment Type

    payment_type = st.sidebar.selectbox(
        "Payment Type",
        ["All"] +
        sorted(
            df["payment_type"]
            .dropna()
            .unique()
            .tolist()
        )
    )

    if payment_type != "All":

        df = df[
            df["payment_type"]
            == payment_type
        ]

    # Revenue Range

    revenue_range = st.sidebar.slider(
        "Payment Value",
        float(df["payment_value"].min()),
        float(df["payment_value"].max()),
        (
            float(df["payment_value"].min()),
            float(df["payment_value"].max())
        )
    )

    df = df[
        (df["payment_value"] >= revenue_range[0])
        &
        (df["payment_value"] <= revenue_range[1])
    ]

    if not df.empty:

        df["order_purchase_timestamp"] = pd.to_datetime(
            df["order_purchase_timestamp"]
        )

        date_range = st.sidebar.date_input(
            "Order Date Range",
            value=(
                df["order_purchase_timestamp"].min().date(),
                df["order_purchase_timestamp"].max().date()
            )
        )

        if len(date_range) == 2:

            start_date = pd.to_datetime(
                date_range[0]
            )

            end_date = pd.to_datetime(
                date_range[1]
            )

            df = df[
                (
                    df["order_purchase_timestamp"]
                    >= start_date
                )
                &
                (
                    df["order_purchase_timestamp"]
                    <= end_date
                )
            ]


    st.markdown(
        """
        Interactive E-Commerce Analytics Platform
        with Customer, Product, Revenue,
        AI and ML Insights.
        """
    )

    total_orders = df["order_id"].nunique()

    total_customers = df["customer_id"].nunique()

    total_products = df["product_id"].nunique()

    total_revenue = round(
        df["payment_value"].sum(),
        2
    )

    avg_order_value = (
        total_revenue /
        total_orders
    )

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "Orders",
            f"{total_orders:,}"
        )

    with col2:
        st.metric(
            "Customers",
            f"{total_customers:,}"
        )

    with col3:
        st.metric(
            "Products",
            f"{total_products:,}"
        )

    with col4:
        st.metric(
            "Revenue",
            f"R$ {total_revenue:,.0f}"
        )

    tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8, tab9, tab10, tab11, tab12 = st.tabs([
        "Overview",
        "Customer Analytics",
        "Product Analytics",
        "Revenue Analytics",
        "Reviews",
        "RFM Analysis",
        "AI Insights",
        "ML Prediction",
        "Forecasting",
        "Market Basket",
        "Churn Risk",
        "Reports"
    ])

    with tab1:

        st.subheader(
            "📈 Business Overview"
        )

        overview_df = df.copy()

        overview_df["order_purchase_timestamp"] = pd.to_datetime(
            overview_df["order_purchase_timestamp"]
        )

        overview_df["Month"] = (
            overview_df["order_purchase_timestamp"]
            .dt.to_period("M")
            .astype(str)
        )

        monthly_sales = (
            overview_df
            .groupby("Month")["payment_value"]
            .sum()
            .reset_index()
        )

        fig = px.line(
            monthly_sales,
            x="Month",
            y="payment_value",
            title="Monthly Revenue Trend"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

        col1, col2 = st.columns(2)

        with col1:

            status_df = (
                df["order_status"]
                .value_counts()
                .reset_index()
            )

            status_df.columns = [
                "Status",
                "Count"
            ]

            fig = px.pie(
                status_df,
                names="Status",
                values="Count",
                title="Order Status Distribution"
            )

            fig.update_layout(
                height=850
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )

        with col2:

            state_df = (
                df.groupby("customer_state")
                ["payment_value"]
                .sum()
                .sort_values(
                    ascending=False
                )
                .head(10)
                .reset_index()
            )

            fig = px.bar(
                state_df,
                x="customer_state",
                y="payment_value",
                title="Top Revenue States"
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )

    with tab2:

        st.subheader(
            "👥 Customer Analytics"
        )

        top_customers = (
            df.groupby("customer_unique_id")
            ["payment_value"]
            .sum()
            .sort_values(
                ascending=False
            )
            .head(10)
            .reset_index()
        )

        fig = px.bar(
            top_customers,
            x="customer_unique_id",
            y="payment_value",
            title="Top 10 Customers by Revenue"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

        st.divider()

        st.subheader(
            "🔄 Repeat Customers"
        )

        repeat_customers = (
            df.groupby("customer_unique_id")
            ["order_id"]
            .nunique()
            .sort_values(
                ascending=False
            )
            .head(10)
            .reset_index()
        )

        st.dataframe(
            repeat_customers,
            use_container_width=True
        )

        st.divider()

        st.subheader(
            "🌎 Customers by State"
        )

        state_df = (
            df.groupby("customer_state")
            ["customer_unique_id"]
            .nunique()
            .reset_index()
        )

        fig = px.bar(
            state_df,
            x="customer_state",
            y="customer_unique_id",
            title="Customers by State"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        ) 

    with tab3:

        st.subheader(
            "📦 Product Analytics"
        )

        top_products = (
            df.groupby(
                "product_category_name_english"
            )["payment_value"]
            .sum()
            .sort_values(
                ascending=False
            )
            .head(15)
            .reset_index()
        )

        fig = px.bar(
            top_products,
            x="payment_value",
            y="product_category_name_english",
            orientation="h",
            title="Top Product Categories"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    with tab4:

        st.subheader("💰 Revenue Analytics")

        revenue_df = df.copy()

        revenue_df["order_purchase_timestamp"] = pd.to_datetime(
            revenue_df["order_purchase_timestamp"]
        )

        revenue_df["YearMonth"] = (
            revenue_df["order_purchase_timestamp"]
            .dt.to_period("M")
            .astype(str)
        )

        monthly_revenue = (
            revenue_df
            .groupby("YearMonth")["payment_value"]
            .sum()
            .reset_index()
        )

        fig = px.line(
            monthly_revenue,
            x="YearMonth",
            y="payment_value",
            title="Monthly Revenue Trend"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

        st.divider()

        st.subheader(
            "🏆 Top Product Categories"
        )

        top_categories = (
            df.groupby(
                "product_category_name_english"
            )["payment_value"]
            .sum()
            .sort_values(
                ascending=False
            )
            .head(10)
            .reset_index()
        )

        fig = px.bar(
            top_categories,
            x="payment_value",
            y="product_category_name_english",
            orientation="h",
            title="Top 10 Categories by Revenue"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    with tab5:

        st.subheader(
            "⭐ Review Analytics"
        )

        review_df = (
            df.groupby("review_score")
            .size()
            .reset_index(
                name="Count"
            )
        )

        fig = px.bar(
            review_df,
            x="review_score",
            y="Count",
            title="Review Score Distribution"
        )

        fig.update_layout(
            height=600
        )

        fig.update_layout(
            height=850
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    with tab6:

        st.subheader(
            "🎯 RFM Customer Segmentation"
        )

        rfm = df.groupby(
            "customer_unique_id"
        ).agg({

            "order_purchase_timestamp":"max",

            "order_id":"nunique",

            "payment_value":"sum"

        })

        rfm.columns = [

            "Recency",

            "Frequency",

            "Monetary"

        ]

        latest_date = pd.to_datetime(
            df["order_purchase_timestamp"]
        ).max()

        rfm["Recency"] = (
            latest_date
            -
            pd.to_datetime(
                rfm["Recency"]
            )
        ).dt.days

        rfm["Segment"] = "Regular"

        rfm.loc[
            (
                rfm["Frequency"] >= 2
            )
            &
            (
                rfm["Monetary"]
                >=
                rfm["Monetary"].quantile(0.90)
            ),
            "Segment"
        ] = "VIP"

        segment_df = (
            rfm["Segment"]
            .value_counts()
            .reset_index()
        )

        segment_df.columns = [
            "Segment",
            "Customers"
        ]

        fig = px.pie(
            segment_df,
            names="Segment",
            values="Customers",
            title="Customer Segmentation"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

        st.divider()

        st.subheader(
            "🏆 Top VIP Customers"
        )

        vip_customers = (
            rfm[
                rfm["Segment"] == "VIP"
            ]
            .sort_values(
                "Monetary",
                ascending=False
            )
            .head(10)
        )

        st.dataframe(
            vip_customers,
            use_container_width=True
        )

    with tab7:

        st.subheader("🤖 AI Business Insights")

        top_state = (
            df.groupby("customer_state")["payment_value"]
            .sum()
            .idxmax()
        )

        top_category = (
            df.groupby(
                "product_category_name_english"
            )["payment_value"]
            .sum()
            .idxmax()
        )

        avg_review = round(
            df["review_score"].mean(),
            2
        )

        st.success(
            f"""
            📈 Highest Revenue State: {top_state}

            🏆 Best Product Category: {top_category}

            ⭐ Average Review Score: {avg_review}

            💡 Recommendation:
            Focus marketing campaigns on
            {top_state} and increase inventory
            for {top_category}.
            """
        )

    with tab8:

        st.subheader("🤖 Revenue Prediction Model")

        ml_df = df.copy()

        ml_df = ml_df[
            [
                "payment_value",
                "review_score"
            ]
        ].dropna()

        X = ml_df[["review_score"]]

        y = ml_df["payment_value"]

        X_train, X_test, y_train, y_test = train_test_split(
            X,
            y,
            test_size=0.2,
            random_state=42
        )

        model = LinearRegression()

        model.fit(
            X_train,
            y_train
        )

        predictions = model.predict(
            X_test
        )

        accuracy = r2_score(
            y_test,
            predictions
        )

        st.metric(
            "Model Accuracy (R²)",
            round(accuracy, 3)
        )

        review_input = st.slider(
            "Review Score",
            1,
            5,
            5
        )

        predicted_revenue = model.predict(
            [[review_input]]
        )[0]

        st.success(
            f"Predicted Revenue: R$ {predicted_revenue:,.2f}"
        )

        comparison_df = pd.DataFrame({

            "Actual": y_test.head(100),
            "Predicted": predictions[:100]

        })

        fig = px.line(
            comparison_df,
            title="Actual vs Predicted Revenue"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    with tab9:

        st.subheader(
            "📈 Revenue Forecasting"
        )

        forecast_df = df.copy()

        forecast_df[
            "order_purchase_timestamp"
        ] = pd.to_datetime(
            forecast_df[
                "order_purchase_timestamp"
            ]
        )

        monthly_sales = (
            forecast_df
            .groupby(
                pd.Grouper(
                    key="order_purchase_timestamp",
                    freq="ME"
                )
            )["payment_value"]
            .sum()
            .reset_index()
        )

        monthly_sales["Month_Number"] = np.arange(
            len(monthly_sales)
        )

        X = monthly_sales[
            ["Month_Number"]
        ]

        y = monthly_sales[
            "payment_value"
        ]

        model = LinearRegression()

        model.fit(
            X,
            y
        )

        future_months = 6

        future_index = np.arange(
            len(monthly_sales),
            len(monthly_sales)
            + future_months
        )

        future_predictions = model.predict(
            pd.DataFrame(
                future_index,
                columns=["Month_Number"]
            )
        )

        future_dates = pd.date_range(
            start=monthly_sales[
                "order_purchase_timestamp"
            ].max(),
            periods=future_months + 1,
            freq="ME"
        )[1:]

        forecast_future = pd.DataFrame({

            "Month": future_dates,
            "Forecast Revenue": future_predictions

        })

        st.dataframe(
            forecast_future,
            use_container_width=True
        )

        fig = px.line(
            monthly_sales,
            x="order_purchase_timestamp",
            y="payment_value",
            title="Historical Revenue Trend"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

        fig2 = px.line(
            forecast_future,
            x="Month",
            y="Forecast Revenue",
            title="Next 6 Months Forecast"
        )

        st.plotly_chart(
            fig2,
            use_container_width=True
        )

    with tab10:

        st.subheader(
            "🛒 Market Basket Analysis"
        )

        basket_df = df[
            [
                "order_id",
                "product_category_name_english"
            ]
        ].dropna()

        order_products = (
            basket_df
            .groupby("order_id")
            [
                "product_category_name_english"
            ]
            .apply(list)
        )

        pair_counter = Counter()

        for products in order_products:

            unique_products = list(
                set(products)
            )

            if len(unique_products) >= 2:

                pair_counter.update(
                    combinations(
                        sorted(unique_products),
                        2
                    )
                )

        top_pairs = pd.DataFrame(

            pair_counter.most_common(15),

            columns=[
                "Product Pair",
                "Frequency"
            ]
        )

        top_pairs["Product Pair"] = (
            top_pairs["Product Pair"]
            .astype(str)
        )

        st.dataframe(
            top_pairs,
            use_container_width=True
        )

        fig = px.bar(
            top_pairs,
            x="Frequency",
            y="Product Pair",
            orientation="h",
            title="Most Frequently Purchased Together"
        )

        fig.update_layout(
            height=700
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    with tab11:

        st.subheader(
            "🚨 Customer Churn Risk Detection"
        )

        churn_df = (
            df.groupby(
                "customer_unique_id"
            )
            .agg({

                "order_id":"nunique",

                "payment_value":"sum",

                "review_score":"mean"

            })
            .reset_index()
        )

        churn_df.columns = [

            "Customer",

            "Orders",

            "Revenue",

            "Avg Review"

        ]

        churn_df["Risk"] = "Low"

        churn_df.loc[
            churn_df["Orders"] <= 1,
            "Risk"
        ] = "High"

        churn_df.loc[
            (
                churn_df["Orders"] == 2
            ),
            "Risk"
        ] = "Medium"

        risk_summary = (
            churn_df["Risk"]
            .value_counts()
            .reset_index()
        )

        risk_summary.columns = [
            "Risk",
            "Customers"
        ]

        fig = px.pie(
            risk_summary,
            names="Risk",
            values="Customers",
            title="Customer Churn Risk"
        )

        fig.update_layout(
            height=850
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

        st.divider()

        st.subheader(
            "High Risk Customers"
        )

        high_risk = churn_df[
            churn_df["Risk"] == "High"
        ].head(20)

        st.dataframe(
            high_risk,
            use_container_width=True
        )

    with tab12:

        st.subheader(
            "📄 Export Reports"
        )

        def generate_pdf():

            buffer = BytesIO()

            doc = SimpleDocTemplate(
                buffer
            )

            styles = getSampleStyleSheet()

            elements = []

            elements.append(
                Paragraph(
                    "E-Commerce Analytics Report",
                    styles["Title"]
                )
            )

            elements.append(
                Spacer(1, 20)
            )

            elements.append(
                Paragraph(
                    f"Total Orders: {total_orders}",
                    styles["Normal"]
                )
            )

            elements.append(
                Paragraph(
                    f"Total Customers: {total_customers}",
                    styles["Normal"]
                )
            )

            elements.append(
                Paragraph(
                    f"Total Products: {total_products}",
                    styles["Normal"]
                )
            )

            elements.append(
                Paragraph(
                    f"Total Revenue: R$ {total_revenue:,.2f}",
                    styles["Normal"]
                )
            )

            doc.build(
                elements
            )

            buffer.seek(0)

            return buffer

        pdf_file = generate_pdf()

        st.download_button(

            label="📄 Download PDF Report",

            data=pdf_file,

            file_name="ecommerce_report.pdf",

            mime="application/pdf"
        )