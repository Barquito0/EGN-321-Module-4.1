import pytest

from src.validation import validate_inputs


def valid_inputs(**overrides):
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


def test_negative_batch_is_refused_before_iteration():
    with pytest.raises(ValueError, match="batch_checks"):
        validate_inputs(**valid_inputs(batch_checks=-1))


def test_zero_target_is_refused():
    with pytest.raises(ValueError, match="target_minutes"):
        validate_inputs(**valid_inputs(target_minutes=0))


def test_efficiency_above_one_is_refused():
    with pytest.raises(ValueError, match="parallel_efficiency"):
        validate_inputs(**valid_inputs(parallel_efficiency=1.2))


def test_starting_stations_cannot_exceed_maximum():
    with pytest.raises(ValueError, match="starting_stations"):
        validate_inputs(**valid_inputs(starting_stations=11, max_stations=10))
