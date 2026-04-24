import streamlit as st

from app.agent import LifeInsuranceAgent
from app.memory import clear_session, init_db, load_recent_history


st.set_page_config(
    page_title="Life Insurance Support Assistant",
    layout="centered",
)


@st.cache_resource
def get_agent() -> LifeInsuranceAgent:
    return LifeInsuranceAgent()


def render_history(session_id: str) -> None:
    for item in load_recent_history(session_id, limit=50):
        with st.chat_message(item["role"]):
            st.markdown(item["content"])


init_db()

st.title("Life Insurance Support Assistant")

with st.sidebar:
    session_id = st.text_input("Session ID", value="streamlit-demo")

    if st.button("Reset Chat", use_container_width=True):
        clear_session(session_id)
        st.rerun()

    st.divider()
    st.caption("General educational information only.")

if not session_id.strip():
    st.warning("Enter a session ID to start chatting.")
    st.stop()

session_id = session_id.strip()
render_history(session_id)

if prompt := st.chat_input("Ask a life insurance question"):
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            response = get_agent().chat(session_id=session_id, message=prompt)
            st.markdown(response)
        except Exception as exc:
            st.error(f"Unable to generate a response: {exc}")
