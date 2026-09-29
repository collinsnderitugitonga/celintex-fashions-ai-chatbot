import os
import sys
import streamlit as st
import time

# ============================================================
# PROJECT ROOT
# ============================================================

BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)

if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)


from src.chatbot import answer_question


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="Celintex Fashion AI",
    page_icon="👗",
    layout="centered",
    initial_sidebar_state="expanded"
)


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown(
    """
    <style>

    /* ======================================================
       MAIN BACKGROUND
       ====================================================== */

    .stApp {
        background:
            linear-gradient(
                135deg,
                #fff7fb 0%,
                #f8f5ff 45%,
                #f4fbfa 100%
            );
    }

    .block-container {
        max-width: 920px;
        padding-top: 1.5rem;
        padding-bottom: 4rem;
    }

    /* Main text */
    p, li, span, label {
        color: #292535;
    }


    /* ======================================================
       TOP BRAND CARD
       ====================================================== */

    .brand-card {
        background:
            linear-gradient(
                135deg,
                #4b164c 0%,
                #7b3f78 50%,
                #9c6ade 100%
            );

        border-radius: 28px;
        padding: 32px 25px;
        margin-bottom: 24px;

        text-align: center;

        box-shadow:
            0 12px 35px rgba(99, 57, 126, 0.20);
    }

    .brand-icon {
        font-size: 38px;
        margin-bottom: 4px;
    }

    .brand-title {
        color: white !important;
        font-size: 36px;
        font-weight: 850;
        letter-spacing: 4px;
        margin: 0;
    }

    .brand-subtitle {
        color: #f9eefd !important;
        font-size: 15px;
        margin-top: 8px;
    }

    .online-pill {
        display: inline-block;

        margin-top: 16px;
        padding: 7px 15px;

        border-radius: 30px;

        background: rgba(255,255,255,0.18);
        border: 1px solid rgba(255,255,255,0.35);

        color: white !important;
        font-size: 12px;
        font-weight: 700;

        backdrop-filter: blur(8px);
    }


    /* ======================================================
       WELCOME CARD
       ====================================================== */

    .welcome-card {
        background: rgba(255,255,255,0.86);

        border: 1px solid #eaddec;
        border-radius: 22px;

        padding: 25px;

        margin-bottom: 22px;

        box-shadow:
            0 7px 25px rgba(74, 39, 82, 0.07);
    }

    .welcome-title {
        color: #4b164c !important;
        font-size: 24px;
        font-weight: 800;
        margin-bottom: 8px;
    }

    .welcome-text {
        color: #5b5563 !important;
        font-size: 15px;
        line-height: 1.75;
    }


    /* ======================================================
       SECTION HEADINGS
       ====================================================== */

    .section-title {
        color: #4b164c !important;
        font-size: 17px;
        font-weight: 800;
        margin: 22px 0 12px 3px;
    }


    /* ======================================================
       QUICK QUESTION BUTTONS
       ====================================================== */

    div.stButton > button {

        width: 100%;
        min-height: 52px;

        border-radius: 15px;

        border: 1px solid #e2d4e8;

        background: rgba(255,255,255,0.92);

        color: #392b3d !important;

        font-weight: 650;

        box-shadow:
            0 4px 14px rgba(77, 39, 83, 0.06);

        transition:
            transform 0.18s ease,
            box-shadow 0.18s ease,
            border 0.18s ease;
    }

    div.stButton > button:hover {

        transform: translateY(-2px);

        border-color: #a66bb1;

        background: #fff8ff;

        color: #4b164c !important;

        box-shadow:
            0 8px 20px rgba(105, 55, 120, 0.13);
    }


    /* ======================================================
       CHAT AREA
       ====================================================== */

    [data-testid="stChatMessage"] {

        border-radius: 20px;

        padding: 10px 12px;

        margin-bottom: 14px;

        border: 1px solid #e7dfe9;

        box-shadow:
            0 4px 16px rgba(70, 45, 76, 0.05);
    }


    /* User message */

    [data-testid="stChatMessage"]:has(
        [data-testid="chatAvatarIcon-user"]
    ) {

        background:
            linear-gradient(
                135deg,
                #f1e6ff,
                #f8efff
            );

        border-color: #dfcbed;
    }


    /* Assistant message */

    [data-testid="stChatMessage"]:has(
        [data-testid="chatAvatarIcon-assistant"]
    ) {

        background: rgba(255,255,255,0.95);

        border-color: #dce9e4;
    }


    /* ======================================================
       CHAT INPUT
       ====================================================== */

    [data-testid="stChatInput"] {
        margin-top: 20px;
    }

    [data-testid="stChatInput"] textarea {

        background: white !important;

        color: #292535 !important;

        border: 2px solid #d8c7df !important;

        border-radius: 17px !important;

        font-size: 15px !important;

        box-shadow:
            0 5px 20px rgba(72, 42, 80, 0.07);
    }

    [data-testid="stChatInput"] textarea::placeholder {
        color: #8a8190 !important;
    }

    [data-testid="stChatInput"] textarea:focus {

        border-color: #8d55a3 !important;

        box-shadow:
            0 0 0 2px rgba(141,85,163,0.12) !important;
    }


    /* ======================================================
       CONTACT CARD
       ====================================================== */

    .contact-card {

        background:
            linear-gradient(
                135deg,
                #39203d,
                #603d66
            );

        border-radius: 22px;

        padding: 24px;

        margin-top: 28px;

        text-align: center;

        box-shadow:
            0 10px 30px rgba(63, 32, 69, 0.18);
    }

    .contact-title {
        color: white !important;
        font-size: 18px;
        font-weight: 800;
    }

    .contact-text {
        color: #f3e9f5 !important;
        font-size: 14px;
        line-height: 1.8;
        margin-top: 7px;
    }


    /* ======================================================
       SIDEBAR
       ====================================================== */

    [data-testid="stSidebar"] {

        background:
            linear-gradient(
                180deg,
                #fff8fc,
                #f7f2fb
            );

        border-right: 1px solid #eaddec;
    }

    [data-testid="stSidebar"] h2 {

        color: #4b164c !important;
    }

    [data-testid="stSidebar"] h3 {

        color: #633c69 !important;
    }


    /* ======================================================
       SIDEBAR CONTACT BOX
       ====================================================== */

    .sidebar-contact {

        background: white;

        border: 1px solid #eaddec;

        border-radius: 16px;

        padding: 16px;

        margin-top: 10px;

        box-shadow:
            0 5px 18px rgba(71, 41, 78, 0.06);
    }


    /* ======================================================
       FOOTER
       ====================================================== */

    .footer {

        text-align: center;

        color: #8b808e !important;

        font-size: 12px;

        margin-top: 22px;
    }


    /* ======================================================
       SPINNER
       ====================================================== */

    .stSpinner > div {
        color: #7b3f78 !important;
    }


    /* ======================================================
       DIVIDER
       ====================================================== */

    hr {
        border-color: #eaddec !important;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# BRAND HEADER
# ============================================================

st.markdown(
    """
    <div class="brand-card">

        <div class="brand-icon">
            👗
        </div>

        <div class="brand-title">
            CELINTEX
        </div>

        <div class="brand-subtitle">
            Fashion • Design • Tailoring • Style
        </div>

        <div class="online-pill">
            🟢 AI ASSISTANT ONLINE
        </div>

    </div>
    """,
    unsafe_allow_html=True
)


# ============================================================
# CHAT HISTORY
# ============================================================

if "messages" not in st.session_state:

    st.session_state.messages = []


# ============================================================
# WELCOME SCREEN
# ============================================================

if not st.session_state.messages:

    st.markdown(
        """
        <div class="welcome-card">

            <div class="welcome-title">
                ✨ Welcome to Celintex
            </div>

            <div class="welcome-text">
                I'm your Celintex AI Fashion Assistant.
                Ask me about custom clothing, Vitenge fashion,
                men's suits, wedding gowns, repairs,
                alterations, pricing and more.
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="section-title">💬 Quick questions</div>',
        unsafe_allow_html=True
    )

    col1, col2 = st.columns(2)

    with col1:

        if st.button(
            "💰  Custom suit pricing",
            use_container_width=True
        ):

            st.session_state.quick_question = (
                "How much is a custom suit?"
            )

        if st.button(
            "👰  Wedding gown hire",
            use_container_width=True
        ):

            st.session_state.quick_question = (
                "Can I hire a wedding gown?"
            )

        if st.button(
            "🧵  Custom Vitenge",
            use_container_width=True
        ):

            st.session_state.quick_question = (
                "Do you make customized Vitenge clothing?"
            )

    with col2:

        if st.button(
            "📍  Find Celintex",
            use_container_width=True
        ):

            st.session_state.quick_question = (
                "Where is Celintex located?"
            )

        if st.button(
            "🕐  Opening hours",
            use_container_width=True
        ):

            st.session_state.quick_question = (
                "What are your opening hours?"
            )

        if st.button(
            "🛠️  Repairs & alterations",
            use_container_width=True
        ):

            st.session_state.quick_question = (
                "Do you repair clothes?"
            )


# ============================================================
# DISPLAY CHAT
# ============================================================

for message in st.session_state.messages:

    with st.chat_message(message["role"]):

        st.markdown(message["content"])


# ============================================================
# CHAT INPUT
# ============================================================

user_input = st.chat_input(
    "✨ Ask Celintex anything..."
)


# ============================================================
# QUICK QUESTION HANDLER
# ============================================================

if (
    "quick_question" in st.session_state
    and not user_input
):

    user_input = st.session_state.quick_question

    del st.session_state.quick_question


# ============================================================
# PROCESS QUESTION
# ============================================================

if user_input:

    st.session_state.messages.append(
        {
            "role": "user",
            "content": user_input
        }
    )

    with st.chat_message("user"):

        st.markdown(user_input)


    with st.chat_message("assistant"):

        with st.spinner(
            "✨ Celintex AI is thinking..."
        ):

            try:

                response = answer_question(
                    user_input
                )

            except Exception:

                response = (
                    "Sorry, I couldn't process that request "
                    "right now. Please try again or contact "
                    "Celintex on **0722285544**."
                )

        st.markdown(response)


    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": response
        }
    )


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.markdown("## 👗 CELINTEX")

    st.caption(
        "AI Fashion Assistant"
    )

    st.divider()

    st.markdown("### ✨ Services")

    st.markdown(
        """
        👗 **Custom clothing**

        🧵 **Vitenge fashion**

        🤵 **Men's suits**

        👰 **Wedding gowns**

        🛠️ **Repairs & alterations**

        🛍️ **Ready-made clothing**
        """
    )

    st.divider()

    st.markdown("### 📞 Contact")

    st.markdown(
        """
        <div class="sidebar-contact">

        📱 <b>0722285544</b><br><br>

        📍 Nairobi CBD<br>
        Accra Road<br>
        Scorpio Building

        </div>
        """,
        unsafe_allow_html=True
    )

    st.divider()

    if st.button(
        "🗑️ Clear conversation",
        use_container_width=True
    ):

        st.session_state.messages = []

        st.rerun()


# ============================================================
# CONTACT SECTION
# ============================================================

st.markdown(
    """
    <div class="contact-card">

        <div class="contact-title">
            💜 Need a quotation?
        </div>

        <div class="contact-text">
            Speak directly with the Celintex team.<br>
            📞 <b>0722285544</b>
        </div>

    </div>

    <div class="footer">
        Celintex Fashion AI Assistant • Fashion made personal
    </div>
    """,
    unsafe_allow_html=True
)
