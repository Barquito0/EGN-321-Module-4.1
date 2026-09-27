from generated_version.ai_generated_solver import generated_capacity_solver
from src.iteration import CONVERGED, solve_capacity


def test_generated_version_defect_exact_equality_ignores_valid_tolerance():
    # Five stations produce 60.0 minutes. A target of 61.0 minutes with a
    # 1.0-minute tolerance should be accepted because |60 - 61| == 1.0.
    trusted = solve_capacity(
        batch_checks=600,
        cycle_time_seconds=30,
        parallel_efficiency=1.0,
        target_minutes=61,
        starting_stations=5,
        tolerance_minutes=1.0,
        max_iterations=6,
        max_stations=10,
    )
    generated = generated_capacity_solver(
        batch_checks=600,
        cycle_time_seconds=30,
        target_minutes=61,
        starting_stations=5,
        tolerance_minutes=1.0,
        max_iterations=6,
    )

    assert trusted["status"] == CONVERGED
    assert trusted["solution_stations"] == 5
    assert generated["status"] == "NOT CONVERGED"
