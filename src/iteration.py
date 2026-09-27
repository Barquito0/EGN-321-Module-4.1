"""Iterative solver for SyntraTech verification-capacity sizing."""

from __future__ import annotations

import math

from .calculation import estimate_batch_time_minutes
from .validation import validate_inputs

CONVERGED = "CONVERGED"
NOT_CONVERGED = "NOT CONVERGED"
INVALID_INPUT = "INVALID INPUT"


def _round_half_up_positive(value: float) -> int:
    """Round a non-negative value to the nearest integer, .5 upward."""
    return int(math.floor(value + 0.5))


def solve_capacity(
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
    """Iteratively size concurrent verification stations.

    The update rule uses the proportional relationship between time and station
    count. Because stations must be whole numbers, a too-tight tolerance can
    cause the method to alternate between neighboring station counts. The
    maximum-iteration limit guarantees a safe stop in that case.
    """
    try:
        inputs = validate_inputs(
            batch_checks=batch_checks,
            cycle_time_seconds=cycle_time_seconds,
            parallel_efficiency=parallel_efficiency,
            target_minutes=target_minutes,
            starting_stations=starting_stations,
            tolerance_minutes=tolerance_minutes,
            max_iterations=max_iterations,
            max_stations=max_stations,
        )
    except ValueError as exc:
        return {
            "status": INVALID_INPUT,
            "message": str(exc),
            "solution_stations": None,
            "final_result_minutes": None,
            "final_error_minutes": None,
            "iterations": 0,
            "history": [],
        }

    station_count = inputs["starting_stations"]
    history: list[dict] = []

    for iteration in range(1, inputs["max_iterations"] + 1):
        result_minutes = estimate_batch_time_minutes(
            batch_checks=inputs["batch_checks"],
            cycle_time_seconds=inputs["cycle_time_seconds"],
            active_stations=station_count,
            parallel_efficiency=inputs["parallel_efficiency"],
        )
        error_minutes = result_minutes - inputs["target_minutes"]
        absolute_error = abs(error_minutes)

        history.append(
            {
                "iteration": iteration,
                "stations": station_count,
                "estimated_minutes": result_minutes,
                "target_minutes": inputs["target_minutes"],
                "error_minutes": error_minutes,
                "absolute_error_minutes": absolute_error,
            }
        )

        if absolute_error <= inputs["tolerance_minutes"]:
            return {
                "status": CONVERGED,
                "message": "A station count reached the target within tolerance.",
                "solution_stations": station_count,
                "final_result_minutes": result_minutes,
                "final_error_minutes": error_minutes,
                "iterations": iteration,
                "history": history,
            }

        ideal_stations = station_count * result_minutes / inputs["target_minutes"]
        proposed = _round_half_up_positive(ideal_stations)
        proposed = max(1, min(inputs["max_stations"], proposed))

        if proposed == station_count:
            if error_minutes > 0 and station_count < inputs["max_stations"]:
                proposed = station_count + 1
            elif error_minutes < 0 and station_count > 1:
                proposed = station_count - 1

        station_count = proposed

    last = history[-1]
    return {
        "status": NOT_CONVERGED,
        "message": (
            "Valid inputs were supplied, but no evaluated whole-station count "
            "reached the target within tolerance before the maximum iteration limit."
        ),
        "solution_stations": None,
        "final_result_minutes": last["estimated_minutes"],
        "final_error_minutes": last["error_minutes"],
        "iterations": inputs["max_iterations"],
        "history": history,
    }
