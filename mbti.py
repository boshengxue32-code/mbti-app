import streamlit as st

# -----------------------------
# AI Personality V1
# 40-question personality quiz
# -----------------------------

st.set_page_config(
    page_title="AI Personality",
    page_icon="🧠",
    layout="centered",
)

# Simple styling
st.markdown("""
<style>
.main-title { font-size: 48px; font-weight: 800; margin-bottom: 0; }
.subtitle { color: #111111; font-size: 18px; margin-top: 4px; margin-bottom: 28px; }
.result-box { padding: 28px; border-radius: 24px; background: #f7f7f8; text-align: center; margin-top: 20px;}
</style>
""", unsafe_allow_html=True)

questions = [
    # E / I
    ("E/I", "周末突然没有任何安排，你通常会？", ["马上找朋友出去玩", "找一两个朋友聊天", "自己找事情做", "很享受一个人待着"]),
    ("E/I", "到了一个完全陌生的聚会，你通常会？", ["主动认识很多人", "找一个人先聊起来", "等别人来找我", "基本不会主动说话"]),
    ("E/I", "上课时老师问了一个问题，你更可能？", ["马上举手回答", "想好了就回答", "除非确定才回答", "尽量不主动回答"]),
    ("E/I", "你认识一个新同学时通常？", ["很快就能聊起来", "比较容易聊天", "需要一点时间", "通常很难主动开口"]),
    ("E/I", "长时间和很多人待在一起以后，你通常？", ["感觉更有精神", "感觉还不错", "有点累", "很想一个人安静一下"]),
    ("E/I", "朋友临时邀请你出去，你通常？", ["马上答应", "大多数时候会去", "看当天状态", "更想留在家里"]),
    ("E/I", "如果你在一个陌生城市旅行，你更可能？", ["主动和当地人聊天", "偶尔和别人交流", "主要和同行的人交流", "尽量自己行动"]),
    ("E/I", "聊天时如果出现冷场，你会？", ["主动找新话题", "尝试让聊天继续", "等对方说话", "觉得安静也没关系"]),
    ("E/I", "你更喜欢哪一种生日？", ["很多朋友一起庆祝", "几个朋友一起", "和家人或少数人", "自己安静地过"]),
    ("E/I", "你遇到有趣的事情时，第一反应通常是？", ["马上告诉别人", "找朋友分享", "先自己消化", "通常不会主动分享"]),

    # N / S
    ("N/S", "看到一个新科技产品时，你最容易想到？", ["它未来还能做什么", "它还有哪些可能", "它现在有什么用途", "它具体怎么使用"]),
    ("N/S", "你更喜欢哪类电影？", ["科幻、奇幻、脑洞类", "剧情复杂的电影", "现实题材", "简单直接的故事"]),
    ("N/S", "老师讲一个新概念时，你通常？", ["马上联想到其他东西", "喜欢想它还能怎么用", "先理解例子", "希望老师给具体步骤"]),
    ("N/S", "做一个项目时，你更喜欢？", ["自由发挥新的想法", "尝试不同方法", "按照已有方法完成", "按照明确步骤完成"]),
    ("N/S", "别人告诉你一个新理论，你会？", ["马上想它意味着什么", "想继续探索", "先找实际证据", "更相信已经验证的事实"]),
    ("N/S", "你更喜欢讨论？", ["未来会发生什么", "各种可能性", "最近发生的事情", "具体事实和细节"]),
    ("N/S", "旅行时你更容易注意到？", ["整体氛围和感觉", "有趣的新发现", "景点的具体信息", "路线、时间和细节"]),
    ("N/S", "如果一个任务没有明确要求，你通常？", ["自己创造一种新方法", "尝试不同方式", "参考以前做过的", "希望先得到明确说明"]),
    ("N/S", "你看到一个故事时更容易记住？", ["主题和隐藏含义", "人物的想法", "发生了什么", "具体细节"]),
    ("N/S", "你突然有一个创业想法，你更可能？", ["立刻想很多新方向", "研究这个想法还能怎么发展", "先判断有没有现实需求", "先考虑具体怎么执行"]),

    # F / T
    ("F/T", "朋友犯错后找你，你通常会？", ["先安慰他", "先听他把话说完", "帮他分析问题", "直接指出问题在哪里"]),
    ("F/T", "发生争论时，你最在意？", ["不要伤害对方感受", "双方能互相理解", "哪个观点更有依据", "哪个观点更符合逻辑"]),
    ("F/T", "朋友心情不好时，你更可能？", ["陪着他", "主动问他怎么了", "帮他分析原因", "直接给解决办法"]),
    ("F/T", "做重要决定时，你更依赖？", ["自己的感觉", "自己和别人的感受", "事实和信息", "逻辑和结果"]),
    ("F/T", "如果一个决定对大多数人有好处，但会让一个朋友失望，你会？", ["非常在意朋友的感受", "会认真考虑朋友", "比较看重整体结果", "主要看哪个方案更合理"]),
    ("F/T", "别人批评你的时候，你第一反应更接近？", ["先想对方是不是难过或生气", "比较在意语气", "先判断内容有没有道理", "直接分析批评是否正确"]),
    ("F/T", "你更喜欢别人怎么给你建议？", ["温柔一点说", "先理解我的感受", "直接讲重点", "告诉我最有效的解决方法"]),
    ("F/T", "朋友和你意见不同，你通常？", ["不希望因为意见影响关系", "会考虑他的立场", "和他讨论证据", "坚持自己认为合理的观点"]),
    ("F/T", "你看到别人被不公平对待时？", ["很容易产生情绪", "会很在意对方感受", "先判断发生了什么", "先考虑怎么解决问题"]),
    ("F/T", "你认为一个好的领导应该？", ["关心团队成员", "让大家感觉被尊重", "做出合理决定", "提高团队效率"]),

    # P / J
    ("P/J", "旅行时你通常？", ["完全看当天心情", "只安排大概计划", "提前安排主要事情", "提前安排得很详细"]),
    ("P/J", "有一个星期后的作业，你通常？", ["经常拖到最后", "想到就做一点", "提前几天开始", "很早就开始"]),
    ("P/J", "你的房间通常？", ["比较乱也无所谓", "有一点乱", "大部分时候整齐", "通常很整齐"]),
    ("P/J", "计划突然改变时，你会？", ["觉得很正常", "很快适应", "需要一点时间", "非常不喜欢突然改变"]),
    ("P/J", "你更喜欢哪种生活？", ["每天有很多变化", "大部分事情比较自由", "有一定计划", "比较规律和确定"]),
    ("P/J", "考试前你通常？", ["最后才开始准备", "有空就看看", "提前几天准备", "提前很久准备"]),
    ("P/J", "如果明天要去旅行，你会？", ["到了再决定", "只查几个地方", "提前做一个计划", "把路线和时间都安排好"]),
    ("P/J", "做团队项目时，你更喜欢？", ["边做边决定", "先开始再调整", "先分工再开始", "先把完整计划确定下来"]),
    ("P/J", "如果一天突然空出来，你会？", ["完全随机安排", "想到什么做什么", "安排几个事情", "提前规划好怎么用这一天"]),
    ("P/J", "你更喜欢任务是？", ["开放式、可以自由发挥", "有方向但有自由", "有明确目标", "步骤和截止时间都明确"]),
]

# 完整 16 种 MBTI 类型描述
type_descriptions = {
    "ENFP": "你通常充满好奇心，喜欢新鲜事物，也容易因为新的想法而兴奋。",
    "ENTP": "你喜欢探索新的可能性，也喜欢和别人讨论有趣的想法。",
    "ENFJ": "你富有同理心与热情，善于鼓舞他人，非常看重团队的和谐与成长。",
    "ENTJ": "你通常喜欢明确的目标，也比较习惯主动解决问题和引领方向。",
    "INFP": "你通常比较重视自己的感受，也很在意人与人之间的关系。",
    "INFJ": "你可能比较安静，但通常会认真观察周围的人和事情，洞察力强。",
    "INTJ": "你通常喜欢自己思考问题，并且比较重视长期目标与系统规划。",
    "INTP": "你喜欢独立思考，对知识充满好奇，擅长逻辑分析与抽象思维。",
    "ESFP": "你通常喜欢体验当下，也容易从和别人相处中获得能量。",
    "ESTP": "你通常比较喜欢行动，而不是花很长时间讨论理论。",
    "ESFJ": "你通常比较关注身边的人，也比较重视关系、秩序和合作。",
    "ESTJ": "你通常喜欢明确的规则、目标和结果，执行力极强。",
    "ISFP": "你可能比较安静，但通常很重视自己的兴趣和真实的感受。",
    "ISTP": "你通常喜欢自己解决问题，并且比较重视实际结果和动手能力。",
    "ISFJ": "你通常比较稳定，也会认真关注和照顾自己在乎的人。",
    "ISTJ": "你通常比较认真负责，也喜欢按照明确的方式踏实完成事情。",
}

if "started" not in st.session_state:
    st.session_state.started = False
if "submitted" not in st.session_state:
    st.session_state.submitted = False

if not st.session_state.started:
    st.markdown('<div class="main-title">🧠 AI Personality</div>', unsafe_allow_html=True)
    st.markdown('<div class="subtitle">40 questions · 3–5 minutes · Discover a more interesting side of you.</div>', unsafe_allow_html=True)
    st.write("这是一个娱乐和自我探索产品原型，不是心理诊断，也不能证明一个人一定属于某种人格类型。")

    if st.button("🚀 Start Test", use_container_width=True):
        st.session_state.started = True
        st.rerun()

elif st.session_state.submitted:
    result = st.session_state.result
    scores = result["scores"]
    ptype = result["type"]

    st.markdown('<div class="main-title">🧠 AI Personality</div>', unsafe_allow_html=True)
    st.markdown(
        f'<div class="result-box">'
        f'<div style="color:#777;">YOUR PERSONALITY</div>'
        f'<div style="font-size:72px;font-weight:800;">{ptype}</div>'
        f'</div>',
        unsafe_allow_html=True
    )

    st.markdown("### About you")
    st.write(type_descriptions.get(ptype, "你的结果包含多种不同特点，这只是一个娱乐性的自我探索结果。"))

    def percentage(a, b):
        total = scores[a] + scores[b]
        return round(scores[a] / total * 100) if total else 50

    social = percentage("E", "I")
    curiosity = percentage("N", "S")
    emotion = percentage("F", "T")
    flexibility = percentage("P", "J")

    st.markdown("### Your Personality Profile")
    c1, c2 = st.columns(2)
    with c1:
        st.metric("Social Energy", f"{social}%")
        st.metric("Curiosity", f"{curiosity}%")
    with c2:
        st.metric("Emotional Focus", f"{emotion}%")
        st.metric("Flexibility", f"{flexibility}%")

    st.progress(social / 100, text=f"Social Energy · {social}%")
    st.progress(curiosity / 100, text=f"Curiosity · {curiosity}%")
    st.progress(emotion / 100, text=f"Emotional Focus · {emotion}%")
    st.progress(flexibility / 100, text=f"Flexibility · {flexibility}%")

    st.info("提示：这个结果是产品原型中的娱乐性人格分类，不是经过临床验证的心理测量，也不应该用于诊断、招聘或重要人生决定。")

    share_text = f"My AI Personality is {ptype}! Try the test too."
    st.code(share_text, language=None)

    if st.button("🔄 Take Test Again", use_container_width=True):
        st.session_state.started = False
        st.session_state.submitted = False
        st.session_state.pop("result", None)
        st.rerun()

else:
    st.markdown('<div class="main-title">🧠 AI Personality</div>', unsafe_allow_html=True)

    with st.form("personality_form"):
        answers = []
        for i, (dimension, question, options) in enumerate(questions):
            st.markdown(f"### {i + 1}. {question}")
            answer = st.radio(
                "选择最符合你的选项",
                options,
                index=None,
                key=f"answer_{i}",
                label_visibility="collapsed",
            )
            answers.append(answer)

        submitted = st.form_submit_button("✨ 查看我的 Personality", use_container_width=True)

        if submitted:
            missing = [str(i + 1) for i, a in enumerate(answers) if a is None]
            if missing:
                st.error(f"还有 {len(missing)} 道题没有回答，请完成所有问题。")
            else:
                scores = {"E": 0, "I": 0, "N": 0, "S": 0, "F": 0, "T": 0, "P": 0, "J": 0}
                for (dimension, question, options), answer in zip(questions, answers):
                    index = options.index(answer)
                    first, second = dimension.split("/")
                    weights = [2, 1, 1, 2]

                    if index < 2:
                        scores[first] += weights[index]
                    else:
                        scores[second] += weights[index]

                personality_type = (
                    ("E" if scores["E"] >= scores["I"] else "I") +
                    ("N" if scores["N"] >= scores["S"] else "S") +
                    ("F" if scores["F"] >= scores["T"] else "T") +
                    ("P" if scores["P"] >= scores["J"] else "J")
                )

                st.session_state.result = {"type": personality_type, "scores": scores}
                st.session_state.submitted = True
                st.rerun()
