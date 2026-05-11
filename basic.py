
# USC ID: Solhjouk
# USC ID Number: 1424729265
"""
CSCI-570 Final Project — Basic Sequence Alignment (Dynamic Programming)
O(mn) time, O(mn) space

Usage: python3 basic.py <input_file> <output_file>
"""

import sys
import time
import psutil


# ──────────────────────────────────────────────
# Hardcoded penalties (Section I-C of spec)
# ──────────────────────────────────────────────
DELTA = 30  # gap penalty

#             A    C    G    T
ALPHA = {
    ('A', 'A'):   0, ('A', 'C'): 110, ('A', 'G'):  48, ('A', 'T'):  94,
    ('C', 'A'): 110, ('C', 'C'):   0, ('C', 'G'): 118, ('C', 'T'):  48,
    ('G', 'A'):  48, ('G', 'C'): 118, ('G', 'G'):   0, ('G', 'T'): 110,
    ('T', 'A'):  94, ('T', 'C'):  48, ('T', 'G'): 110, ('T', 'T'):   0,
}


# ──────────────────────────────────────────────
# Input parsing & string generation (Section I-B)
# ──────────────────────────────────────────────
def generate_string(base, indices):
    """
    Iteratively double the string by inserting a copy of itself
    right after the given 0-indexed position.
    E.g. ACTG with index 3 -> ACTG|ACTG  (insert after position 3)
    """
    s = base
    for idx in indices:
        s = s[:idx + 1] + s + s[idx + 1:]
    return s


def parse_input(filepath):
    """
    Read the input file and return the two generated strings.
    Format: base1, then numeric indices, then base2, then numeric indices.
    """
    with open(filepath, 'r') as f:
        lines = [line.strip() for line in f if line.strip()]

    idx = 0
    # First base string
    base1 = lines[idx]; idx += 1
    indices1 = []
    while idx < len(lines) and lines[idx].isdigit():
        indices1.append(int(lines[idx])); idx += 1

    # Second base string
    base2 = lines[idx]; idx += 1
    indices2 = []
    while idx < len(lines) and lines[idx].isdigit():
        indices2.append(int(lines[idx])); idx += 1

    return generate_string(base1, indices1), generate_string(base2, indices2)


# ──────────────────────────────────────────────
# Memory helper (matches spec sample code, p11)
# ──────────────────────────────────────────────
def process_memory():
    """Current RSS in KB (matches the provided Python sample)."""
    process = psutil.Process()
    return int(process.memory_info().rss / 1024)


# ──────────────────────────────────────────────
# Basic DP alignment  —  O(mn) time, O(mn) space
# ──────────────────────────────────────────────
def basic_alignment(x, y):
    """
    Standard bottom-up DP for sequence alignment.
    Returns (cost, aligned_x, aligned_y, memory_in_kb).

    IMPORTANT: memory is measured *inside* this function while the
    DP table is still allocated, per the spec's Important Note (p12).
    """
    m = len(x)
    n = len(y)

    # ---- Step 1: Build the full (m+1) x (n+1) DP table ----
    dp = [[0] * (n + 1) for _ in range(m + 1)]

    # Base cases: aligning a prefix with the empty string
    for i in range(m + 1):
        dp[i][0] = i * DELTA
    for j in range(n + 1):
        dp[0][j] = j * DELTA

    # Fill table bottom-up
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            match_cost = dp[i - 1][j - 1] + ALPHA[(x[i - 1], y[j - 1])]
            gap_in_y   = dp[i - 1][j]     + DELTA   # x[i] aligned with gap
            gap_in_x   = dp[i][j - 1]     + DELTA   # y[j] aligned with gap
            dp[i][j] = min(match_cost, gap_in_y, gap_in_x)

    # ---- Measure memory NOW while dp table is still alive ----
    memory_used = process_memory()

    # ---- Step 2: Traceback to recover the alignment ----
    ax = []   # aligned version of x
    ay = []   # aligned version of y
    i, j = m, n

    while i > 0 and j > 0:
        if dp[i][j] == dp[i - 1][j - 1] + ALPHA[(x[i - 1], y[j - 1])]:
            ax.append(x[i - 1])
            ay.append(y[j - 1])
            i -= 1; j -= 1
        elif dp[i][j] == dp[i - 1][j] + DELTA:
            ax.append(x[i - 1])
            ay.append('_')
            i -= 1
        else:
            ax.append('_')
            ay.append(y[j - 1])
            j -= 1

    # Remaining characters pair with gaps
    while i > 0:
        ax.append(x[i - 1])
        ay.append('_')
        i -= 1
    while j > 0:
        ax.append('_')
        ay.append(y[j - 1])
        j -= 1

    ax.reverse()
    ay.reverse()

    return dp[m][n], ''.join(ax), ''.join(ay), memory_used


# ──────────────────────────────────────────────
# Main
# ──────────────────────────────────────────────
def main():
    input_file  = sys.argv[1]
    output_file = sys.argv[2]

    # Parse and generate strings
    s1, s2 = parse_input(input_file)

    # Run alignment with timing
    start_time = time.time()
    cost, align1, align2, memory_used = basic_alignment(s1, s2)
    end_time = time.time()

    time_taken = (end_time - start_time) * 1000   # convert to ms

    # Write output — 5 lines exactly (spec Section II-B)
    with open(output_file, 'w') as f:
        f.write(f"{cost}\n")
        f.write(f"{align1}\n")
        f.write(f"{align2}\n")
        f.write(f"{time_taken}\n")
        f.write(f"{memory_used}\n")


if __name__ == '__main__':
    main()




# USC ID: Solhjouk
# USC ID Number: 1424729265