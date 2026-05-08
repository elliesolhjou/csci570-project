# CSCI-570 Final Project — Basic Sequence Alignment

## Approach

The basic solution implements the **bottom-up dynamic programming** approach for global sequence alignment, as covered in Professor Shamsian's lecture slides (Lecture 8, Sequence Alignment).

### Algorithm Overview

Given two strings X = x₁x₂...xₘ and Y = y₁y₂...yₙ, we define a subproblem OPT(i, j) as the minimum alignment cost of the prefixes X[1..i] and Y[1..j]. The recurrence is:

```
OPT(i, j) = min {
    OPT(i-1, j-1) + α(xᵢ, yⱼ)    — match/mismatch
    OPT(i-1, j)   + δ              — gap in Y (xᵢ unmatched)
    OPT(i, j-1)   + δ              — gap in X (yⱼ unmatched)
}
```

**Base cases:**
- OPT(i, 0) = i · δ for all i (every character in X paired with a gap)
- OPT(0, j) = j · δ for all j (every character in Y paired with a gap)

**Final answer:** OPT(m, n)

### Implementation Steps

1. **Parse input** — read the base strings and insertion indices from the input file, then iteratively generate the full strings using the doubling-insertion method described in the spec.

2. **Build the DP table** — allocate a full (m+1) × (n+1) table and fill it bottom-up using the recurrence above.

3. **Measure memory** — captured inside the alignment function while the DP table is still allocated, per the spec's Important Note (page 12). Uses `psutil` RSS measurement matching the provided Python sample code.

4. **Traceback** — walk backwards from OPT(m, n) to (0, 0), checking which of the three choices produced each cell's value. Append the corresponding character or gap `_` at each step, then reverse.

5. **Write output** — exactly 5 lines: cost (integer), aligned string 1, aligned string 2, time in ms (float), memory in KB (float). Nothing is printed to stdout.

### Complexity

| | Time | Space |
|---|---|---|
| **Basic DP** | O(mn) | O(mn) |

### Hardcoded Parameters

- **Gap penalty (δ):** 30
- **Mismatch costs (α):**

|   | A   | C   | G   | T   |
|---|-----|-----|-----|-----|
| A | 0   | 110 | 48  | 94  |
| C | 110 | 0   | 118 | 48  |
| G | 48  | 118 | 0   | 110 |
| T | 94  | 48  | 110 | 0   |

---

## Verification

### Correctness

- **String generation** matches the spec's ACTG/TACG example exactly, producing `ACACTGACTACTGACTGGTGACTACTGACTGG` and `TATTATACGCTATTATACGCGACGCGGACGCG`.
- **Alignment cost of 660** verified by independently recomputing from the aligned output (summing gap and mismatch penalties character by character).
- **Aligned strings reconstruct** back to the originals when gaps are removed.

### Edge Cases (all pass)

| Test | Expected | Result |
|---|---|---|
| Identical strings (ACGT vs ACGT) | Cost 0, no gaps | Pass |
| Empty string (ACG vs "") | Cost 90 (3 gaps) | Pass |
| A vs C | Cost 60 (two gaps < mismatch 110) | Pass |
| A vs G | Cost 48 (mismatch < two gaps 60) | Pass |
| No-insertion input parsing | Strings unchanged | Pass |

### Performance

| Problem Size | Time | Memory |
|---|---|---|
| 32 × 32 (spec example) | ~0.6 ms | ~13 MB |
| 1000 × 1000 | ~544 ms | ~52 MB |
| 2000 × 2000 (upper bound) | ~2.8 s | ~170 MB |

The 2000×2000 upper bound finishes well under the grading kill threshold of a few minutes.

### Spec Compliance

- Zero stdout output — only writes to the output file.
- Exactly 5 lines in the output file in the correct order.
- Memory measured inside the solution function while the DP table is still allocated.
- Single-file program as required.
- Uses only standard libraries plus `psutil` (provided in the spec's sample code).

---

## Usage

```bash
python3 basic.py input.txt output.txt
```

Or via the shell script:

```bash
./basic.sh input.txt output.txt
```
