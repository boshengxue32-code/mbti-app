import streamlit as st
import streamlit.components.v1 as components
from openai import OpenAI
import os
import json

# ==========================================
# 1. Page Configuration & Styling
# ==========================================
st.set_page_config(
page_title="Cosmic MBTI Sync & Alignment",
page_icon="✨",
layout="centered"
)

st.markdown("""
<style>
.main {
background: #090A0F;
color: #F0F0F2;
}
.stButton>button {
background: linear-gradient(135deg, #6366f1 0%, #a855f7 50%, #ec4899 100%);
color: #FFFFFF;
border: none;
border-radius: 12px;
padding: 12px 24px;
font-weight: 700;
letter-spacing: 0.5px;
box-shadow: 0 4px 20px rgba(168, 85, 247, 0.4);
transition: all 0.3s ease;
width: 100%;
}
.stButton>button:hover {
transform: translateY(-2px);
box-shadow: 0 6px 30px rgba(168, 85, 247, 0.6);
}
.stRadio label {
color: #e2e8f0 !important;
}
</style>
""", unsafe_allow_html=True)

# ==========================================
# 2. English Questions Database
# ==========================================
STAGE1_QUESTIONS = [
{"q": "1. After attending a large social gathering, you usually feel:", "a": "Energized and ready for more (E)", "b": "Drained and in need of solo time (I)", "dim": "EI"},
{"q": "2. When making important decisions, you tend to rely more on:", "a": "Logical analysis and objective facts (T)", "b": "Personal values and feelings of others (F)", "dim": "TF"},
{"q": "3. When planning your weekend, you prefer to:", "a": "Schedule activities in advance and stick to them (J)", "b": "Keep options open and go with the flow (P)", "dim": "JP"},
{"q": "4. When learning something new, you are more drawn to:", "a": "Practical applications and concrete details (S)", "b": "Theoretical frameworks and abstract concepts (N)", "dim": "SN"},
{"q": "5. In conversations, you usually prefer to:", "a": "Think out loud and respond quickly (E)", "b": "Reflect carefully before sharing your thoughts (I)", "dim": "EI"},
{"q": "6. When a friend comes to you with a problem, your first instinct is to:", "a": "Analyze the cause and offer practical solutions (T)", "b": "Show empathy and offer emotional support (F)", "dim": "TF"},
{"q": "7. Your living space or desk is usually:", "a": "Organized, with everything in its place (J)", "b": "Relaxed and somewhat cluttered (P)", "dim": "JP"},
{"q": "8. How do you view the future?", "a": "Grounded in realistic, present-day facts (S)", "b": "Filled with endless possibilities and ideas (N)", "dim": "SN"},
{"q": "9. In group projects, you tend to take on the role of:", "a": "An active speaker driving the discussion (E)", "b": "A quiet thinker focused on execution (I)", "dim": "EI"},
{"q": "10. When faced with rules and guidelines:", "a": "Follow them objectively to ensure fairness and efficiency (T)", "b": "Consider exceptions based on human elements and circumstances (F)", "dim": "TF"},
{"q": "11. Before going on a vacation, you usually:", "a": "Create a detailed itinerary and packing list (J)", "b": "Pack last minute and explore spontaneously (P)", "dim": "JP"},
{"q": "12. You trust information more when it comes from:", "a": "Direct experience and verified data (S)", "b": "Intuitive insights and future trends (N)", "dim": "SN"},
{"q": "13. Spending time completely alone feels like:", "a": "Okay for a short while, but boring after time (E)", "b": "An essential way to recharge your mental energy (I)", "dim": "EI"},
{"q": "14. When evaluating someone's performance, you value:", "a": "Fairness, objectivity, and competence (T)", "b": "Kindness, empathy, and personal effort (F)", "dim": "TF"},
{"q": "15. When dealing with an unexpected challenge, you prefer to:", "a": "Rely on proven methods and past experience (S)", "b": "Brainstorm novel and unconventional approaches (N)", "dim": "SN"}
]

def build_stage2_questions():
dims = ["EI", "SN", "TF", "JP"]
questions = []
texts = [
("In social events, you naturally tend to", "Initiate conversations with new people", "Wait for others to approach you"),
("When processing complex information, you focus on", "Specific facts and present reality", "Underlying patterns and future possibilities"),
("During disagreements, you prioritize", "Truth, principles, and logical consistency", "Harmony, empathy, and mutual understanding"),
("When working toward long-term goals, you like to", "Set clear benchmarks and follow a structured plan", "Adapt as you go and explore flexible pathways"),
("Your mental energy is primarily derived from", "Interacting with the external world", "Reflecting quietly in your inner world"),
("When describing an event, you prefer to", "Stick to chronological details and facts", "Use metaphors and convey the overall impression"),
("When evaluating a proposed idea, you look at", "Efficiency, feasibility, and objective logic", "Its human impact and team morale"),
("As deadlines approach, you tend to", "Finish early to avoid stress", "Feel inspired and work best under pressure"),
("When expressing an opinion, you tend to", "Speak candidly and directly", "Choose your words carefully to protect feelings"),
("When encountering something new, your first reaction is", "How can this be practically used?", "What potential options does this open up?")
]
idx = 1
for t in texts:
for dim in dims:
questions.append({
"q": f"Q{idx}. {t[0]}:",
"a": f"{t[1]} ({dim[0]})",
"b": f"{t[2]} ({dim[1]})",
"dim": dim
})
idx += 1
return questions

STAGE2_QUESTIONS = build_stage2_questions()

# ==========================================
# 3. Helper Functions
# ==========================================
def calculate_mbti(answers, questions):
scores = {"E": 0, "I": 0, "S": 0, "N": 0, "T": 0, "F": 0, "J": 0, "P": 0}
for idx, ans in answers.items():
q_info = questions[idx]
dim = q_info["dim"]
if ans == "A":
scores[dim[0]] += 1
else:
scores[dim[1]] += 1

mbti = ""
mbti += "E" if scores["E"] >= scores["I"] else "I"
mbti += "S" if scores["S"] >= scores["N"] else "N"
mbti += "T" if scores["T"] >= scores["F"] else "F"
mbti += "J" if scores["J"] >= scores["P"] else "P"
return mbti

def get_eastern_element(year):
last_digit = year % 10
element_map = {
0: "Metal 🪙", 1: "Metal 🪙",
2: "Water 💧", 3: "Water 💧",
4: "Wood 🌿", 5: "Wood 🌿",
6: "Fire 💥", 7: "Fire 💥",
8: "Earth 🪐", 9: "Earth 🪐"
}
return element_map.get(last_digit, "Cosmic Energy ✨")

def generate_ai_card(mbti, element):
prompt = f"""
You are a modern intuitive counselor combining Western MBTI psychology with Eastern Five-Element Archetypes.
User's Profile:
- Confirmed MBTI: {mbti}
- Eastern Element: {element}

Generate a highly aesthetic, empowering "Energy Blueprint" report.
Avoid traditional fortune-telling terms. Use modern spiritual/psychological terms like "Cosmic Weather", "Inner Alignment", "Vibe Check".

MUST respond ONLY with valid JSON in this exact structure:
{{
"archetype_title": "Short cool title (e.g. The Intuitive Water Architect)",
"daily_vibe": "A concise 2-sentence psychological insight about how their {mbti} interacts with {element}.",
"actionable_dos": "1 specific empowering advice for today.",
"actionable_donts": "1 thing to avoid today.",
"power_quote": "A 1-line catchy quote for Instagram story."
}}
"""
api_key = st.secrets.get("GROQ_API_KEY") or os.getenv("GROQ_API_KEY")
if not api_key:
raise ValueError("GROQ_API_KEY not found in Streamlit Secrets.")

client = OpenAI(api_key=api_key, base_url="https://api.groq.com/openai/v1")
response = client.chat.completions.create(
model="llama-3.3-70b-versatile",
messages=[{"role": "user", "content": prompt}],
response_format={"type": "json_object"}
)
return json.loads(response.choices[0].message.content)

# ==========================================
# 4. Main App Logic & Multi-Stage State
# ==========================================
if "step" not in st.session_state:
st.session_state.step = 1
if "stage1_answers" not in st.session_state:
st.session_state.stage1_answers = {}
if "stage2_answers" not in st.session_state:
st.session_state.stage2_answers = {}
if "prelim_mbti" not in st.session_state:
st.session_state.prelim_mbti = ""
if "final_mbti" not in st.session_state:
st.session_state.final_mbti = ""

st.title("✨ COSMIC MBTI & VIBE SYNC")

# ------------------------------------------
# Stage 1: 15-Question Fast Assessment
# ------------------------------------------
if st.session_state.step == 1:
st.subheader("Stage 1: 15-Question Fast Screening")
st.caption("Answer according to your intuition to estimate your initial MBTI type.")
st.progress(0.2)

with st.form("stage1_form"):
for i, q_data in enumerate(STAGE1_QUESTIONS):
st.write(q_data["q"])
st.session_state.stage1_answers[i] = st.radio(
label=f"Q{i+1}",
options=["A", "B"],
format_func=lambda x, q=q_data: q["a"] if x == "A" else q["b"],
key=f"s1_q_{i}",
label_visibility="collapsed"
)
st.write("")

submit_s1 = st.form_submit_button("Submit Fast Assessment 🚀")
if submit_s1:
st.session_state.prelim_mbti = calculate_mbti(st.session_state.stage1_answers, STAGE1_QUESTIONS)
st.session_state.step = 2
st.rerun()

# ------------------------------------------
# Stage 2: 40-Question Deep Assessment
# ------------------------------------------
elif st.session_state.step == 2:
st.subheader("Stage 2: 40-Question Deep Calibration")
st.info(f"Your preliminary MBTI estimation from Stage 1: **{st.session_state.prelim_mbti}**")
st.write("Please complete these 40 detailed questions to recalibrate and confirm your final personality profile.")
st.progress(0.6)

with st.form("stage2_form"):
for i, q_data in enumerate(STAGE2_QUESTIONS):
st.write(q_data["q"])
st.session_state.stage2_answers[i] = st.radio(
label=f"S2_Q{i+1}",
options=["A", "B"],
format_func=lambda x, q=q_data: q["a"] if x == "A" else q["b"],
key=f"s2_q_{i}",
label_visibility="collapsed"
)
st.write("")

submit_s2 = st.form_submit_button("Submit Deep Calibration 🧬")
if submit_s2:
st.session_state.final_mbti = calculate_mbti(st.session_state.stage2_answers, STAGE2_QUESTIONS)
st.session_state.step = 3
st.rerun()

# ------------------------------------------
# Stage 3: Birth Year + Eastern Element Card
# ------------------------------------------
elif st.session_state.step == 3:
st.subheader("Stage 3: Energy Alignment & Blueprint Generation")
st.success(f"🎉 Calibration Complete! Your final confirmed MBTI is: **{st.session_state.final_mbti}**")
st.progress(1.0)

birth_year = st.number_input("Select your birth year (To calculate your Eastern Element):", min_value=1950, max_value=2026, value=2000)
user_element = get_eastern_element(birth_year)
st.write(f"Your Eastern Archetypal Element: **{user_element}**")

col_gen, col_reset = st.columns([3, 1])
with col_gen:
gen_btn = st.button("Generate Cosmic Energy Blueprint ✨")
with col_reset:
if st.button("Restart 🔄"):
st.session_state.step = 1
st.rerun()

if gen_btn:
with st.spinner("Synthesizing MBTI and Eastern Archetypes..."):
try:
data = generate_ai_card(st.session_state.final_mbti, user_element)

card_html = f"""
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;600;800&display=swap');
* {{ box-sizing: border-box; }}
body {{
margin: 0;
padding: 8px;
background: transparent;
font-family: 'Plus Jakarta Sans', sans-serif;
}}
.card {{
background: linear-gradient(135deg, #13151f 0%, #1e1b4b 50%, #311042 100%);
border: 1px solid rgba(255, 255, 255, 0.15);
border-radius: 20px;
padding: 24px;
box-shadow: 0 10px 30px rgba(0,0,0,0.5);
color: #FFFFFF;
}}
.header {{
display: flex;
justify-content: space-between;
align-items: center;
margin-bottom: 16px;
}}
.tag {{
font-size: 11px;
font-weight: 800;
letter-spacing: 1.5px;
color: #a855f7;
text-transform: uppercase;
}}
.badge {{
background: rgba(255, 255, 255, 0.1);
border: 1px solid rgba(255, 255, 255, 0.2);
padding: 4px 10px;
border-radius: 12px;
font-size: 12px;
font-weight: 600;
color: #e2e8f0;
}}
.title {{
font-size: 22px;
font-weight: 800;
background: linear-gradient(90deg, #ffffff, #c084fc);
-webkit-background-clip: text;
-webkit-text-fill-color: transparent;
margin: 0 0 14px 0;
}}
.vibe {{
font-size: 14px;
line-height: 1.5;
color: #cbd5e1;
background: rgba(0, 0, 0, 0.25);
padding: 14px;
border-radius: 10px;
border-left: 3px solid #a855f7;
margin-bottom: 16px;
}}
.grid {{
display: grid;
grid-template-columns: 1fr 1fr;
gap: 12px;
margin-bottom: 16px;
}}
.box {{
padding: 12px;
border-radius: 10px;
font-size: 13px;
line-height: 1.4;
}}
.do-box {{
background: rgba(34, 197, 94, 0.12);
border: 1px solid rgba(34, 197, 94, 0.25);
}}
.dont-box {{
background: rgba(239, 68, 68, 0.12);
border: 1px solid rgba(239, 68, 68, 0.25);
}}
.box-title {{
font-weight: 800;
margin-bottom: 4px;
display: block;
}}
.do-title {{ color: #4ade80; }}
.dont-title {{ color: #f87171; }}
.box-text {{ color: #f1f5f9; }}
.quote {{
text-align: center;
font-size: 14px;
font-style: italic;
font-weight: 600;
color: #f472b6;
border-top: 1px dashed rgba(255,255,255,0.15);
padding-top: 14px;
margin: 0;
}}
</style>
</head>
<body>
<div class="card">
<div class="header">
<span class="tag">Cosmic Energy Blueprint</span>
<span class="badge">{st.session_state.final_mbti} × {user_element}</span>
</div>
<div class="title">{data.get('archetype_title', 'Energy Sync')}</div>
<div class="vibe">{data.get('daily_vibe', '')}</div>
<div class="grid">
<div class="box do-box">
<span class="box-title do-title">✨ DO</span>
<span class="box-text">{data.get('actionable_dos', '')}</span>
</div>
<div class="box dont-box">
<span class="box-title dont-title">🚫 DON'T</span>
<span class="box-text">{data.get('actionable_donts', '')}</span>
</div>
</div>
<div class="quote">"{data.get('power_quote', '')}"</div>
</div>
</body>
</html>
"""

components.html(card_html, height=460, scrolling=False)
except Exception as e:
st.error(f"Failed to generate card: {str(e)}")

