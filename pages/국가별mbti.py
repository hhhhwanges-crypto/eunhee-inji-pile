"""
Streamlit MBTI 국가별 시각화 앱

파일 구성:
- 이 파일: streamlit_mbti_app.py
- requirements.txt 내용은 아래에 포함되어 있습니다. (캔버스에서 복사해 requirements.txt로 저장하세요)

설치/배포:
1) 로컬에서 실행:
   - pip install -r requirements.txt
   - streamlit run streamlit_mbti_app.py
2) Streamlit Cloud에 배포:
   - 이 파일과 requirements.txt를 저장소에 올리고 Streamlit Cloud에 연결 후 배포

주의: 기본적으로 업로드된 CSV 파일을 사용합니다. (파일 경로: /mnt/data/countriesMBTI_16types.csv)
    파일이 없으면 우측 사이드바에서 CSV 파일을 업로드하세요.

requirements.txt 내용:
streamlit>=1.25
pandas>=1.5
plotly>=5.10

"""

import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
from io import StringIO

st.set_page_config(page_title="MBTI by Country — Interactive", layout="wide")

st.title("국가별 MBTI 분포 — 인터랙티브 시각화")
st.write("국가를 선택하면 해당 국가의 16개 MBTI 유형 비율을 막대그래프로 보여줍니다.")

# 유틸리티: 헥스 색상 보간
def hex_to_rgb(h):
    h = h.lstrip('#')
    return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))

def rgb_to_hex(rgb):
    return '#%02x%02x%02x' % rgb

def interp_color(c1, c2, t):
    r1, g1, b1 = hex_to_rgb(c1)
    r2, g2, b2 = hex_to_rgb(c2)
    return rgb_to_hex((int(r1 + (r2-r1)*t), int(g1 + (g2-g1)*t), int(b1 + (b2-b1)*t)))

# 데이터 불러오기: 업로드 우선, 없으면 기본 경로 사용
uploaded = st.sidebar.file_uploader("CSV 파일 업로드 (countriesMBTI_16types.csv)", type=['csv'])

@st.cache_data
def load_data(uploaded_file):
    if uploaded_file is not None:
        try:
            return pd.read_csv(uploaded_file)
        except Exception as e:
            st.error(f"업로드한 파일을 읽는 중 오류가 발생했습니다: {e}")
            return None
    else:
        # 기본 경로 시도
        default_path = "/mnt/data/countriesMBTI_16types.csv"
        try:
            return pd.read_csv(default_path)
        except FileNotFoundError:
            return None


df = load_data(uploaded)

if df is None:
    st.sidebar.info("데이터파일을 찾을 수 없습니다. CSV 파일을 업로드하세요.")
    st.stop()

# 국가 선택 UI
countries = df['Country'].tolist()
selected_country = st.sidebar.selectbox("국가 선택", countries, index=0)

# MBTI 컬럼 순서를 보장 (Country 제외)
mbti_cols = [c for c in df.columns if c != 'Country']

country_row = df[df['Country'] == selected_country]
if country_row.empty:
    st.error("선택한 국가의 데이터가 없습니다.")
    st.stop()

vals = country_row[mbti_cols].iloc[0]
vals = vals.astype(float)

# 정렬 여부 선택 (원래 16개 고정 순서 vs 비율 순서)
sort_mode = st.sidebar.radio("정렬 방식", ("원본 순서", "비율 내림차순"))
if sort_mode == "비율 내림차순":
    vals = vals.sort_values(ascending=False)
else:
    vals = vals[mbti_cols]

# 색상 생성: 1등은 노랑(#FFD400), 나머지는 파란색 그라데이션 (연-진)
yellow = '#FFD400'
blue_light = '#cfe9ff'  # 연한 파랑
blue_dark = '#0b5ed7'   # 진한 파랑

# 1등 인덱스
max_idx = vals.idxmax()

# 정규화해서 그라데이션 결정
norm = (vals - vals.min()) / (vals.max() - vals.min()) if vals.max() != vals.min() else pd.Series(0.5, index=vals.index)

colors = []
for k in vals.index:
    if k == max_idx:
        colors.append(yellow)
    else:
        t = float(norm[k])  # 0 ~ 1
        colors.append(interp_color(blue_light, blue_dark, t))

# Plotly 바 차트
fig = px.bar(x=vals.index, y=vals.values, labels={'x':'MBTI 유형', 'y':'비율'}, title=f"{selected_country}의 MBTI 분포")
fig.update_traces(marker_color=colors, marker_line_color='rgba(0,0,0,0)', hovertemplate='%{x}: %{y:.4f}<extra></extra>')
fig.update_layout(xaxis_tickangle=-45, yaxis_tickformat=',.2%', uniformtext_minsize=10)

# 퍼센트 포맷: 데이터가 0~1이면 곱하기100하여 퍼센트 표기
# 만약 데이터가 이미 퍼센트(0~100)일 경우를 대비해 자동 감지
sample_val = vals.values[0]
if sample_val <= 1.01:
    # 0~1 범위
    fig.update_yaxes(tickformat='.1%')
else:
    fig.update_yaxes(tickformat='.1f')

# 레이아웃 출력
st.plotly_chart(fig, use_container_width=True)

# 보조 정보: 상위 3개 유형 및 간단 통계
with st.expander("상세 정보 보기 (Top 3, 통계)", expanded=False):
    top3 = vals.sort_values(ascending=False).head(3)
    st.write("Top 3 MBTI:")
    st.table(pd.DataFrame({'MBTI': top3.index, '비율': top3.values}))

    st.write("기본 통계:")
    stats = df[mbti_cols].describe().loc[['mean','min','max','std']].T
    st.dataframe(stats.style.format('{:.4f}'))

# 하단: CSV 다운로드 (선택사항)
@st.cache_data
def to_csv_bytes(df_):
    return df_.to_csv(index=False).encode('utf-8')

csv_bytes = to_csv_bytes(df)
st.download_button(label='원본 데이터 다운로드 (CSV)', data=csv_bytes, file_name='countriesMBTI_16types.csv', mime='text/csv')

st.sidebar.markdown("---")
st.sidebar.markdown("앱 사용법: \n1) 좌측에서 CSV 업로드(선택) 또는 기본 파일 사용\n2) 국가 선택\n3) 정렬 방식 선택\n4) 그래프와 상위 3개 유형 확인")

# 끝
