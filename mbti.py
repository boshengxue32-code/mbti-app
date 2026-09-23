import streamlit as st
import streamlit.components.v1 as components
from openai import OpenAI
import os
import json

# ==========================================
# 1. Page Configuration & Cyberpunk Styling
# ==========================================
st.set_page_config(
    page_title="Cosmic Vibe Sync",
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
        padding: 14px 28px;
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
""", unsafe_allow_html=True)

# ==========================================
# 2. Core Helper Functions
# ==========================================
def get_eastern_element(year):
    """Maps birth year to Eastern Five Elements Archetype"""
    last_digit = year % 10
    element_map = {
        0: "Metal 🪙", 1: "Metal 🪙",
        2: "Water 💧", 3: "Water 💧",
        4: "Wood 🌿",  5: "Wood 🌿",
        6: "Fire 💥",  7: "Fire 💥",
        8: "Earth 🪐", 9: "Earth 🪐"
    }
    return element_map.get(last_digit, "Cosmic Energy ✨")

def generate_insights_via_ai(mbti, element):
    """Fetches modern intuitive insight using Free Groq API"""
    prompt = f"""
    You are a modern intuitive counselor combining Western MBTI psychology with Eastern Five-Element Archetypes.
    User's Profile:
    - MBTI: {mbti}
    - Eastern Element: {element}

    Generate a highly aesthetic, empowering, and modern "Energy Blueprint" report. Avoid traditional fortune-telling terms like "Suan Gua", "Bazi", or "Fate". Use modern spiritual/psychological terms like "Cosmic Weather", "Inner Alignment", "Vibe Check".

    Please output in the following JSON format ONLY:
    {{
        "archetype_title": "Short cool title like 'The Intuitive Water Architect'",
        "daily_vibe": "A 2-sentence psychological insight about how their {mbti} energy interacts with {element} element today.",
        "actionable_dos": "1 specific empowering advice for today.",
        "actionable_donts": "1 thing to avoid today.",
        "power_quote": "A 1-line catchy quote for Instagram story."
    }}
    """
    
    api_key = st.secrets.get("GROQ_API_KEY") or os.getenv("GROQ_API_KEY")
    
    if not api_key:
        raise ValueError("GROQ_API_KEY not found. Please configure it in your Streamlit Secrets.")

    client = OpenAI(
        api_key=api_key,
        base_url="https://api.groq.com/openai/v1"
    )
    
    response = client.chat.completions.create(
        model="openai/gpt-oss-20b",
        messages=[{"role": "user", "content": prompt}],
        response_format={"type": "json_object"}
    )
    
    return json.loads(response.choices[0].message.content)

# ==========================================
# 3. User Interface & Dynamic Card Layout
# ==========================================
st.title("✨ COSMIC VIBE SYNC")
st.caption("Synthesizing MBTI Cognitive Functions with Eastern Archetypal Energies.")

st.markdown("---")

col1, col2 = st.columns(2)

with col1:
    mbti_list = ["INTJ", "INTP", "ENTJ", "ENTP", "INFJ", "INFP", "ENFJ", "ENFP",
                 "ISTJ", "ISFJ", "ESTJ", "ESFJ", "ISTP", "ISFP", "ESTP", "ESFP"]
    selected_mbti = st.selectbox("Select Your MBTI Type", mbti_list)

with col2:
    birth_year = st.number_input("Select Birth Year", min_value=1950, max_value=2026, value=2000)

user_element = get_eastern_element(birth_year)
st.write(f"Your Eastern Core Element: **{user_element}**")

if st.button("Generate Energy Blueprint"):
    with st.spinner("Aligning cosmic frequencies..."):
        try:
            data = generate_insights_via_ai(selected_mbti, user_element)
            
            # 使用精准无报错的高颜值卡片模板
            card_html = f"""
            <!DOCTYPE html>
            <html>
            <head>
            <style>
                @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;600;800&display=swap');
                body {{
                    margin: 0;
                    padding: 10px;
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
                    gap: 10px;
                    margin-bottom: 16px;
                }}
                .box {{
                    padding: 10px 12px;
                    border-radius: 10px;
                    font-size: 12px;
                }}
                .do-box {{
                    background: rgba(34, 197, 94, 0.12);
                    border: 1px solid rgba(34, 197, 94, 0.25);
                    color: #4ade80;
                }}
                .dont-box {{
                    background: rgba(239, 68, 68, 0.12);
                    border: 1px solid rgba(239, 68, 68, 0.25);
                    color: #f87171;
                }}
                .box-title {{
                    font-weight: 800;
                    margin-bottom: 2px;
                    display: block;
                }}
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
                        <span class="badge">{selected_mbti} × {user_element}</span>
                    </div>
                    <div class="title">{data['archetype_title']}</div>
                    <div class="vibe">{data['daily_vibe']}</div>
                    <div class="grid">
                        <div class="box do-box">
                            <span class="box-title">✨ DO</span>
                            <span style="color: #f0fdf4;">{data['actionable_dos']}</span>
                        </div>
                        <div class="box dont-box">
                            <span class="box-title">🚫 DON'T</span>
                            <span style="color: #fef2f2;">{data['actionable_donts']}</span>
                        </div>
                    </div>
                    <div class="quote">"{data['power_quote']}"</div>
                </div>
            </body>
            </html>
            """
            
            # 使用专属 HTML 渲染组件
            components.html(card_html, height=380)

        except Exception as e:
            st.error(f"Error generating insight: {str(e)}")
