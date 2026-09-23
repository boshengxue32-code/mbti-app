import streamlit as st
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
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;600;800&display=swap');
    
    * {
        font-family: 'Plus Jakarta Sans', sans-serif;
    }
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
            
            # 高颜值 HTML 卡片模版
            card_html = f"""
            <div style="
                background: linear-gradient(135deg, #13151f 0%, #1e1b4b 50%, #311042 100%);
                border: 1px solid rgba(255, 255, 255, 0.15);
                border-radius: 24px;
                padding: 32px;
                box-shadow: 0 20px 40px rgba(0,0,0,0.6), inset 0 1px 0 rgba(255,255,255,0.2);
                margin: 20px 0;
                position: relative;
                overflow: hidden;
            ">
                <!-- 装饰背景圈 -->
                <div style="position: absolute; top: -50px; right: -50px; width: 180px; height: 180px; background: rgba(168, 85, 247, 0.25); filter: blur(50px); border-radius: 50%;"></div>
                <div style="position: absolute; bottom: -50px; left: -50px; width: 180px; height: 180px; background: rgba(236, 72, 153, 0.25); filter: blur(50px); border-radius: 50%;"></div>

                <!-- 头部 Badge -->
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px;">
                    <span style="font-size: 12px; font-weight: 800; letter-spacing: 2px; color: #a855f7; text-transform: uppercase;">Cosmic Energy Blueprint</span>
                    <span style="background: rgba(255, 255, 255, 0.1); border: 1px solid rgba(255, 255, 255, 0.15); padding: 4px 12px; border-radius: 20px; font-size: 13px; font-weight: 600; color: #e2e8f0;">
                        {selected_mbti} × {user_element}
                    </span>
                </div>

                <!-- 主称号 -->
                <h2 style="font-size: 26px; font-weight: 800; background: linear-gradient(90deg, #ffffff, #c084fc); -webkit-background-clip: text; -webkit-text-fill-color: transparent; margin: 0 0 16px 0;">
                    {data['archetype_title']}
                </h2>

                <!-- Vibe 描述 -->
                <p style="font-size: 15px; line-height: 1.6; color: #cbd5e1; margin-bottom: 24px; background: rgba(0, 0, 0, 0.2); padding: 16px; border-radius: 12px; border-left: 3px solid #a855f7;">
                    {data['daily_vibe']}
                </p >

                <!-- Do & Don't 网格 -->
                <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 12px; margin-bottom: 24px;">
                    <div style="background: rgba(34, 197, 94, 0.1); border: 1px solid rgba(34, 197, 94, 0.2); border-radius: 12px; padding: 12px 16px;">
                        <span style="color: #4ade80; font-size: 12px; font-weight: 700; text-transform: uppercase;">✨ DO</span>
                        <p style="font-size: 13px; color: #f0fdf4; margin: 4px 0 0 0; font-weight: 500;">{data['actionable_dos']}</p >
                    </div>
                    <div style="background: rgba(239, 68, 68, 0.1); border: 1px solid rgba(239, 68, 68, 0.2); border-radius: 12px; padding: 12px 16px;">
                        <span style="color: #f87171; font-size: 12px; font-weight: 700; text-transform: uppercase;">🚫 DON'T</span>
                        <p style="font-size: 13px; color: #fef2f2; margin: 4px 0 0 0; font-weight: 500;">{data['actionable_donts']}</p >
                    </div>
                </div>

                <!-- 金句金格 -->
                <div style="text-align: center; padding-top: 16px; border-top: 1px dashed rgba(255, 255, 255, 0.15);">
                    <p style="font-size: 16px; font-style: italic; font-weight: 600; color: #f472b6; margin: 0;">
                        "{data['power_quote']}"
                    </p >
                </div>
            </div>
            """
            
            # 渲染卡片
            st.markdown(card_html, unsafe_allow_html=True)

        except Exception as e:
            st.error(f"Error generating insight: {str(e)}")
