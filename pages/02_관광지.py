# app.py
import streamlit as st
import pandas as pd
import folium
from folium.plugins import MarkerCluster
from streamlit_folium import folium_static

st.set_page_config(page_title="Seoul: Top10 for Foreigners (Map)", layout="wide")

st.title("🇰🇷 Seoul — 외국인들이 좋아하는 주요 관광지 Top 10 (지도)")
st.markdown(
    """
아래 지도는 외국인 방문객들이 자주 찾는 **서울의 주요 관광지 Top10**을 Folium으로 표시한 것입니다.
마커를 클릭하면 간단한 설명을 볼 수 있습니다.  
(출처: VisitSeoul, TripAdvisor, Lonely Planet 등)
"""
)

# 데이터: 명소 이름, 위도, 경도, 간단설명
places = [
    {
        "name": "Gyeongbokgung Palace (경복궁)",
        "lat": 37.579617,
        "lon": 126.977041,
        "desc": "조선의 법궁. 경복궁과 광화문 광장 주변 관광 중심지."
    },
    {
        "name": "Changdeokgung Palace (창덕궁)",
        "lat": 37.579447,
        "lon": 126.991028,
        "desc": "후원(비원)으로 유명한 왕궁 — UNESCO 세계유산."
    },
    {
        "name": "Bukchon Hanok Village (북촌한옥마을)",
        "lat": 37.582600,
        "lon": 126.983000,
        "desc": "전통 한옥이 모여 있는 고즈넉한 골목."
    },
    {
        "name": "Insadong (인사동)",
        "lat": 37.574378,
        "lon": 126.985012,
        "desc": "전통 공예품, 찻집, 기념품 거리."
    },
    {
        "name": "Myeongdong (명동)",
        "lat": 37.560200,
        "lon": 126.985000,
        "desc": "쇼핑·길거리음식의 중심 상업지구."
    },
    {
        "name": "N Seoul Tower / Namsan (남산서울타워)",
        "lat": 37.551169,
        "lon": 126.988227,
        "desc": "도심 전망을 즐길 수 있는 랜드마크 타워."
    },
    {
        "name": "Hongdae (홍대 / 홍익대학교 주변)",
        "lat": 37.556303,
        "lon": 126.924703,
        "desc": "젊음의 거리, 공연·카페·거리문화."
    },
    {
        "name": "Dongdaemun Design Plaza (동대문DDP)",
        "lat": 37.566299,
        "lon": 127.009005,
        "desc": "현대 건축 & 패션 쇼핑의 중심지."
    },
    {
        "name": "Lotte World Tower & Mall (롯데월드타워)",
        "lat": 37.513078,
        "lon": 127.102538,
        "desc": "초고층 전망대, 쇼핑몰, 아쿠아리움 등 복합시설."
    },
    {
        "name": "Hangang (Yeouido) Park (한강공원 여의도)",
        "lat": 37.526000,
        "lon": 126.932600,
        "desc": "한강변 공원 — 피크닉·자전거·야경 명소."
    },
]

df = pd.DataFrame(places)

# 사이드바: 옵션
st.sidebar.header("지도 옵션")
zoom_start = st.sidebar.slider("지도 초기 확대 레벨", min_value=11, max_value=15, value=12)
cluster_toggle = st.sidebar.checkbox("마커 클러스터 사용", value=True)
show_table = st.sidebar.checkbox("명소 목록 표 보기", value=True)

# Folium 맵 생성
center_lat = df["lat"].mean()
center_lon = df["lon"].mean()
m = folium.Map(location=[center_lat, center_lon], zoom_start=zoom_start)

if cluster_toggle:
    marker_cluster = MarkerCluster().add_to(m)
    for _, row in df.iterrows():
        popup_html = f"<b>{row['name']}</b><br>{row['desc']}"
        folium.Marker(
            location=[row["lat"], row["lon"]],
            popup=popup_html,
            tooltip=row["name"],
        ).add_to(marker_cluster)
else:
    for _, row in df.iterrows():
        popup_html = f"<b>{row['name']}</b><br>{row['desc']}"
        folium.Marker(
            location=[row["lat"], row["lon"]],
            popup=popup_html,
            tooltip=row["name"],
        ).add_to(m)

# 지도 출력 (큰 화면)
st.subheader("지도 (Folium)")
folium_static(m, width=1200, height=700)

if show_table:
    st.subheader("명소 목록")
    st.table(df[["name", "lat", "lon", "desc"]])

# 코드 표시: 사용자가 쉽게 복사하도록 앱 내에 소스코드 보여주기
st.markdown("---")
st.subheader("앱 소스코드 (복사해서 사용하세요)")
with open(__file__, "r", encoding="utf-8") as f:
    source = f.read()
st.code(source, language="python")

st.markdown("""
---
**설치/배포 팁**
1. 이 파일을 `app.py`로 저장하세요.  
2. 같은 레포지토리에 `requirements.txt`를 추가한 후 Streamlit Cloud(또는 Streamlit Community Cloud)에 업로드하세요.  
3. Streamlit Cloud에서 `Run`을 누르면 앱이 배포됩니다.
""")
