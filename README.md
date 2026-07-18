# proteinmask

A toy masked protein-like sequence infiller. It does not design real proteins.
It builds a small synthetic family with conserved positions, learns a profile
model, samples new strings, and reports motif recovery against held-out toy
sequences.

![CI](https://github.com/ahmeddoghri/proteinmask/actions/workflows/ci.yml/badge.svg)
![python](https://img.shields.io/badge/python-3.9%2B-blue)
![deps](https://img.shields.io/badge/runtime%20deps-none-success)
![license](https://img.shields.io/badge/license-MIT-black)

## Run it

```bash
git clone https://github.com/ahmeddoghri/proteinmask
cd proteinmask
pip install -e ".[dev]"
python -m proteinmask.benchmark
```

Generated toy sequences are written to `artifacts/designs.fasta`.

## Verified benchmark

These numbers were generated locally with `python -m proteinmask.benchmark`:

```text
profile_motif_recovery  0.915
random_motif_recovery   0.000
recovery_gain           0.915
design_novelty          1.000
```

## Research trail

- ESM3, 2024: https://www.science.org/doi/10.1126/science.ads0018
- Protein language models review, 2025: https://arxiv.org/html/2502.06881v1
- ProteinGuide, 2025: https://arxiv.org/abs/2505.04823
- PFMBench, 2025: https://arxiv.org/abs/2506.14796

## Safety note

This repository is only a software benchmark over synthetic strings. It makes
no wet-lab claims and should not be used to select real biological constructs.

## Tests

```bash
pytest -q
ruff check .
```

MIT © Ahmed Doghri
