import streamlit as st

st.set_page_config(page_title="🎬 MBTI 영화 & 노래 추천기", page_icon="🎧", layout="centered")

st.title("🎬 MBTI 유형별 영화 & 노래 추천기 🎵")
st.write("너의 MBTI를 선택하면, 너에게 딱 어울리는 영화랑 노래를 추천해줄게 😎")

# MBTI 목록
mbti_types = [
    "ISTJ", "ISFJ", "INFJ", "INTJ",
    "ISTP", "ISFP", "INFP", "INTP",
    "ESTP", "ESFP", "ENFP", "ENTP",
    "ESTJ", "ESFJ", "ENFJ", "ENTJ"
]

# MBTI별 데이터
mbti_data = {
    "ISTJ": {
        "movies": ["인셉션", "인터스텔라"],
        "songs": ["Imagine Dragons - Whatever It Takes", "Coldplay - Viva La Vida"],
        "desc": "책임감 강하고 현실적인 너에게는 논리와 계획이 중요한 영화가 어울려! 🚀 현실을 넘어서는 스토리가 자극이 될 거야."
    },
    "ISFJ": {
        "movies": ["원더", "하이큐!!"],
        "songs": ["IU - 마음", "Shawn Mendes - Treat You Better"],
        "desc": "따뜻하고 배려 많은 ISFJ! 💕 감동적이고 따뜻한 이야기 속에서 너의 마음이 빛나."
    },
    "INFJ": {
        "movies": ["인사이드 아웃", "죽은 시인의 사회"],
        "songs": ["Lauv - Modern Loneliness", "AKMU - 어떻게 이별까지 사랑하겠어"],
        "desc": "깊은 생각과 감성이 있는 INFJ 🌌 감정이 풍부한 영화와 노래가 너의 내면 세계를 더 반짝이게 만들어줄 거야."
    },
    "INTJ": {
        "movies": ["셜록", "더 소셜 네트워크"],
        "songs": ["Imagine Dragons - Believer", "방탄소년단 - MIC Drop"],
        "desc": "분석력과 통찰력이 뛰어난 전략가 INTJ 🧠 논리적이고 통찰력 있는 영화가 잘 맞아!"
    },
    "ISTP": {
        "movies": ["매드맥스: 분노의 도로", "킹스맨"],
        "songs": ["Linkin Park - Numb", "Zedd - Clarity"],
        "desc": "도전과 액션을 즐기는 ISTP! ⚙️ 박진감 넘치는 영화와 강렬한 음악이 에너지를 채워줄 거야."
    },
    "ISFP": {
        "movies": ["라라랜드", "월-E"],
        "songs": ["Billie Eilish - Ocean Eyes", "태연 - Fine"],
        "desc": "감성 넘치는 예술가 ISFP 🎨 감정선을 자극하는 영화와 잔잔한 노래가 마음을 어루만져줘."
    },
    "INFP": {
        "movies": ["이터널 선샤인", "코코"],
        "songs": ["Lorde - Liability", "잔나비 - 주저하는 연인들을 위해"],
        "desc": "상상력 풍부하고 따뜻한 INFP 🌷 감성적인 영화와 노래에서 네 마음을 찾을 수 있을 거야."
    },
    "INTP": {
        "movies": ["매트릭스", "테넷"],
        "songs": ["Radiohead - Creep", "혁오 - 톱스타"],
        "desc": "논리와 호기심의 천재 INTP 🤔 머리를 쓰게 만드는 영화와 실험적인 노래가 찰떡이야!"
    },
    "ESTP": {
        "movies": ["분노의 질주", "탑건: 매버릭"],
        "songs": ["The Weeknd - Blinding Lights", "GD - 삐딱하게"],
        "desc": "모험심 가득한 ESTP 🏎️ 스릴 있고 에너지 넘치는 영화와 비트가 강한 음악이 잘 어울려!"
    },
    "ESFP": {
        "movies": ["맘마미아!", "주토피아"],
        "songs": ["Doja Cat - Say So", "Red Velvet - Power Up"],
        "desc": "파티의 중심, ESFP 🎉 밝고 즐거운 영화와 신나는 음악으로 에너지 업!"
    },
    "ENFP": {
        "movies": ["위대한 쇼맨", "인턴"],
        "songs": ["Pharrell Williams - Happy", "잔나비 - 뜨거운 여름밤은 가고 남은 건 볼품없지만"],
        "desc": "에너지 넘치고 상상력이 풍부한 ENFP 🌈 자유롭고 희망찬 분위기의 영화랑 노래가 찰떡!"
    },
    "ENTP": {
        "movies": ["아이언맨", "나우 유 씨 미"],
        "songs": ["Imagine Dragons - Thunder", "BIGBANG - BANG BANG BANG"],
        "desc": "재치 있고 토론을 즐기는 ENTP ⚡ 반전과 창의적인 영화가 자극이 돼!"
    },
    "ESTJ": {
        "movies": ["머니볼", "스포트라이트"],
        "songs": ["Queen - Don't Stop Me Now", "ITZY - Not Shy"],
        "desc": "리더십 넘치는 ESTJ 💪 현실적이고 목표지향적인 영화와 강렬한 노래가 잘 어울려!"
    },
    "ESFJ": {
        "movies": ["인턴", "어바웃 타임"],
        "songs": ["Maroon 5 - Sugar", "멜로망스 - 선물"],
        "desc": "사람을 좋아하고 따뜻한 ESFJ 💖 따뜻한 감동이 있는 영화와 밝은 노래가 어울려."
    },
    "ENFJ": {
        "movies": ["어바웃 타임", "인사이드 아웃"],
        "songs": ["Coldplay - Fix You", "태연 - 그대라는 시"],
        "desc": "공감 능력 최고 ENFJ 🌟 감정을 나누는 영화와 진심이 담긴 음악이 너에게 잘 맞아!"
    },
    "ENTJ": {
        "movies": ["더 울프 오브 월 스트리트", "인셉션"],
        "songs": ["Eminem - Lose Yourself", "Stray Kids - 미친 놈"],
        "desc": "목표 지향적이고 야망 있는 ENTJ 🔥 카리스마 넘치는 영화와 강렬한 노래가 딱이야!"
    },
}

# 사용자 입력
user_mbti = st.selectbox("👉 너의 MBTI를 골라봐!", mbti_types)

if user_mbti:
    st.subheader(f"✨ {user_mbti} 유형 추천 결과 ✨")
    data = mbti_data[user_mbti]

    st.write(f"**🎬 추천 영화:** {data['movies'][0]} / {data['movies'][1]}")
    st.write(f"**🎵 추천 노래:** {data['songs'][0]} / {data['songs'][1]}")
    st.write(" ")
    st.info(data['desc'])
    st.success("🎉 네 성격과 완전 찰떡이야! 한 번 꼭 들어보고 봐봐 😉")

st.caption("💡 제작: ChatGPT GPT-5 | 기본 Streamlit만 사용 (설치 필요 X)")
