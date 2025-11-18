import streamlit as st
import pandas as pd
import plotly.express as px

# ------------------------------
# 1. 데이터 불러오기
# ------------------------------
@st.cache_data
def load_data():
    # 업로드한 CSV 파일을 불러옴
    df = pd.read_csv("eunseoinjiSSUNI.csv", encoding="cp949")
    df['총승객수'] = df['승차총승객수'] + df['하차총승객수']
    return df

df = load_data()

# ------------------------------
# 2. 제목
# ------------------------------
st.title("🚇 2025년 지하철 승·하차 데이터 분석 대시보드")
st.write("날짜와 노선을 선택하면 승·하차 총합이 가장 큰 역 순으로 막대그래프를 보여줍니다.")

# ------------------------------
# 3. 필터 UI
# ------------------------------

# 날짜 목록 (2025년 11월만 걸러서 제공)
df['사용일자'] = df['사용일자'].astype(str)
november_dates = sorted(df[df['사용일자'].str.startswith("202511")]['사용일자'].unique())

selected_date = st.selectbox("📅 날짜 선택 (2025년 11월)", november_dates)

# 선택한 날짜 필터링
filtered_by_date = df[df['사용일자'] == selected_date]

# 노선 선택
lines = sorted(filtered_by_date['노선명'].unique())
selected_line = st.selectbox("🚉 노선 선택", lines)

# 노선 필터링
filtered = filtered_by_date[filtered_by_date['노선명'] == selected_line]

# ------------------------------
# 4. Top 역 데이터 가공
# ------------------------------
top_stations = (
    filtered.groupby("역명")["총승객수"]
    .sum()
    .reset_index()
    .sort_values("총승객수", ascending=False)
)

# ------------------------------
# 5. Plotly 그래프
# ------------------------------
fig = px.bar(
    top_stations,
    x="역명",
    y="총승객수",
    title=f"📊 {selected_date} · {selected_line} 승차+하차 총합 Top 역",
    labels={"역명": "역명", "총승객수": "총 승객수"},
)

fig.update_layout(
    xaxis_tickangle=-45,
    template="plotly_white",
)

st.plotly_chart(fig, use_container_width=True)

# ------------------------------
# 6. 데이터 표시
# ------------------------------
st.subheader("📄 데이터 테이블")
st.dataframe(top_stations)

