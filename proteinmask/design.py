from __future__ import annotations

import random
from collections import Counter
from pathlib import Path

from .family import ALPHABET


def train_profile(family: list[str], alpha: float = 0.5) -> list[dict[str, float]]:
    length = len(family[0])
    profile = []
    for pos in range(length):
        counts = Counter(seq[pos] for seq in family)
        total = sum(counts.values()) + alpha * len(ALPHABET)
        profile.append({aa: (counts[aa] + alpha) / total for aa in ALPHABET})
    return profile


def _pair_bonus(family: list[str], pos: int, aa: str, seq: list[str]) -> float:
    bonus = 0.0
    for near in (pos - 1, pos + 1):
        if 0 <= near < len(seq) and seq[near] != "?":
            pair = aa + seq[near] if near > pos else seq[near] + aa
            count = sum(1 for item in family if item[min(pos, near) : min(pos, near) + 2] == pair)
            bonus += count / max(1, len(family))
    return bonus


def design_sequence(family: list[str], seed: int = 6, fixed: dict[int, str] | None = None) -> str:
    rng = random.Random(seed)
    profile = train_profile(family)
    length = len(family[0])
    fixed = fixed or {0: "M"}
    seq = ["?"] * length
    for pos, aa in fixed.items():
        seq[pos] = aa
    for _ in range(4):
        for pos in range(length):
            if pos in fixed:
                continue
            weights = []
            for aa in ALPHABET:
                weights.append(profile[pos][aa] + 0.35 * _pair_bonus(family, pos, aa, seq))
            total = sum(weights)
            pick = rng.random() * total
            acc = 0.0
            for aa, weight in zip(ALPHABET, weights):
                acc += weight
                if acc >= pick:
                    seq[pos] = aa
                    break
    return "".join(seq)


def motif_recovery(family: list[str], heldout: list[str]) -> tuple[float, float]:
    profile = train_profile(family)
    positions = [2, 5, 9, 14, 19]
    guided = random_baseline = 0
    total = len(heldout) * len(positions)
    for seq in heldout:
        for pos in positions:
            pred = max(profile[pos].items(), key=lambda item: item[1])[0]
            guided += int(pred == seq[pos])
            random_baseline += int(ALPHABET[(pos * 7) % len(ALPHABET)] == seq[pos])
    return guided / total, random_baseline / total


def write_fasta(sequences: list[str], path: str | Path) -> Path:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    lines = []
    for idx, seq in enumerate(sequences, start=1):
        lines.append(f">proteinmask_{idx}")
        lines.append(seq)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return path
