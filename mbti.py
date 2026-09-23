import streamlit as st
from openai import OpenAI
import os
import json
import io
from PIL import Image, ImageDraw

# ==========================================
# 1. Page Configuration & Dark Cyber Theme
# ==========================================
st.set_page_config(
    page_title="Cosmic Vibe Sync",
    page_icon="✨",
    layout="centered"
)

st.markdown("""
    <style>
    .main {
        background-color: #0E0E10;
        color: #F0F0F2;
    }
    h1, h2, h3 {
        font-family: 'Helvetica Neue', sans-serif;
        font-weight: 300;
        letter-spacing: 1.5px;
    }
    .stButton>button {
        background-color: #1F1F24;
        color: #FFFFFF;
        border: 1px solid #33333E;
        border-radius: 8px;
        padding: 12px 24px;
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        border-color: #8A2BE2;
        box-shadow: 0 0 10px rgba(138, 43, 226, 0.5);
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
        0: "Metal", 1: "Metal",
        2: "Water", 3: "Water",
        4: "Wood",  5: "Wood",
        6: "Fire",  7: "Fire",
        8: "Earth", 9: "Earth"
    }
    return element_map.get(last_digit, "Cosmic Energy")

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
        "actionable_donts": "1 thing to avoid today (social burn-out, micro-managing, etc.).",
        "power_quote": "A 1-line catchy quote for Instagram story."
    }}
    """
    
    api_key = st.secrets.get("GROQ_API_KEY") or os.getenv("GROQ_API_KEY")
    
    if not api_key:
        raise ValueError("GROQ_API_KEY not found. Please configure it in your Streamlit Secrets.")

    # 使用 Groq 的免费 OpenAI 兼容接口
    client = OpenAI(
        api_key=api_key,
        base_url="https://api.groq.com/openai/v1"
    )
    
    # 此处已修正模型名称为 Groq 目前可用的标准免费模型
    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": prompt}],
        response_format={"type": "json_object"}
    )
    
    return json.loads(response.choices[0].message.content)

def create_social_card(mbti, element, title, quote):
    """Generates a dynamic social share card image"""
    img = Image.new('RGB', (600, 600), color='#121215')
    draw = ImageDraw.Draw(img)
    
    draw.rectangle([20, 20, 580, 580], outline='#33333E', width=2)
    draw.text((50, 60), "COSMIC VIBE SYNC", fill='#8A2BE2')
    draw.text((50, 120), f"TYPE: {mbti} × {element.upper()}", fill='#888888')
    draw.text((50, 180), title, fill='#FFFFFF')
    draw.line([(50, 250), (550, 250)], fill='#33333E', width=1)
    draw.text((50, 300), f'"{quote}"', fill='#E0E0E0')
    draw.text((50, 520), "→ Discover your vibe: cosmicvibe.app", fill='#666666')
    
    buf = io.BytesIO()
    img.save(buf, format='PNG')
    return buf.getvalue()

# ==========================================
# 3. User Interface & Page Layout
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
    with st.spinner("Aligning cosmic frequencies & generating analysis..."):
        try:
            data = generate_insights_via_ai(selected_mbti, user_element)
            
            st.markdown("---")
            st.subheader(f"🔮 Archetype: {data['archetype_title']}")
            st.markdown(f"**Daily Energy Vibe:**\n{data['daily_vibe']}")
            
            col_a, col_b = st.columns(2)
            with col_a:
                st.success(f"**Do:** {data['actionable_dos']}")
            with col_b:
                st.error(f"**Don't:** {data['actionable_donts']}")
            
            st.markdown("### 📸 Your Shareable Card")
            card_img_bytes = create_social_card(
                selected_mbti, 
                user_element, 
                data['archetype_title'], 
                data['power_quote']
            )
            
            st.image(card_img_bytes, caption="Press & hold / Right-click to save for your Story")
            
            st.download_button(
                label="Download Story Card",
                data=card_img_bytes,
                file_name=f"{selected_mbti}_cosmic_vibe.png",
                mime="image/png"
            )

        except Exception as e:
            st.error(f"Error generating insight: {str(e)}")
