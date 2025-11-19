import streamlit as st
import pandas as pd
import plotly.express as px

# 1. 데이터 준비 (앞선 CSV 데이터를 딕셔너리로 변환)
# 순위는 1위부터 5위까지 중요도를 나타낸다고 가정하고, 시각화를 위해 가상의 '인기 점수'를 부여합니다.
# 1위: 5점, 2위: 4점, 3위: 3점, 4위: 2점, 5위: 1점
data = {
    "대한민국": {
        "메뉴": ["엄마는 외계인", "아몬드 봉봉", "민트 초콜릿 칩", "뉴욕 치즈케이크", "체리쥬빌레"],
        "점수": [5, 4, 3, 2, 1],
        "설명": "🇰🇷 한국의 1위 메뉴는 '엄마는 외계인'이야! 초콜릿, 바닐라, 그리고 팝핑볼의 조화가 독특해서 독보적인 인기를 자랑해. 😋 '아몬드 봉봉'이나 '민초'처럼 견과류나 클래식한 맛도 강세지.",
    },
    "미국": {
        "메뉴": ["Vanilla", "Oreo Cookies 'n Cream", "Mint Chocolate Chip", "Pralines 'n Cream", "Chocolate"],
        "점수": [5, 4, 3, 2, 1],
        "설명": "🇺🇸 배라의 본고장, 미국에서는 의외로 'Vanilla(바닐라)'가 1위야!🍦 클래식한 맛을 선호하는 경향이 크고, '오레오 쿠키 앤 크림'이나 '민트 초콜릿 칩' 같은 달콤하고 식감이 있는 메뉴가 중요해.",
    },
    "일본": {
        "메뉴": ["ポッピングシャワー", "チョコレートミント", "ロッキーロード", "ストロベリーチーズケーキ", "ベリーベリーストロベリー"],
        "점수": [5, 4, 3, 2, 1],
        "설명": "🇯🇵 일본의 'ポッピングシャワー(팝핑 샤워)'는 입안에서 톡톡 터지는 식감이 대박! 🍬 민트와 초콜릿의 조합, 그리고 '로키 로드'처럼 다양한 식재료가 섞인 화려한 메뉴들이 특히 중요하게 여겨져.",
    },
    "캐나다": {
        "메뉴": ["Mint Chocolate Chip", "Vanilla", "Chocolate", "Chocolate Chip Cookie Dough", "Pralines 'n Cream"],
        "점수": [5, 4, 3, 2, 1],
        "설명": "🇨🇦 캐나다에서는 '민트 초콜릿 칩'이 탑이야. 상쾌함과 달콤함을 동시에 잡는 맛을 좋아하지. 🍪 '초콜릿 칩 쿠키 도우'처럼 큼직한 식감이 있는 메뉴도 중요한 선택지야.",
    },
    "멕시코": {
        "메뉴": ["Love Potion #31", "Mango Tango", "Vanilla", "Chocolate", "Strawberry"],
        "점수": [5, 4, 3, 2, 1],
        "설명": "🇲🇽 멕시코는 화려하고 열정적인 맛을 좋아해! 'Love Potion #31' 같은 로맨틱한 이름의 메뉴나 'Mango Tango'처럼 열대과일 맛이 강세야. 🌶️ 전통적인 맛보다는 새롭고 강렬한 맛이 중요해.",
    },
    "브라질": {
        "메뉴": ["Limão", "Pistache", "Morango", "Coco", "Chocolate"],
        "점수": [5, 4, 3, 2, 1],
        "설명": "🇧🇷 브라질에서는 'Limão(레몬)'처럼 상큼한 과일 맛이나 'Pistache(피스타치오)' 같은 견과류 맛이 중요해. 🥥 'Coco(코코넛)'는 열대 국가답게 꾸준한 인기를 누리는 중요한 메뉴지.",
    },
    "영국": {
        "메뉴": ["Vanilla", "Chocolate", "Strawberry", "Chocolate Chip Cookie Dough", "Mint Chocolate Chip"],
        "점수": [5, 4, 3, 2, 1],
        "설명": "🇬🇧 영국은 깔끔하고 클래식한 맛을 선호하는 편이야. '바닐라', '초콜릿', '딸기' 이 세 가지 기본 맛이 인기의 중심이지. ☕️ 여기에 '쿠키 도우'처럼 조금 더 재밌는 식감을 추가한 메뉴도 선호해.",
    },
    "중국": {
        "메뉴": ["Vanilla", "Red Bean", "Green Tea", "Chocolate", "Strawberry"],
        "점수": [5, 4, 3, 2, 1],
        "설명": "🇨🇳 중국에서는 'Vanilla(바닐라)'와 함께 현지 특색을 살린 'Red Bean(팥)', 'Green Tea(녹차)'가 중요해. 🍵 특히 팥이나 녹차는 디저트에서 자주 쓰이는 재료라 배스킨라빈스에서도 꼭 찾는 메뉴야.",
    },
    "말레이시아": {
        "메뉴": ["Mint Chocolate Chip", "Pralines 'n Cream", "Vanilla", "Chocolate", "Strawberry"],
        "점수": [5, 4, 3, 2, 1],
        "설명": "🇲🇾 더운 나라 말레이시아에서는 '민트 초콜릿 칩'의 상쾌함이 최고! 시원한 민트 맛이 중요한 포인트야. 🥜 '프랄린 앤 크림'처럼 견과류와 카라멜의 조합도 달콤한 걸 좋아하는 현지인들에게 인기지.",
    },
    "태국": {
        "메뉴": ["Mint Chocolate Chip", "Vanilla", "Chocolate", "Strawberry", "Mango"],
        "점수": [5, 4, 3, 2, 1],
        "설명": "🇹🇭 태국도 '민트 초콜릿 칩'이 최고 인기야. 하지만 열대 과일의 나라답게 'Mango(망고)' 같은 현지 과일 메뉴도 아주 중요해. ☀️ 시원하고 달콤한 열대 과일 맛을 빼놓을 수 없어!",
    },
    "사우디아라비아": {
        "메뉴": ["Pralines 'n Cream", "Vanilla", "Chocolate", "Strawberry", "Mint Chocolate Chip"],
        "점수": [5, 4, 3, 2, 1],
        "설명": "🇸🇦 사우디에서는 'Pralines 'n Cream(프랄린 앤 크림)'의 달콤하고 고급스러운 맛을 선호해. 🌰 바닐라 아이스크림에 카라멜과 견과류가 들어간 메뉴가 제일 중요하고 인기가 많아.",
    },
}

# 2. 스트림릿 앱 구성
st.set_page_config(
    page_title="🌎 11개국 배라 인기 메뉴 탐험!",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.title("🍦 11개국 배스킨라빈스 인기 메뉴 TOP 5!")
st.markdown("---")
st.markdown("궁금한 나라를 골라봐! 그 나라에서 제일 잘 나가는 배스킨라빈스 아이스크림 5개를 그래프로 보여줄게. 😉")

# 3. 사이드바 (나라 선택)
countries = list(data.keys())
selected_country = st.sidebar.selectbox(
    "👉 나라를 선택해봐!", 
    countries, 
    index=countries.index("대한민국")
)

# 4. 데이터프레임 생성 및 그래프 그리기
if selected_country:
    country_data = data[selected_country]
    
    # 데이터프레임 만들기 (그래프용)
    df = pd.DataFrame({
        "메뉴 이름": country_data["메뉴"],
        "인기 점수 (가중치)": country_data["점수"]
    })
    
    # 5. 그래프 시각화 (막대 그래프)
    st.header(f"✨ {selected_country}의 인기 메뉴 TOP 5 순위")
    
    # Plotly로 막대 그래프 그리기 (순위에 따라 색상 다르게)
    fig = px.bar(
        df, 
        x="인기 점수 (가중치)", 
        y="메뉴 이름", 
        orientation='h', 
        color="인기 점수 (가중치)",
        color_continuous_scale=px.colors.sequential.Plasma,
        text="메뉴 이름"
    )
    
    # 그래프 레이아웃 설정
    fig.update_layout(
        xaxis_title="인기 점수 (높을수록 중요)",
        yaxis_title="",
        yaxis={'categoryorder':'total ascending'}, # 1위가 위에 오도록 정렬
        coloraxis_showscale=False, # 색상 스케일 숨기기
        height=400
    )
    # 메뉴 이름을 그래프 위에 직접 표시
    fig.update_traces(textposition='inside', insidetextanchor='middle')

    st.plotly_chart(fig, use_container_width=True)
    
    # 6. 아이스크림의 '중요성' 설명
    st.markdown("---")
    st.header(f"🧐 {selected_country}에서 이 아이스크림이 중요한 이유!")
    st.info(country_data["설명"])

# 7. 마무리
st.sidebar.markdown("---")
st.sidebar.caption("데이터는 공식 자료 및 현지 보도를 참고하여 구성되었습니다.")
