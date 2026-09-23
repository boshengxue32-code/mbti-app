import json
import os
from openai import OpenAI
import streamlit as st
import streamlit.components.v1 as components

# ==========================================
# 1. Page Configuration & Adaptive Styling
# ==========================================
st.set_page_config(
    page_title="Cosmic MBTI Sync & Alignment",
    page_icon="✨",
    layout="centered",
)

st.markdown(
    """
    <style>
    /* 适配深色/浅色模式文字颜色 */
    .stRadio p, .stRadio div, div[role="radiogroup"] label p, div[role="radiogroup"] span {
        color: #1f2937 !important;
        font-weight: 600 !important;
        font-size: 15px !important;
        opacity: 1 !important;
    }

    @media (prefers-color-scheme: dark) {
        .stRadio p, .stRadio div, div[role="radiogroup"] label p, div[role="radiogroup"] span {
            color: #FFFFFF !important;
        }
    }

    [data-theme="dark"] .stRadio p, 
    [data-theme="dark"] div[role="radiogroup"] label p {
        color: #FFFFFF !important;
    }

    /* 渐变按钮样式 */
    .stButton>button {
        background: linear-gradient(135deg, #6366f1 0%, #a855f7 50%, #ec4899 100%);
        color: #FFFFFF !important;
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
    </style>
""",
    unsafe_allow_html=True,
)

# ==========================================
# 2. English Questions Database
# ==========================================
STAGE1_QUESTIONS = [
    {
        "q": "1. After attending a large social gathering, you usually feel:",
        "a": "Energized and ready for more (E)",
        "b": "Drained and in need of solo time (I)",
        "dim": "EI",
    },
    {
        "q": "2. When making important decisions, you tend to rely more on:",
        "a": "Logical analysis and objective facts (T)",
        "b": "Personal values and feelings of others (F)",
        "dim": "TF",
    },
    {
        "q": "3. When planning your weekend, you prefer to:",
        "a": "Schedule activities in advance and stick to them (J)",
        "b": "Keep options open and go with the flow (P)",
        "dim": "JP",
    },
    {
        "q": "4. When learning something new, you are more drawn to:",
        "a": "Practical applications and concrete details (S)",
        "b": "Theoretical frameworks and abstract concepts (N)",
        "dim": "SN",
    },
    {
        "q": "5. In conversations, you usually prefer to:",
        "a": "Think out loud and respond quickly (E)",
        "b": "Reflect carefully before sharing your thoughts (I)",
        "dim": "EI",
    },
    {
        "q": (
            "6. When a friend comes to you with a problem, your first instinct"
            " is to:"
        ),
        "a": "Analyze the cause and offer practical solutions (T)",
        "b": "Show empathy and offer emotional support (F)",
        "dim": "TF",
    },
    {
        "q": "7. Your living space or desk is usually:",
        "a": "Organized, with everything in its place (J)",
        "b": "Relaxed and somewhat cluttered (P)",
        "dim": "JP",
    },
    {
        "q": "8. How do you view the future?",
        "a": "Grounded in realistic, present-day facts (S)",
        "b": "Filled with endless possibilities and ideas (N)",
        "dim": "SN",
    },
    {
        "q": "9. In group projects, you tend to take on the role of:",
        "a": "An active speaker driving the discussion (E)",
        "b": "A quiet thinker focused on execution (I)",
        "dim": "EI",
    },
    {
        "q": "10. When faced with rules and guidelines:",
        "a": (
            "Follow them objectively to ensure fairness and efficiency (T)"
        ),
        "b": (
            "Consider exceptions based on human elements and circumstances (F)"
        ),
        "dim": "TF",
    },
    {
        "q": "11. Before going on a vacation, you usually:",
        "a": "Create a detailed itinerary and packing list (J)",
        "b": "Pack last minute and explore spontaneously (P)",
        "dim": "JP",
    },
    {
        "q": "12. You trust information more when it comes from:",
        "a": "Direct experience and verified data (S)",
        "b": "Intuitive insights and future trends (N)",
        "dim": "SN",
    },
    {
        "q": "13. Spending time completely alone feels like:",
        "a": "Okay for a short while, but boring after time (E)",
        "b": "An essential way to recharge your mental energy (I)",
        "dim": "EI",
    },
    {
        "q": "14. When evaluating someone's performance, you value:",
        "a": "Fairness, objectivity, and competence (T)",
        "b": "Kindness, empathy, and personal effort (F)",
        "dim": "TF",
    },
    {
        "q": "15. When dealing with an unexpected challenge, you prefer to:",
        "a": "Rely on proven methods and past experience (S)",
        "b": "Brainstorm novel and unconventional approaches (N)",
        "dim": "SN",
    },
]


def build_stage2_questions():
  raw_questions = [
      {
          "q": "In social events, you naturally tend to:",
          "a": "Initiate conversations with new people (E)",
          "b": "Wait for others to approach you (I)",
          "dim": "EI",
      },
      {
          "q": "Your mental energy is primarily derived from:",
          "a": "Interacting with the external world (E)",
          "b": "Reflecting quietly in your inner world (I)",
          "dim": "EI",
      },
      {
          "q": "When processing thoughts, you usually:",
          "a": "Speak as you think and discuss with others (E)",
          "b": "Formulate ideas fully before speaking (I)",
          "dim": "EI",
      },
      {
          "q": "In group settings, you typically feel:",
          "a": "Engaged, motivated, and highly interactive (E)",
          "b": "Observant, cautious, and selective (I)",
          "dim": "EI",
      },
      {
          "q": "After a long and busy week, your ideal recovery is:",
          "a": "Hanging out with a lively group of friends (E)",
          "b": "Staying home alone with a cozy activity (I)",
          "dim": "EI",
      },
      {
          "q": "When starting a new project, you prefer to:",
          "a": "Brainstorm out loud with a team (E)",
          "b": "Research and outline on your own first (I)",
          "dim": "EI",
      },
      {
          "q": "How do you feel about being the center of attention?",
          "a": "Comfortable and energized by it (E)",
          "b": "Uncomfortable or preferred to be avoided (I)",
          "dim": "EI",
      },
      {
          "q": "Your communication style is generally:",
          "a": "Expressive, fast-paced, and broad (E)",
          "b": "Reserved, deep, and focused (I)",
          "dim": "EI",
      },
      {
          "q": "When facing a crisis, you first tend to:",
          "a": "Reach out to others for immediate action (E)",
          "b": "Pause silently to assess the situation (I)",
          "dim": "EI",
      },
      {
          "q": "When meeting distant acquaintances, you usually:",
          "a": "Eagerly make small talk to keep things active (E)",
          "b": "Nod politely and stick to necessary exchanges (I)",
          "dim": "EI",
      },
      {
          "q": "When processing complex information, you focus on:",
          "a": "Specific facts, data, and present reality (S)",
          "b": "Underlying patterns and future possibilities (N)",
          "dim": "SN",
      },
      {
          "q": "When describing an event, you prefer to:",
          "a": "Stick to chronological details and facts (S)",
          "b": "Use metaphors and convey the overall impression (N)",
          "dim": "SN",
      },
      {
          "q": "When encountering something new, your first reaction is:",
          "a": "How can this be practically used? (S)",
          "b": "What potential options does this open up? (N)",
          "dim": "SN",
      },
      {
          "q": "You trust information more when it comes from:",
          "a": "Direct sensory experience and proven history (S)",
          "b": "Intuitive hunches and logical theories (N)",
          "dim": "SN",
      },
      {
          "q": "You are naturally more attracted to:",
          "a": "Concrete facts and hands-on execution (S)",
          "b": "Abstract theories and imaginative concepts (N)",
          "dim": "SN",
      },
      {
          "q": "When reading a book or watching a movie, you prefer:",
          "a": "Clear storylines with realistic scenarios (S)",
          "b": "Symbolic plots with room for interpretation (N)",
          "dim": "SN",
      },
      {
          "q": "People often describe you as:",
          "a": "Grounded, sensible, and realistic (S)",
          "b": "Creative, visionary, and unconventional (N)",
          "dim": "SN",
      },
      {
          "q": "When solving a problem, you prefer to use:",
          "a": "Standard operating procedures that work (S)",
          "b": "Novel and innovative strategies (N)",
          "dim": "SN",
      },
      {
          "q": "When learning a new subject, you like to start with:",
          "a": "Step-by-step examples and concrete facts (S)",
          "b": "Big-picture concepts and overall architecture (N)",
          "dim": "SN",
      },
      {
          "q": "In daily conversations, you tend to talk more about:",
          "a": "What actually happened and practical matters (S)",
          "b": "Ideas, meanings, and future visions (N)",
          "dim": "SN",
      },
      {
          "q": "During disagreements, you prioritize:",
          "a": "Truth, principles, and logical consistency (T)",
          "b": "Harmony, empathy, and mutual understanding (F)",
          "dim": "TF",
      },
      {
          "q": "When evaluating a proposed idea, you look at:",
          "a": "Efficiency, feasibility, and objective logic (T)",
          "b": "Its human impact and team morale (F)",
          "dim": "TF",
      },
      {
          "q": "When expressing an opinion, you tend to:",
          "a": "Speak candidly, directly, and objectively (T)",
          "b": "Choose words carefully to protect feelings (F)",
          "dim": "TF",
      },
      {
          "q": "When critique is necessary, you aim to be:",
          "a": "Truthful and constructive, even if harsh (T)",
          "b": "Encouraging and gentle, preserving relationships (F)",
          "dim": "TF",
      },
      {
          "q": "When making difficult team decisions, you rely on:",
          "a": "Impartial rules and metrics (T)",
          "b": "Individual circumstances and personal needs (F)",
          "dim": "TF",
      },
      {
          "q": "What bothers you more in a debate?",
          "a": "Illogical arguments and fallacies (T)",
          "b": "Insensitive remarks and harsh tones (F)",
          "dim": "TF",
      },
      {
          "q": "When a colleague struggles, your instinct is to:",
          "a": "Troubleshoot their practical problem (T)",
          "b": "Offer emotional comfort and validation (F)",
          "dim": "TF",
      },
      {
          "q": "You feel most accomplished when you achieve:",
          "a": "A high-quality, objective result (T)",
          "b": "Deep personal connection or appreciation (F)",
          "dim": "TF",
      },
      {
          "q": "In a leadership role, you focus primarily on:",
          "a": "Task optimization and performance metrics (T)",
          "b": "Team cohesion and individual growth (F)",
          "dim": "TF",
      },
      {
          "q": "When judging an action, you value more:",
          "a": "Fairness and consistency (T)",
          "b": "Compassion and mercy (F)",
          "dim": "TF",
      },
      {
          "q": "When working toward long-term goals, you like to:",
          "a": "Set clear benchmarks and follow a structured plan (J)",
          "b": "Adapt as you go and explore flexible pathways (P)",
          "dim": "JP",
      },
      {
          "q": "As deadlines approach, you tend to:",
          "a": "Finish early to avoid stress (J)",
          "b": "Feel inspired and work best under pressure (P)",
          "dim": "JP",
      },
      {
          "q": "Your work and living space is usually:",
          "a": "Structured, organized, and tidy (J)",
          "b": "Spontaneous, adaptable, and flexible (P)",
          "dim": "JP",
      },
      {
          "q": "How do you feel about sudden plan changes?",
          "a": "Disrupted and frustrated (J)",
          "b": "Excited and adaptable (P)",
          "dim": "JP",
      },
      {
          "q": "When starting your workday, you prefer to:",
          "a": "Follow a predetermined to-do list (J)",
          "b": "Address whatever feels most pressing or interesting (P)",
          "dim": "JP",
      },
      {
          "q": "Decisions and choices give you a sense of:",
          "a": "Relief and closure once settled (J)",
          "b": "Constraint; you like keeping options open (P)",
          "dim": "JP",
      },
      {
          "q": "When packing for a trip, you usually:",
          "a": "Categorize items days in advance (J)",
          "b": "Throw things in the bag right before leaving (P)",
          "dim": "JP",
      },
      {
          "q": "In your daily life, you prefer to have:",
          "a": "Clear routines and predictable schedules (J)",
          "b": "Freedom to act spontaneously without fixed schedules (P)",
          "dim": "JP",
      },
      {
          "q": "When given a long-term project, you prefer to:",
          "a": "Divide it into micro-tasks and complete them steadily (J)",
          "b": "Explore broad ideas first and do bursts of intense work (P)",
          "dim": "JP",
      },
      {
          "q": "You feel most comfortable when things are:",
          "a": "Settled, organized, and decided (J)",
          "b": "Open-ended, flexible, and subject to change (P)",
          "dim": "JP",
      },
  ]

  questions = []
  for idx, item in enumerate(raw_questions, start=1):
    questions.append({
        "q": f"Q{idx}. {item['q']}",
        "a": item["a"],
        "b": item["b"],
        "dim": item["dim"],
    })
  return questions


STAGE2_QUESTIONS = build_stage2_questions()
# ==========================================
# 3. Helper Functions with Robust Model Fallback
# ==========================================
def calculate_mbti(answers, questions):
  scores = {"E": 0, "I": 0, "S": 0, "N": 0, "T": 0, "F": 0, "J": 0, "P": 0}
  for idx, ans in answers.items():
    if ans is None:
      continue
    q_info = questions[idx]
    dim = q_info["dim"]
    if ans == "A":
      scores[dim[0]] += 1
    elif ans == "B":
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
      0: "Metal 🪙",
      1: "Metal 🪙",
      2: "Water 💧",
      3: "Water 💧",
      4: "Wood 🌿",
      5: "Wood 🌿",
      6: "Fire 💥",
      7: "Fire 💥",
      8: "Earth 🪐",
      9: "Earth 🪐",
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

  # 更新为 Groq 当前可用且最稳定的模型列表 (优先级从高到低)
  candidate_models = [
      "llama-3.3-70b-versatile",  # 旗舰主力模型 (推荐)
      "llama-3.1-8b-instant",  # 轻量高频模型
      "qwen-2.5-32b",  # 高性能通用备用模型
      "deepseek-r1-distill-llama-70b",  # 推理能力强力的备用模型
  ]

  errors = []
  for model_name in candidate_models:
    try:
      response = client.chat.completions.create(
          model=model_name,
          messages=[{"role": "user", "content": prompt}],
          response_format={"type": "json_object"},
          temperature=0.7,
      )
      return json.loads(response.choices[0].message.content)
    except Exception as e:
      errors.append(f"{model_name}: {str(e)}")
      continue

  raise RuntimeError(
      "All candidate models failed. Details:\n" + "\n".join(errors)
  )


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
  st.caption(
      "Answer according to your intuition to estimate your initial MBTI type."
  )
  st.progress(0.2)

  with st.form("stage1_form"):
    for i, q_data in enumerate(STAGE1_QUESTIONS):
      st.write(f"**{q_data['q']}**")
      st.session_state.stage1_answers[i] = st.radio(
          label=f"Q{i+1}",
          options=["A", "B"],
          index=None,
          format_func=lambda x, q=q_data: q["a"] if x == "A" else q["b"],
          key=f"s1_q_{i}",
          label_visibility="collapsed",
      )
      st.write("")

    submit_s1 = st.form_submit_button("Submit Fast Assessment 🚀")
    if submit_s1:
      if None in st.session_state.stage1_answers.values() or len(
          st.session_state.stage1_answers
      ) < len(STAGE1_QUESTIONS):
        st.warning("Please answer all questions before submitting!")
      else:
        st.session_state.prelim_mbti = calculate_mbti(
            st.session_state.stage1_answers, STAGE1_QUESTIONS
        )
        st.session_state.step = 2
        st.rerun()

# ------------------------------------------
# Stage 2: 40-Question Deep Assessment
# ------------------------------------------
elif st.session_state.step == 2:
  st.subheader("Stage 2: 40-Question Deep Calibration")
  st.info(
      "Your preliminary MBTI estimation from Stage 1:"
      f" **{st.session_state.prelim_mbti}**"
  )
  st.write(
      "Please complete these 40 detailed questions to recalibrate and confirm"
      " your final personality profile."
  )
  st.progress(0.6)

  with st.form("stage2_form"):
    for i, q_data in enumerate(STAGE2_QUESTIONS):
      st.write(f"**{q_data['q']}**")
      st.session_state.stage2_answers[i] = st.radio(
          label=f"S2_Q{i+1}",
          options=["A", "B"],
          index=None,
          format_func=lambda x, q=q_data: q["a"] if x == "A" else q["b"],
          key=f"s2_q_{i}",
          label_visibility="collapsed",
      )
      st.write("")

    submit_s2 = st.form_submit_button("Submit Deep Calibration 🧬")
    if submit_s2:
      if None in st.session_state.stage2_answers.values() or len(
          st.session_state.stage2_answers
      ) < len(STAGE2_QUESTIONS):
        st.warning("Please answer all questions before submitting!")
      else:
        st.session_state.final_mbti = calculate_mbti(
            st.session_state.stage2_answers, STAGE2_QUESTIONS
        )
        st.session_state.step = 3
        st.rerun()

# ------------------------------------------
# Stage 3: Birth Year + Eastern Element Card
# ------------------------------------------
elif st.session_state.step == 3:
  st.subheader("Stage 3: Energy Alignment & Blueprint Generation")
  st.success(
      "🎉 Calibration Complete! Your final confirmed MBTI is:"
      f" **{st.session_state.final_mbti}**"
  )
  st.progress(1.0)

  birth_year = st.number_input(
      "Select your birth year (To calculate your Eastern Element):",
      min_value=1950,
      max_value=2026,
      value=2000,
  )
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


