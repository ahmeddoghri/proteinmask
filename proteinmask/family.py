from __future__ import annotations

import random

ALPHABET = "ACDEFGHIKLMNPQRSTVWY"
MOTIF = {2: "G", 5: "L", 9: "D", 14: "K", 19: "Y"}


def make_family(seed: int = 31, n: int = 160, length: int = 24) -> list[str]:
    rng = random.Random(seed)
    family = []
    hydrophobic = "AILMFWV"
    polar = "STNQ"
    for _ in range(n):
        seq = []
        for pos in range(length):
            if pos in MOTIF and rng.random() < 0.92:
                seq.append(MOTIF[pos])
            elif pos % 4 == 0:
                seq.append(rng.choice(hydrophobic))
            elif pos % 4 == 2:
                seq.append(rng.choice(polar + "G"))
            else:
                seq.append(rng.choice(ALPHABET))
        family.append("".join(seq))
    return family
