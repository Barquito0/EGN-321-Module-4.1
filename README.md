# SyntraTech Verification Capacity Sizing Tool

## Project Overview

This EGN 321 Module 4 Assignment 4.1 project replaces a manual goal-seek style capacity-planning process with a tested Python iterative solver and Streamlit interface.

The tool estimates how many whole concurrent verification stations would be required for an aggregate SyntraTech batch to finish near a target time. No driver names, license numbers, dates of birth, credentials, keys, payment data, or customer identities are used.

> **Coursework note:** The Module 4 support package did not include a separate assigned engineering workbook. This project therefore uses a student-created, synthetic classroom workbook based on a real SyntraTech planning problem. Instructor approval should be obtained if an assigned workbook is later provided or required.

## Original Workbook / Process

`SyntraTech_Verifier_Capacity_GoalSeek_SYNTHETIC.xlsx` documents the manual process used for this project. A user proposes a station count, calculates estimated batch time, compares it with the target, and tries another station count until the result is close enough.

The workbook clearly distinguishes existing SyntraTech aggregate planning values from classroom assumptions.

## Inputs and Units

| Input | Unit | Default |
|---|---|---:|
| Batch size | checks | 600 |
| Planning cycle time | seconds/check | 30.0 |
| Parallel efficiency | fraction | 1.0 |
| Target completion time | minutes | 60.0 |
| Starting stations | stations | 1 |
| Tolerance | minutes | 0.5 |
| Maximum iterations | iterations | 10 |
| Maximum supported stations | stations | 10 |

The 600-check batch is an existing SyntraTech aggregate planning benchmark. The 30 sec/check default is derived from the historical manual benchmark of roughly 600 checks in roughly 5 hours. It is **not measured automated SyntraTech timing**. The 60-minute target and 0.5-minute tolerance are classroom assumptions.

## Iterative Calculation

The proposed value is the number of concurrent verification stations.

For one proposed station count:

```text
estimated_minutes = (batch_checks × cycle_time_seconds)
                    / (active_stations × parallel_efficiency × 60)
```

The solver then compares the estimated time with the target.

## Starting Condition

The default starting condition is 1 station. The user may choose another supported starting count.

## Convergence Rule

```text
absolute_error = abs(estimated_minutes - target_minutes)
```

The result is **CONVERGED** when:

```text
absolute_error <= tolerance_minutes
```

Exact numeric equality is not required.

## Tolerance

The default tolerance is **0.5 minute**. This means an estimated batch time up to 0.5 minute above or below the target is accepted.

## Maximum Iterations

The default limit is **10 iterations**. A maximum is required because station count is an integer. With an unrealistically tight tolerance, two neighboring station counts can fall on opposite sides of the target and the solver can alternate between them.

## Validation Rules

The application rejects inputs before iteration when:

- batch size is zero or negative;
- cycle time is zero or negative;
- parallel efficiency is <= 0 or > 1;
- target time is zero or negative;
- tolerance is zero or negative;
- starting stations, maximum stations, or maximum iterations are not positive integers;
- starting stations exceed maximum stations;
- required numeric values are missing, non-numeric, infinite, or NaN.

## Non-Convergence Behavior

If the inputs are valid but the solver reaches the iteration limit without meeting tolerance, the status is **NOT CONVERGED**. No successful station recommendation is presented. The last calculated result, last error, iteration count, and full history remain available for review.

## Iteration History

Each iteration records:

- iteration number;
- proposed station count;
- estimated batch time;
- target time;
- signed error;
- absolute error.

This allows a reviewer to answer: **How did the program reach this result?**

## Testing

Run:

```bash
pytest
```

The project contains more than the required eight meaningful tests, including:

- known convergence;
- convergence from a different start;
- tolerance boundary;
- non-convergence;
- invalid inputs;
- history production;
- maximum-iteration enforcement;
- deterministic formula checks;
- efficiency behavior;
- AI-generated-version defect evidence.

## AI-Generated Version

`generated_version/ai_generated_solver.py` is a separate alternate implementation produced using ChatGPT (GPT-5.6 Sol). It is not imported by the trusted solver.

## Generated-Version Defect

The alternate implementation accepts `tolerance_minutes` but ignores it. It uses exact equality:

```python
if result == target_minutes:
```

The automated challenge test uses a target of 61 minutes and a tolerance of 1 minute. Five stations produce 60 minutes, which is exactly at the accepted tolerance boundary. The trusted solver reports CONVERGED, while the generated version reports NOT CONVERGED. This exposes a meaningful violation of the convergence requirement.

## Ollama / AI Use

The assignment allows approved AI tools. This project used ChatGPT for planning, review, and the alternate generated implementation. Every accepted calculation behavior is verified with deterministic tests. `AI_LOG.md` records the assistance and verification.

## Assumptions

- 600 checks is a classroom-safe aggregate SyntraTech planning value.
- 30 sec/check is derived from a historical manual benchmark, not measured app performance.
- All active stations are assumed to contribute equally except for the parallel-efficiency factor.
- Station count is a whole positive integer.
- The default target, tolerance, max station count, and efficiency are planning/classroom assumptions.

## Known Limitations

- The model is not a production capacity guarantee.
- It does not model state-site CAPTCHA, throttling, retry rates, network latency, server CPU/memory, Selenium/browser overhead, or outages.
- It uses one average cycle time across all checks and states.
- It does not determine whether the current SyntraTech server can safely run a specific number of simultaneous workers.
- Very tight tolerances may be impossible with whole station counts, which correctly produces NOT CONVERGED.

## How to Run Locally

```bash
python -m venv .venv
```

Activate the environment, then:

```bash
pip install -r requirements.txt
pytest
streamlit run app.py
```

## Live Streamlit Application

**Deployment URL:** https://egn-321-module-41-nwgqqcatuz2gxm4zukphya.streamlit.app/
