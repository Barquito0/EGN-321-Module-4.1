# Calculation Map

## Problem purpose

Estimate how many whole concurrent SyntraTech verification stations are required for an aggregate batch of checks to finish near a target completion time. This is a classroom-safe capacity-planning model and does not use driver personal information.

## Inputs and units

| Input | Unit | Valid range / rule | Source |
|---|---|---|---|
| Batch size | checks | > 0 | SyntraTech planning benchmark: about 600 checks per typical batch |
| Planning cycle time | sec/check | > 0 | Default 30 sec/check is derived from ~600 manual checks in ~5 hours; not measured automated timing |
| Parallel efficiency | fraction | > 0 and <= 1 | Classroom modeling assumption |
| Target batch time | minutes | > 0 | 60-minute classroom target |
| Starting stations | stations | integer >= 1 | Iteration starting condition |
| Tolerance | minutes | > 0 | 0.5-minute classroom tolerance |
| Maximum iterations | iterations | integer >= 1 | Safety limit against endless iteration |
| Maximum stations | stations | integer >= starting stations | Classroom bound; default 10 |

## Output / target

- Engineering output for one proposed station count: estimated batch completion time in minutes.
- Target: 60.0 minutes by default.
- Final sizing output: a whole number of stations whose estimated time is within the specified tolerance.

## Value adjusted during iteration

`active_stations` — the proposed whole number of concurrent verification stations.

## One-pass calculation steps

| Step | Operation | Output | Unit |
|---|---|---|---|
| 1 | `active_stations * parallel_efficiency` | Effective parallel capacity | effective stations |
| 2 | `batch_checks * cycle_time_seconds` | Total serial work | seconds |
| 3 | `total_serial_work / effective_parallel_capacity` | Estimated elapsed work time | seconds |
| 4 | `elapsed_seconds / 60` | Estimated batch time | minutes |
| 5 | `estimated_minutes - target_minutes` | Signed error | minutes |

## Assumptions

- Default batch size of 600 checks comes from existing SyntraTech aggregate planning.
- The 30 sec/check default is a planning benchmark derived from a ~5-hour manual process for ~600 checks; it is not measured automated application performance.
- The first model assumes equal parallel contribution from each station, modified by one efficiency factor.
- Stations are indivisible whole numbers.
- Default 60-minute target, 0.5-minute tolerance, and 10-station bound are classroom assumptions.
- No private driver, customer, credential, or payment data is used.

## Questions that still need verification

- What is the measured automated seconds/check by supported state under normal conditions?
- How does real throughput change with multiple simultaneous stations?
- At what concurrency do state-site throttling, CAPTCHA, network, CPU, or memory become limiting?
- Should retry/failure rates be modeled separately from average cycle time?
