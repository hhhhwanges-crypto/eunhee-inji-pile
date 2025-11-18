import streamlit as st
import pandas as pd
import plotly.graph_objects as go

st.set_page_config(page_title="지하철 승하차 분석", layout="wide")

# -----------------------------
# 1. 데이터 불러오기
# -----------------------------
@st.cache_data
def load_data():
    df = pd.read_csv("eunseoinjiSSUNI.csv", encoding="cp949")
    df["사용일자"] = df["사용일자"].astype(str)
    df["총승객수"] = df["승차총승객수"] + df["하차총승객수"]
    return df

df = load_data()

st.title("🚇 2025년 11월 지하철 승·하차 데이터 분석")

# -----------------------------
# 2. 날짜 선택 (2025년 11월 데이터만)
# -----------------------------
nov_dates = sorted(df[df["사용일자"].str.startswith("202511")]["사용일자"].unique())

if len(nov_dates) == 0:
    st.error("⚠ CSV 파일에 2025년 11월 데이터가 없습니다.")
    st.stop()

selected_date = st.selectbox("📅 날짜 선택", nov_dates)

df_date = df[df["사용일자"] == selected_date]

# -----------------------------
# 3. 노선 선택
# -----------------------------
lines = sorted(df_date["노선명"].unique())
selected_line = st.selectbox("🚉 노선 선택", lines)

df_filtered = df_date[df_date["노선명"] == selected_line]

# -----------------------------
# 4. 역별 총 승객수 정렬
# -----------------------------
top_stations = (
    df_filtered.groupby("역명")["총승객수"]
    .sum()
    .reset_index()
    .sort_values("총승객수", ascending=False)
)

# -----------------------------
# 5. 갈색 → 고동색 그라데이션 색상 생성
# -----------------------------
def brown_gradient(n):
    colors = []
    for i in range(n):
        # 가장 진한 색 → 점점 연한 색
        base = 120 - int((i / max(1, n-1)) * 80)
        base = max(40, base)  # 너무 밝아지는 것 방지
        colors.append(f"rgb({base}, {base*0.6}, {base*0.3})")
    return colors

colors = brown_gradient(len(top_stations))

# -----------------------------
# 6. Plotly 그래프
# -----------------------------
fig = go.Figure()

fig.add_trace(
    go.Bar(
        x=top_stations["역명"],
        y=top_stations["총승객수"],
        marker=dict(color=colors),
    )
)

fig.update_layout(
    title=f"📊 {selected_date} · {selected_line} 승차+하차 총합 TOP 역",
    xaxis_title="역명",
    yaxis_title="총 승객수",
    template="plotly_white",
    xaxis_tickangle=-45,
)

st.plotly_chart(fig, use_container_width=True)

# -----------------------------
# 7. 데이터 테이블 표시
# -----------------------------
st.subheader("📄 데이터 테이블")
st.dataframe(top_stations)

