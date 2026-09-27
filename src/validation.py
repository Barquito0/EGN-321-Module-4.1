"""Input validation for the SyntraTech verification-capacity solver."""

from __future__ import annotations

import math
from numbers import Real


def _finite_number(name: str, value: object) -> float:
    if isinstance(value, bool) or not isinstance(value, Real):
        raise ValueError(f"{name} must be a numeric value")
    value = float(value)
    if not math.isfinite(value):
        raise ValueError(f"{name} must be finite")
    return value


def _positive_integer(name: str, value: object) -> int:
    numeric = _finite_number(name, value)
    if not numeric.is_integer() or numeric < 1:
        raise ValueError(f"{name} must be an integer greater than or equal to 1")
    return int(numeric)


def validate_inputs(
    *,
    batch_checks: float,
    cycle_time_seconds: float,
    parallel_efficiency: float,
    target_minutes: float,
    starting_stations: int,
    tolerance_minutes: float,
    max_iterations: int,
    max_stations: int,
) -> dict:
    """Validate all supported engineering and iteration inputs.

    Returns normalized numeric values. Raises ``ValueError`` before any
    iteration begins when a rule is violated.
    """
    batch_checks = _finite_number("batch_checks", batch_checks)
    cycle_time_seconds = _finite_number("cycle_time_seconds", cycle_time_seconds)
    parallel_efficiency = _finite_number("parallel_efficiency", parallel_efficiency)
    target_minutes = _finite_number("target_minutes", target_minutes)
    tolerance_minutes = _finite_number("tolerance_minutes", tolerance_minutes)
    starting_stations = _positive_integer("starting_stations", starting_stations)
    max_iterations = _positive_integer("max_iterations", max_iterations)
    max_stations = _positive_integer("max_stations", max_stations)

    if batch_checks <= 0:
        raise ValueError("batch_checks must be greater than 0")
    if cycle_time_seconds <= 0:
        raise ValueError("cycle_time_seconds must be greater than 0")
    if not (0 < parallel_efficiency <= 1):
        raise ValueError("parallel_efficiency must be greater than 0 and less than or equal to 1")
    if target_minutes <= 0:
        raise ValueError("target_minutes must be greater than 0")
    if tolerance_minutes <= 0:
        raise ValueError("tolerance_minutes must be greater than 0")
    if starting_stations > max_stations:
        raise ValueError("starting_stations cannot be greater than max_stations")

    return {
        "batch_checks": batch_checks,
        "cycle_time_seconds": cycle_time_seconds,
        "parallel_efficiency": parallel_efficiency,
        "target_minutes": target_minutes,
        "starting_stations": starting_stations,
        "tolerance_minutes": tolerance_minutes,
        "max_iterations": max_iterations,
        "max_stations": max_stations,
    }
