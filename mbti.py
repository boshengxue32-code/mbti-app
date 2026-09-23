import json
import os
import streamlit as st
import streamlit.components.v1 as components
from openai import OpenAI

# Set Page Config
st.set_page_config(
    page_title="Cosmic MBTI & Vibe Sync", page_icon="✨", layout="centered"
)

# ==========================================
# 1. DATA DEFINITIONS (Questions)
# ==========================================
STAGE1_QUESTIONS = [
    {
        "q": "At a crowded party, you usually:",
        "a": "Enjoy talking with many people",
        "b": "Stay with close friends or leave early",
        "dim": "EI",
    },
    {
        "q": "When processing information, you lean toward:",
        "a": "Concrete facts and present details",
        "b": "Patterns, future possibilities, and big picture",
        "dim": "SN",
    },
    {
        "q": "When making tough decisions, you prioritize:",
        "a": "Objective logic and consistency",
        "b": "Personal values and impact on people",
        "dim": "TF",
    },
    {
        "q": "In your daily life, you prefer:",
        "a": "Having a clear plan and schedule",
        "b": "Keeping options open and being spontaneous",
        "dim": "JP",
    },
    {
        "q": "After a stressful week, you regain energy by:",
        "a": "Going out with friends or attending events",
        "b": "Spending quiet time alone",
        "dim": "EI",
    },
    {
        "q": "You trust information more if it is:",
        "a": "Proven by past experience and practical evidence",
        "b": "Inspiring and open to interpretation",
        "dim": "SN",
    },
    {
        "q": "People often describe you as more:",
        "a": "Analytical and direct",
        "b": "Empathetic and compassionate",
        "dim": "TF",
    },
    {
        "q": "When going on vacation, you usually:",
        "a": "Book itineraries and reservations in advance",
        "b": "Explore freely without a strict agenda",
        "dim": "JP",
    },
    {
        "q": "In group conversations, you usually:",
        "a": "Speak up quickly and share thoughts freely",
        "b": "Listen first and speak when asked",
        "dim": "EI",
    },
    {
        "q": "You are more fascinated by:",
        "a": "How things work in reality today",
        "b": "What could be created in the future",
        "dim": "SN",
    },
    {
        "q": "If a friend is wrong in an argument, you tend to:",
        "a": "Point out the logical flaw directly",
        "b": "Soften your words to protect their feelings",
        "dim": "TF",
    },
    {
        "q": "When working on projects, you feel comfortable when:",
        "a": "Milestones and deadlines are strictly set",
        "b": "Deadlines are flexible as long as progress is made",
        "dim": "JP",
    },
    {
        "q": "When meeting new people, you:",
        "a": "Initiate conversation easily",
        "b": "Wait for them to reach out first",
        "dim": "EI",
    },
    {
        "q": "You pay more attention to:",
        "a": "Specific details and immediate observations",
        "b": "Underlying meanings and symbolic connections",
        "dim": "SN",
    },
    {
        "q": "You consider yourself more driven by:",
        "a": "Head over heart",
        "b": "Heart over head",
        "dim": "TF",
    },
]
STAGE2_QUESTIONS = [
    {
        "q": "In team discussions, you naturally:",
        "a": "Lead the conversation and think aloud",
        "b": "Reflect internally before speaking",
        "dim": "EI",
    },
    {
        "q": "You prefer instructions that are:",
        "a": "Step-by-step and explicit",
        "b": "Conceptual and open-ended",
        "dim": "SN",
    },
    {
        "q": "When giving feedback, you focus on:",
        "a": "Constructive criticism and accuracy",
        "b": "Encouragement and maintaining harmony",
        "dim": "TF",
    },
    {
        "q": "Your workspace is usually:",
        "a": "Organized and structured",
        "b": "Casual and flexible",
        "dim": "JP",
    },
    {
        "q": "Networking events make you feel:",
        "a": "Energized and excited",
        "b": "Drained and eager to leave",
        "dim": "EI",
    },
    {
        "q": "You are more drawn to books/movies about:",
        "a": "Real historical events or true stories",
        "b": "Fantasy, sci-fi, or deep philosophical themes",
        "dim": "SN",
    },
    {
        "q": "You feel most accomplished when you achieve:",
        "a": "An efficient and flawless outcome",
        "b": "A outcome that brings deep joy to others",
        "dim": "TF",
    },
    {
        "q": "Unexpected changes to your daily plan make you:",
        "a": "Annoyed or stressed",
        "b": "Adaptable and excited for something new",
        "dim": "JP",
    },
    {
        "q": "You tend to have:",
        "a": "A wide circle of acquaintances",
        "b": "A few deeply intimate friendships",
        "dim": "EI",
    },
    {
        "q": "When learning something new, you prefer:",
        "a": "Hands-on practice and real examples",
        "b": "Understanding theories and core concepts first",
        "dim": "SN",
    },
    {
        "q": "When resolving conflict, you aim for:",
        "a": "Fairness based on facts",
        "b": "Harmony based on mutual understanding",
        "dim": "TF",
    },
    {
        "q": "To-do lists are something you:",
        "a": "Rely on daily and cross items off rigorously",
        "b": "Make occasionally but rarely stick to strictly",
        "dim": "JP",
    },
    {
        "q": "In a social group, you are often seen as:",
        "a": "The outgoing initiator",
        "b": "The quiet observer",
        "dim": "EI",
    },
    {
        "q": "You focus more on:",
        "a": "What is actually happening right now",
        "b": "What possibilities lie ahead",
        "dim": "SN",
    },
    {
        "q": "When evaluating success, you value:",
        "a": "Measurable results and metrics",
        "b": "Personal growth and human connection",
        "dim": "TF",
    },
    {
        "q": "Your working style is best described as:",
        "a": "Steady pace with early completion",
        "b": "Last-minute burst of energy near deadlines",
        "dim": "JP",
    },
    {
        "q": "You feel comfortable being the center of attention:",
        "a": "Yes, I enjoy it",
        "b": "No, I prefer remaining background",
        "dim": "EI",
    },
    {
        "q": "You tend to trust:",
        "a": "Your past experience",
        "b": "Your gut intuition",
        "dim": "SN",
    },
    {
        "q": "If someone asks for advice, you give:",
        "a": "Practical solutions and actionable steps",
        "b": "Emotional support and active listening",
        "dim": "TF",
    },
    {
        "q": "You prefer your life to feel:",
        "a": "Settled and organized",
        "b": "Flexible and evolving",
        "dim": "JP",
    },
    {
        "q": "After talking to people for hours, you feel:",
        "a": "Supercharged",
        "b": "Exhausted",
        "dim": "EI",
    },
    {
        "q": "You consider yourself more of a:",
        "a": "Realistic practitioner",
        "b": "Visionary dreamer",
        "dim": "SN",
    },
    {
        "q": "You care more about being:",
        "a": "Right and truthful",
        "b": "Kind and considerate",
        "dim": "TF",
    },
    {
        "q": "When starting a project, you prefer to:",
        "a": "Outline the full schedule first",
        "b": "Dive right in and figure it out as you go",
        "dim": "JP",
    },
    {
        "q": "In new environments, you:",
        "a": "Adapt quickly and talk to strangers",
        "b": "Take time to observe before stepping in",
        "dim": "EI",
    },
    {
        "q": "You find metaphor and allegory:",
        "a": "Sometimes impractical or confusing",
        "b": "Engaging and rich in meaning",
        "dim": "SN",
    },
    {
        "q": "When making decisions, you rely more on:",
        "a": "Cold objective analysis",
        "b": "Personal values and ethics",
        "dim": "TF",
    },
    {
        "q": "You prefer tasks with:",
        "a": "Clear boundaries and guidelines",
        "b": "Freedom to define your own approach",
        "dim": "JP",
    },
    {
        "q": "In social gatherings, you usually:",
        "a": "Stay until late and keep social energy up",
        "b": "Leave early to recharge",
        "dim": "EI",
    },
    {
        "q": "You pay attention to:",
        "a": "Specific details and data points",
        "b": "Overall trends and underlying meanings",
        "dim": "SN",
    },
    {
        "q": "You consider yourself more:",
        "a": "Firm-minded and objective",
        "b": "Gentle-hearted and accommodating",
        "dim": "TF",
    },
    {
        "q": "Your ideal weekend is:",
        "a": "Planned out with activities",
        "b": "Completely free-flowing",
        "dim": "JP",
    },
    {
        "q": "When faced with silence in a conversation, you:",
        "a": "Fill it with a new topic",
        "b": "Feel comfortable letting the silence sit",
        "dim": "EI",
    },
    {
        "q": "You prefer to focus on:",
        "a": "Practical realities of today",
        "b": "Future possibilities of tomorrow",
        "dim": "SN",
    },
    {
        "q": "Which quality do you value more in yourself?",
        "a": "Rationality and clarity",
        "b": "Compassion and warmth",
        "dim": "TF",
    },
    {
        "q": "Your workspace or desk is:",
        "a": "Neat and well-arranged",
        "b": "Cluttered but functional for you",
        "dim": "JP",
    },
    {
        "q": "When sharing ideas, you prefer to:",
        "a": "Discuss in a group setting",
        "b": "Write them down or talk one-on-one",
        "dim": "EI",
    },
    {
        "q": "You appreciate art mostly for its:",
        "a": "Craftsmanship, skill, and technique",
        "b": "Emotional resonance, symbolism, and depth",
        "dim": "SN",
    },
    {
        "q": "When helping a friend, you start with:",
        "a": "Logical problem solving",
        "b": "Emotional validation",
        "dim": "TF",
    },
    {
        "q": "You feel better when an event is:",
        "a": "Decided and finalized",
        "b": "Tentative and flexible",
        "dim": "JP",
    },
]
# ==========================================
# 2. HELPER FUNCTIONS
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
  element_explanations = {
      "Metal": "Precision, Clarity & Inner Boundaries",
      "Water": "Flow, Depth & Intuitive Wisdom",
      "Wood": "Growth, Expansion & Creative Vision",
      "Fire": "Passion, Charisma & Expressive Energy",
      "Earth": "Grounding, Stability & Nurturing Strength",
  }

  clean_element = element.split()[0] if " " in element else element
  meaning_tag = element_explanations.get(clean_element, "Cosmic Energy")

  prompt = f"""
    You are a modern intuitive counselor combining Western MBTI psychology with Eastern Five-Element Archetypes.
    User's Profile:
    - Confirmed MBTI: {mbti}
    - Eastern Element: {element} (Core Psychological Vibe: {meaning_tag})

    Generate a highly aesthetic, empowering "Energy Blueprint" report.
    IMPORTANT: Explain what {clean_element} energy represents in modern psychological terms.

    MUST respond ONLY with valid JSON in this exact structure:
    {{
        "archetype_title": "Short cool title (e.g. The Precision Idealist)",
        "daily_vibe": "A concise 2-sentence insight explaining how {clean_element} energy ({meaning_tag}) interacts with their {mbti} cognitive style.",
        "actionable_dos": "1 specific empowering advice for today.",
        "actionable_donts": "1 thing to avoid today.",
        "power_quote": "A 1-line catchy quote for Instagram story."
    }}
    """
  api_key = st.secrets.get("GROQ_API_KEY") or os.getenv("GROQ_API_KEY")
  if not api_key:
    raise ValueError("GROQ_API_KEY not found in Streamlit Secrets.")

  client = OpenAI(api_key=api_key, base_url="https://api.groq.com/openai/v1")

  try:
    available_models_resp = client.models.list()
    available_ids = [m.id for m in available_models_resp.data]
  except Exception as e:
    raise RuntimeError(f"无法获取 Groq 模型列表: {str(e)}")

  if not available_ids:
    raise RuntimeError("当前 Groq 账户下没有可用的模型。")

  errors = []
  for model_name in available_ids:
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

  raise RuntimeError("所有可用模型请求失败:\n" + "\n".join(errors))


def save_subscriber_to_db(email, mbti, element):
  try:
    pass  # 预留用于保存数据库
  except Exception as e:
    print(f"Database save error: {e}")


# ==========================================
# 3. MAIN APP LOGIC
# ==========================================
if "step" not in st.session_state:
  st.session_state.step = 0
if "user_email" not in st.session_state:
  st.session_state.user_email = ""
if "stage1_answers" not in st.session_state:
  st.session_state.stage1_answers = {}
if "stage2_answers" not in st.session_state:
  st.session_state.stage2_answers = {}
if "prelim_mbti" not in st.session_state:
  st.session_state.prelim_mbti = ""
if "final_mbti" not in st.session_state:
  st.session_state.final_mbti = ""

st.title("✨ COSMIC MBTI & VIBE SYNC")

# --- Stage 0: Email Login ---
if st.session_state.step == 0:
  st.subheader("Welcome to Your Cosmic Alignment Assessment")
  st.caption(
      "Enter your email to save your personality profile and begin your 2-stage"
      " cosmic assessment."
  )

  with st.form("login_form"):
    email_input = st.text_input(
        "Enter your Email to start:", placeholder="yourname@example.com"
    )
    submit_login = st.form_submit_button("Start Assessment 🚀")

    if submit_login:
      if "@" in email_input and "." in email_input:
        st.session_state.user_email = email_input.strip()
        st.session_state.step = 1
        st.rerun()
      else:
        st.error("Please enter a valid email address to proceed.")

# --- Stage 1: 15 Questions ---
elif st.session_state.step == 1:
  st.caption(f"Logged in as: `{st.session_state.user_email}`")
  st.subheader("Stage 1: 15-Question Fast Screening")
  st.progress(0.25)

  with st.form("stage1_form_unique"):
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

    submit_s1 = st.form_submit_button("Next Stage 🚀")
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

# --- Stage 2: 40 Questions ---
elif st.session_state.step == 2:
  st.caption(f"Logged in as: `{st.session_state.user_email}`")
  st.subheader("Stage 2: 40-Question Deep Calibration")
  st.info(
      "Preliminary Alignment Result:"
      f" **{st.session_state.prelim_mbti}**"
  )
  st.progress(0.65)

  with st.form("stage2_form_unique"):
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

    submit_s2 = st.form_submit_button("Confirm & Align 🧬")
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

# --- Stage 3: Card Generation ---
elif st.session_state.step == 3:
  st.caption(f"Account: `{st.session_state.user_email}`")
  st.subheader("Stage 3: Energy Alignment")
  st.success(
      "🎉 Calibration Complete! Your confirmed MBTI is:"
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
    gen_btn = st.button("Reveal My Energy Blueprint ✨")
  with col_reset:
    if st.button("Restart 🔄"):
      st.session_state.step = 0
      st.rerun()

  if gen_btn:
    save_subscriber_to_db(
        st.session_state.user_email, st.session_state.final_mbti, user_element
    )

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
                        padding: 4px;
                        background: transparent;
                        font-family: 'Plus Jakarta Sans', sans-serif;
                    }}
                    .card {{
                        background: linear-gradient(135deg, #13151f 0%, #1e1b4b 50%, #311042 100%);
                        border: 1px solid rgba(255, 255, 255, 0.15);
                        border-radius: 20px;
                        padding: 20px;
                        box-shadow: 0 10px 30px rgba(0,0,0,0.5);
                        color: #FFFFFF;
                    }}
                    .header {{
                        display: flex;
                        justify-content: space-between;
                        align-items: center;
                        margin-bottom: 12px;
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
                        font-size: 20px;
                        font-weight: 800;
                        background: linear-gradient(90deg, #ffffff, #c084fc);
                        -webkit-background-clip: text;
                        -webkit-text-fill-color: transparent;
                        margin: 0 0 12px 0;
                    }}
                    .vibe {{
                        font-size: 13px;
                        line-height: 1.5;
                        color: #cbd5e1;
                        background: rgba(0, 0, 0, 0.25);
                        padding: 12px;
                        border-radius: 10px;
                        border-left: 3px solid #a855f7;
                        margin-bottom: 12px;
                    }}
                    .grid {{
                        display: grid;
                        grid-template-columns: 1fr 1fr;
                        gap: 10px;
                        margin-bottom: 12px;
                    }}
                    .box {{
                        padding: 10px 12px;
                        border-radius: 10px;
                        font-size: 12px;
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
                        font-size: 13px;
                        font-style: italic;
                        font-weight: 600;
                        color: #f472b6;
                        border-top: 1px dashed rgba(255,255,255,0.15);
                        padding-top: 12px;
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

        components.html(card_html, height=600, scrolling=False)
      except Exception as e:
        st.error(f"Failed to generate card: {str(e)}")
