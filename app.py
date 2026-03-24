import json
import time
import streamlit as st
from code_editor import code_editor
from reviewer import review_code

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(page_title="Python Code Reviewer", page_icon="🐍", layout="wide")

# ── Usage protection ──────────────────────────────────────────────────────────
MAX_REQUESTS_PER_SESSION = 5
COOLDOWN_SECONDS = 15
MAX_CODE_LENGTH = 6000

if "request_count" not in st.session_state:
    st.session_state.request_count = 0

if "last_request_time" not in st.session_state:
    st.session_state.last_request_time = 0

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown(
    """
<style>
    .stApp {
        background: linear-gradient(135deg, #0b1020 0%, #161b33 45%, #1f2550 100%);
        color: #f8fafc;
    }

    .block-container {
        max-width: 1100px;
        padding-top: 2rem;
        padding-bottom: 3rem;
    }

    .hero {
        text-align: center;
        padding: 1.2rem 0 2rem 0;
    }

    .main-title {
        font-size: 3.2rem;
        font-weight: 800;
        margin-bottom: 0.4rem;
        background: linear-gradient(90deg, #ff4ecd, #7c5cff);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }

    .subtitle {
        color: #cbd5e1;
        font-size: 1.08rem;
        line-height: 1.7;
        max-width: 760px;
        margin: 0 auto;
    }

    .section-heading {
        font-size: 2rem;
        font-weight: 800;
        color: #ffffff;
        margin-top: 1rem;
        margin-bottom: 0.8rem;
    }

    .card {
        background: rgba(255, 255, 255, 0.06);
        border: 1px solid rgba(255, 255, 255, 0.10);
        border-radius: 18px;
        padding: 1.25rem;
        margin-top: 1rem;
        margin-bottom: 1rem;
        box-shadow: 0 8px 24px rgba(0, 0, 0, 0.18);
    }

    .section-title {
        font-size: 1.15rem;
        font-weight: 700;
        margin-bottom: 1rem;
        letter-spacing: 0.2px;
    }

    .bug-title { color: #ff7b7b; }
    .complex-title { color: #ffd54a; }
    .oop-title { color: #68e0a1; }
    .rewrite-title { color: #69a8ff; }

    .helper-text {
        color: #dbe4f0;
        font-size: 0.97rem;
        line-height: 1.8;
    }

    /* Text area */
    .stTextArea textarea {
        background: #07122b !important;
        color: #f8fafc !important;
        border: 1px solid rgba(255,255,255,0.18) !important;
        border-radius: 14px !important;
        font-family: Consolas, "Courier New", monospace !important;
        font-size: 0.95rem !important;
        line-height: 1.6 !important;
        padding: 1rem !important;
    }
    .stTextArea textarea::placeholder {
    color: #94a3b8 !important;
    opacity: 1 !important;
    }

    .stTextArea label {
        color: #e2e8f0 !important;
        font-weight: 700 !important;
    }

    /* Button */
    .stButton > button {
        background: linear-gradient(90deg, #ff4ecd, #7c5cff);
        color: white;
        border: none;
        border-radius: 12px;
        padding: 0.85rem 1.2rem;
        font-size: 1rem;
        font-weight: 700;
        width: 100%;
        box-shadow: 0 8px 20px rgba(124, 92, 255, 0.35);
        transition: 0.2s ease;
    }

    .stButton > button:hover {
        transform: translateY(-1px);
        opacity: 0.97;
    }

    /* Metrics */
    div[data-testid="stMetric"] {
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255,255,255,0.10);
        padding: 1rem;
        border-radius: 14px;
    }

    div[data-testid="stMetricLabel"] {
        color: #cbd5e1;
        font-weight: 600;
    }

    div[data-testid="stMetricValue"] {
        color: #ffffff;
        font-weight: 800;
    }

    /* Tabs */
    div[data-testid="stTabs"] {
        margin-top: 0.4rem;
    }

    button[data-baseweb="tab"] {
        color: #94a3b8 !important;
        font-weight: 600 !important;
        background: transparent !important;
        border: none !important;
    }

    button[data-baseweb="tab"]:hover {
        color: #ffffff !important;
        background: transparent !important;
    }

    button[data-baseweb="tab"][aria-selected="true"] {
        color: #ffffff !important;
        border-bottom: 2px solid #7c5cff !important;
    }

    /* Expander */
    div[data-testid="stExpander"] {
        background: rgba(255,255,255,0.04) !important;
        border: 1px solid rgba(255,255,255,0.08) !important;
        border-radius: 12px !important;
        overflow: hidden !important;
    }

    div[data-testid="stExpander"] summary {
        color: #e2e8f0 !important;
        font-weight: 600 !important;
    }

    div[data-testid="stExpander"] div[role="region"] {
        color: #dbe4f0 !important;
    }

    /* Inline code */
    code {
        background: rgba(255,255,255,0.08) !important;
        color: #f8fafc !important;
        padding: 2px 6px !important;
        border-radius: 6px !important;
    }

    /* Code block */
    pre {
        background: #020617 !important;
        color: #f8fafc !important;
        border-radius: 12px !important;
    }

    .stCodeBlock {
        border-radius: 14px;
        overflow: hidden;
    }

    hr {
        border: none;
        height: 1px;
        background: rgba(255,255,255,0.08);
        margin: 1.2rem 0 1.8rem 0;
    }
    /* REMOVE TOP WHITE BAR */
    header[data-testid="stHeader"] {
        background: transparent !important;
    }

    header {
        visibility: hidden;
        height: 0px;
    }

    div[data-testid="stDecoration"] {
        display: none !important;
    }
    
    
    .editor-label {
    color: #e2e8f0;
    font-weight: 700;
    font-size: 1.05rem;
    margin-bottom: 0.6rem;
    letter-spacing: 0.3px;
    }
    div[data-testid="stElementContainer"]:has(.streamlit_code-editor) {
    border: 1px solid rgba(255,255,255,0.25);  
    border-radius: 5px;                      
    overflow: hidden;
    background: transparent;                  
    padding: 2px;
    }

    div[data-testid="stElementContainer"]:has(.streamlit_code-editor) iframe {
        border: none !important;
        display: block;
    }     
    .metric-box {
    background: rgba(255,255,255,0.05);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 14px;
    padding: 1rem;
    }

    .metric-label {
        color: #94a3b8;
        font-size: 0.85rem;
        font-weight: 600;
        margin-bottom: 0.4rem;
    }

    .metric-value {
        color: #ffffff;
        font-size: 1.6rem;
        font-weight: 800;
    }
</style>
""",
    unsafe_allow_html=True,
)

# ── Header ────────────────────────────────────────────────────────────────────
st.markdown(
    """
<div class="hero">
    <div class="main-title">🐍 Python Code Reviewer</div>
    <div class="subtitle">
        Paste your Python code and get a clean AI-powered review with bug detection,
        complexity analysis, design suggestions, and improved code.
    </div>
</div>
""",
    unsafe_allow_html=True,
)

# ── Input section ─────────────────────────────────────────────────────────────
st.markdown(
    '<div class="editor-label">Paste your Python code</div>', unsafe_allow_html=True
)

editor_result = code_editor(
    code="def my_function():\n    # paste your Python code here\n    pass",
    lang="python",
    theme="monokai",
    height=[14, 16],
    options={
        "wrap": True,
        "showLineNumbers": True,
    },
    response_mode=["debounce"],
    props={"style": {"borderRadius": "14px", "fontSize": "15px"}},
    component_props={
        "style": {
            "width": "100%",
            "borderRadius": "14px",
            "overflow": "hidden",
            "background": "#07122b",
            "boxSizing": "border-box",
        },
        "css": """
            font-weight: 500;
            border-radius: 14px;
            overflow: hidden;

            &.streamlit_code-editor {
                border-radius: 14px;
                overflow: hidden;
                background: #07122b !important;
            }

            &.streamlit_code-editor .ace-streamlit-dark.ace_editor {
                    background-color: #07122b !important;
                    color: #f8fafc !important;
                    border-radius: 14px !important;
                    overflow: hidden !important;
            }

            &.streamlit_code-editor .ace_gutter {
                background: #0b1633 !important;
                color: #94a3b8 !important;
                border-top-left-radius: 14px !important;
                border-bottom-left-radius: 14px !important;
            }

            &.streamlit_code-editor .ace_scroller {
                background-color: #07122b !important;
            }

            &.streamlit_code-editor .ace_content {
                background-color: #07122b !important;
            }

            &.streamlit_code-editor .ace_layer.ace_gutter-layer {
                background: #0b1633 !important;
            }

            &.streamlit_code-editor .ace_active-line {
                background: rgba(255,255,255,0.04) !important;
            }

            &.streamlit_code-editor .ace_cursor {
                color: #ffffff !important;
            }

            &.streamlit_code-editor .ace_identifier {
                color: #f8f8f2 !important;
            }

            &.streamlit_code-editor .ace_variable {
                color: #f8f8f2 !important;
            }

            &.streamlit_code-editor .ace_text-layer {
                color: #f8f8f2 !important;
            }
            
            &.streamlit_code-editor,
            &.streamlit_code-editor * {
                box-sizing: border-box !important;
            }

            &.streamlit_code-editor {
                border-radius: 12px !important;
                overflow: hidden !important;
            }
        """,
        "globalCSS": """
            :root {
                --streamlit-dark-background-color: #07122b;
            }
        """,
    },
    key="code_editor_main",
)

code_input = ""
if editor_result and isinstance(editor_result, dict):
    code_input = editor_result.get("text", "")

col1, col2 = st.columns([5.2, 1.3])
with col2:
    analyse_btn = st.button("🔍 Analyse My Code", key="analyse_main")

st.caption(
    f"Usage this session: {st.session_state.request_count}/{MAX_REQUESTS_PER_SESSION} • Cooldown: {COOLDOWN_SECONDS}s"
)

# ── Results ───────────────────────────────────────────────────────────────────
if analyse_btn:
    current_time = time.time()

    if not code_input.strip():
        st.warning("⚠️ Please paste some Python code first.")

    elif len(code_input) > MAX_CODE_LENGTH:
        st.warning(f"⚠️ Code is too long. Please keep it under {MAX_CODE_LENGTH} characters.")

    elif st.session_state.request_count >= MAX_REQUESTS_PER_SESSION:
        st.error(
            f"❌ Session limit reached. You can only analyse {MAX_REQUESTS_PER_SESSION} times per session."
        )

    elif current_time - st.session_state.last_request_time < COOLDOWN_SECONDS:
        remaining = int(COOLDOWN_SECONDS - (current_time - st.session_state.last_request_time))
        st.warning(f"⏳ Please wait {remaining} more seconds before trying again.")

    else:
        st.session_state.request_count += 1
        st.session_state.last_request_time = current_time

        with st.spinner("Reviewing your code..."):
            try:
                result = review_code(code_input)

                st.markdown("---")
                st.markdown(
                    '<div class="section-heading">Review Summary</div>',
                    unsafe_allow_html=True,
                )

                bugs_tab, complexity_tab, design_tab, rewritten_tab = st.tabs(
                    ["Bugs", "Complexity", "Design Suggestions", "Rewritten Code"]
                )

                with bugs_tab:
                    st.markdown('<div class="card">', unsafe_allow_html=True)
                    st.markdown(
                        '<div class="section-title bug-title">🐛 Bug Detection</div>',
                        unsafe_allow_html=True,
                    )

                    bugs = result.get("bugs", [])
                    if not bugs:
                        st.success("✅ No bugs detected.")
                    else:
                        for bug in bugs:
                            line = bug.get("line", "?")
                            issue = bug.get("issue", "Issue found")
                            fix = bug.get("fix", "No fix provided")

                            with st.expander(f"Line {line} — {issue}"):
                                st.markdown(f"**Fix:** {fix}")

                    st.markdown("</div>", unsafe_allow_html=True)

                with complexity_tab:
                    st.markdown('<div class="card">', unsafe_allow_html=True)
                    st.markdown(
                        '<div class="section-title complex-title">⏱️ Complexity Analysis</div>',
                        unsafe_allow_html=True,
                    )

                    complexity = result.get("complexity", {})

                    col_t, col_s = st.columns(2)

                    with col_t:
                        st.markdown(
                            f"""
                        <div class="metric-box">
                            <div class="metric-label">Time Complexity</div>
                            <div class="metric-value">{complexity.get("time", "N/A")}</div>
                        </div>
                        """,
                            unsafe_allow_html=True,
                        )

                    with col_s:
                        st.markdown(
                            f"""
                        <div class="metric-box">
                            <div class="metric-label">Space Complexity</div>
                            <div class="metric-value">{complexity.get("space", "N/A")}</div>
                        </div>
                        """,
                            unsafe_allow_html=True,
                        )

                    st.markdown(
                        f'<div class="helper-text">{complexity.get("explanation", "No explanation provided.")}</div>',
                        unsafe_allow_html=True,
                    )

                    st.markdown("</div>", unsafe_allow_html=True)

                with design_tab:
                    st.markdown('<div class="card">', unsafe_allow_html=True)
                    st.markdown(
                        '<div class="section-title oop-title">🏗️ Design Suggestions</div>',
                        unsafe_allow_html=True,
                    )

                    oop_suggestions = result.get("oop_suggestions", [])
                    if not oop_suggestions:
                        st.success("✅ No design improvements needed.")
                    else:
                        for i, suggestion in enumerate(oop_suggestions, 1):
                            st.markdown(
                                f'<div class="helper-text"><b>{i}.</b> {suggestion}</div>',
                                unsafe_allow_html=True,
                            )

                    st.markdown("</div>", unsafe_allow_html=True)

                with rewritten_tab:
                    st.markdown('<div class="card">', unsafe_allow_html=True)
                    st.markdown(
                        '<div class="section-title rewrite-title">✨ Rewritten Code</div>',
                        unsafe_allow_html=True,
                    )

                    rewritten = result.get("rewritten_code", "")
                    if rewritten:
                        st.code(rewritten, language="python")
                    else:
                        st.warning("No rewritten code provided.")

                    st.markdown("</div>", unsafe_allow_html=True)

            except json.JSONDecodeError:
                st.error("❌ Could not parse the AI response. Please try again.")
            except Exception as e:
                st.error(f"❌ Something went wrong: {e}")
