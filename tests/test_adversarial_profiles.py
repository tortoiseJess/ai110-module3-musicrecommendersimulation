import os

from src.recommender import load_songs, recommend_songs, score_song

SONGS_CSV = os.path.join(os.path.dirname(__file__), "..", "data", "songs.csv")


def load_real_songs():
    return load_songs(SONGS_CSV)


def test_conflicting_energy_and_mood_still_returns_ranked_results():
    """
    Profile #1: high target_energy (0.9) paired with a low-energy mood (sad).
    No song in songs.csv is both sad and high-energy, so this checks that the
    algorithm picks a reasonable compromise instead of erroring or returning
    nonsense, and that the mismatch is visible in the explanation.
    """
    songs = load_real_songs()
    user_prefs = {"genre": "rock", "mood": "sad", "energy": 0.9, "likes_acoustic": False}

    results = recommend_songs(user_prefs, songs, k=3)

    assert len(results) == 3
    # Scores should be sorted descending
    scores = [score for _, score, _ in results]
    assert scores == sorted(scores, reverse=True)

    top_song, top_score, top_explanation = results[0]
    # No sad+high-energy song exists, so the mood mismatch reason should show up
    assert "mood mismatch" in top_explanation
    assert 0.0 <= top_score <= 1.0


def test_out_of_range_target_energy_breaks_the_0_to_1_score_assumption():
    """
    Profile #2: target_energy outside the valid [0, 1] range.
    energy_closeness = 1 - (song.energy - target_energy) ** 2 assumes both
    values live in [0, 1]. There's no validation on target_energy, so an
    out-of-range value can push energy_contribution negative and drag the
    total score below 0 -- silently breaking the intended score range
    instead of raising an error.
    """
    songs = load_real_songs()
    extreme_user_prefs = {"genre": "pop", "mood": "happy", "energy": 3.0, "likes_acoustic": False}

    song = next(s for s in songs if s["title"] == "Sunrise City")  # energy 0.82
    score, reasons = score_song(extreme_user_prefs, song)

    energy_diff = song["energy"] - extreme_user_prefs["energy"]
    expected_energy_contribution = 0.2 * (1 - energy_diff ** 2)

    assert expected_energy_contribution < 0
    assert any("energy closeness" in r for r in reasons)
    # No exception was raised, and the score is no longer bounded to [0, 1]
    assert score < 0.4 + 0.3  # genre+mood contribution alone, energy dragged it down


def test_genre_and_mood_absent_from_dataset_collapses_ranking_to_energy_and_acoustic():
    """
    Profile #3: favorite_genre/favorite_mood that don't exist anywhere in
    songs.csv ("opera"/"ecstatic"). genre_match and mood_match are 0 for
    every song, so 70% of the scoring weight (genre 0.4 + mood 0.3) is
    zeroed out and the ranking is decided entirely by energy closeness and
    acousticness fit. Confirms recommend_songs degrades gracefully instead
    of erroring or producing an arbitrary/tied order.
    """
    songs = load_real_songs()
    user_prefs = {"genre": "opera", "mood": "ecstatic", "energy": 0.5, "likes_acoustic": True}

    for song in songs:
        score, reasons = score_song(user_prefs, song)
        assert "genre mismatch" in reasons[0]
        assert "mood mismatch" in reasons[1]

    results = recommend_songs(user_prefs, songs, k=3)
    assert len(results) == 3

    # Winner should be explainable purely by energy closeness to 0.5 + high acousticness
    top_song, top_score, _ = results[0]
    energy_closeness = 1 - (top_song["energy"] - 0.5) ** 2
    expected_score = 0.2 * energy_closeness + 0.1 * top_song["acousticness"]
    assert abs(top_score - expected_score) < 1e-9
