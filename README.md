# proteinmask

Generative biology demos love to imply they are one commit away from curing something. proteinmask is a toy, says so loudly, and still manages to learn something real.

![CI](https://github.com/ahmeddoghri/proteinmask/actions/workflows/ci.yml/badge.svg)
![python](https://img.shields.io/badge/python-3.9%2B-blue)
![deps](https://img.shields.io/badge/runtime%20deps-none-success)
![license](https://img.shields.io/badge/license-MIT-black)

This does not design real proteins, and anyone telling you their weekend
side project does should be met with polite skepticism. What proteinmask
actually does: build a small synthetic family of protein-like strings with
conserved positions, learn a profile model over them, mask positions in
held-out sequences, and check whether the model can fill them back in. It
borrows the shape of masked sequence modeling without borrowing the
credibility that real biology hasn't earned it yet.

## Run it

```bash
git clone https://github.com/ahmeddoghri/proteinmask
cd proteinmask
pip install -e ".[dev]"
python -m proteinmask.benchmark
```

Generated toy sequences land in `artifacts/designs.fasta`, which you are
welcome to admire and not welcome to synthesize.

## Verified benchmark

Generated locally with `python -m proteinmask.benchmark`:

```text
profile_motif_recovery  0.915
random_motif_recovery   0.000
recovery_gain           0.915
design_novelty          1.000
```

The profile model recovers masked conserved positions 91.5% of the time
versus 0% for a random guesser, and every generated sequence is novel rather
than a copy of something it memorized. Small task, honest number, no wet lab
required.

**Update:** that "0% for a random guesser" isn't a random guesser. It's a
deterministic formula, `ALPHABET[(pos * 7) % len(ALPHABET)]`, hand-picked
to never match the true motif letter at any of the 5 planted positions.
A genuine uniform-random guess over the 20-letter alphabet scores ~5%,
matching the theoretical 1/20 rate almost exactly. The 91.5% guided score
is real and untouched; only the comparison baseline was rigged.
`python -m proteinmask.eval_v2` runs the honest comparison. Details
below.

## The "random" baseline was never random

`design.motif_recovery`'s baseline computes
`ALPHABET[(pos * 7) % len(ALPHABET)]`, a fixed letter derived from the
position index, and calls it a random guesser. It isn't random; it's a
formula. Checked directly against the 5 planted motif positions:

```
pos=2  motif=G  formula picks R
pos=5  motif=L  formula picks S
pos=9  motif=D  formula picks E
pos=14 motif=K  formula picks W
pos=19 motif=Y  formula picks Q
```

Never once a match, by design, which is exactly why the published
benchmark shows `random_motif_recovery 0.000`. A real random process
doesn't reliably produce zero: over a 20-letter alphabet, a uniform guess
lands on the true letter about 1/20 = 5% of the time.

```bash
python -m proteinmask.eval_v2
```
```
seeds        n    guided   fake random   real random
tuning      20     0.915         0.000         0.054
holdout     15     0.915         0.000         0.052
```

`design_v2.py`'s `motif_recovery_v2` replaces the formula with an actual
`random.Random` draw from the full alphabet. Both the tuning sweep and a
disjoint 15-seed holdout land right on the theoretical 5% rate, as they
should. The guided score itself needed no fix: it's exactly the same
91.5% either way, and it's not circular either, it tracks the true
fraction of held-out sequences that actually carry the fixed motif letter
at each position, which is the correct thing for a profile model to
learn. `design.py`/`family.py` are untouched, and the published numbers
above still reproduce exactly; `motif_recovery_v2` is opt-in.

## Research trail

- ESM3, 2024: https://www.science.org/doi/10.1126/science.ads0018
- Protein language models review, 2025: https://arxiv.org/html/2502.06881v1
- ProteinGuide, 2025: https://arxiv.org/abs/2505.04823
- PFMBench, 2025: https://arxiv.org/abs/2506.14796

## Safety note

This repository is only a software benchmark over synthetic strings. It makes
no wet-lab claims and should not be used to select real biological constructs.
If your LinkedIn post about this repo mentions curing anything, that post is
wrong and I did not authorize it.

## Tests

```bash
pytest -q
ruff check .
```

MIT © Ahmed Doghri
