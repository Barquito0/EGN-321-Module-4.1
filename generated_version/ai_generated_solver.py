"""Independent AI-generated alternate implementation for challenge testing.

IMPORTANT: This version is intentionally preserved as generated for evaluation.
It is not the trusted engineering implementation.

Known behavior to investigate: it uses exact equality instead of the supplied
convergence tolerance.
"""


def generated_capacity_solver(
    batch_checks,
    cycle_time_seconds,
    target_minutes,
    starting_stations=1,
    tolerance_minutes=0.5,
    max_iterations=10,
):
    stations = starting_stations
    history = []

    for iteration in range(1, max_iterations + 1):
        result = batch_checks * cycle_time_seconds / (stations * 60)
        history.append({"iteration": iteration, "stations": stations, "result": result})

        # Defect: tolerance_minutes is accepted but ignored.
        if result == target_minutes:
            return {"status": "CONVERGED", "stations": stations, "history": history}

        if result > target_minutes:
            stations += 1
        else:
            stations = max(1, stations - 1)

    return {"status": "NOT CONVERGED", "stations": None, "history": history}
