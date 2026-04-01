import streamlit as st
import html
from src.database import (
    insert_evaluation,
    evaluation_count,
    load_next_video_for_theme,
    load_adjacent_video,
    load_adjacent_labeled_for_theme,
    load_first_labeled_for_theme,
    load_video_by_videoId,
    load_video_theme_status,
    db_creator,
)

st.set_page_config(page_title="Video Evaluator", page_icon="🎬", layout="centered")

st.markdown(
    """
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Mono:wght@400;500&family=Syne:wght@700;800&family=DM+Sans:wght@300;400;500&display=swap');
html, body, [class*="css"] { font-family: 'DM Sans', sans-serif; background-color: #0d0f12; color: #e8e6e1; }
.stApp { background-color: #0d0f12; } #MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 3rem 2rem 4rem; max-width: 720px; }
.eval-header { display: flex; align-items: center; justify-content: space-between; margin-bottom: 2rem; padding-bottom: 1.25rem; border-bottom: 1px solid #1e2129; }
.eval-brand { font-family: 'Syne', sans-serif; font-weight: 800; font-size: 1.1rem; letter-spacing: 0.08em; text-transform: uppercase; color: #c8f560; }
.eval-badge { font-family: 'DM Mono', monospace; font-size: 0.72rem; color: #5a5f6e; letter-spacing: 0.05em; }
.theme-label { font-family: 'DM Mono', monospace; font-size: 0.7rem; text-transform: uppercase; letter-spacing: 0.1em; color: #5a5f6e; margin-bottom: 0.4rem; }
.theme-active { font-family: 'DM Mono', monospace; font-size: 0.75rem; color: #c8f560; margin-top: 0.35rem; margin-bottom: 1.5rem; }
.theme-empty { font-family: 'DM Mono', monospace; font-size: 0.75rem; color: #3a3f4e; margin-top: 0.35rem; margin-bottom: 1.5rem; }
.stTextInput > div > div > input { background: #13161c !important; border: 1px solid #1e2129 !important; border-radius: 4px !important; color: #e8e6e1 !important; font-family: 'DM Sans', sans-serif !important; font-size: 0.9rem !important; padding: 0.55rem 0.85rem !important; }
.stTextInput > div > div > input:focus { border-color: #c8f560 !important; box-shadow: 0 0 0 1px rgba(200, 245, 96, 0.2) !important; }
.stTextInput label { display: none !important; }
.progress-wrap { margin-bottom: 2rem; }
.progress-meta { display: flex; justify-content: space-between; align-items: baseline; margin-bottom: 0.5rem; }
.progress-label { font-family: 'DM Mono', monospace; font-size: 0.7rem; text-transform: uppercase; letter-spacing: 0.1em; color: #5a5f6e; }
.progress-count { font-family: 'DM Mono', monospace; font-size: 0.78rem; color: #c8f560; }
.progress-bar-bg { background: #1a1d24; border-radius: 2px; height: 4px; width: 100%; overflow: hidden; }
.progress-bar-fill { background: #c8f560; height: 100%; border-radius: 2px; transition: width 0.5s ease; }
.video-card { background: #13161c; border: 1px solid #1e2129; border-radius: 8px; overflow: hidden; margin-bottom: 1.25rem; }
.video-card img { width: 100%; display: block; }
.video-card-body { padding: 1.25rem 1.5rem; }
.video-title { font-family: 'Syne', sans-serif; font-weight: 700; font-size: 1.5rem; line-height: 1.35; color: #e8e6e1; margin: 0; }
.video-meta { display: flex; gap: 0.6rem; margin-top: 0.5rem; align-items: center; flex-wrap: wrap; }
.video-id { font-family: 'DM Mono', monospace; font-size: 0.68rem; color: #3a3f4e; }
.label-badge { font-family: 'DM Mono', monospace; font-size: 0.68rem; padding: 0.15rem 0.5rem; border-radius: 3px; }
.label-relevant { background: rgba(200, 245, 96, 0.12); color: #c8f560; border: 1px solid rgba(200, 245, 96, 0.3); }
.label-irrelevant { background: rgba(255, 95, 95, 0.1); color: #ff5f5f; border: 1px solid rgba(255, 95, 95, 0.25); }
.label-unlabeled { background: rgba(90, 95, 110, 0.15); color: #5a5f6e; border: 1px solid #1e2129; }
.theme-badge { font-family: 'DM Mono', monospace; font-size: 0.68rem; padding: 0.15rem 0.5rem; border-radius: 3px; background: rgba(255, 255, 255, 0.04); color: #8888aa; border: 1px solid #2a2d36; }
.theme-eval-badge { font-family: 'DM Mono', monospace; font-size: 0.68rem; padding: 0.15rem 0.5rem; border-radius: 3px; background: rgba(200, 245, 96, 0.06); color: #8aaa55; border: 1px solid rgba(200, 245, 96, 0.2); }
.stButton > button { font-family: 'DM Sans', sans-serif !important; font-weight: 500 !important; font-size: 0.88rem !important; letter-spacing: 0.03em !important; border-radius: 4px !important; padding: 0.65rem 1rem !important; height: auto !important; transition: all 0.15s ease !important; width: 100% !important; }
div[data-testid="stHorizontalBlock"]:nth-of-type(1) div[data-testid="column"]:nth-child(1) .stButton > button { background: #c8f560 !important; color: #0d0f12 !important; border: 2px solid #c8f560 !important; }
div[data-testid="stHorizontalBlock"]:nth-of-type(1) div[data-testid="column"]:nth-child(1) .stButton > button:hover { background: #d8ff72 !important; border-color: #d8ff72 !important; transform: translateY(-1px); box-shadow: 0 4px 20px rgba(200, 245, 96, 0.25) !important; }
div[data-testid="stHorizontalBlock"]:nth-of-type(1) div[data-testid="column"]:nth-child(2) .stButton > button { background: transparent !important; color: #5a5f6e !important; border: 2px solid #1e2129 !important; }
div[data-testid="stHorizontalBlock"]:nth-of-type(1) div[data-testid="column"]:nth-child(2) .stButton > button:hover { border-color: #ff5f5f !important; color: #ff5f5f !important; transform: translateY(-1px); }
div[data-testid="stHorizontalBlock"]:nth-of-type(2) .stButton > button { background: transparent !important; color: #5a5f6e !important; border: 2px solid #1e2129 !important; font-size: 0.8rem !important; }
div[data-testid="stHorizontalBlock"]:nth-of-type(2) .stButton > button:hover { border-color: #3a3f4e !important; color: #e8e6e1 !important; transform: translateY(-1px); }
.done-state { text-align: center; padding: 5rem 2rem; }
.done-icon { font-size: 3rem; margin-bottom: 1rem; }
.done-title { font-family: 'Syne', sans-serif; font-size: 1.6rem; font-weight: 800; color: #c8f560; margin-bottom: 0.5rem; }
.done-sub { color: #5a5f6e; font-size: 0.9rem; }
</style>
""",
    unsafe_allow_html=True,
)

def _row_to_dict(row):
    return dict(row) if row is not None else None

def _ensure_base_id(video):
    if video is None:
        return None
    if video.get("theme") is None:
        return video["id"]
    base = load_video_by_videoId(video["videoId"])
    return base["id"] if base else video["id"]

def get_theme():
    return st.session_state.get("theme", "").strip() or None

def label_badge(relevant):
    if relevant == 1:
        return '<span class="label-badge label-relevant">✓ Relevant</span>'
    if relevant == 0:
        return '<span class="label-badge label-irrelevant">✕ Irrelevant</span>'
    return '<span class="label-badge label-unlabeled">Unlabeled</span>'

def main():
    db_creator()
    st.markdown('<div class="eval-header"><span class="eval-brand">🎬 Video Evaluator</span><span class="eval-badge">Pipeline · Labeling Tool</span></div>', unsafe_allow_html=True)
    st.markdown('<div class="theme-label">Current theme</div>', unsafe_allow_html=True)
    theme_input = st.text_input(label="theme", placeholder="e.g. dogs, climate, finance ...", key="theme")
    theme = theme_input.strip() if theme_input else None
    prev_theme = st.session_state.get("_prev_theme")
    if prev_theme != theme:
        st.session_state["_prev_theme"] = theme
        st.session_state["video"] = None
        st.session_state["nav_mode"] = "candidates"
    if theme:
        st.markdown(f'<div class="theme-active">⬡ &nbsp;Labeling as: <strong>{html.escape(theme)}</strong></div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="theme-empty">No theme set — evaluations will have no theme attached</div>', unsafe_allow_html=True)
    if not theme:
        st.markdown('<div class="video-card" style="opacity:0.85;"><div class="video-card-body"><p class="video-title">Enter a theme to load videos</p><div class="video-meta"><span class="video-id">ID: —</span><span class="label-badge label-unlabeled">No theme</span></div></div></div>', unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        with col1:
            st.button("✓  Relevant", key="relevant", disabled=True)
        with col2:
            st.button("✕  Irrelevant", key="irrelevant", disabled=True)
        col3, col4 = st.columns(2)
        with col3:
            st.button("← Previous", key="prev", disabled=True)
        with col4:
            st.button("Next →", key="next", disabled=True)
        st.info("Please enter a theme (for example: dogs, climate, finance) to begin labeling.")
        st.stop()
    if "nav_mode" not in st.session_state:
        st.session_state["nav_mode"] = "candidates"
    nav_mode = st.radio("Navigation mode", ("candidates", "labeled"), index=0, horizontal=True, key="nav_mode_radio")
    st.session_state["nav_mode"] = nav_mode
    labeled, unlabeled = evaluation_count(theme)
    total = labeled + unlabeled
    if total == 0 and nav_mode == "candidates":
        st.markdown('<div class="done-state"><div class="done-icon">✅</div><div class="done-title">All done!</div><div class="done-sub">Every video has been evaluated for this theme.</div></div>', unsafe_allow_html=True)
    pct = int((labeled / total) * 100) if total > 0 else 0
    st.markdown(f'<div class="progress-wrap"><div class="progress-meta"><span class="progress-label">Evaluation progress</span><span class="progress-count">{labeled} / {total} · {pct}%</span></div><div class="progress-bar-bg"><div class="progress-bar-fill" style="width:{pct}%"></div></div></div>', unsafe_allow_html=True)
    if "video" not in st.session_state or st.session_state["video"] is None:
        if nav_mode == "candidates":
            row = load_next_video_for_theme(theme)
            st.session_state["video"] = _row_to_dict(row)
        else:
            row = load_first_labeled_for_theme(theme)
            st.session_state["video"] = _row_to_dict(row)
    video = st.session_state["video"]
    if video is None:
        st.markdown('<div class="done-state"><div class="done-icon">✅</div><div class="done-title">No videos to show</div><div class="done-sub">Try switching navigation mode or seeding base videos.</div></div>', unsafe_allow_html=True)
        st.stop()
    row = load_video_theme_status(video["videoId"], theme)
    theme_status = row["relevant"] if row else None
    safe_title = html.escape(video.get("title", "") or "")
    safe_video_id = html.escape(video.get("videoId", "") or "")
    safe_thumbnail = html.escape(video.get("thumbnail", "") or "")
    safe_theme = html.escape(theme)
    if theme_status is None:
        label_word = "Unlabeled"
    elif theme_status == 1:
        label_word = "Relevant"
    else:
        label_word = "Irrelevant"
    theme_eval_note = f'<span class="theme-eval-badge">Already labeled \"{label_word}\" for {safe_theme}</span>'
    badge_html = ""
    st.markdown(f'<div class="video-card"><img src=\"{safe_thumbnail}\" alt=\"thumbnail\" /><div class=\"video-card-body\"><p class=\"video-title\">{safe_title}</p><div class=\"video-meta\"><span class=\"video-id\">ID: {safe_video_id}</span>{badge_html}<span class=\"theme-badge\">⬡ {safe_theme}</span>{theme_eval_note}</div></div></div>', unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        if st.button("✓  Relevant", key="relevant"):
            insert_evaluation((video["videoId"], 1, theme))
            if nav_mode == "candidates":
                row = load_next_video_for_theme(theme)
            else:
                row = load_first_labeled_for_theme(theme)
            st.session_state["video"] = _row_to_dict(row)
            st.rerun()
    with col2:
        if st.button("✕  Irrelevant", key="irrelevant"):
            insert_evaluation((video["videoId"], 0, theme))
            if nav_mode == "candidates":
                row = load_next_video_for_theme(theme)
            else:
                row = load_first_labeled_for_theme(theme)
            st.session_state["video"] = _row_to_dict(row)
            st.rerun()
    col3, col4 = st.columns(2)
    with col3:
        if st.button("← Previous", key="prev"):
            if nav_mode == "candidates":
                base_id = _ensure_base_id(video)
                row = load_adjacent_video(base_id, direction="prev", theme=theme)
            else:
                cur_theme_row = load_video_theme_status(video["videoId"], theme)
                cur_id = cur_theme_row["id"] if cur_theme_row and "id" in cur_theme_row.keys() else None
                if cur_id:
                    row = load_adjacent_labeled_for_theme(cur_id, direction="prev", theme=theme)
                else:
                    row = None
            st.session_state["video"] = _row_to_dict(row)
            st.rerun()
    with col4:
        if st.button("Next →", key="next"):
            if nav_mode == "candidates":
                base_id = _ensure_base_id(video)
                row = load_adjacent_video(base_id, direction="next", theme=theme)
            else:
                cur_theme_row = load_video_theme_status(video["videoId"], theme)
                cur_id = cur_theme_row["id"] if cur_theme_row and "id" in cur_theme_row.keys() else None
                if cur_id:
                    row = load_adjacent_labeled_for_theme(cur_id, direction="next", theme=theme)
                else:
                    row = None
            st.session_state["video"] = _row_to_dict(row)
            st.rerun()

if __name__ == "__main__":
    main()
