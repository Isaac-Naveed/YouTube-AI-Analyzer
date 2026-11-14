import os
import streamlit as st
from textwrap import dedent
from urllib.parse import urlparse
from youtube_analyzer import build_youtube_agent
from dotenv import load_dotenv

# ==========================================
# 1. PAGE CONFIGURATION
# ==========================================

load_dotenv()

if not os.getenv("GROQ_API_KEY"):
    try:
        os.environ["GROQ_API_KEY"] = st.secrets["GROQ_API_KEY"]
    except Exception:
        st.error("Groq API key is not configured.")
        st.stop()


st.set_page_config(
    page_title="YouTube AI Analyzer",
    page_icon="🎥",
    layout="wide",
    initial_sidebar_state="collapsed"
)


# ==========================================
# 2. CUSTOM CSS
# ==========================================

st.markdown("""
<style>

/* Main background */
.stApp {
    background: linear-gradient(
        135deg,
        #080d1b 0%,
        #10172a 55%,
        #111827 100%
    );
    color: #f8fafc;
}

/* Hide default Streamlit header */
header[data-testid="stHeader"] {
    background: transparent;
}

/* Main container */
.block-container {
    max-width: 1050px;
    padding-top: 2rem;
    padding-bottom: 3rem;
}

/* Hero section */
.hero {
    text-align: center;
    padding: 45px 15px 35px 15px;
}

.hero-badge {
    display: inline-block;
    background: rgba(139, 92, 246, 0.15);
    border: 1px solid rgba(139, 92, 246, 0.4);
    color: #c4b5fd;
    padding: 9px 20px;
    border-radius: 30px;
    font-size: 13px;
    font-weight: 700;
    letter-spacing: 1px;
    margin-bottom: 22px;
}

.hero h1 {
    font-size: clamp(36px, 6vw, 58px);
    font-weight: 800;
    color: #ffffff;
    letter-spacing: -2px;
    margin-bottom: 15px;
}

.gradient-text {
    background: linear-gradient(
        90deg,
        #a78bfa,
        #60a5fa
    );
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.hero p {
    color: #94a3b8;
    font-size: 17px;
    max-width: 680px;
    margin: auto;
    line-height: 1.8;
}

/* Input card */
div[data-testid="stVerticalBlockBorderWrapper"] {
    background: rgba(30, 41, 59, 0.55);
    border: 1px solid rgba(148, 163, 184, 0.16);
    border-radius: 18px;
}

/* Text input */
div[data-testid="stTextInput"] input {
    background-color: #111827;
    color: #ffffff;
    border: 1px solid #334155;
    border-radius: 10px;
    min-height: 48px;
}

div[data-testid="stTextInput"] input:focus {
    border-color: #8b5cf6;
    box-shadow: 0 0 0 2px rgba(139, 92, 246, 0.2);
}

/* Analyze button */
div.stButton > button,
div[data-testid="stFormSubmitButton"] > button {
    background: linear-gradient(
        90deg,
        #7c3aed,
        #4f46e5
    );
    color: white;
    border: none;
    border-radius: 10px;
    min-height: 48px;
    font-size: 16px;
    font-weight: 700;
    transition: all 0.25s ease;
}

div.stButton > button:hover,
div[data-testid="stFormSubmitButton"] > button:hover {
    background: linear-gradient(
        90deg,
        #6d28d9,
        #4338ca
    );
    color: white;
    border: none;
    transform: translateY(-2px);
    box-shadow: 0 8px 25px rgba(124, 58, 237, 0.3);
}

/* Feature cards */
.feature-card {
    background: rgba(30, 41, 59, 0.65);
    border: 1px solid rgba(148, 163, 184, 0.15);
    border-radius: 16px;
    padding: 25px 18px;
    min-height: 175px;
    text-align: center;
    transition: all 0.25s ease;
}

.feature-card:hover {
    border-color: rgba(139, 92, 246, 0.6);
    transform: translateY(-4px);
}

.feature-icon {
    font-size: 32px;
    margin-bottom: 12px;
}

.feature-title {
    color: #f1f5f9;
    font-size: 17px;
    font-weight: 700;
    margin-bottom: 10px;
}

.feature-description {
    color: #94a3b8;
    font-size: 13px;
    line-height: 1.6;
}

/* Section headings */
.section-heading {
    color: #ffffff;
    font-size: 25px;
    font-weight: 750;
    margin-bottom: 18px;
}

/* Footer */
.footer {
    text-align: center;
    color: #64748b;
    font-size: 13px;
    line-height: 1.8;
    padding: 35px 0 10px 0;
}

/* Divider */
hr {
    border-color: rgba(148, 163, 184, 0.15);
}

</style>
""", unsafe_allow_html=True)


# ==========================================
# 3. INITIALIZE AGNO AGENT
# ==========================================

@st.cache_resource
def get_agent():
    return build_youtube_agent()


# ==========================================
# 4. YOUTUBE URL VALIDATION
# ==========================================

def is_valid_youtube_url(url):

    try:
        parsed = urlparse(url.strip())

        hostname = parsed.hostname or ""

        valid_domains = [
            "youtube.com",
            "www.youtube.com",
            "m.youtube.com",
            "music.youtube.com",
            "youtu.be",
            "www.youtu.be"
        ]

        return (
            parsed.scheme in ["http", "https"]
            and hostname.lower() in valid_domains
        )

    except Exception:
        return False


# ==========================================
# 5. HERO SECTION
# ==========================================

st.html("""
<div class="hero">

    <div class="hero-badge">
        ✨ POWERED BY AGNO + GROQ
    </div>

    <h1>
        YouTube <span class="gradient-text">AI Analyzer</span>
    </h1>

    <p>
        Turn hours of YouTube content into structured insights.
        Get detailed summaries, meaningful timestamps, key concepts,
        and organized learning points with AI.
    </p>

</div>
""")


# ==========================================
# 6. VIDEO INPUT SECTION
# ==========================================

st.write("")

with st.container(border=True):

    st.markdown(
        '<h3 style="color:#f8fafc;">🎬 Analyze a YouTube Video</h3>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<p style="color:#94a3b8; font-size:14px;">'
        'Paste your YouTube video link below to get started.'
        '</p>',
        unsafe_allow_html=True
    )

    with st.form("youtube_analysis_form"):

        video_url = st.text_input(
            "YouTube Video URL",
            placeholder="https://www.youtube.com/watch?v=...",
            label_visibility="collapsed"
        )

        submitted = st.form_submit_button(
            "✨  Analyze Video",
            use_container_width=True
        )


# ==========================================
# 7. ANALYZE VIDEO
# ==========================================

if submitted:

    if not video_url.strip():

        st.warning("⚠️ Please enter a YouTube video URL.")

    elif not is_valid_youtube_url(video_url):

        st.error("❌ Invalid YouTube URL. Please enter a valid link.")

    else:

        try:

            with st.spinner(
                "🤖 Your AI agent is analyzing the video. Please wait..."
            ):

                agent = get_agent()

                response = agent.run(
                    f"""
                    Analyze this YouTube video in detail:

                    {video_url}

                    Provide a comprehensive analysis with accurate
                    timestamps, overview, key topics, and learning points.
                    """
                )

                report = response.content

                if not report:
                    raise ValueError(
                        "The agent returned an empty response."
                    )

                st.session_state["analysis_report"] = report
                st.session_state["video_url"] = video_url

        except Exception as e:

            st.error("Something went wrong while analyzing the video.")

            st.exception(e)


# ==========================================
# 8. DISPLAY ANALYSIS REPORT
# ==========================================

if "analysis_report" in st.session_state:

    st.markdown("---")

    st.markdown(
        '<div class="section-heading">'
        '📊 Video Analysis Report'
        '</div>',
        unsafe_allow_html=True
    )

    st.success("Your video analysis is ready!")

    # Video preview
    st.video(st.session_state["video_url"])

    # Analysis report
    with st.container(border=True):

        st.markdown(
            st.session_state["analysis_report"]
        )

    # Download report
    st.download_button(
        label="⬇️ Download Analysis Report",
        data=st.session_state["analysis_report"],
        file_name="youtube_analysis_report.md",
        mime="text/markdown",
        use_container_width=True
    )


# ==========================================
# 9. FEATURES SECTION
# ==========================================

st.markdown("---")

st.markdown(
    """
    <h2 style="
        text-align:center;
        color:#ffffff;
        font-size:28px;
        font-weight:750;
    ">
        What You Get
    </h2>
    """,
    unsafe_allow_html=True
)

st.markdown(
    """
    <p style="
        text-align:center;
        color:#94a3b8;
        margin-bottom:30px;
    ">
        Powerful AI features to help you understand videos faster.
    </p>
    """,
    unsafe_allow_html=True
)

col1, col2, col3 = st.columns(3)

with col1:

    st.markdown(
        dedent("""
        <div class="feature-card">
            <div class="feature-icon">📝</div>
            <div class="feature-title">Video Overview</div>
            <div class="feature-description">
                Understand the video's main topics,
                structure, and content.
            </div>
        </div>
        """),
        unsafe_allow_html=True
    )

with col2:

    st.markdown(
        dedent("""
        <div class="feature-card">
            <div class="feature-icon">⏱️</div>
            <div class="feature-title">Smart Timestamps</div>
            <div class="feature-description">
                Discover important moments and
                navigate through key sections.
            </div>
        </div>
        """),
        unsafe_allow_html=True
    )

with col3:

    st.markdown(
        dedent("""
        <div class="feature-card">
            <div class="feature-icon">🧠</div>
            <div class="feature-title">Key Insights</div>
            <div class="feature-description">
                Extract valuable learning points
                and organize important concepts.
            </div>
        </div>
        """),
        unsafe_allow_html=True
    )


# ==========================================
# 10. FOOTER
# ==========================================

st.markdown(
    dedent("""
    <div class="footer">
        Built with ❤️ using Streamlit, Agno & Groq
        <br>
        YouTube AI Analyzer © 2026
        <br>
        Turning videos into knowledge.
    </div>
    """),
    unsafe_allow_html=True
)
