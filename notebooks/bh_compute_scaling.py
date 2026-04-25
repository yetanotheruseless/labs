"""Tiny numerical sanity check for notebooks/bh_compute_scaling.md.

Compares "matched-quality tokens per second at infinity" between:
  - BH inference at horizon: tokens/sec ~ 1/M
  - flat-space + test-time compute: tokens/sec ~ exp(-(c/beta) * M^-gamma)

All in Planck units. M is in Planck masses.

R(M) = (flat tokens/sec) / (BH tokens/sec) = M * exp(-(c/beta) * M^-gamma)
R > 1  -> flat-space wins.
"""

import math

GAMMA = 0.31           # Chinchilla loss-vs-N exponent (Hoffmann 2022, Approach 3)
C_OVER_BETA = 1.0      # O(1) prefactor lumping in the constants A, beta
                       # (loss prefactor / TTC log slope)


def R(M, gamma=GAMMA, c_over_beta=C_OVER_BETA):
    """tokens/sec ratio (flat / BH); >1 means flat wins."""
    return M * math.exp(-c_over_beta * M ** (-gamma))


def find_crossover(gamma=GAMMA, c_over_beta=C_OVER_BETA):
    """Bisect for M* with R(M*) = 1."""
    lo, hi = 1e-3, 1e6
    for _ in range(200):
        mid = math.sqrt(lo * hi)
        if R(mid, gamma, c_over_beta) < 1:
            lo = mid
        else:
            hi = mid
    return math.sqrt(lo * hi)


def main():
    print(f"gamma = {GAMMA}, c/beta = {C_OVER_BETA}")
    print()
    print("M (Planck masses) |   R(M) = (flat tok/s) / (BH tok/s)")
    print("-" * 56)
    for log10M in range(-3, 13):
        M = 10.0 ** log10M
        try:
            r = R(M)
            print(f"  10^{log10M:+3d}              |  {r:.4e}")
        except OverflowError:
            print(f"  10^{log10M:+3d}              |  overflow (flat dominates)")
    print()

    M_star = find_crossover()
    print(f"crossover M*  ≈  {M_star:.4g} Planck masses")
    print(f"            ≈  {M_star * 2.176e-8:.4g} kg")

    # show sensitivity to c/beta and gamma
    print()
    print("Sensitivity of crossover M* to constants:")
    print(f"{'c/beta':>8} {'gamma':>6}   {'M* (Planck)':>14}")
    for cb in (0.1, 1.0, 10.0, 100.0):
        for g in (0.15, 0.31, 0.5):
            print(f"{cb:>8.2f} {g:>6.2f}   {find_crossover(g, cb):>14.4g}")


if __name__ == "__main__":
    main()
