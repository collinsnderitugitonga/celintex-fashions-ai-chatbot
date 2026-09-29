import streamlit as st
import time


from src.rag import get_context
from src.llm import stream_response


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="Celintex AI Assistant",
    page_icon="👗",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown(
    """
    <style>

    /* ========================================================
       GLOBAL
    ======================================================== */

    .stApp {
        background:
            radial-gradient(
                circle at top left,
                #fff4fa 0%,
                #faf8ff 45%,
                #f3fbf8 100%
            );
    }


    /* ========================================================
       SIDEBAR
    ======================================================== */

    section[data-testid="stSidebar"] {
        background:
            linear-gradient(
                180deg,
                #fffafd 0%,
                #f8f1fb 100%
            );

        border-right:
            1px solid rgba(75, 22, 76, 0.10);
    }


    section[data-testid="stSidebar"] > div {
        padding-top: 1.5rem;
    }


    .sidebar-brand {
        text-align: center;

        padding:
            18px 10px 22px 10px;

        border-bottom:
            1px solid rgba(75, 22, 76, 0.10);

        margin-bottom: 20px;
    }


    .sidebar-logo {
        font-size: 42px;
    }


    .sidebar-title {
        color: #4b164c;

        font-size: 24px;

        font-weight: 800;

        letter-spacing: 1px;

        margin-top: 4px;
    }


    .sidebar-subtitle {
        color: #766477;

        font-size: 12px;

        margin-top: 3px;
    }


    .sidebar-section-title {
        color: #4b164c;

        font-size: 15px;

        font-weight: 750;

        margin-top: 22px;

        margin-bottom: 10px;
    }


    .sidebar-item {
        color: #514451;

        font-size: 13px;

        padding:
            7px 8px;

        margin:
            3px 0;

        border-radius: 10px;
    }


    .sidebar-item:hover {
        background: #f0e4f4;
    }


    .sidebar-contact {
        background:
            linear-gradient(
                135deg,
                #4b164c,
                #70406d
            );

        color: white;

        padding: 16px;

        border-radius: 16px;

        margin-top: 18px;

        box-shadow:
            0 8px 25px rgba(75, 22, 76, 0.16);
    }


    .sidebar-contact-title {
        font-size: 15px;

        font-weight: 700;

        margin-bottom: 8px;
    }


    .sidebar-phone {
        font-size: 19px;

        font-weight: 800;

        margin-bottom: 10px;
    }


    .sidebar-contact-text {
        font-size: 12px;

        line-height: 1.6;

        opacity: 0.92;
    }


    /* ========================================================
       MAIN CONTENT
    ======================================================== */

    .main-container {
        max-width: 1050px;

        margin:
            0 auto;

        padding:
            10px 25px 100px 25px;
    }


    /* ========================================================
       CELINTEX HEADER
    ======================================================== */

    .brand-card {
        background:
            linear-gradient(
                135deg,
                #431344 0%,
                #6e286c 48%,
                #8f5ad2 100%
            );

        padding:
            28px 30px;

        border-radius:
            0 0 28px 28px;

        margin-bottom:
            22px;

        color: white;

        text-align: center;

        box-shadow:
            0 12px 35px
            rgba(75, 22, 76, 0.22);
    }


    .brand-icon {
        font-size: 36px;

        margin-bottom: 4px;
    }


    .brand-title {
        font-size: 32px;

        font-weight: 850;

        letter-spacing: 2px;
    }


    .brand-subtitle {
        font-size: 14px;

        opacity: 0.90;

        margin-top: 4px;
    }


    .online-pill {
        display: inline-block;

        margin-top: 14px;

        padding:
            7px 14px;

        border-radius: 30px;

        background:
            rgba(255,255,255,0.15);

        border:
            1px solid rgba(255,255,255,0.18);

        font-size: 12px;

        font-weight: 650;
    }


    /* ========================================================
       WELCOME
    ======================================================== */

    .welcome-card {
        background:
            rgba(255,255,255,0.88);

        padding:
            18px 21px;

        border-radius:
            18px;

        margin-bottom:
            18px;

        border:
            1px solid rgba(123,63,120,0.10);

        box-shadow:
            0 6px 20px rgba(60,30,70,0.06);
    }


    .welcome-title {
        color: #4b164c;

        font-size: 19px;

        font-weight: 750;
    }


    .welcome-text {
        color: #665a67;

        font-size: 13px;

        line-height: 1.6;

        margin-top: 5px;
    }


    /* ========================================================
       CHAT AREA
    ======================================================== */

    .chat-area {
        background:
            rgba(255,255,255,0.45);

        border-radius:
            22px;

        padding:
            8px 4px;
    }


    .user-bubble {
        background:
            linear-gradient(
                135deg,
                #dfd0ff,
                #f1e8ff
            );

        color: #38233e;

        padding:
            12px 16px;

        border-radius:
            18px 18px 5px 18px;

        margin:
            10px 0 10px auto;

        max-width:
            78%;

        width:
            fit-content;

        box-shadow:
            0 4px 12px
            rgba(80,50,100,0.07);

        font-size: 14px;
    }


    .assistant-bubble {
        background:
            rgba(255,255,255,0.95);

        color: #302834;

        padding:
            15px 18px;

        border-radius:
            18px 18px 18px 5px;

        margin:
            10px auto 10px 0;

        max-width:
            88%;

        border-left:
            4px solid #9c6ade;

        box-shadow:
            0 5px 18px
            rgba(70,40,80,0.07);

        font-size: 14px;

        line-height: 1.65;
    }


    /* ========================================================
       THINKING STATUS
    ======================================================== */

    .thinking {
        background:
            linear-gradient(
                90deg,
                #fff3fb,
                #f2efff,
                #effaf7
            );

        padding:
            10px 14px;

        border-radius:
            14px;

        margin:
            8px 0;

        color:
            #674a69;

        font-size:
            13px;

        border:
            1px solid
            rgba(123,63,120,0.10);
    }


    /* ========================================================
       CHAT INPUT
    ======================================================== */

    div[data-testid="stChatInput"] {
        background:
            rgba(255,255,255,0.95);

        border:
            2px solid
            rgba(123,63,120,0.14);

        border-radius:
            18px;

        box-shadow:
            0 8px 30px
            rgba(60,30,70,0.12);

        padding:
            4px;
    }


    div[data-testid="stChatInput"] textarea {
        font-size: 14px;
    }


    /* ========================================================
       FOOTER
    ======================================================== */

    .footer {
        text-align: center;

        color: #776b78;

        font-size: 11px;

        margin-top: 20px;

        padding-bottom: 20px;
    }


    /* ========================================================
       MOBILE
    ======================================================== */

    @media (max-width: 768px) {

        .main-container {
            padding:
                5px 10px 90px 10px;
        }

        .brand-card {
            padding:
                22px 15px;
        }

        .brand-title {
            font-size: 26px;
        }

        .user-bubble {
            max-width: 88%;
        }

        .assistant-bubble {
            max-width: 94%;
        }

    }

    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.markdown(
        """
        <div class="sidebar-brand">

            <div class="sidebar-logo">
                👗
            </div>

            <div class="sidebar-title">
                CELINTEX
            </div>

            <div class="sidebar-subtitle">
                AI Fashion Assistant
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )


    st.markdown(
        """
        <div class="sidebar-section-title">
            ✨ Services
        </div>

        <div class="sidebar-item">
            🧵 Custom clothing
        </div>

        <div class="sidebar-item">
            🌍 Vitenge & African-inspired fashion
        </div>

        <div class="sidebar-item">
            👔 Men's suits
        </div>

        <div class="sidebar-item">
            👗 Wedding gowns
        </div>

        <div class="sidebar-item">
            🛠️ Repairs & alterations
        </div>

        <div class="sidebar-item">
            🛍️ Ready-made clothing
        </div>
        """,
        unsafe_allow_html=True
    )


    st.markdown(
        """
        <div class="sidebar-contact">

            <div class="sidebar-contact-title">
                📞 Contact
            </div>

            <div class="sidebar-phone">
                0722285544
            </div>

            <div class="sidebar-contact-text">

                📍 Nairobi CBD<br>
                Accra Road<br>
                Scorpio Building<br><br>

                🕐 Physical Office<br>
                Monday – Saturday<br>
                8:00 AM – 6:00 PM<br><br>

                💻 Online Support<br>
                Monday – Sunday<br>
                9:00 AM – 8:00 PM

            </div>

        </div>
        """,
        unsafe_allow_html=True
    )


# ============================================================
# MAIN HEADER
# ============================================================

st.markdown(
    """
    <div class="main-container">

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

    </div>
    """,
    unsafe_allow_html=True
)


# ============================================================
# WELCOME
# ============================================================

st.markdown(
    """
    <div class="main-container">

        <div class="welcome-card">

            <div class="welcome-title">
                Welcome to Celintex AI 👋
            </div>

            <div class="welcome-text">
                Ask me about our fashion services, custom clothing,
                wedding gowns, men's suits, repairs, pricing and more.
            </div>

        </div>

    </div>
    """,
    unsafe_allow_html=True
)


# ============================================================
# SESSION STATE
# ============================================================

if "messages" not in st.session_state:

    st.session_state.messages = []


# ============================================================
# CHAT HISTORY
# ============================================================

st.markdown(
    '<div class="main-container"><div class="chat-area">',
    unsafe_allow_html=True
)


for message in st.session_state.messages:

    if message["role"] == "user":

        st.markdown(
            f"""
            <div class="user-bubble">
                {message["content"]}
            </div>
            """,
            unsafe_allow_html=True
        )

    else:

        st.markdown(
            f"""
            <div class="assistant-bubble">
                {message["content"]}
            </div>
            """,
            unsafe_allow_html=True
        )


st.markdown(
    "</div></div>",
    unsafe_allow_html=True
)


# ============================================================
# CHAT INPUT
# ============================================================

query = st.chat_input(
    "Ask Celintex anything..."
)


# ============================================================
# HANDLE USER MESSAGE
# ============================================================

if query:

    # --------------------------------------------------------
    # SAVE USER MESSAGE
    # --------------------------------------------------------

    st.session_state.messages.append(
        {
            "role": "user",
            "content": query
        }
    )


    # --------------------------------------------------------
    # DISPLAY USER MESSAGE
    # --------------------------------------------------------

    st.markdown(
        f"""
        <div class="main-container">

            <div class="user-bubble">
                {query}
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )


    # --------------------------------------------------------
    # RAG RETRIEVAL
    # --------------------------------------------------------

    retrieval_start = time.perf_counter()

    context = get_context(
        query,
        3
    )

    retrieval_time = (
        time.perf_counter()
        - retrieval_start
    )


    # --------------------------------------------------------
    # THINKING STATUS
    # --------------------------------------------------------

    status_box = st.empty()

    status_box.markdown(
        """
        <div class="main-container">

            <div class="thinking">
                🧵 Checking Celintex fashion knowledge...
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )


    # --------------------------------------------------------
    # STREAM RESPONSE
    # --------------------------------------------------------

    response_placeholder = st.empty()

    full_response = ""

    generation_start = time.perf_counter()


    try:

        for chunk in stream_response(
            query,
            context
        ):

            full_response += chunk

            response_placeholder.markdown(
                f"""
                <div class="main-container">

                    <div class="assistant-bubble">
                        {full_response}
                    </div>

                </div>
                """,
                unsafe_allow_html=True
            )

            status_box.markdown(
                """
                <div class="main-container">

                    <div class="thinking">
                        ✨ Styling your answer...
                    </div>

                </div>
                """,
                unsafe_allow_html=True
            )


    except Exception as e:

        error_message = str(e)


        if (
            "429" in error_message
            or "Rate limit" in error_message
        ):

            full_response = (
                "⚠️ Celintex AI is temporarily unavailable "
                "because the AI request limit has been reached. "
                "Please try again later or contact Celintex "
                "directly on 0722285544."
            )

        else:

            full_response = (
                "⚠️ I'm having trouble connecting to Celintex AI "
                "right now. Please try again shortly or contact "
                "Celintex on 0722285544."
            )


        response_placeholder.markdown(
            f"""
            <div class="main-container">

                <div class="assistant-bubble">
                    {full_response}
                </div>

            </div>
            """,
            unsafe_allow_html=True
        )


    # --------------------------------------------------------
    # GENERATION TIME
    # --------------------------------------------------------

    generation_time = (
        time.perf_counter()
        - generation_start
    )


    # --------------------------------------------------------
    # REMOVE STATUS
    # --------------------------------------------------------

    status_box.empty()


    # --------------------------------------------------------
    # SAVE RESPONSE
    # --------------------------------------------------------

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": full_response
        }
    )


    # --------------------------------------------------------
    # SPEED INFO
    # --------------------------------------------------------

    st.caption(
        f"⚡ RAG: {retrieval_time:.2f}s • "
        f"Gemini: {generation_time:.2f}s"
    )


# ============================================================
# FOOTER
# ============================================================

st.markdown(
    """
    <div class="footer">
        Celintex Fashion Company • AI Customer Assistant
    </div>
    """,
    unsafe_allow_html=True
)
