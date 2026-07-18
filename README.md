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
