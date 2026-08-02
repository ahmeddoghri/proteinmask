"""Tests for the fake "random" baseline finding and its fix."""

from __future__ import annotations

from proteinmask.adversarial import HOLDOUT_SEEDS, TUNING_SEEDS
from proteinmask.design import motif_recovery
from proteinmask.design_v2 import motif_recovery_v2
from proteinmask.eval_v2 import _summarize, build_report
from proteinmask.family import ALPHABET, MOTIF, make_family

# --- the finding: the "random" baseline is a rigged deterministic formula --

def test_formula_baseline_never_matches_any_motif_letter():
    """The formula ALPHABET[(pos*7) % len(ALPHABET)] is hand-picked to
    always miss every one of the 5 planted motif positions."""
    for pos, true_letter in MOTIF.items():
        formula_letter = ALPHABET[(pos * 7) % len(ALPHABET)]
        assert formula_letter != true_letter


def test_original_baseline_is_always_exactly_zero():
    family = make_family()
    _, fake_random = motif_recovery(family[:120], family[120:])
    assert fake_random == 0.0


# --- the fix: an actual random draw ------------------------------------------

def test_fixed_baseline_is_a_real_random_draw_near_the_theoretical_rate():
    """A genuine uniform guess over a 20-letter alphabet should land near
    1/20 = 0.05, not exactly 0."""
    result = _summarize(TUNING_SEEDS)
    assert result["mean_real_random_baseline"] > 0.0
    assert abs(result["mean_real_random_baseline"] - 0.05) < 0.03


def test_fixed_baseline_varies_by_seed_unlike_the_rigged_formula():
    family = make_family()
    train, heldout = family[:120], family[120:]
    scores = {motif_recovery_v2(train, heldout, seed=s)[1] for s in range(10)}
    assert len(scores) > 1  # a real random process produces different draws


def test_guided_score_is_unaffected_by_the_baseline_fix():
    """The profile model's own recovery rate doesn't need fixing; only the
    comparison baseline was wrong."""
    family = make_family()
    train, heldout = family[:120], family[120:]
    guided_v1, _ = motif_recovery(train, heldout)
    guided_v2, _ = motif_recovery_v2(train, heldout, seed=0)
    assert guided_v1 == guided_v2


def test_guided_score_tracks_the_true_base_rate_not_a_circular_metric():
    """Sanity check the profile model isn't itself circular: its recovery
    rate should be close to the actual fraction of held-out sequences that
    carry the fixed motif letter at each position."""
    family = make_family()
    heldout = family[120:]
    positions = [2, 5, 9, 14, 19]
    base_rates = [
        sum(1 for seq in heldout if seq[pos] == MOTIF[pos]) / len(heldout)
        for pos in positions
    ]
    mean_base_rate = sum(base_rates) / len(base_rates)
    guided, _ = motif_recovery(family[:120], heldout)
    assert abs(guided - mean_base_rate) < 0.05


# --- held out, evaluated once ------------------------------------------------

def test_holdout_seeds_are_disjoint_from_tuning_seeds():
    assert not (set(TUNING_SEEDS) & set(HOLDOUT_SEEDS))


def test_holdout_confirms_the_theoretical_rate():
    result = _summarize(HOLDOUT_SEEDS)
    assert abs(result["mean_real_random_baseline"] - 0.05) < 0.03


# --- the original module is untouched ---------------------------------------

def test_original_design_module_untouched():
    import proteinmask.design as design_module

    assert not hasattr(design_module, "motif_recovery_v2")


def test_original_benchmark_still_reproduces():
    family = make_family()
    guided, fake_random = motif_recovery(family[:120], family[120:])
    assert round(guided, 3) == 0.915
    assert round(fake_random, 3) == 0.0


# --- the full report ---------------------------------------------------------

def test_report_is_reproducible():
    assert build_report() == build_report()
