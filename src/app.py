"""Streamlit entrypoint for Student OS Agent Phase 1."""

from __future__ import annotations

import streamlit as st

from config.settings import SETTINGS


def main() -> None:
    """Render the Phase 1 foundation status page."""

    st.set_page_config(page_title="Student OS Agent", page_icon="🎓", layout="centered")

    st.title("Student OS Agent")
    st.subheader("System Status")

    st.success("Phase 1 complete")
    st.write("Foundation layer is configured. Agent logic is not enabled yet.")

    st.divider()

    st.caption("Default model")
    st.code(SETTINGS.default_model)

    st.caption("Locked memory paths")
    for path in SETTINGS.locked_memory_paths:
        st.code(str(path))

    st.caption("Scholarship scoring weights")
    st.json(SETTINGS.scholarship_scoring_weights)

    st.caption("Agent statuses")
    st.json(sorted(SETTINGS.agent_statuses))


if __name__ == "__main__":
    main()
