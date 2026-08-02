"""Seeds for the fixed random baseline, and a disjoint holdout evaluated
exactly once.
"""
from __future__ import annotations

TUNING_SEEDS = list(range(20))
HOLDOUT_SEEDS = list(range(1000, 1015))
