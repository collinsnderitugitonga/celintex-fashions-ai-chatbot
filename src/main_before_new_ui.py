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
    layout="centered",
    initial_sidebar_state="expanded"
)


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown(
    """
    <style>

    /* --------------------------------------------------------
       MAIN BACKGROUND
    -------------------------------------------------------- */

    .stApp {
        background:
            radial-gradient(
                circle at top left,
                #fff0f8 0%,
                #faf7ff 45%,
                #f2fbf8 100%
            );
    }


    /* --------------------------------------------------------
       HEADER
    -------------------------------------------------------- */

    .brand-card {
        background:
            linear-gradient(
                135deg,
                #4b164c,
                #7b3f78,
                #9c6ade
            );

        padding: 28px;
        border-radius: 28px;
        margin-bottom: 22px;

        box-shadow:
            0 12px 35px rgba(75, 22, 76, 0.20);

        color: white;
    }

    .brand-icon {
        font-size: 42px;
        margin-bottom: 4px;
    }

    .brand-title {
        font-size: 34px;
        font-weight: 800;
        letter-spacing: 1px;
    }

    .brand-subtitle {
        font-size: 15px;
        opacity: 0.90;
        margin-top: 4px;
    }

    .online-pill {
        display: inline-block;

        margin-top: 16px;
        padding: 7px 13px;

        border-radius: 30px;

        background: rgba(255,255,255,0.16);

        font-size: 13px;
        font-weight: 600;
    }


    /* --------------------------------------------------------
       WELCOME CARD
    -------------------------------------------------------- */

    .welcome-card {
        background: rgba(255,255,255,0.82);

        padding: 20px 22px;

        border-radius: 20px;

        margin-bottom: 18px;

        border: 1px solid rgba(123,63,120,0.10);

        box-shadow:
            0 8px 25px rgba(60,30,70,0.07);
    }

    .welcome-title {
        font-size: 21px;
        font-weight: 750;
        color: #4b164c;
    }

    .welcome-text {
        color: #5e5360;
        margin-top: 5px;
    }


    /* --------------------------------------------------------
       CHAT BUBBLES
    -------------------------------------------------------- */

    .user-bubble {
        background:
            linear-gradient(
                135deg,
                #eadcff,
                #f4eaff
            );

        padding: 13px 17px;

        border-radius:
            20px 20px 5px 20px;

        margin:
            10px 0 10px auto;

        max-width: 85%;

        color: #3f2946;
    }

    .assistant-bubble {
        background: rgba(255,255,255,0.94);

        padding: 15px 18px;

        border-radius:
            20px 20px 20px 5px;

        margin: 10px auto 10px 0;

        max-width: 88%;

        color: #302834;

        border-left:
            4px solid #9c6ade;

        box-shadow:
            0 6px 18px rgba(70,40,80,0.07);
    }


    /* --------------------------------------------------------
       STATUS
    -------------------------------------------------------- */

    .thinking {
        background:
            linear-gradient(
                90deg,
                #fff3fb,
                #f2efff,
                #effaf7
            );

        padding: 12px 16px;

        border-radius: 16px;

        margin: 10px 0;

        color: #674a69;

        font-size: 14px;

        border: 1px solid rgba(123,63,120,0.10);
    }


    /* --------------------------------------------------------
       CONTACT CARD
    -------------------------------------------------------- */

    .contact-card {
        background:
            linear-gradient(
                135deg,
                #4b164c,
                #68325f
            );

        color: white;

        padding: 18px;

        border-radius: 18px;

        margin-top: 20px;
    }

    .contact-title {
        font-size: 17px;
        font-weight: 700;
    }

    .contact-number {
        font-size: 20px;
        font-weight: 800;

        margin-top: 8px;
    }


    /* --------------------------------------------------------
       FOOTER
    -------------------------------------------------------- */

    .footer {
        text-align: center;

        color: #776b78;

        font-size: 12px;

        margin-top: 30px;

        padding-bottom: 20px;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# HEADER
# ============================================================

st.markdown(
    """
    <div class="brand-card">

        <div class="brand-icon">👗</div>

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
# WELCOME
# ============================================================

st.markdown(
    """
    <div class="welcome-card">

        <div class="welcome-title">
            Welcome to Celintex AI 👋
        </div>

        <div class="welcome-text">
            Ask me about our fashion services, custom clothing,
            wedding gowns, men's suits, repairs, pricing and more.
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
# DISPLAY PREVIOUS MESSAGES
# ============================================================

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


# ============================================================
# CHAT INPUT
# ============================================================

query = st.chat_input(
    "Ask Celintex AI anything..."
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
        <div class="user-bubble">
            {query}
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
        <div class="thinking">
            🧵 Checking Celintex fashion knowledge...
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
                <div class="assistant-bubble">
                    {full_response}
                </div>
                """,
                unsafe_allow_html=True
            )

            status_box.markdown(
                """
                <div class="thinking">
                    ✨ Styling your answer...
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
            <div class="assistant-bubble">
                {full_response}
            </div>
            """,
            unsafe_allow_html=True
        )


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
# SIDEBAR
# ============================================================

with st.sidebar:

    st.markdown(
        """
        ## 👗 Celintex Fashion

        **Services**

        🧵 Custom tailoring

        🌍 Vitenge & African-inspired fashion

        👔 Men's suits

        👗 Wedding gowns

        🛍️ Ready-made clothing

        ✂️ Repairs & alterations

        ---

        ### 📍 Location

        Nairobi CBD  
        Accra Road  
        Scorpio Building

        ### 📞 Contact

        **0722285544**

        ### 🕐 Physical Office

        Monday – Saturday  
        8:00 AM – 6:00 PM

        ### 💻 Online Support

        Monday – Sunday  
        9:00 AM – 8:00 PM

        """
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
