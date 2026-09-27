import pytest

from src.calculation import estimate_batch_time_minutes


def test_one_pass_default_case_is_60_minutes_at_five_stations():
    result = estimate_batch_time_minutes(
        batch_checks=600,
        cycle_time_seconds=30,
        active_stations=5,
        parallel_efficiency=1.0,
    )
    assert result == pytest.approx(60.0)


def test_parallel_efficiency_changes_estimated_time():
    result = estimate_batch_time_minutes(
        batch_checks=600,
        cycle_time_seconds=30,
        active_stations=5,
        parallel_efficiency=0.8,
    )
    assert result == pytest.approx(75.0)
