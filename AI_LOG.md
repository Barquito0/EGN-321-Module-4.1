# AI Use Log

| Date | Tool / model | Purpose | Prompt summary | Used / Modified / Rejected | Verification method | Result |
|---|---|---|---|---|---|---|
| 2026-09-27 | ChatGPT / GPT-5.6 Sol | Select a classroom-safe SyntraTech problem | Build Assignment 4.1 around aggregate verification-capacity sizing rather than private driver data | Modified | Compared against assignment requirements and documented synthetic vs real values | Accepted as project direction |
| 2026-09-27 | ChatGPT / GPT-5.6 Sol | Map deterministic calculation | Propose a one-pass batch-time model using checks, cycle time, station count, and efficiency | Modified | Hand calculation: 600 × 30 / (5 × 1 × 60) = 60 min | Accepted |
| 2026-09-27 | ChatGPT / GPT-5.6 Sol | Design iterative update rule | Suggest a proportional station update and integer rounding | Modified | Pytest convergence, non-convergence, tolerance-boundary, and max-iteration tests | Accepted after tests |
| 2026-09-27 | ChatGPT / GPT-5.6 Sol | Generate alternate AI implementation | Create an independent solver for challenge testing | Used as generated | Automated adversarial test | Defect exposed: exact equality ignores supplied tolerance |
| 2026-09-27 | ChatGPT / GPT-5.6 Sol | Review documentation and edge cases | Identify assumptions, limitations, and invalid inputs | Modified | Cross-checked against validation tests and project files | Accepted |

## Verification rule

AI suggestions are not treated as numerical evidence. The trusted result is based on the documented deterministic formula, explicit assumptions, and automated tests.
