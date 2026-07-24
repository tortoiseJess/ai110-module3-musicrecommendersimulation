# 🎵 Music Recommender Simulation

## Project Summary

In this project you will build and explain a small music recommender system.

Your goal is to:

- Represent songs and a user "taste profile" as data
- Design a scoring rule that turns that data into recommendations
- Evaluate what your system gets right and wrong
- Reflect on how this mirrors real world AI recommenders

Replace this paragraph with your own summary of what your version does.

---

## How The System Works

The scoring rule I will use uses genre, mood, energy, and acousticness; tempo_bpm, valence, and danceability are stored but not yet used in scoring to keep it simple and also in adherence with UserProfile
UserProfile will store:
1.favorite_genre (str) — exact-match target
2.favorite_mood (str) — exact-match target
3.target_energy (float, 0–1) — desired energy level to get close to, not maximize
4.likes_acoustic (bool) — whether the user prefers high-acousticness songs
eg 
intense_rock_fan = {
    "favorite_genre": "rock",
    "favorite_mood": "intense",
    "target_energy": 0.9,
    "likes_acoustic": False,
}

Recommender will use this simple but intuitive formula to compute score: --this is my algorithm receipe: 
score = 0.4*genre_match + 0.3*mood_match + 0.2*energy_closeness + 0.1*acoustic_match
ie genre_match / mood_match: 1.0 if exact string match to the user's favorite, else 0.0
energy_closeness: 1 - (song.energy - user.target_energy)**2 — rewards proximity to the target rather than "higher is always better" --the AI suggested this square becuase one would want to punish big misses more than small ones (e.g., 0.5 off should hurt a lot more than two 0.25-off songs would suggest).
This is the more common choice in recommenders because near-matches barely get penalized while a song way off-target gets crushed — it makes rankings more decisive.
acoustic_match: rewards high acousticness if likes_acoustic is True (and low if False)

The reason of those weights is due to :
Genre (0.4, highest) — genre is close to an identity statement. "I like jazz" is a durable, deliberate preference someone states about themselves, not a mood. It's also the most user-controllable input we have (they typed it directly), so it deserves the most trust.
Mood (0.3) — mood is real taste signal but more situational than genre — someone who loves lofi generally might still want "intense" on a given day. It matters, but it's more of a filter/vibe than a core identity trait, so it sits just below genre.
Energy (0.2) — energy is a continuous number, and continuous features are inherently "softer" matches (near-misses still score well via the closeness formula), so giving it a smaller weight keeps it as a fine-tuning signal rather than a dominant one. It also somewhat overlaps with mood (intense↔high energy, chill↔low energy), so weighting it heavily risks double-counting mood's influence.
Acousticness (0.1, lowest) — it's a single binary-ish preference (likes_acoustic) about one audio characteristic, the narrowest and most granular of the four. It's useful as a tiebreaker-level nudge, not a primary driver.

we choose which songs to recommend based on the Ranking Rule: recommend_songs/Recommender.recommend calls score_song on every song in the catalog, sorts the results by score descending, and returns the top k. Ties aren't currently broken by anything beyond original list order. 

Potential biases in this system
Over-prioritizes genre, at mood's expense. With genre weighted at 0.4 vs. mood at 0.3, a song can lose to a worse-matching-mood song purely for having the "right" genre
Penalizes cross-genre discovery. Because genre match is all-or-nothing (exact string equality), the system can never recommend something adjacent to a user's stated genre (e.g., "indie pop" for a "pop" fan) there is no nlp involved at this stage.
---

## Getting Started

### Setup

1. Create a virtual environment (optional but recommended):

   ```bash
   python -m venv .venv
   source .venv/bin/activate      # Mac or Linux
   .venv\Scripts\activate         # Windows

2. Install dependencies

```bash
pip install -r requirements.txt
```

3. Run the app:

```bash
python -m src.main
```

### Running Tests

Run the starter tests with:

```bash
pytest
```

You can add more tests in `tests/test_recommender.py`.

---

## Sample Recommendation Output

Paste a sample of your recommender's output here as a text block so a reader can see what it produces:

```

# User profile: genre=pop, mood=happy, energy=0.8
Top Recommendations
============================================================

1. Sunrise City — Neon Echo
   Score: 0.98
   Reasons:
     - genre match (+0.40)
     - mood match (+0.30)
     - energy closeness 0.82 vs target 0.80 (+0.20)
     - acousticness fit (+0.08)

2. Gym Hero — Max Pulse
   Score: 0.69
   Reasons:
     - genre match (+0.40)
     - mood mismatch (intense vs happy) (+0.00)
     - energy closeness 0.93 vs target 0.80 (+0.20)
     - acousticness fit (+0.10)

3. Rooftop Lights — Indigo Parade
   Score: 0.56
   Reasons:
     - genre mismatch (indie pop vs pop) (+0.00)
     - mood match (+0.30)
     - energy closeness 0.76 vs target 0.80 (+0.20)
     - acousticness fit (+0.07)

4. Crimson Riot — Ashfall
   Score: 0.29
   Reasons:
     - genre mismatch (metal vs pop) (+0.00)
     - mood mismatch (angry vs happy) (+0.00)
     - energy closeness 0.97 vs target 0.80 (+0.19)
     - acousticness fit (+0.10)

5. Basement Warehouse — DJ Fracture
   Score: 0.29
   Reasons:
     - genre mismatch (edm vs pop) (+0.00)
     - mood mismatch (euphoric vs happy) (+0.00)
     - energy closeness 0.88 vs target 0.80 (+0.20)
     - acousticness fit (+0.09)

============================================================
```

**Screenshot or video** *(optional)*: <!-- Insert a screenshot or demo video link here -->

---

## Experiments You Tried

Use this section to document the experiments you ran. For example:

- What happened when you changed the weight on genre from 2.0 to 0.5
- What happened when you added tempo or valence to the score
- How did your system behave for different types of users

---

## Limitations and Risks

Summarize some limitations of your recommender.

Examples:

- It only works on a tiny catalog
- It does not understand lyrics or language
- It might over favor one genre or mood

You will go deeper on this in your model card.

---

## Reflection
- When implementing Songs, it did not load all the attributes into a dictionary from csv 
Read and complete `model_card.md`:

[**Model Card**](model_card.md)

Write 1 to 2 paragraphs here about what you learned:

- about how recommenders turn data into predictions
- about where bias or unfairness could show up in systems like this



