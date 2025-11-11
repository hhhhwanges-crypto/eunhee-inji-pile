# app.py
import streamlit as st
import pandas as pd
import folium
from folium.plugins import MarkerCluster
from streamlit_folium import folium_static
import math

st.set_page_config(page_title="서울 외국인 인기 관광지 지도", layout="wide")

st.title("🇰🇷 외국인들이 사랑하는 서울 관광지 TOP10")
st.markdown("""
서울을 처음 방문하는 외국인들에게 인기 있는 관광 명소 10곳을 한눈에 볼 수 있어요.  
지도 마커를 클릭하면 **한글 설명 + 가장 가까운 지하철역 정보**를 볼 수 있습니다.  
""")

# 🔹 관광지 정보 (한국어 설명 + 지하철역 정보 추가)
places = [
    {
        "name": "경복궁",
        "lat": 37.579617,
        "lon": 126.977041,
        "desc": "조선 왕조의 중심 궁궐로, 아름다운 건축과 광화문으로 이어지는 산책로가 인기입니다.",
        "subway": "3호선 경복궁역"
    },
    {
        "name": "창덕궁",
        "lat": 37.579447,
        "lon": 126.991028,
        "desc": "비원(후원)으로 유명한 고궁으로, 자연과 조화를 이루는 경관이 뛰어난 세계문화유산입니다.",
        "subway": "3호선 안국역"
    },
    {
        "name": "북촌한옥마을",
        "lat": 37.582600,
        "lon": 126.983000,
        "desc": "전통 한옥이 잘 보존된 마을로, 골목길을 따라 걷기 좋은 명소입니다.",
        "subway": "3호선 안국역"
    },
    {
        "name": "인사동",
        "lat": 37.574378,
        "lon": 126.985012,
        "desc": "전통 찻집, 공예품 가게, 거리 공연 등으로 외국인에게 인기 많은 전통 거리입니다.",
        "subway": "3호선 안국역 / 1호선 종각역"
    },
    {
        "name": "명동",
        "lat": 37.560200,
        "lon": 126.985000,
        "desc": "서울의 대표 쇼핑 거리로, 화장품·패션 브랜드와 길거리 음식이 가득한 곳입니다.",
        "subway": "4호선 명동역"
    },
    {
        "name": "남산서울타워",
        "lat": 37.551169,
        "lon": 126.988227,
        "desc": "서울 도심을 한눈에 볼 수 있는 랜드마크 전망 타워입니다.",
        "subway": "4호선 명동역 / 케이블카 접근"
    },
    {
        "name": "홍대거리",
        "lat": 37.556303,
        "lon": 126.924703,
        "desc": "젊음과 예술의 거리로, 버스킹 공연·카페·클럽 문화가 활발한 지역입니다.",
        "subway": "2호선 홍대입구역"
    },
    {
        "name": "동대문디자인플라자(DDP)",
        "lat": 37.566299,
        "lon": 127.009005,
        "desc": "자하 하디드가 설계한 곡선형 현대 건축물로, 패션·전시·야경 명소입니다.",
        "subway": "2·4·5호선 동대문역사문화공원역"
    },
    {
        "name": "롯데월드타워",
        "lat": 37.513078,
        "lon": 127.102538,
        "desc": "123층 초고층 타워로, 전망대·쇼핑몰·아쿠아리움이 있는 복합 명소입니다.",
        "subway": "2호선 잠실역"
    },
    {
        "name": "여의도한강공원",
        "lat": 37.526000,
        "lon": 126.932600,
        "desc": "야경과 피크닉, 자전거로 즐기는 한강 대표 공원입니다.",
        "subway": "5호선 여의나루역"
    },
]

df = pd.DataFrame(places)

# 🔹 지도 옵션
st.sidebar.header("🗺️ 지도 옵션")
zoom_start = st.sidebar.slider("지도 확대 레벨", 11, 15, 12)
cluster_toggle = st.sidebar.checkbox("마커 클러스터 사용", True)
show_table = st.sidebar.checkbox("명소 표 보기", True)

# 🔹 Folium 지도 생성
center_lat, center_lon = df["lat"].mean(), df["lon"].mean()
m = folium.Map(location=[center_lat, center_lon], zoom_start=zoom_start)
if cluster_toggle:
    marker_cluster = MarkerCluster().add_to(m)
    for _, row in df.iterrows():
        popup_html = f"<b>{row['name']}</b><br>{row['desc']}<br><br><b>🚇 지하철:</b> {row['subway']}"
        folium.Marker([row["lat"], row["lon"]], popup=popup_html, tooltip=row["name"]).add_to(marker_cluster)
else:
    for _, row in df.iterrows():
        popup_html = f"<b>{row['name']}</b><br>{row['desc']}<br><br><b>🚇 지하철:</b> {row['subway']}"
        folium.Marker([row["lat"], row["lon"]], popup=popup_html, tooltip=row["name"]).add_to(m)

st.subheader("📍 관광지도")
folium_static(m, width=1200, height=700)

if show_table:
    st.subheader("📋 관광지 정보 요약")
    st.dataframe(df[["name", "subway", "desc"]], use_container_width=True)

# 🔹 일정 추천 기능
st.markdown("---")
st.subheader("🗓️ 나만의 서울 여행 일정 만들기")

days = st.slider("여행 일수 선택 (1~3일)", 1, 3, 1)
st.write(f"➡️ {days}일 동안 서울 주요 관광지 10곳을 여행하는 추천 일정입니다:")

# 일정 분배
places_per_day = math.ceil(len(df) / days)
itinerary = []
for d in range(days):
    start_idx = d * places_per_day
    end_idx = start_idx + places_per_day
    day_places = df.iloc[start_idx:end_idx]
    itinerary.append(day_places)

# 일정표 표시
for i, day_df in enumerate(itinerary, 1):
    st.markdown(f"### 🏖️ Day {i}")
    for _, row in day_df.iterrows():
        st.markdown(f"- **{row['name']}** ({row['subway']}) — {row['desc']}")

st.markdown("""
---
💡 *팁:* 여행 동선 순서는 실제 위치 기준이 아니라 단순 추천 순서입니다.  
원하신다면 거리 기반 자동 최적 동선 기능도 추가해드릴 수 있어요! 🚶‍♀️
""")
