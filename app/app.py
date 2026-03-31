import streamlit as st
from src.database import insert_evaluation,  evaluation_count, load_next_video,load_adjacent_video


st.set_page_config(
    page_title="Video Evaluator",
    page_icon="🎬",
    layout="centered",
)


st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Mono:wght@400;500&family=Syne:wght@700;800&family=DM+Sans:wght@300;400;500&display=swap');

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
    background-color: #0d0f12;
    color: #e8e6e1;
}
.stApp { background-color: #0d0f12; }
#MainMenu, footer, header { visibility: hidden; }
.block-container {
    padding: 3rem 2rem 4rem;
    max-width: 720px;
}

.eval-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 2.5rem;
    padding-bottom: 1.25rem;
    border-bottom: 1px solid #1e2129;
}
.eval-brand {
    font-family: 'Syne', sans-serif;
    font-weight: 800;
    font-size: 1.1rem;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    color: #c8f560;
}
.eval-badge {
    font-family: 'DM Mono', monospace;
    font-size: 0.72rem;
    color: #5a5f6e;
    letter-spacing: 0.05em;
}

.progress-wrap { margin-bottom: 2.5rem; }
.progress-meta {
    display: flex;
    justify-content: space-between;
    align-items: baseline;
    margin-bottom: 0.5rem;
}
.progress-label {
    font-family: 'DM Mono', monospace;
    font-size: 0.7rem;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    color: #5a5f6e;
}
.progress-count {
    font-family: 'DM Mono', monospace;
    font-size: 0.78rem;
    color: #c8f560;
}
.progress-bar-bg {
    background: #1a1d24;
    border-radius: 2px;
    height: 4px;
    width: 100%;
    overflow: hidden;
}
.progress-bar-fill {
    background: #c8f560;
    height: 100%;
    border-radius: 2px;
    transition: width 0.5s ease;
}

.video-card {
    background: #13161c;
    border: 1px solid #1e2129;
    border-radius: 8px;
    overflow: hidden;
    margin-bottom: 1.25rem;
}
.video-card img { width: 100%; display: block; }
.video-card-body { padding: 1.25rem 1.5rem; }
.video-title {
    font-family: 'Syne', sans-serif;
    font-weight: 700;
    font-size: 2rem;
    line-height: 1.35;
    color: #e8e6e1;
    margin: 0;
}
.video-meta {
    display: flex;
    gap: 1rem;
    margin-top: 0.5rem;
    align-items: center;
}
.video-id {
    font-family: 'DM Mono', monospace;
    font-size: 0.68rem;
    color: #3a3f4e;
}
.label-badge {
    font-family: 'DM Mono', monospace;
    font-size: 0.68rem;
    padding: 0.15rem 0.5rem;
    border-radius: 3px;
}
.label-relevant {
    background: rgba(200, 245, 96, 0.12);
    color: #c8f560;
    border: 1px solid rgba(200, 245, 96, 0.3);
}
.label-irrelevant {
    background: rgba(255, 95, 95, 0.1);
    color: #ff5f5f;
    border: 1px solid rgba(255, 95, 95, 0.25);
}
.label-unlabeled {
    background: rgba(90, 95, 110, 0.15);
    color: #5a5f6e;
    border: 1px solid #1e2129;
}

/* All buttons base */
.stButton > button {
    font-family: 'DM Sans', sans-serif !important;
    font-weight: 500 !important;
    font-size: 0.88rem !important;
    letter-spacing: 0.03em !important;
    border-radius: 4px !important;
    padding: 0.65rem 1rem !important;
    height: auto !important;
    transition: all 0.15s ease !important;
    width: 100% !important;
}

/* Row 1: Relevant (col 0) | Irrelevant (col 1) */
div[data-testid="stHorizontalBlock"]:nth-of-type(1)
    div[data-testid="column"]:nth-child(1) .stButton > button {
    background: #c8f560 !important;
    color: #0d0f12 !important;
    border: 2px solid #c8f560 !important;
}
div[data-testid="stHorizontalBlock"]:nth-of-type(1)
    div[data-testid="column"]:nth-child(1) .stButton > button:hover {
    background: #d8ff72 !important;
    border-color: #d8ff72 !important;
    transform: translateY(-1px);
    box-shadow: 0 4px 20px rgba(200, 245, 96, 0.25) !important;
}
div[data-testid="stHorizontalBlock"]:nth-of-type(1)
    div[data-testid="column"]:nth-child(2) .stButton > button {
    background: transparent !important;
    color: #5a5f6e !important;
    border: 2px solid #1e2129 !important;
}
div[data-testid="stHorizontalBlock"]:nth-of-type(1)
    div[data-testid="column"]:nth-child(2) .stButton > button:hover {
    border-color: #ff5f5f !important;
    color: #ff5f5f !important;
    transform: translateY(-1px);
}

/* Row 2: Prev (col 0) | Next (col 1) — both ghost neutral */
div[data-testid="stHorizontalBlock"]:nth-of-type(2) .stButton > button {
    background: transparent !important;
    color: #5a5f6e !important;
    border: 2px solid #1e2129 !important;
    font-size: 0.8rem !important;
}
div[data-testid="stHorizontalBlock"]:nth-of-type(2) .stButton > button:hover {
    border-color: #3a3f4e !important;
    color: #e8e6e1 !important;
    transform: translateY(-1px);
}

.done-state {
    text-align: center;
    padding: 5rem 2rem;
}
.done-icon { font-size: 3rem; margin-bottom: 1rem; }
.done-title {
    font-family: 'Syne', sans-serif;
    font-size: 1.6rem;
    font-weight: 800;
    color: #c8f560;
    margin-bottom: 0.5rem;
}
.done-sub { color: #5a5f6e; font-size: 0.9rem; }
</style>
""", unsafe_allow_html=True)



def set_video(video):
    st.session_state.video = video


def label_current(relevancy: int):
    video = st.session_state.video
    insert_evaluation((video["videoId"], relevancy))
    next_video = load_adjacent_video(video["id"], direction="next")
    st.session_state.video = next_video if next_video else load_next_video()


def go_adjacent(direction: str):
    video = st.session_state.video
    adjacent = load_adjacent_video(video["id"], direction=direction)
    if adjacent:
        st.session_state.video = adjacent


def label_badge(relevant):
    if relevant == 1:
        return '<span class="label-badge label-relevant">✓ Relevant</span>'
    elif relevant == 0:
        return '<span class="label-badge label-irrelevant">✕ Irrelevant</span>'
    return '<span class="label-badge label-unlabeled">Unlabeled</span>'



def main():
    st.markdown("""
    <div class="eval-header">
        <span class="eval-brand">🎬 Video Evaluator</span>
        <span class="eval-badge">Pipeline · Labeling Tool</span>
    </div>
    """, unsafe_allow_html=True)

    labeled, unlabeled = evaluation_count()
    total = labeled + unlabeled

    if total == 0:
        st.markdown("""
        <div class="done-state">
            <div class="done-icon">📭</div>
            <div class="done-title">No videos loaded</div>
            <div class="done-sub">Insert videos into the database first.</div>
        </div>
        """, unsafe_allow_html=True)
        st.stop()


    progress = labeled / total
    pct = int(progress * 100)
    st.markdown(f"""
    <div class="progress-wrap">
        <div class="progress-meta">
            <span class="progress-label">Evaluation progress</span>
            <span class="progress-count">{labeled} / {total} &nbsp;·&nbsp; {pct}%</span>
        </div>
        <div class="progress-bar-bg">
            <div class="progress-bar-fill" style="width:{pct}%"></div>
        </div>
    </div>
    """, unsafe_allow_html=True)

  
    if "video" not in st.session_state:
        st.session_state.video = load_next_video()

    video = st.session_state.video

    if video is None:
        st.markdown("""
        <div class="done-state">
            <div class="done-icon">✅</div>
            <div class="done-title">All done!</div>
            <div class="done-sub">Every video has been evaluated.</div>
        </div>
        """, unsafe_allow_html=True)
        st.stop()


    badge = label_badge(video["relevant"])
    st.markdown(f"""
    <div class="video-card">
        <img src="{video['thumbnail']}" alt="thumbnail" />
        <div class="video-card-body">
            <p class="video-title">{video['title']}</p>
            <div class="video-meta">
                <span class="video-id">ID: {video['videoId']}</span>
                {badge}
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        if st.button("✓  Relevant", key="relevant"):
            label_current(1)
            st.rerun()
    with col2:
        if st.button("✕  Irrelevant", key="irrelevant"):
            label_current(0)
            st.rerun()
    
    col3, col4 = st.columns(2)
    with col3:
        if st.button("← Previous", key="prev"):
            go_adjacent("prev")
            st.rerun()
    with col4:
        if st.button("Next →", key="next"):
            go_adjacent("next")
            st.rerun()


if __name__ == "__main__":
    main()