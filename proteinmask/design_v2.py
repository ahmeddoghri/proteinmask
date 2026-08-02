"""The "random" baseline isn't random. Fix it.

``motif_recovery``'s baseline picks ``ALPHABET[(pos * 7) % len(ALPHABET)]``,
a fixed letter computed from the position index, framed as a random
guesser. It is deterministic, and by construction it never once equals
the true motif letter at any of the 5 planted positions:

    pos=2  motif=G  formula picks R
    pos=5  motif=L  formula picks S
    pos=9  motif=D  formula picks E
    pos=14 motif=K  formula picks W
    pos=19 motif=Y  formula picks Q

That's not a coincidence a real random process would produce; a genuine
uniform-random guess over a 20-letter alphabet lands on the true letter
about 1/20 = 5% of the time, not 0%. The published "random_motif_recovery
0.000" is a hand-picked non-match, not a measurement of chance
performance, and it inflates ``recovery_gain`` by roughly 5-6 points it
didn't earn.

``motif_recovery_v2`` replaces the formula with an actual
``random.Random`` draw from the full alphabet, seeded for reproducibility.
The profile model's own recovery rate is untouched and doesn't need
fixing: it already tracks the true base rate of the motif letter in the
held-out data almost exactly, which is the correct behavior for a profile
model, not an artifact.
"""
from __future__ import annotations

import random

from .design import train_profile
from .family import ALPHABET


def motif_recovery_v2(family: list[str], heldout: list[str], seed: int = 0) -> tuple[float, float]:
    profile = train_profile(family)
    positions = [2, 5, 9, 14, 19]
    rng = random.Random(seed)
    guided = random_baseline = 0
    total = len(heldout) * len(positions)
    for seq in heldout:
        for pos in positions:
            pred = max(profile[pos].items(), key=lambda item: item[1])[0]
            guided += int(pred == seq[pos])
            random_guess = rng.choice(ALPHABET)
            random_baseline += int(random_guess == seq[pos])
    return guided / total, random_baseline / total
