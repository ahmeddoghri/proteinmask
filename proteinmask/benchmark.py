from __future__ import annotations

from pathlib import Path

from .design import design_sequence, motif_recovery, write_fasta
from .family import make_family


def main() -> None:
    family = make_family()
    train = family[:120]
    heldout = family[120:]
    guided, random_baseline = motif_recovery(train, heldout)
    designed = [design_sequence(train, seed=idx) for idx in range(1, 6)]
    write_fasta(designed, Path("artifacts") / "designs.fasta")
    novelty = sum(1 for seq in designed if seq not in train) / len(designed)
    print("proteinmask benchmark: toy masked protein-like infilling")
    print(f"profile_motif_recovery  {guided:.3f}")
    print(f"random_motif_recovery   {random_baseline:.3f}")
    print(f"recovery_gain           {guided - random_baseline:.3f}")
    print(f"design_novelty          {novelty:.3f}")
    print("artifact                artifacts/designs.fasta")


if __name__ == "__main__":
    main()
