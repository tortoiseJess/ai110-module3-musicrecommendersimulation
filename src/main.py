"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

from recommender import load_songs, recommend_songs, score_song


def main() -> None:
    songs = load_songs("data/songs.csv")

    # Sample user profiles covering distinct listener tastes
    user_profiles = {
        "High-Energy Pop": {"genre": "pop", "mood": "happy", "energy": 0.8, "likes_acoustic": False},
        "Chill Lofi": {"genre": "lofi", "mood": "calm", "energy": 0.2, "likes_acoustic": True},
        "Deep Intense Rock": {"genre": "rock", "mood": "intense", "energy": 0.9, "likes_acoustic": False},
    }

    # Adversarial / edge-case profiles: designed to stress-test the scoring
    # logic rather than represent a realistic listener.
    adversarial_profiles = {
        # Conflicting preferences: high target energy paired with a mood
        # (sad) that no high-energy song in the dataset has.
        "Conflicting: High-Energy Sad": {"genre": "rock", "mood": "sad", "energy": 0.9, "likes_acoustic": False},
        # Out-of-range target_energy (valid range is 0-1). Tests whether
        # energy_closeness silently breaks its [0,1] assumption.
        "Edge Case: Out-of-Range Energy": {"genre": "pop", "mood": "happy", "energy": 3.0, "likes_acoustic": False},
        # Genre/mood that don't exist anywhere in songs.csv. Tests that
        # ranking degrades gracefully to energy + acousticness only.
        "Edge Case: Unknown Genre/Mood": {"genre": "opera", "mood": "ecstatic", "energy": 0.5, "likes_acoustic": True},
    }
    user_profiles.update(adversarial_profiles)

    for profile_name, user_prefs in user_profiles.items():
        recommendations = recommend_songs(user_prefs, songs, k=3)

        print(f"\nTop Recommendations for: {profile_name}")
        print("=" * 60)
        for rank, (song, score, explanation) in enumerate(recommendations, start=1):
            print(f"\n{rank}. {song['title']} — {song['artist']}")
            print(f"   Score: {score:.2f}")
            print("   Reasons:")
            for reason in explanation.split("; "):
                print(f"     - {reason}")
        print("\n" + "=" * 60)

if __name__ == "__main__":
    main()
