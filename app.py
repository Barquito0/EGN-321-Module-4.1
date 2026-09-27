import streamlit as st

from src.iteration import CONVERGED, INVALID_INPUT, solve_capacity

st.set_page_config(page_title="SyntraTech Capacity Sizing", layout="wide")
st.title("SyntraTech Verification Capacity Sizing Tool")
st.caption("EGN 321 Module 4 Assignment 4.1 — classroom-safe aggregate planning model")

st.info(
    "The default 600-check batch is a SyntraTech aggregate planning value. "
    "The default 30 sec/check is derived from the historical manual benchmark "
    "of about 600 checks in about 5 hours; it is NOT measured automated-app timing. "
    "The 60-minute target and 0.5-minute tolerance are classroom assumptions."
)

left, right = st.columns(2)
with left:
    st.subheader("Engineering inputs")
    batch_checks = st.number_input("Batch size (checks)", min_value=1, value=600, step=1)
    cycle_time_seconds = st.number_input(
        "Planning cycle time (seconds/check)", min_value=0.01, value=30.0, step=0.5
    )
    parallel_efficiency = st.number_input(
        "Parallel efficiency (0–1)", min_value=0.01, max_value=1.0, value=1.0, step=0.05
    )
    target_minutes = st.number_input(
        "Target batch completion time (minutes)", min_value=0.01, value=60.0, step=1.0
    )

with right:
    st.subheader("Iteration controls")
    starting_stations = st.number_input("Starting stations", min_value=1, value=1, step=1)
    tolerance_minutes = st.number_input(
        "Convergence tolerance (minutes)", min_value=0.000001, value=0.5, format="%.6f"
    )
    max_iterations = st.number_input("Maximum iterations", min_value=1, value=10, step=1)
    max_stations = st.number_input("Maximum supported stations", min_value=1, value=10, step=1)

if st.button("Run capacity sizing", type="primary"):
    result = solve_capacity(
        batch_checks=batch_checks,
        cycle_time_seconds=cycle_time_seconds,
        parallel_efficiency=parallel_efficiency,
        target_minutes=target_minutes,
        starting_stations=starting_stations,
        tolerance_minutes=tolerance_minutes,
        max_iterations=max_iterations,
        max_stations=max_stations,
    )

    st.subheader("Calculation status")
    if result["status"] == CONVERGED:
        st.success("CONVERGED")
    elif result["status"] == INVALID_INPUT:
        st.error("INVALID INPUT")
    else:
        st.warning("NOT CONVERGED")

    st.write(result["message"])

    if result["status"] == CONVERGED:
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Recommended stations", result["solution_stations"])
        c2.metric("Estimated time", f'{result["final_result_minutes"]:.3f} min')
        c3.metric("Final error", f'{result["final_error_minutes"]:.3f} min')
        c4.metric("Iterations", result["iterations"])
    elif result["status"] != INVALID_INPUT:
        c1, c2, c3 = st.columns(3)
        c1.metric("Last estimated time", f'{result["final_result_minutes"]:.3f} min')
        c2.metric("Last error", f'{result["final_error_minutes"]:.3f} min')
        c3.metric("Iterations performed", result["iterations"])

    if result["history"]:
        st.subheader("Iteration history")
        st.dataframe(result["history"], use_container_width=True, hide_index=True)

with st.expander("Assumptions and limitations"):
    st.markdown(
        """
- This is a classroom-safe planning model, not a production capacity guarantee.
- The default 30 sec/check is derived from a manual process benchmark, not measured SyntraTech automation timing.
- The model assumes each active station contributes equal parallel capacity adjusted by one efficiency factor.
- Station counts are whole numbers; some targets cannot be reached within a very tight tolerance.
- The model does not include CAPTCHA delays, state-site throttling, network latency, failures, retries, or server CPU/memory limits.
- No driver names, license numbers, dates of birth, credentials, keys, or customer identities are used.
        """
    )
