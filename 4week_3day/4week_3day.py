# streamlit가상환경에서 실행
# import streamlit as st

# st.write("Hello, Streamlit!") 

# 예제1
# import streamlit as st
# st.title("👋첫 인터랙티브 앱")      # title은 그냥 큰 글자
# name = st.text_input("이름이 무엇인가요?")
# mood = st.select_slider("오늘 기분은?", ["😢", "😐", "🙂", "😄", "🤩"], value="🙂")
# if name:
#     st.write(f"### {name}님, 오늘 기분은 {mood} 이군요!")       # write는 그냥 title보다 작은 글자
#     st.balloons() 

# 예제2
# import streamlit as st
# import numpy as np
# import pandas as pd
# st.title("📈임의 데이터 차트")
# n = st.slider("샘플 개수", 10, 1000, 200, step=10)
# freq= st.slider("주파수", 0.1, 5.0, 1.0, step=0.1)

# x = np.linspace(0, 10, n)
# df = pd.DataFrame({
#     "x": x,
#     "sin": np.sin(freq* x),
#     "cos": np.cos(freq* x),
# })
# st.line_chart(df, x="x", y=["sin", "cos"])
# with st.expander("원본데이터보기"):
#     st.dataframe(df, use_container_width=True)

# 예제3
# import streamlit as st
# import numpy as np
# import pandas as pd

# st.set_page_config(page_title="첫 앱", page_icon="📊", layout="wide")
# st.title("📊미니 대시보드")
# with st.sidebar:
#     st.header("설정")
#     n = st.slider("샘플", 50, 2000, 500)
#     seed = st.number_input("랜덤 시드", value=42) 
# rng= np.random.default_rng(seed)
# df = pd.DataFrame({"x": np.arange(n), "value": rng.normal(0, 1, n).cumsum(),})
# c1, c2, c3 = st.columns(3)
# c1.metric("샘플 수", f"{n:,}")
# c2.metric("평균", f"{df['value'].mean():.2f}")
# c3.metric("표준편차", f"{df['value'].std():.2f}")

# st.line_chart(df, x="x", y="value")
# st.dataframe(df.tail(10), use_container_width=True) 

# 예제4
import streamlit as st

# st.title("📊분기 리포트")
# st.caption("2026 Q1 · 자동 생성됨")

# st.header("개요")
# st.write("이번 분기 :blue[매출]은 **전분기 대비 12% 증가**했습니다.")

# st.subheader("주요 지표")
# st.markdown("""
# - 신규 고객: **1,240명** (↑8%) 
# - 이탈률: **2.3%** (↓0.4pp) 
# - ARPU: **₩28,400** (↑5%)
# """)

# st.divider()
# st.text("주의: 이 문서는 자동 생성되었습니다.")

# 예제
# import streamlit as st
# if st.button("저장"):
#     # save_data()
#     st.success("저장되었습니다.")

# # 강조형
# st.button("결제하기", type="primary", icon="💳", use_container_width=True)
# st.button("삭제", type="secondary", disabled=True)

# # checkbox
# agree = st.checkbox("이용약관에 동의합니다")
# dark = st.toggle("다크 모드", value=True)

# # 라디오 버튼 위젯.
# my_choice= st.radio("다음 중 한가지 선택", ["부먹","찍먹"] )

# # 드롭다운 선택 위젯.
# my_choice= st.selectbox("다음 중 한가지 선택", ["부먹","찍먹"])

# # 멀티셀렉트 위젯.
# my_choices= st.multiselect("후식 선택", ["티라미수","아이스크림","과일 샐러드","수정과"])

# # 컬러 피커 위젯. 선택 결과는 16진수 (HEX) 컬러값.
# my_choice= st.color_picker("컬러 선택")

# 예제
# with st.sidebar:
#     st.title("타이틀-대")
#     st.header("타이틀-중")
#     st.subheader("타이틀-소")
#     ""                              
#     "---"
#     ""
#     x = st.selectbox("다음 중 한가지 선택", [ "부먹","찍먹"] )
#     st.write(f"Selectbox 선택= {x}")
#     ""                              
#     "---"
#     ""

import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config("매출 분석", layout = "wide")

with st.sidebar:
    st.title("📊Sales")
    region = st.multiselect("지역", ["서울", "부산", "대구"], default = ["서울"])
    period = st.select_slider("기간", ["1주", "1개월", "3개월", "1년"], value = "1개월")
    show_breakdown= st.checkbox("세부 보기", value=True)
    st.divider()
    if st.button("🔄데이터 새로고침", use_container_width = True):
        st.cache_data.clear()
        st.rerun()
st.title("매출 대시보드")

# KPI
c1, c2, c3 = st.columns(3)
c1.metric("매출", "₩12.4M", "+8%")
c2.metric("주문", "1,240", "+58")
c3.metric("이탈", "2.3%", "-0.4pp", delta_color = "inverse")

# 차트
rng = np.random.default_rng(0)
df = pd.DataFrame({"day": pd.date_range("2026-01-01", periods = 60), "sales": rng.integers(100, 500, 60)})
st.line_chart(df, x = "day", y = "sales")
if show_breakdown:
    st.subheader("지역별 세부")
    st.dataframe(df.tail(10), use_container_width = True)







