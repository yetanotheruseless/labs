# Chinchilla LLMs vs. the Bekenstein bound

A back-of-the-envelope comparison of two extremal "compute substrates":

* **(A) Black-hole compute.** Run the LLM in the near-horizon region of a
  Schwarzschild BH of mass `M`. Information density approaches the
  Bekenstein bound (`I ≤ A/4ℓ_P²`), but proper time runs slow relative
  to a flat-space observer (gravitational redshift).
* **(B) Flat-space compute.** Run the LLM far from the hole, where you
  cannot saturate the holographic bound, and compensate for the smaller
  native model by burning *test-time compute*.

We assume:

1. **Chinchilla scaling holds forever.** At Chinchilla-optimal training
   (`D ∝ N`, total training FLOPs `C_train ∝ N²`), the loss above the
   irreducible floor obeys `L − L∞ ∝ N^(−γ)` for some small γ.
   Empirically γ ≈ 0.31 (Hoffmann et al. 2022; loss-vs-compute exponent
   ≈ 0.154 ⇒ loss-vs-N exponent ≈ 0.308).
2. **Test-time compute buys log loss.** Spending a multiplicative factor
   `k` of inference compute on a query reduces the effective loss by
   `β·log k` for some β > 0 (the empirical "o1 line").

All quantities below are in **Planck units** (`ℏ = c = G = k_B = 1`).
The black-hole mass `M` is therefore measured in Planck masses
(`m_P ≈ 2·10⁻⁸ kg ≈ 10¹⁹ GeV/c²`).

---

## 1. Black-hole compute (function of M)

Static Schwarzschild metric:

```
r_s   = 2M
A     = 4π r_s²            = 16π M²
S_BH  = A/4                = 4π M²              (nats)
T_H   = 1/(8πM)
P_H   ∼ T_H⁴ · A           ∼ 1/M²              (Hawking power)
t_evap∼ M / P_H            ∼ M³                (evaporation time)
```

A static observer at `r = r_s(1+ε)`, ε ≪ 1, sees proper time

```
dτ/dt = √(1 − r_s/r) = √(ε/(1+ε)) ≈ √ε.
```

So things "near the horizon" look slow by `√ε` from infinity.

### Model size N_A

Take the LLM's parameter count to saturate the holographic bound for
the BH's horizon area:

```
N_A(M)  ∼  S_BH  ∼  M²        (bits, hence ≈ params at O(1) bits/param)
```

### Effective inference rate seen from infinity

There are several robust ways to estimate the rate at which the BH
"thinks" as observed from infinity, and they all give the same scaling:

| route                                                               | rate (ops / Planck-time) |
| ------------------------------------------------------------------- | ------------------------ |
| Lloyd / Margolus–Levitin: `≤ 2E_∞ / πℏ` with `E_∞ = M`              | `~ M`                    |
| Scrambling time `t_scr ∼ M log M`, `N` d.o.f. updated per scramble  | `~ M / log M`            |
| Hawking quanta emitted per Schwarzschild time `r_s = 2M`            | `~ 1/M` *quanta*/time    |

Taking the Lloyd bound as the "true" ops budget at infinity, total
inference ops / second ≈ `M`. A single forward pass costs `~ N_A = M²`
ops, so

```
tokens_per_second_A(M)  =  M / M²  =  1/M.
```

(The scrambling-time and Hawking-rate estimates give the same `1/M`
scaling up to log factors.)

### Loss achieved by the BH-trained model

Chinchilla:

```
L_A(M) − L∞  ∝  N_A^(−γ)  =  M^(−2γ).
```

---

## 2. Flat-space compute (function of M)

Give the flat-space substrate the *same* energy budget `E = M` so the
comparison is apples-to-apples (you "spend" mass `M` worth of stuff
either as a BH or as ordinary computronium).

Ordinary computronium can store at most ~ `E^(d/(d+1))` bits at fixed
size; for the purposes of this sketch take a much weaker (more
generous-to-flat-space) assumption:

```
N_B(M)  ∼  M.
```

(Linear in mass-energy: e.g. ~one qubit per quantum of rest energy.
Note: this is already enormously more generous than realistic silicon,
which gives `~M^0` since most of the mass is dead nuclei.)

Lloyd bound on ops at infinity (no time dilation):

```
ops_per_second_B  ∼  M.
```

Single forward pass costs `~ N_B = M` ops, so the *native* tokens per
second is

```
tokens_per_second_B,native(M)  =  M / M  =  1   (constant in M).
```

### Native loss

```
L_B(M) − L∞  ∝  N_B^(−γ)  =  M^(−γ).
```

So the flat-space model has a **larger** loss gap than the BH model:

```
ΔL(M) ≡ L_B(M) − L_A(M)  =  c · ( M^(−γ) − M^(−2γ) ).
```

For large M both shrink to zero; the BH advantage is the *difference*,
which scales like `M^(−γ)` for `M ≫ 1`.

---

## 3. Closing the loss gap with test-time compute

By assumption, multiplying test-time compute by `k` reduces effective
loss by `β log k`. To match `L_A`:

```
β · log k  =  ΔL(M)  =  c · M^(−γ)             (large-M limit)
⇒  k(M)  =  exp( (c/β) · M^(−γ) ).
```

So the multiplicative test-time-compute tax on flat-space is

```
k(M)  ≈  1 + (c/β) M^(−γ)   for large M
k(M)  ≈  exp( (c/β) M^(−γ) )    in general
```

This vanishes (→ 1) as `M → ∞` — at huge BH masses both models are
essentially perfect, the gap closes, and the flat-space tax is gone.
It blows up only when `M` is so small that the loss gap is order unity.

### Effective tokens per second of the flat-space substrate

```
tokens_per_second_B,eff(M)  =  1 / k(M)  =  exp( −(c/β) M^(−γ) ).
```

---

## 4. The horse race

Putting it together, the ratio of "matched-quality tokens / sec at
infinity" is

```
       tokens/sec (flat)      exp( −(c/β) M^(−γ) )
R(M) = ─────────────────  =  ──────────────────────  =  M · exp(−(c/β) M^(−γ)).
       tokens/sec (BH)             1 / M
```

### Asymptotic behaviour

* `M → ∞`: `R(M) → M · 1 = M → ∞`. **Flat-space wins by a factor of M.**
  This is the dominant regime: the time-dilation tax on the BH
  (`1/M`) is polynomial in M, while the test-time-compute tax on
  flat-space is sub-exponential in `M^(−γ)` — i.e. it shrinks to 1.
* `M → 0` (Planck-mass BH): `M^(−γ) → ∞`, so
  `R(M) ≈ M · exp(−large) → 0`. **BH wins**, because the loss gap is
  order unity and closing it costs flat-space exponential test-time
  compute.

### Crossover

Set `R(M*) = 1`:

```
log M*  =  (c/β) · M*^(−γ).
```

For `γ ≈ 0.3` and `c/β` an O(1) constant this gives `M* ≈ 1`–a few
*Planck masses*. I.e. the BH beats flat-space only for objects with
mass at most a handful of `m_P ≈ 2·10⁻⁸ kg`. Anything macroscopic —
let alone astrophysical — is firmly in the regime where flat-space +
test-time compute wins.

---

## 5. Why this happens, in one sentence

> **Chinchilla loss falls polynomially in N, but test-time compute
> closes a loss gap exponentially-cheaply (log dependence ⇒ exp
> dependence the other way). Time dilation taxes the BH polynomially
> in M. Polynomial < exp(polynomial⁻¹), so flat-space wins everywhere
> above the Planck scale.**

A nice way to see it: in the limit `M → ∞`, *both* substrates' losses
approach `L∞`. Their *difference* `M^(−γ)` shrinks. The TTC required
to close it shrinks too (log of a number near 1). Meanwhile the BH is
permanently paying a `1/M` redshift tax. So flat-space's
disadvantage evaporates while the BH's persists.

---

## 6. What if we change the assumptions?

| change                                                     | effect on conclusion                                         |
| ---------------------------------------------------------- | ------------------------------------------------------------ |
| TTC is *power-law* not log (e.g. `L ∝ C_test^(−γ′)`)       | TTC tax becomes polynomial; horse race becomes sensitive to constants but **still flat-favoured for large M** because gap shrinks. |
| Chinchilla saturates (`L∞` is unreachable; harder floor)   | Both substrates cap at the same loss; flat wins outright.    |
| BH compute rate is `T_H ~ 1/M` not Lloyd's `M`             | BH tokens/sec ∼ `1/M³`; flat wins by `M³`, even more decisively. |
| Flat-space `N_B ∼ M^p` with any `p < 2`                    | `ΔL ∼ M^(−pγ) − M^(−2γ) → 0`; flat still wins for M large.   |
| Flat-space `N_B ∼ M^2` too (i.e. flat-space also holographic) | Loss gap is zero, no TTC tax, flat wins by the full `M`.   |

The conclusion is robust: **once you accept Chinchilla + log-TTC, the
holographic memory of a black hole can never overcome its
gravitational-redshift compute tax, except possibly within a few
Planck masses of the quantum-gravity regime where all of this breaks
down anyway.**

---

## 7. Numbers

See `bh_compute_scaling.py` for a tiny script that evaluates
`R(M) = M · exp(−(c/β) M^(−γ))` and prints a table of crossovers.
