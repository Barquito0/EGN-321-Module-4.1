import pytest

from src.iteration import CONVERGED, INVALID_INPUT, NOT_CONVERGED, solve_capacity


def default_case(**overrides):
    data = {
        "batch_checks": 600,
        "cycle_time_seconds": 30,
        "parallel_efficiency": 1.0,
        "target_minutes": 60,
        "starting_stations": 1,
        "tolerance_minutes": 0.5,
        "max_iterations": 10,
        "max_stations": 10,
    }
    data.update(overrides)
    return data


def test_known_case_converges_to_five_stations():
    result = solve_capacity(**default_case())
    assert result["status"] == CONVERGED
    assert result["solution_stations"] == 5
    assert result["final_result_minutes"] == pytest.approx(60.0)


def test_second_starting_condition_also_converges_to_five_stations():
    result = solve_capacity(**default_case(starting_stations=8))
    assert result["status"] == CONVERGED
    assert result["solution_stations"] == 5


def test_tolerance_boundary_is_inclusive():
    result = solve_capacity(
        batch_checks=100,
        cycle_time_seconds=30,
        parallel_efficiency=1.0,
        target_minutes=24.5,
        starting_stations=2,
        tolerance_minutes=0.5,
        max_iterations=5,
        max_stations=10,
    )
    assert result["status"] == CONVERGED
    assert result["final_result_minutes"] == pytest.approx(25.0)
    assert abs(result["final_error_minutes"]) == pytest.approx(0.5)


def test_valid_but_discrete_case_reports_not_converged():
    result = solve_capacity(
        batch_checks=100,
        cycle_time_seconds=30,
        parallel_efficiency=1.0,
        target_minutes=20,
        starting_stations=1,
        tolerance_minutes=0.1,
        max_iterations=6,
        max_stations=10,
    )
    assert result["status"] == NOT_CONVERGED
    assert result["solution_stations"] is None


def test_invalid_input_has_distinct_status_and_zero_iterations():
    result = solve_capacity(**default_case(batch_checks=-600))
    assert result["status"] == INVALID_INPUT
    assert result["iterations"] == 0
    assert result["history"] == []
    assert "batch_checks" in result["message"]


def test_iteration_history_contains_required_trace_fields():
    result = solve_capacity(**default_case())
    assert result["history"]
    first = result["history"][0]
    assert {
        "iteration",
        "stations",
        "estimated_minutes",
        "target_minutes",
        "error_minutes",
        "absolute_error_minutes",
    }.issubset(first)


def test_maximum_iteration_limit_is_enforced_exactly():
    result = solve_capacity(
        batch_checks=100,
        cycle_time_seconds=30,
        parallel_efficiency=1.0,
        target_minutes=20,
        starting_stations=1,
        tolerance_minutes=0.1,
        max_iterations=3,
        max_stations=10,
    )
    assert result["status"] == NOT_CONVERGED
    assert result["iterations"] == 3
    assert len(result["history"]) == 3
