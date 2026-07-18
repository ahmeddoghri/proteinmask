from proteinmask import ALPHABET, design_sequence, make_family, motif_recovery


def test_family_is_deterministic() -> None:
    assert make_family(seed=1) == make_family(seed=1)


def test_design_uses_valid_alphabet() -> None:
    seq = design_sequence(make_family(n=60))
    assert set(seq).issubset(set(ALPHABET))
    assert len(seq) == 24


def test_profile_recovers_motif_better_than_random() -> None:
    family = make_family()
    guided, random_baseline = motif_recovery(family[:120], family[120:])
    assert guided > random_baseline + 0.5
