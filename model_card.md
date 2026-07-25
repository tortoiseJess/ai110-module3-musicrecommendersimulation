# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name  

**Claw Recommender**

---

## 2. Intended Use  

Claw Recommender takes a simple user profile (favorite genre, favorite mood, target energy, and whether they like acoustic songs) and ranks a small song catalog to suggest the best matches. It's built for classroom exploration of how recommender scoring works, not for real listeners. It assumes a person's whole music taste can be boiled down to those four traits, which is a big simplification.

---

## 3. How the Model Works  

Every song gets a score out of 1.0, built from four pieces:

- **Genre match** — full points if the song's genre matches the user's favorite genre, zero if not. Worth 20% of the score.
- **Mood match** — full points if the song's mood matches the user's favorite mood, zero if not. Worth 30% of the score.
- **Energy closeness** — the closer the song's energy is to the user's target energy, the more points. Being off by a little costs a little; being off by a lot costs a lot more (the penalty grows faster than the gap itself). Worth 40% of the score.
- **Acoustic fit** — rewards acoustic songs for users who like acoustic, and rewards non-acoustic songs for users who don't. Worth 10% of the score.

These four pieces are added up, and the app prints the top-scoring songs with plain-English reasons for each score. The starter logic weighted genre highest (0.4) and energy lowest (0.2); we flipped that so energy now matters most (0.4) and genre matters less (0.2).

---

## 4. Data  

The catalog is tiny: 18 songs in `data/songs.csv`, each with a genre, mood, energy, tempo, valence, danceability, and acousticness score. There are 15 different genres represented (pop, lofi, rock, ambient, jazz, synthwave, indie pop, folk, hip-hop, country, reggae, metal, classical, edm, blues), but most genres only have one song each — only pop and lofi have more than one. With so few songs per genre, there's not much real choice within a genre, and whole styles of music (like R&B, latin, or k-pop) aren't represented at all.

---

## 5. Strengths  

- For users whose favorite genre has more than one song (pop, lofi), the recommender does a good job surfacing songs that match on genre and mood together, like "Sunrise City" for a happy, high-energy pop fan.
- The energy-closeness scoring correctly ranks near-target songs above far-off ones — a user wanting energy 0.9 reliably gets pointed at the catalog's loudest, fastest tracks (Storm Runner, Crimson Riot, Gym Hero).
- The explanations are easy to read and make it clear *why* a song was recommended, which is good for teaching/debugging the scoring logic.

---

## 6. Limitations and Bias 

Where the system struggles or behaves unfairly. 

Prompts:  

- Features it does not consider  
- Genres or moods that are underrepresented  
- Cases where the system overfits to one preference  
- Ways the scoring might unintentionally favor some users  

**Energy weight dominance flattens genre identity.** After doubling `ENERGY_WEIGHT` to 0.4 and halving `GENRE_WEIGHT` to 0.2, the scorer starts collapsing distinct genre identities into a single "energy level" bucket: my High-Energy Pop profile (target energy 0.8) and Deep Intense Rock profile (target energy 0.9) both rank Gym Hero highly even though it's only a genre match for one of them, because their target energies are close enough that energy closeness outweighs the genre mismatch. This means the system can create a filter bubble around *energy level* rather than *genre or mood* — a user who says they like rock could end up mostly hearing pop and metal simply because those tracks happen to be loud/fast, not because they share rock's actual sound or instrumentation. The `energy_closeness = 1 - (energy_diff)**2` formula also means the penalty for being off-target grows quadratically, so users with unusual or extreme target energies (very chill listeners around 0.2–0.3, like the Chill Lofi profile) are especially sensitive to small mismatches in genre and get recommended the catalog songs that has their exact energy value.
Compounding this, the dataset itself is skewed — genres like ambient, jazz, folk, hip-hop, country, reggae, metal, classical, edm, and blues each have only a single song, while pop and lofi have multiple, so users whose favorite genre is one of those single-song genres have almost no alternatives if that one song's energy or mood doesn't line up, effectively pushing them toward the more populous genres' recommendations instead.

---

## 7. Evaluation  

How you checked whether the recommender behaved as expected. 

Prompts:  

- Which user profiles you tested  
- What you looked for in the recommendations  
- What surprised you  
- Any simple tests or comparisons you ran  

No need for numeric metrics unless you created some.

**Profiles tested:** the three main listener profiles from `src/main.py` — High-Energy Pop (genre `pop`, mood `happy`, target energy 0.8), Chill Lofi (genre `lofi`, mood `calm`, target energy 0.2, likes acoustic), and Deep Intense Rock (genre `rock`, mood `intense`, target energy 0.9) — plus the three adversarial edge-case profiles (conflicting mood/energy, out-of-range energy, unknown genre/mood).

**Experiment: weight shift.** I changed `GENRE_WEIGHT` from 0.4 to 0.2 and `ENERGY_WEIGHT` from 0.2 to 0.4 (mood and acousticness unchanged, weights still sum to 1.0) and re-ran all profiles to compare against the baseline weights.

| Profile | Baseline (genre 0.4 / energy 0.2) | Weight-shifted (genre 0.2 / energy 0.4) |
|---|---|---|
| High-Energy Pop | #1 Sunrise City, #2 Gym Hero, #3 Rooftop Lights | #1 Sunrise City, #2 **Rooftop Lights**, #3 Gym Hero |
| Deep Intense Rock | #1 Storm Runner, #2 Gym Hero (0.59) | #1 Storm Runner, #2 Gym Hero (**0.79**) |

**What I learnt from the tests/ Surprises:** I expected genre to matter less, but I didn't expect it to change the ranking order between two other genre-mismatched songs instead. Rooftop Lights (`indie pop`, not an exact `pop` match) jumped ahead of Gym Hero (an exact genre match) for the High-Energy Pop profile, purely because its energy (0.76) sits closer to the target (0.80) than Gym Hero's mood mismatch could offset. This makes sense once you see the math: with genre worth only 0.2, a genre mismatch (0.0) plus a mood match (0.3) can outscore a genre match (0.2) plus a mood mismatch (0.0) if energy closeness tips the balance.

I also noticed Gym Hero (`pop`/`intense`) is a strong pick for *both* the High-Energy Pop and Deep Intense Rock profiles under the shifted weights, even though it's only a genre match for one of them. That's a direct consequence of boosting energy's weight: two profiles with similar target energy (0.8 and 0.9) start converging on the same "high energy" songs regardless of genre, which shows the model is now weighting energy over genre — a real tradeoff. 
I also noticed usually the top song recommended has the exact match but all the other ones that follow is unrelated and are there because of energy/ acoustic contributions to the scoring function.

---

## 8. Future Work  

Ideas for how you would improve the model next.  

Prompts:  

- Additional features or preferences  
- Better ways to explain recommendations  
- Improving diversity among the top results  
- Handling more complex user tastes  

I think it would be cool if we have enough data to do a ML model on the weights so its learnt instead of fixed.
For the interface, in addition to user profile, it would be great to include a chatbot for the user to ask what she wants because it largely depends on what she needs to do while playing the music.

---

## 9. Personal Reflection  

The biggest learning moment was the weight-shift experiment in section 7: bumping `ENERGY_WEIGHT` from 0.2 to 0.4 didn't just reorder songs within a genre, it let energy override genre matches entirely (Rooftop Lights beating Gym Hero, Gym Hero showing up as a top pick for both the pop and rock profiles). That's when it really clicked that a recommender isn't "smart" or "dumb" — it's just arithmetic, and every weight you pick is a value judgment about what should matter, with tradeoffs you often don't see until you test edge cases.

AI helped with generating experiments and additional songs. It somehow got the code writing wrong this time.

It surprised me that simple algorithms can still feel like real recommendations based on simple weighted sums and ranking logic. Modern recommendation apps may be a bunch of weighted sums and scores leading to my recommendation playlist. I also learnt the model is very easy to fall into bias towards certain songs or user profiles get more accurate recommendations.

I would want to expand this futher to incorporate NLP in the mood and genre instead of a string match. 


