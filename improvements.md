Limitations
No personalization beyond 4 fields. A user is reduced to genre + mood + target energy + acoustic preference — no memory of listening history, no nuance like "usually likes lofi but wants something upbeat today."
Brittle exact-match on genre/mood. "lofi" vs "lo-fi" or "indie pop" vs "pop" score zero even though they're conceptually close — string equality has no sense of category similarity.
Hand-picked weights, not learned. 0.4/0.3/0.2/0.1 is a guess. There's no data-driven justification, and it can't adapt — a real system would learn weights from actual user feedback and update them over time.
No collaborative signal. It can't recommend a song purely because "similar users liked it" if that song doesn't score well on the raw content features — it's blind to patterns that live in behavior, not attributes.
Cold-start requires explicit input. Without stated preferences, there's no fallback (e.g., popularity-based defaults, trending songs) — the system does nothing for a user who hasn't filled out a profile.
No diversity or novelty control. A ranking rule that's pure "sort by score, take top-k" can return 5 near-duplicate songs (same artist, same genre/mood) with nothing to encourage variety.
Static, no feedback loop. Scores don't update based on skips/likes/plays — recommend once, same result every time for the same profile, no session-to-session learning.
Small, closed catalog. With only 10 songs and unnormalized string categories, it hasn't been tested against real scale/messiness (missing fields, inconsistent casing, thousands of genres).
Ignores available features it could use. We deliberately dropped tempo_bpm, valence, danceability for simplicity — real recommenders wouldn't leave signal on the table.
