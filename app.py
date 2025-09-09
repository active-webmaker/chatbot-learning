import streamlit as st
import openai
import os
from dotenv import load_dotenv

# .env 파일에서 API 키 로드
def get_api_key():
    openai_api_key = st.secrets['openai']['api_key']
    if openai_api_key:
        return openai_api_key
    # .env 파일이 없거나 키가 없으면 입력 받기
    return st.text_input('OpenAI API 키를 입력하세요', type='password')

# ChatGPT API 호출 함수
def generate_learning_material(prompt, difficulty, api_key):
    system_prompt = f"""
    당신은 교사의 요청을 분석하여 맞춤형 학습 자료(개념 설명, 연습 문제, 연습 문제 해설)를 생성하는 AI입니다. 
    반드시 학습과 관련된 요청에만 답변하세요.
    요청에 따라 아래와 같이 답변을 구성하세요:
    1. 개념 설명
    2. 연습 문제({difficulty} 난이도)
    3. 연습 문제 해설
    """
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": prompt}
    ]
    try:
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages,
            max_tokens=1200,
            temperature=0.7
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"오류 발생: {e}"

# md 파일로 저장
def save_to_md(content):
    st.download_button(
        label="자료를 md 파일로 저장",
        data=content,
        file_name="learning_material.md",
        mime="text/markdown"
    )

# Streamlit UI
st.set_page_config(page_title="교사용 ChatGPT 학습자료 생성기", page_icon="📚", layout="centered", initial_sidebar_state="auto")
st.markdown("""
    <style>
    body {
        background-color: #f8f9fa;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("📚 ChatGPT 기반 맞춤형 학습자료 생성기")
st.write("교사의 요청을 입력하면 개념 설명, 연습 문제, 해설을 자동으로 생성합니다. (학습 관련 요청만 가능)")

difficulty = st.selectbox('난이도 선택', ['초급', '중급', '고급'])
prompt = st.text_area('학습 자료로 만들 요청을 입력하세요', height=120)
api_key = get_api_key()

if api_key:
    openai.api_key = api_key
    if st.button('학습 자료 생성'):
        with st.spinner('자료 생성 중...'):
            result = generate_learning_material(prompt, difficulty, api_key)
        st.markdown(result)
        save_to_md(result)
else:
    st.info('OpenAI API 키를 입력하거나 secret 파일을 준비해 주세요.')
