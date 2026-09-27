"""Deterministic engineering calculation for verification-capacity planning.

The one-pass model estimates the time required to process a batch of checks
using a proposed integer number of concurrent verification stations.
"""


def estimate_batch_time_minutes(
    *,
    batch_checks: float,
    cycle_time_seconds: float,
    active_stations: int,
    parallel_efficiency: float = 1.0,
) -> float:
    """Estimate batch completion time in minutes for one proposed station count.

    Formula:
        time_min = batch_checks * cycle_time_seconds /
                   (active_stations * parallel_efficiency * 60)

    Validation is intentionally kept in ``validation.py``. This function still
    refuses values that would cause division by zero so it is safe when called
    independently.
    """
    if active_stations <= 0:
        raise ValueError("active_stations must be greater than 0")
    if parallel_efficiency <= 0:
        raise ValueError("parallel_efficiency must be greater than 0")

    return (
        float(batch_checks)
        * float(cycle_time_seconds)
        / (int(active_stations) * float(parallel_efficiency) * 60.0)
    )
