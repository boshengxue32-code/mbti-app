import streamlit as st
import openai
import os
import json
import io
from PIL import Image, ImageDraw, ImageFont

# ==========================================
# 1. 页面基本配置 (页面标题、图标、极简暗黑风样式)
# ==========================================
st.set_page_config(
    page_title="Cosmic Vibe Sync",
    page_icon="✨",
    layout="centered"
)

# 注入 CSS 打造黑白极简/赛博神秘感 UI (Minimalist Mysticism)
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
# 2. 逻辑辅助函数 (五行计算与 OpenAI 调用)
# ==========================================
def get_eastern_element(year):
    """根据出生年份简单映射东方五行元素 (Eastern Element)"""
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
    """调用 OpenAI 生成符合美式语境的心理学/能量解读"""
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
    
    # 填入你的真实 OpenAI API Key
    OPENAI_API_KEY = "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"
    
    client = openai.OpenAI(api_key=api_key)
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        response_format={"type": "json_object"}
    )
    
    return json.loads(response.choices[0].message.content)

def create_social_card(mbti, element, title, quote):
    """动态生成极简高颜值图片卡片 (Social Share Card)"""
    img = Image.new('RGB', (600, 600), color='#121215')
    draw = ImageDraw.Draw(img)
    
    # 绘制外边框线
    draw.rectangle([20, 20, 580, 580], outline='#33333E', width=2)
    
    # 写入文本信息
    draw.text((50, 60), "COSMIC VIBE SYNC", fill='#8A2BE2')
    draw.text((50, 120), f"TYPE: {mbti} × {element.upper()}", fill='#888888')
    draw.text((50, 180), title, fill='#FFFFFF')
    
    # 分割线
    draw.line([(50, 250), (550, 250)], fill='#33333E', width=1)
    
    # 金句
    draw.text((50, 300), f'"{quote}"', fill='#E0E0E0')
    
    draw.text((50, 520), "→ Discover your vibe: cosmicvibe.app", fill='#666666')
    
    buf = io.BytesIO()
    img.save(buf, format='PNG')
    return buf.getvalue()

# ==========================================
# 3. 页面 UI 布局与逻辑响应
# ==========================================
st.title("✨ COSMIC VIBE SYNC")
st.caption("Synthesizing MBTI Cognitive Functions with Eastern Archetypal Energies.")

st.markdown("---")

# 用户输入区
col1, col2 = st.columns(2)

with col1:
    mbti_list = ["INTJ", "INTP", "ENTJ", "ENTP", "INFJ", "INFP", "ENFJ", "ENFP",
                 "ISTJ", "ISFJ", "ESTJ", "ESFJ", "ISTP", "ISFP", "ESTP", "ESFP"]
    selected_mbti = st.selectbox("Your MBTI Type", mbti_list)

with col2:
    birth_year = st.number_input("Birth Year", min_value=1950, max_value=2026, value=2000)

user_element = get_eastern_element(birth_year)

st.write(f"Your Eastern Core Element: **{user_element}**")

# 触发生成按钮
if st.button("Generate Energy Blueprint"):
    with st.spinner("Aligning cosmic frequencies & AI analysis..."):
        try:
            data = generate_insights_via_ai(selected_mbti, user_element)
            
            st.markdown("---")
            
            # 展现 AI 生成结果
            st.subheader(f"🔮 Archetype: {data['archetype_title']}")
            st.markdown(f"**Daily Energy Vibe:**\n{data['daily_vibe']}")
            
            col_a, col_b = st.columns(2)
            with col_a:
                st.success(f"**Do:** {data['actionable_dos']}")
            with col_b:
                st.error(f"**Don't:** {data['actionable_donts']}")
            
            # 生成社交共享卡片
            st.markdown("### 📸 Your Shareable Card")
            card_img_bytes = create_social_card(
                selected_mbti, 
                user_element, 
                data['archetype_title'], 
                data['power_quote']
            )
            
            st.image(card_img_bytes, caption="Press & hold / Right-click to save for your Story")
            
            # 下载按钮
            st.download_button(
                label="Download Story Card",
                data=card_img_bytes,
                file_name=f"{selected_mbti}_cosmic_vibe.png",
                mime="image/png"
            )

        except Exception as e:
            st.error(f"Error generating insight: {str(e)}")
