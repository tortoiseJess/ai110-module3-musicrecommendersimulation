import csv
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass

@dataclass
class Song:
    """
    Represents a song and its attributes.
    Required by tests/test_recommender.py
    """
    id: int
    title: str
    artist: str
    genre: str
    mood: str
    energy: float
    tempo_bpm: float
    valence: float
    danceability: float
    acousticness: float

@dataclass
class UserProfile:
    """
    Represents a user's taste preferences.
    Required by tests/test_recommender.py
    """
    favorite_genre: str
    favorite_mood: str
    target_energy: float
    likes_acoustic: bool

# GENRE_WEIGHT = 0.4
# ENERGY_WEIGHT = 0.2
GENRE_WEIGHT = 0.2   # halved: genre now counts half as much
MOOD_WEIGHT = 0.3
ENERGY_WEIGHT = 0.4  # doubled: energy now counts twice as much
ACOUSTIC_WEIGHT = 0.1

class Recommender:
    """
    OOP implementation of the recommendation logic.
    Required by tests/test_recommender.py
    """
    def __init__(self, songs: List[Song]):
        self.songs = songs

    def score_song(self, user: UserProfile, song: Song) -> Tuple[float, List[str]]:
        """
        Scores a single song against a user profile using the Algorithm Recipe:
        score = 0.4*genre_match + 0.3*mood_match + 0.2*energy_closeness + 0.1*acoustic_match
        """
        reasons: List[str] = []

        genre_match = 1.0 if song.genre == user.favorite_genre else 0.0
        genre_contribution = GENRE_WEIGHT * genre_match
        if genre_match:
            reasons.append(f"genre match (+{genre_contribution:.2f})")
        else:
            reasons.append(f"genre mismatch ({song.genre} vs {user.favorite_genre}) (+{genre_contribution:.2f})")

        mood_match = 1.0 if song.mood == user.favorite_mood else 0.0
        mood_contribution = MOOD_WEIGHT * mood_match
        if mood_match:
            reasons.append(f"mood match (+{mood_contribution:.2f})")
        else:
            reasons.append(f"mood mismatch ({song.mood} vs {user.favorite_mood}) (+{mood_contribution:.2f})")

        energy_closeness = 1 - (song.energy - user.target_energy) ** 2
        energy_contribution = ENERGY_WEIGHT * energy_closeness
        reasons.append(
            f"energy closeness {song.energy:.2f} vs target {user.target_energy:.2f} (+{energy_contribution:.2f})"
        )

        acoustic_match = song.acousticness if user.likes_acoustic else (1 - song.acousticness)
        acoustic_contribution = ACOUSTIC_WEIGHT * acoustic_match
        reasons.append(f"acousticness fit (+{acoustic_contribution:.2f})")

        score = genre_contribution + mood_contribution + energy_contribution + acoustic_contribution
        return score, reasons

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        scored = [(song, self.score_song(user, song)[0]) for song in self.songs]
        scored.sort(key=lambda pair: pair[1], reverse=True)
        return [song for song, _ in scored[:k]]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        score, reasons = self.score_song(user, song)
        return f"Score {score:.2f} — " + "; ".join(reasons)

def load_songs(csv_path: str) -> List[Dict]:
    """
    Loads songs from a CSV file.
    Required by src/main.py
    """
    with open(csv_path, newline="") as f:
        reader = csv.DictReader(f)
        songs = []
        for row in reader:
            songs.append({
                "id": int(row["id"]),
                "title": row["title"],
                "artist": row["artist"],
                "genre": row["genre"],
                "mood": row["mood"],
                "energy": float(row["energy"]),
                "tempo_bpm": float(row["tempo_bpm"]),
                "valence": float(row["valence"]),
                "danceability": float(row["danceability"]),
                "acousticness": float(row["acousticness"]),
            })
    print(f"Loaded songs: {len(songs)} songs.")
    return songs

def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """
    Scores a single song against user preferences using the Algorithm Recipe:
    score = 0.4*genre_match + 0.3*mood_match + 0.2*energy_closeness + 0.1*acoustic_match
    Required by recommend_songs() and src/main.py
    """
    favorite_genre = user_prefs.get("favorite_genre", user_prefs.get("genre"))
    favorite_mood = user_prefs.get("favorite_mood", user_prefs.get("mood"))
    target_energy = user_prefs.get("target_energy", user_prefs.get("energy", 0.0))
    likes_acoustic = user_prefs.get("likes_acoustic", False)

    reasons: List[str] = []

    genre_match = 1.0 if song["genre"] == favorite_genre else 0.0
    genre_contribution = GENRE_WEIGHT * genre_match
    if genre_match:
        reasons.append(f"genre match (+{genre_contribution:.2f})")
    else:
        reasons.append(f"genre mismatch ({song['genre']} vs {favorite_genre}) (+{genre_contribution:.2f})")

    mood_match = 1.0 if song["mood"] == favorite_mood else 0.0
    mood_contribution = MOOD_WEIGHT * mood_match
    if mood_match:
        reasons.append(f"mood match (+{mood_contribution:.2f})")
    else:
        reasons.append(f"mood mismatch ({song['mood']} vs {favorite_mood}) (+{mood_contribution:.2f})")

    energy_closeness = 1 - (song["energy"] - target_energy) ** 2
    energy_contribution = ENERGY_WEIGHT * energy_closeness
    reasons.append(
        f"energy closeness {song['energy']:.2f} vs target {target_energy:.2f} (+{energy_contribution:.2f})"
    )

    acoustic_match = song["acousticness"] if likes_acoustic else (1 - song["acousticness"])
    acoustic_contribution = ACOUSTIC_WEIGHT * acoustic_match
    reasons.append(f"acousticness fit (+{acoustic_contribution:.2f})")

    score = genre_contribution + mood_contribution + energy_contribution + acoustic_contribution
    return score, reasons

def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """
    Functional implementation of the recommendation logic.
    Required by src/main.py
    """
    scored = []
    for song in songs:
        score, reasons = score_song(user_prefs, song)
        explanation = "; ".join(reasons)
        scored.append((song, score, explanation))

    scored.sort(key=lambda item: item[1], reverse=True)
    return scored[:k]
