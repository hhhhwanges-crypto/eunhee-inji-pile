import streamlit as st
st.title('나의 첫 웹 사이트 만들기') 
a=st.text_input('니이름이 뭐임?')
if st.button('인사말 생성'):
  st.write(a+'님 ㅎㅇ')
