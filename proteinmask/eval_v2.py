"""Is the "random" baseline actually random?

``design.motif_recovery`` compares the profile model against
``ALPHABET[(pos * 7) % len(ALPHABET)]``, a deterministic formula the
benchmark calls a random guesser. It's hand-picked to never match the
true motif letter at any of the 5 planted positions, so it always scores
0.000, inflating the published "recovery_gain" by roughly 5-6 points a
genuine random guess wouldn't concede. This module reruns the comparison
with an actual uniform-random draw, across many seeds.

    python -m proteinmask.eval_v2
"""
from __future__ import annotations

import argparse
import json
from typing import Dict, List, Sequence

from .adversarial import HOLDOUT_SEEDS, TUNING_SEEDS
from .design import motif_recovery
from .design_v2 import motif_recovery_v2
from .family import make_family


def _summarize(seeds: Sequence[int]) -> Dict:
    family = make_family()
    train = family[:120]
    heldout = family[120:]

    fake_random_baselines: List[float] = []
    real_random_baselines: List[float] = []
    guided_score = None
    for seed in seeds:
        guided, fake_random = motif_recovery(train, heldout)
        guided_score = guided
        fake_random_baselines.append(fake_random)
        _, real_random = motif_recovery_v2(train, heldout, seed=seed)
        real_random_baselines.append(real_random)

    n = len(seeds)
    return {
        "n": n,
        "guided_score": round(guided_score, 4),
        "mean_fake_random_baseline": round(sum(fake_random_baselines) / n, 4),
        "mean_real_random_baseline": round(sum(real_random_baselines) / n, 4),
        "theoretical_random_rate": round(1 / 20, 4),
    }


def build_report() -> Dict:
    return {
        "tuning": _summarize(TUNING_SEEDS),
        "holdout": _summarize(HOLDOUT_SEEDS),
    }


def format_report(report: Dict) -> str:
    lines = [
        "is the 'random' baseline actually random?",
        "=" * 60,
        f"{'seeds':<10}{'n':>4}{'guided':>10}{'fake random':>14}{'real random':>14}",
        "-" * 60,
    ]
    for name, key in [("tuning", "tuning"), ("holdout", "holdout")]:
        row = report[key]
        lines.append(
            f"{name:<10}{row['n']:>4}{row['guided_score']:>10.3f}"
            f"{row['mean_fake_random_baseline']:>14.3f}{row['mean_real_random_baseline']:>14.3f}"
        )
    lines.append("")
    lines.append(
        f"theoretical uniform-random rate over a 20-letter alphabet: "
        f"1/20 = {report['tuning']['theoretical_random_rate']:.3f}"
    )
    lines.append(
        "the published 'random_motif_recovery 0.000' is a hand-picked formula"
    )
    lines.append(
        "guaranteed to miss the true motif letter at all 5 planted positions,"
    )
    lines.append(
        "not a measurement of chance performance. an actual uniform-random"
    )
    lines.append(
        "guess lands close to the theoretical 5% rate, as it should. the guided"
    )
    lines.append(
        "score itself is untouched and correctly tracks the true base rate of"
    )
    lines.append("the motif letter in held-out data; only the baseline was rigged.")
    return "\n".join(lines)


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--json", default=None)
    args = parser.parse_args(argv)

    report = build_report()
    print(format_report(report))

    if args.json:
        with open(args.json, "w", encoding="utf-8") as handle:
            json.dump(report, handle, indent=2)
            handle.write("\n")
        print(f"\nWrote {args.json}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
