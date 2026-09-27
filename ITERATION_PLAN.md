# Iteration Plan

- **Starting value / starting condition:** 1 active verification station by default.
- **Quantity being adjusted:** Whole number of active verification stations.
- **Target quantity:** Estimated batch completion time in minutes.
- **Error definition:** `estimated_minutes - target_minutes`.
- **Tolerance:** Absolute error <= 0.5 minute by default.
- **Update rule:** Use inverse proportionality between time and station count to estimate the next station count: `ideal = current_stations * current_time / target_time`, round to the nearest whole station, then move one station in the error-reducing direction if rounding would repeat the same unsuccessful value.
- **Maximum iterations:** 10 by default.
- **Condition for CONVERGED:** `abs(error_minutes) <= tolerance_minutes` before the iteration limit.
- **Condition for NOT CONVERGED:** Inputs are valid, but no evaluated whole-station count reaches tolerance before `max_iterations`.
- **Conditions that are INVALID INPUT:** Non-numeric/non-finite values; batch <= 0; cycle time <= 0; efficiency <= 0 or > 1; target <= 0; tolerance <= 0; non-positive/non-integer iteration or station limits; starting stations > maximum stations.
- **History fields to store:** iteration number, station count, estimated time, target time, signed error, absolute error.

## Why a maximum iteration limit is required

Because the adjusted value is an integer, a target can fall between two possible station-count results. With a very tight tolerance the update can alternate between neighboring station counts indefinitely. The maximum iteration limit guarantees a safe stop and a clear NOT CONVERGED result.
