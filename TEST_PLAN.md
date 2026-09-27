# Test Plan

| ID | Test type | Inputs | Expected status/result | Why this matters | Implemented? |
|---|---|---|---|---|---|
| T01 | Known convergence | 600 checks, 30 sec/check, target 60, start 1 | CONVERGED at 5 stations | Confirms default classroom case | Yes |
| T02 | Second convergence | Same case, start 8 | CONVERGED at 5 stations | Shows solver is not dependent on one start | Yes |
| T03 | Tolerance boundary | 100 checks, 30 sec/check, 2 stations, target 24.5, tolerance 0.5 | CONVERGED because error is exactly 0.5 | Confirms inclusive boundary | Yes |
| T04 | Non-convergence | 100 checks, target 20, tolerance 0.1 | NOT CONVERGED | Integer station counts cannot get close enough | Yes |
| T05 | Invalid input | Negative batch size | INVALID INPUT / validation error | Invalid input must be refused before iteration | Yes |
| T06 | Iteration history | Default case | History includes station, result, target, error | Provides traceability | Yes |
| T07 | Maximum iterations | Non-converging case, max 3 | Exactly 3 history rows | Proves loop safety limit | Yes |
| T08 | Generated-version defect | Target 61, tolerance 1, start 5 | Trusted version converges; generated version fails | Exposes exact-equality defect | Yes |
| T09 | One-pass calculation | 600 checks, 30 sec/check, 5 stations | 60 minutes | Verifies deterministic formula | Yes |
| T10 | Efficiency calculation | Same case, efficiency 0.8 | 75 minutes | Verifies efficiency input is used | Yes |
| T11 | Invalid target | target 0 | Refused | Prevents invalid division/engineering target | Yes |
| T12 | Invalid efficiency | efficiency 1.2 | Refused | Enforces documented supported range | Yes |
