import streamlit as st
import time
from tools.crawler import crawl
from tools.jd_generator import generate_jd
from agent.evaluator import evaluate_jd


st.set_page_config(page_title="AI JD Agent", layout="centered")

st.title("🤖 AI JD Generator Agent")
st.markdown("URL 하나로 채용 공고를 분석하고 최적의 JD를 생성합니다.")

url = st.text_input("🔗 채용 공고 URL 입력")

if st.button("🚀 분석 시작"):

    if not url:
        st.warning("URL을 입력해주세요")
        st.stop()

    progress = st.progress(0)
    status = st.empty()

    # 1. 크롤링
    status.text("📡 데이터 수집 중...")
    content = crawl(url)
    progress.progress(20)

    score = 0
    feedback = ""

    results = []

    # 2. Agent Loop
    for i in range(3):
        status.text(f"🧠 JD 생성 및 개선 중... ({i+1}/3)")

        jd = generate_jd(content, feedback)
        result = evaluate_jd(jd)

        score = result["score"]
        feedback = result["feedback"]

        results.append((i+1, score, feedback))

        progress.progress(40 + i*20)
        time.sleep(1)  # UX용

        if score >= 90:
            break

    progress.progress(100)
    status.text("✅ 완료!")

    st.success("분석 완료!")

    # 결과 출력
    st.subheader("📊 개선 과정")
    for r in results:
        st.write(f"Iteration {r[0]} → Score: {r[1]}")
        st.caption(f"Feedback: {r[2]}")

    st.subheader("📄 최종 JD")
    st.write(jd)