import streamlit as st

from dashboards.sales_dashboard import (
    sales_dashboard
)

from dashboards.healthcare_dashboard import (
    healthcare_dashboard
)

# =========================
# PAGE CONFIG
# =========================

st.set_page_config(

    page_title="AI Analytics Platform",

    page_icon="📊",

    layout="wide",

    initial_sidebar_state="expanded"
)

# =========================
# GLOBAL STYLES
# =========================

st.markdown("""
<style>

/* =========================
MAIN APP
========================= */

.stApp {

    background-color: #0E1117;

    color: white;
}

/* =========================
SIDEBAR
========================= */

section[data-testid="stSidebar"] {

    background: linear-gradient(
        180deg,
        #111827,
        #0f172a
    ) !important;

    border-right: 1px solid #1f2937;
}

section[data-testid="stSidebar"] * {

    color: white !important;
}

/* =========================
BUTTONS
========================= */

.stButton > button {

    background-color: #1f2937 !important;

    color: white !important;

    border-radius: 10px !important;

    border: 1px solid #374151 !important;

    transition: 0.3s !important;
}

.stButton > button:hover {

    background-color: #2563eb !important;

    border-color: #2563eb !important;
}

/* =========================
RADIO BUTTONS
========================= */

div[role="radiogroup"] label {

    padding: 6px 0px;
}

/* =========================
INFO BOX
========================= */

div[data-testid="stAlert"] {

    border-radius: 12px;
}

/* =========================
MOBILE RESPONSIVE
========================= */

@media screen and (max-width: 768px) {

    h1 {

        font-size: 28px !important;
    }

    .stButton > button {

        font-size: 14px !important;
    }
}

</style>
""", unsafe_allow_html=True)

# =========================
# LOGIN SESSION
# =========================

if "logged_in" not in st.session_state:

    st.session_state.logged_in = False

# =========================
# LOGIN PAGE
# =========================

if not st.session_state.logged_in:

    st.title(
        "🔐 AI Analytics Platform Login"
    )

    st.markdown(
        """
        Access enterprise analytics dashboards.
        """
    )

    username = st.text_input(
        "Username"
    )

    password = st.text_input(
        "Password",
        type="password"
    )

    if st.button("Login"):

        if (

            username == "admin"

            and

            password == "admin123"

        ):

            st.session_state.logged_in = True

            st.rerun()

        else:

            st.error(
                """
                ❌ Incorrect username or password.
                """
            )

# =========================
# DASHBOARD PLATFORM
# =========================

else:

    # =========================
    # USER INFO
    # =========================

    st.sidebar.success(
        "👨‍💼 Admin User"
    )

    st.sidebar.caption(
        "Enterprise Access"
    )

    # =========================
    # LOGOUT
    # =========================

    if st.sidebar.button(
        "🚪 Logout",
        use_container_width=True
    ):

        st.session_state.logged_in = False

        st.rerun()

    st.sidebar.markdown("---")

    # =========================
    # PLATFORM TITLE
    # =========================

    st.sidebar.title(
        "📊 AI Analytics Platform"
    )

    # =========================
    # PLATFORM INFO
    # =========================

    st.sidebar.info(
        """
        🚀 Enterprise AI Analytics Platform

        Includes:
        • Healthcare Intelligence
        • Sales Forecasting
        • SQL Analytics
        • ML Predictions
        • Anomaly Detection
        """
    )

    # =========================
    # DASHBOARD SELECTOR
    # =========================

    selected_dashboard = st.sidebar.radio(

        "Select Dashboard",

        [

            "📈 Sales Analytics",

            "🏥 Healthcare Analytics",

            "📦 Inventory Analytics",

            "💰 Finance Analytics",

            "🚚 Supply Chain Analytics"

        ]
    )

    # =========================
    # SALES DASHBOARD
    # =========================

    if selected_dashboard == "📈 Sales Analytics":

        sales_dashboard()

    # =========================
    # HEALTHCARE DASHBOARD
    # =========================

    elif selected_dashboard == "🏥 Healthcare Analytics":

        try:

            healthcare_dashboard()

        except Exception as e:

            st.error(
                f"Healthcare Dashboard Error: {e}"
            )

            st.exception(e)

    # =========================
    # COMING SOON
    # =========================

    else:

        st.title(
            "🚧 Dashboard Under Development"
        )

        st.info(
            """
            This analytics module
            will be added soon.
            """
        )