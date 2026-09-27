# First-Time User Review

| Observation | Evidence | Likely cause | Proposed fix | Priority |
|---|---|---|---|---|
| Default cycle time could be mistaken for measured automation timing | 30 sec/check appears as a default input | Historical manual benchmark is being reused for classroom modeling | Keep the prominent warning in the UI and replace the default after measured automated timing is available | High |
| Users may expect every valid case to converge | Integer station counts can alternate when tolerance is too tight | Discrete sizing cannot represent every possible target time | Explain NOT CONVERGED and show iteration history | High |
| Maximum stations could be mistaken for a production server limit | Default is 10 | Bound is classroom/scope control only | Label it as a supported planning bound, not measured infrastructure capacity | Medium |

## Questions for the operator
- Could you identify the required inputs without help?
- Were the units clear?
- Did you understand the status message?
- Could you find the iteration history?
- Did any error message leave you unsure what to fix?
- Did you understand that 30 sec/check is a planning benchmark, not measured app performance?
