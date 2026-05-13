# 👑 DUGOUT DYNASTY: Sovereign Edition
**Challenge 2: Fan Engagement & Gamification | IPL 2026**

Dugout Dynasty is a gamified fan engagement platform built to transform the T20 viewing experience. Unlike standard trackers, this system creates a **"Loyalty Loop"** through real-time rewards, verified predictions, and an adaptive AI progression system powered by **Gemini 2.5 Flash**.

---

## 🎮 Gamification Mechanics

- **✨ Aura Economy:** A comprehensive XP system (Aura) that rewards every interaction.
- **🎯 The Oracle:** A verified prediction engine. Users lock guesses, and Gemini acts as the "Umpire" to judge accuracy against live 2026 match data.
- **🛡️ Player Classes:** Progression isn't just a number. At 100 Aura, users choose a path: *Tactician*, *Chaos Agent*, or *Hype God*, changing the AI's behavior and personality.
- **🛒 The Aura Shop:** A functional economy where users spend earned points on "Streak Shields" and "Hype Boosters."
- **🕵️ Star Scouting:** A tactical multiplier feature. Scout a live player to earn 1.2x Aura while they are on the field.

---

## 🛠️ Tech Stack

- **AI Engine:** Google Gemini 2.5 Flash (Multimodal & Reasoning)
- **Deployment:** Google Cloud Run (Serverless Auto-scaling)
- **Framework:** Streamlit (High-Performance UI)
- **State Management:** Session-based persistent RPG logic.

---

## 🚀 Deployment Instructions

### Local Setup
1. Clone the repo: `git clone https://github.com/Thouseef68/dugout-dynasty-2026.git`
2. Install dependencies: `pip install -r requirements.txt`
3. Run: `streamlit run app.py`

### Cloud Deployment
```bash
gcloud run deploy dugout-dynasty --source . --region asia-northeast1 --allow-unauthenticated --set-env-vars GOOGLE_API_KEY=YOUR_KEY