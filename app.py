"""
Streamlit UI for the Multi-Agent Research Pipeline.

Run with:
    streamlit run streamlit_app.py

Place this file in the same folder as pipeline.py, agents.py, and tools.py.
"""

import io
import contextlib

import streamlit as st

from pipeline import run_research_pipeline


st.set_page_config(
    page_title="Multi-Agent Research System",
    page_icon="🔎",
    layout="wide",
)

st.title("🔎 Multi-Agent Research System")
st.caption("Search agent → Reader agent → Writer chain → Critic chain")

# ---- Session state setup ----
if "state" not in st.session_state:
    st.session_state.state = None
if "logs" not in st.session_state:
    st.session_state.logs = ""

# ---- Input form ----
with st.form("research_form"):
    topic = st.text_input("Enter a research topic", placeholder="e.g. Latest advances in solid-state batteries")
    submitted = st.form_submit_button("Run Research Pipeline", type="primary", use_container_width=True)

if submitted:
    if not topic.strip():
        st.warning("Please enter a topic before running the pipeline.")
    else:
        st.session_state.state = None
        st.session_state.logs = ""

        progress = st.progress(0, text="Starting pipeline...")
        log_placeholder = st.empty()

        # Capture the print() output from run_research_pipeline so it can be shown in the UI
        buffer = io.StringIO()
        try:
            with contextlib.redirect_stdout(buffer):
                progress.progress(10, text="Step 1/4 — Search agent working...")
                result_state = run_research_pipeline(topic)
            progress.progress(100, text="Pipeline complete!")
            st.session_state.state = result_state
            st.session_state.logs = buffer.getvalue()
            st.success("Research pipeline finished successfully.")
        except Exception as e:
            st.session_state.logs = buffer.getvalue()
            progress.progress(100, text="Pipeline failed.")
            st.error(f"Pipeline failed with error: {e}")

# ---- Results display ----
state = st.session_state.state

if state:
    tab_report, tab_feedback, tab_search, tab_scraped, tab_logs = st.tabs(
        ["📄 Final Report", "🧐 Critic Feedback", "🔍 Search Results", "📚 Scraped Content", "🖥️ Run Logs"]
    )

    with tab_report:
        st.subheader("Final Report")
        st.markdown(state.get("report", "_No report generated._"))
        st.download_button(
            "Download report as .md",
            data=str(state.get("report", "")),
            file_name="research_report.md",
            mime="text/markdown",
        )

    with tab_feedback:
        st.subheader("Critic Feedback")
        st.markdown(state.get("feedback", "_No feedback generated._"))

    with tab_search:
        st.subheader("Search Agent Results")
        st.text_area("Raw search results", state.get("search_results", ""), height=400)

    with tab_scraped:
        st.subheader("Reader Agent — Scraped Content")
        st.text_area("Scraped content", state.get("scraped_content", ""), height=400)

    with tab_logs:
        st.subheader("Pipeline Run Logs")
        st.text_area("Console output", st.session_state.logs, height=400)

elif st.session_state.logs:
    st.subheader("Run Logs")
    st.text_area("Console output", st.session_state.logs, height=400)
else:
    st.info("Enter a topic above and click **Run Research Pipeline** to get started.")

with st.sidebar:
    st.header("About")
    st.write(
        "This UI drives the multi-agent research pipeline defined in `pipeline.py`:\n\n"
        "1. **Search agent** finds recent, relevant sources.\n"
        "2. **Reader agent** scrapes the most relevant page.\n"
        "3. **Writer chain** drafts a report from the research.\n"
        "4. **Critic chain** reviews the report and gives feedback."
    )
    st.divider()
    st.caption("Make sure any required API keys are set in your `.env` file before running.")