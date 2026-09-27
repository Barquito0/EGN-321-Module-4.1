# AI-Generated Alternate Version

This folder contains an independent alternate implementation produced with ChatGPT (GPT-5.6 Sol) for the Assignment 4.1 generated-version challenge.

The code is intentionally kept separate from the trusted implementation in `src/`.

## Defect under test

The generated solver accepts a tolerance input but ignores it. It only reports success when the calculated time is **exactly equal** to the target. This violates the assignment requirement to determine convergence using a tolerance rather than exact numeric equality.

The code was **not corrected before testing**. `tests/test_generated_version.py` demonstrates the defect with executable evidence.
