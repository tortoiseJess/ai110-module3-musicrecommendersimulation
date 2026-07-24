# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name  

Give your model a short, descriptive name.  
Example: **VibeFinder 1.0**  

---

## 2. Intended Use  

Describe what your recommender is designed to do and who it is for. 

Prompts:  

- What kind of recommendations does it generate  
- What assumptions does it make about the user  
- Is this for real users or classroom exploration  

---

## 3. How the Model Works  

Explain your scoring approach in simple language.  

Prompts:  

- What features of each song are used (genre, energy, mood, etc.)  
- What user preferences are considered  
- How does the model turn those into a score  
- What changes did you make from the starter logic  

Avoid code here. Pretend you are explaining the idea to a friend who does not program.

---

## 4. Data  

Describe the dataset the model uses.  

Prompts:  

- How many songs are in the catalog  
- What genres or moods are represented  
- Did you add or remove data  
- Are there parts of musical taste missing in the dataset  

---

## 5. Strengths  

Where does your system seem to work well  

Prompts:  

- User types for which it gives reasonable results  
- Any patterns you think your scoring captures correctly  
- Cases where the recommendations matched your intuition  

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

**What surprised me:** I expected genre to matter less, but I didn't expect it to change the ranking order between two other genre-mismatched songs instead. Rooftop Lights (`indie pop`, not an exact `pop` match) jumped ahead of Gym Hero (an exact genre match) for the High-Energy Pop profile, purely because its energy (0.76) sits closer to the target (0.80) than Gym Hero's mood mismatch could offset. This makes sense once you see the math: with genre worth only 0.2, a genre mismatch (0.0) plus a mood match (0.3) can outscore a genre match (0.2) plus a mood mismatch (0.0) if energy closeness tips the balance.

I also noticed Gym Hero (`pop`/`intense`) is a strong pick for *both* the High-Energy Pop and Deep Intense Rock profiles under the shifted weights, even though it's only a genre match for one of them. That's a direct consequence of boosting energy's weight: two profiles with similar target energy (0.8 and 0.9) start converging on the same "high energy" songs regardless of genre, which shows the model is now weighting energy over genre — a real tradeoff. 

---

## 8. Future Work  

Ideas for how you would improve the model next.  

Prompts:  

- Additional features or preferences  
- Better ways to explain recommendations  
- Improving diversity among the top results  
- Handling more complex user tastes  

I think it would be cool if we have enough data to do a ML model on the weights so its learnt instead of fixed.

---

## 9. Personal Reflection  

A few sentences about your experience.  

Prompts:  

- What you learned about recommender systems  
- Something unexpected or interesting you discovered  
- How this changed the way you think about music recommendation apps  
