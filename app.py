import streamlit as st
import google.generativeai as genai
import os
from PIL import Image
from dotenv import load_dotenv

# --- 1. CORE SETUP ---
# Must be the very first Streamlit command
st.set_page_config(page_title="Dugout Dynasty: Sovereign", page_icon="⚡", layout="wide")
load_dotenv()

# Initialize Session State
if 'aura' not in st.session_state: st.session_state.aura = 0
if 'streak' not in st.session_state: st.session_state.streak = 4  
if 'user_role' not in st.session_state: st.session_state.user_role = "Unclassed"
if 'predictions' not in st.session_state: st.session_state.predictions = []
if 'scouted_player' not in st.session_state: st.session_state.scouted_player = None
if 'inventory' not in st.session_state: st.session_state.inventory = []

# --- 2. ADVANCED UI STYLING (Neon Glassmorphism) ---
st.markdown("""
    <style>
    @keyframes pulse {
        0% { box-shadow: 0 0 5px #00f2ff; }
        50% { box-shadow: 0 0 20px #00f2ff; }
        100% { box-shadow: 0 0 5px #00f2ff; }
    }
    .stApp {
        background: linear-gradient(135deg, #0f0c29 0%, #302b63 50%, #24243e 100%);
        color: white;
    }
    .dashboard-card {
        background: rgba(255, 255, 255, 0.07);
        backdrop-filter: blur(10px);
        border-radius: 15px;
        padding: 20px;
        text-align: center;
        border: 1px solid rgba(0, 242, 255, 0.3);
        transition: 0.3s;
        margin-bottom: 15px;
    }
    .dashboard-card:hover {
        transform: translateY(-5px);
        border: 1px solid #00f2ff;
        animation: pulse 2s infinite;
    }
    .shop-item {
        background: rgba(0, 242, 255, 0.05);
        border: 1px dashed #00f2ff;
        padding: 15px;
        border-radius: 10px;
        margin-bottom: 10px;
        text-align: center;
    }
    .icon-header { font-size: 40px; margin-bottom: 10px; }
    .stat-label { color: #aaa; font-size: 12px; text-transform: uppercase; letter-spacing: 1px; }
    .stat-value { color: #00f2ff; font-size: 24px; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. HELPER LOGIC ---
def add_aura(amount, reason):
    # Multiplier Logic: 1.5x for streaks, 1.2x for active scouting
    multiplier = 1.0
    if st.session_state.streak >= 3: multiplier += 0.5
    if st.session_state.scouted_player: multiplier += 0.2
    
    total = int(amount * multiplier)
    st.session_state.aura += total
    st.toast(f"✨ +{total} AURA ({reason})")

# Gemini Config
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
model = genai.GenerativeModel('gemini-2.5-flash')

# --- 4. THE AURA SHOP (Sidebar) ---
with st.sidebar:
    st.markdown("<h2 style='color:#00f2ff;'>🛒 AURA SHOP</h2>", unsafe_allow_html=True)
    st.write("Spend Aura on items and shields.")
    
    # Item 1: Streak Shield
    st.markdown("<div class='shop-item'>🛡️ Streak Shield<br><small>500 Aura</small></div>", unsafe_allow_html=True)
    if st.button("PURCHASE SHIELD"):
        if st.session_state.aura >= 500:
            st.session_state.aura -= 500
            st.session_state.inventory.append("Streak Shield")
            st.success("Shield Purchased!")
        else: st.error("Insufficient Aura!")

    # Item 2: Hype Booster
    st.markdown("<div class='shop-item'>🚀 Hype Booster<br><small>200 Aura</small></div>", unsafe_allow_html=True)
    if st.button("PURCHASE BOOSTER"):
        if st.session_state.aura >= 200:
            st.session_state.aura -= 200
            st.session_state.inventory.append("Hype Booster")
            st.success("Booster Ready!")
        else: st.error("Insufficient Aura!")

    st.write("---")
    st.write("**Inventory:**")
    if not st.session_state.inventory: st.caption("Empty")
    for item in set(st.session_state.inventory):
        st.write(f"📦 {item} x{st.session_state.inventory.count(item)}")

# --- 5. MAIN DASHBOARD ---
st.markdown("<h1 style='text-align: center; color:#ff4b4b; letter-spacing: 5px;'>🏆 DUGOUT DYNASTY 2026</h1>", unsafe_allow_html=True)

# Row 1: Key Metrics
m1, m2, m3, m4 = st.columns(4)
with m1:
    st.markdown(f'<div class="dashboard-card"><div class="icon-header">✨</div><div class="stat-label">Aura</div><div class="stat-value">{st.session_state.aura}</div></div>', unsafe_allow_html=True)
with m2:
    st.markdown(f'<div class="dashboard-card"><div class="icon-header">🔥</div><div class="stat-label">Streak</div><div class="stat-value">{st.session_state.streak} Days</div></div>', unsafe_allow_html=True)
with m3:
    scout_display = st.session_state.scouted_player if st.session_state.scouted_player else "None"
    st.markdown(f'<div class="dashboard-card"><div class="icon-header">🕵️</div><div class="stat-label">Scouting</div><div class="stat-value" style="font-size:18px;">{scout_display}</div></div>', unsafe_allow_html=True)
with m4:
    prog = min(st.session_state.aura / 2000, 1.0)
    st.markdown(f'<div class="dashboard-card"><div class="icon-header">🛡️</div><div class="stat-label">Role</div><div class="stat-value" style="color:#ff4b4b;">{st.session_state.user_role}</div></div>', unsafe_allow_html=True)

# Progress & Badges
c1, c2 = st.columns([1, 2])
with c1:
    st.markdown("<div class='dashboard-card' style='height: 120px;'>", unsafe_allow_html=True)
    st.write("**🏆 COLLECTION**")
    badges = ["💎", "🔥", "🎯", "👁️", "💀", "🚀"]
    badge_str = "".join([f"<span style='font-size: 22px; margin: 0 3px;'>{b if st.session_state.aura > (i*300) else '🔒'}</span>" for i, b in enumerate(badges)])
    st.markdown(f"<div>{badge_str}</div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)
with c2:
    st.markdown("<div class='dashboard-card' style='height: 120px;'>", unsafe_allow_html=True)
    st.write("**⭐ RANK PROGRESS**")
    st.progress(prog)
    st.caption(f"{int(prog*100)}% to Legend Status")
    st.markdown("</div>", unsafe_allow_html=True)

# Role Unlock
if st.session_state.aura >= 100 and st.session_state.user_role == "Unclassed":
    st.markdown("<div class='dashboard-card' style='border: 2px solid #ff4b4b;'>", unsafe_allow_html=True)
    st.subheader("⚠️ UNLOCKED: CHOOSE YOUR PLAYER CLASS")
    b1, b2, b3 = st.columns(3)
    if b1.button("🧠 Tactical Mastermind"): st.session_state.user_role = "Tactician"; st.rerun()
    if b2.button("💀 Chaos Agent"): st.session_state.user_role = "Chaos"; st.rerun()
    if b3.button("📣 Hype God"): st.session_state.user_role = "Hype"; st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

st.markdown("---")

# --- 6. GAME FEATURES TABS ---
tabs = st.tabs(["🎯 THE ORACLE", "👁️ VISION UMPIRE", "💀 SLEDGE VAULT", "🕵️ STAR SCOUT", "🔥 HYPE RADAR"])

with tabs[0]: # THE ORACLE
    st.markdown("<div class='dashboard-card'>", unsafe_allow_html=True)
    st.subheader("🎯 The Oracle: Predict the Script")
    col_l, col_r = st.columns(2)
    with col_l:
        market = st.selectbox("Predict:", ["Next Over Runs", "Next Wicket", "Match Result"])
        guess = st.text_input("Your Guess:", placeholder="e.g. 10 runs")
        if st.button("LOCK PREDICTION 🔒"):
            st.session_state.predictions.append({"m": market, "g": guess})
            add_aura(100, "Future Predicted")
    with col_r:
        if st.session_state.predictions:
            if st.button("JUDGE RESULTS 🧐"):
                with st.spinner("Checking live 2026 data..."):
                    p = st.session_state.predictions[-1]
                    res = model.generate_content(f"In KKR vs RCB (KKR 86/2), user guessed '{p['g']}' for '{p['m']}'. Was it right? Be a savage judge.")
                    st.info(res.text); add_aura(150, "Accuracy Bonus")
        else: st.caption("No predictions pending.")
    st.markdown("</div>", unsafe_allow_html=True)

with tabs[1]: # VISION UMPIRE
    st.markdown("<div class='dashboard-card'>", unsafe_allow_html=True)
    img_f = st.camera_input("Scan Live Scene")
    if img_f:
        img = Image.open(img_f)
        with st.spinner("Scanning field..."):
            res = model.generate_content(["Quick tactical roast of this match image:", img])
            st.write(res.text); add_aura(150, "Visual Data Analyzed")
    st.markdown("</div>", unsafe_allow_html=True)

with tabs[2]: # SLEDGE VAULT
    st.markdown("<div class='dashboard-card'>", unsafe_allow_html=True)
    st.subheader("💀 The Sledge Vault")
    st.write("Gemini rates your banter. High scores = High Aura.")
    roast_input = st.text_area("Draft your roast:", placeholder="Type something savage...")
    if st.button("JUDGE BANTER"):
        with st.spinner("Roast Referee is thinking..."):
            res = model.generate_content(f"Rate this cricket roast 1-100 and explain why: {roast_input}")
            st.write(res.text); add_aura(75, "Banter Skill")
    st.markdown("</div>", unsafe_allow_html=True)

with tabs[3]: # STAR SCOUT
    st.markdown("<div class='dashboard-card'>", unsafe_allow_html=True)
    st.subheader("🕵️ Star Player Scout")
    st.write("Scout a player for a 20% multiplier on all Aura earned!")
    player = st.selectbox("Select Star Player:", ["Virat Kohli", "Andre Russell", "Shreyas Iyer", "Mohammed Siraj"])
    if st.button("START SCOUTING"):
        st.session_state.scouted_player = player
        st.success(f"Now following {player}. Multiplier Active! 🚀")
    st.markdown("</div>", unsafe_allow_html=True)

with tabs[4]: # HYPE RADAR
    st.markdown("<div class='dashboard-card'>", unsafe_allow_html=True)
    energy = st.slider("Stadium Decibels", 0, 120, 60)
    if energy > 100:
        st.snow()
        if st.button("CLAIM ENERGY"): add_aura(energy // 2, "Crowd Hype")
    st.markdown("</div>", unsafe_allow_html=True)