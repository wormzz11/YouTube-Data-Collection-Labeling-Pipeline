
import os
import streamlit as st
from googleapiclient.errors import HttpError
from src.export import export
from src.fetch import title_fetcher
from src.database import db_creator, insert_videos
from src.processor import processing

st.set_page_config(
    page_title="Control Panel",
    page_icon="⚙️",
    layout="centered",
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Mono:wght@400;500&family=Syne:wght@700;800&family=DM+Sans:wght@300;400;500&display=swap');

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
    background-color: #0d0f12;
    color: #e8e6e1;
    font-size: 1rem;
}
.stApp { background-color: #0d0f12; }
#MainMenu, footer, header { visibility: hidden; }
.block-container {
    padding: 3rem 2rem 4rem;
    max-width: 720px;
}
.ctrl-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 2.5rem;
    padding-bottom: 1.25rem;
    border-bottom: 1px solid #1e2129;
}
.ctrl-brand {
    font-family: 'Syne', sans-serif;
    font-weight: 800;
    font-size: 1.4rem;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    color: #c8f560;
}
.ctrl-badge {
    font-family: 'DM Mono', monospace;
    font-size: 0.88rem;
    color: #5a5f6e;
    letter-spacing: 0.05em;
}
.section {
    background: #13161c;
    border: 1px solid #1e2129;
    border-radius: 8px;
    padding: 1.5rem;
    margin-bottom: 1.5rem;
}
.section-title {
    font-family: 'Syne', sans-serif;
    font-weight: 700;
    font-size: 1.25rem;
    color: #e8e6e1;
    margin: 0 0 0.25rem 0;
}
.section-sub {
    font-family: 'DM Mono', monospace;
    font-size: 0.85rem;
    color: #5a5f6e;
    margin-bottom: 1.25rem;
}
.stTextInput > div > div > input {
    background: #0d0f12 !important;
    border: 1px solid #1e2129 !important;
    border-radius: 4px !important;
    color: #e8e6e1 !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 1rem !important;
    padding: 0.6rem 0.9rem !important;
}
.stTextInput > div > div > input:focus {
    border-color: #c8f560 !important;
    box-shadow: 0 0 0 1px rgba(200, 245, 96, 0.2) !important;
}
.stTextInput label {
    font-family: 'DM Mono', monospace !important;
    font-size: 0.82rem !important;
    text-transform: uppercase !important;
    letter-spacing: 0.08em !important;
    color: #5a5f6e !important;
}
.stNumberInput > div > div > input {
    background: #0d0f12 !important;
    border: 1px solid #1e2129 !important;
    border-radius: 4px !important;
    color: #e8e6e1 !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 1rem !important;
}
.stNumberInput label {
    font-family: 'DM Mono', monospace !important;
    font-size: 0.82rem !important;
    text-transform: uppercase !important;
    letter-spacing: 0.08em !important;
    color: #5a5f6e !important;
}
.stSelectbox > div > div {
    background: #0d0f12 !important;
    border: 1px solid #1e2129 !important;
    border-radius: 4px !important;
    color: #e8e6e1 !important;
    font-size: 1rem !important;
}
.stSelectbox label {
    font-family: 'DM Mono', monospace !important;
    font-size: 0.82rem !important;
    text-transform: uppercase !important;
    letter-spacing: 0.08em !important;
    color: #5a5f6e !important;
}
.stButton > button {
    font-family: 'DM Sans', sans-serif !important;
    font-weight: 500 !important;
    font-size: 1rem !important;
    letter-spacing: 0.03em !important;
    border-radius: 4px !important;
    padding: 0.7rem 1rem !important;
    height: auto !important;
    transition: all 0.15s ease !important;
    width: 100% !important;
    background: #c8f560 !important;
    color: #0d0f12 !important;
    border: 2px solid #c8f560 !important;
    margin-top: 0.75rem !important;
}
.stButton > button:hover {
    background: #d8ff72 !important;
    border-color: #d8ff72 !important;
    transform: translateY(-1px);
    box-shadow: 0 4px 20px rgba(200, 245, 96, 0.25) !important;
}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="ctrl-header">
    <span class="ctrl-brand">⚙️ Control Panel</span>
    <span class="ctrl-badge">Pipeline · Export · Fetch</span>
</div>
""", unsafe_allow_html=True)

st.markdown('<div class="section">', unsafe_allow_html=True)
st.markdown('<p class="section-title">Export</p>', unsafe_allow_html=True)
st.markdown('<p class="section-sub">Export labeled data for a theme to CSV or Excel</p>', unsafe_allow_html=True)

export_theme = st.text_input("Theme", placeholder="e.g. dogs", key="export_theme")
export_mode = st.selectbox("Mode", options=["labeled", "unlabeled", "all"], key="export_mode")
export_format = st.selectbox("File format", options=["csv", "xlsx"], key="export_format")

if st.button("Export", key="btn_export"):
    if not export_theme.strip():
        st.error("Enter a theme before exporting.")
    else:
        os.makedirs("data/exports", exist_ok=True)
        try:
            export(export_theme.strip(), export_mode, export_format)
            st.success(f"Exported to data/exports/{export_theme.strip()}_{export_mode}.{export_format}")
        except Exception as e:
            st.error(f"Export failed: {e}")

st.markdown('</div>', unsafe_allow_html=True)

st.markdown('<div class="section">', unsafe_allow_html=True)
st.markdown('<p class="section-title">Run Pipeline</p>', unsafe_allow_html=True)
st.markdown('<p class="section-sub">Fetch, process, and insert videos into the database</p>', unsafe_allow_html=True)

pipeline_query = st.text_input("Query", placeholder="e.g. Python", key="pipeline_query")
pipeline_quantity = st.number_input("Quantity", min_value=1, max_value=500, value=20, step=1, key="pipeline_quantity")
pipeline_theme = st.text_input("Assign theme", placeholder="e.g. meow", key="pipeline_theme")

if st.button("Run Pipeline", key="btn_pipeline"):
    if not pipeline_query.strip():
        st.error("Enter a query before running the pipeline.")
    else:
        with st.spinner("Running pipeline..."):
            try:
                db_creator()
                data = title_fetcher(pipeline_query.strip(), int(pipeline_quantity))
                processed_data = processing(data)
                theme = pipeline_theme.strip() if pipeline_theme and pipeline_theme.strip() else None
                insert_videos(processed_data, theme=theme)
                if theme:
                    st.success(f"Pipeline complete — {len(processed_data)} videos processed and inserted with theme \"{theme}\".")
                else:
                    st.success(f"Pipeline complete — {len(processed_data)} videos processed and inserted without a theme.")
            except HttpError as e:
                if getattr(e, "resp", None) and getattr(e.resp, "status", None) == 403:
                    st.error("YouTube API quota exceeded. Resets daily at midnight Pacific Time.")
                else:
                    st.error(f"YouTube API error: {e}")
            except Exception as e:
                st.error(f"Pipeline failed: {e}")
st.markdown('</div>', unsafe_allow_html=True)
