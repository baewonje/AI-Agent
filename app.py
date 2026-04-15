import streamlit as st
import time
from tools.crawler import crawl
from tools.jd_generator import generate_jd
from agent.evaluator import evaluate_jd
import pandas as pd

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
    max_iterations  = 5
    # 2. Agent Loop
    for i in range(max_iterations):
        status.text(f"🧠 JD 생성 및 개선 중... ({i+1}/{max_iterations})")

        jd = generate_jd(content, feedback)
        result = evaluate_jd(jd)

        score = result["score"]
        feedback = result["feedback"]

        results.append((i+1, score, feedback))

        progress.progress(int((i+1) / max_iterations * 100))
        time.sleep(1)  # UX용

        if score >= 90:
            break

    progress.progress(100)
    status.text("✅ 완료!")

    st.success("분석 완료!")


    # 데이터 준비
    iterations = [r[0] for r in results]
    scores = [r[1] for r in results]

    # 데이터프레임 생성
    df = pd.DataFrame({
        "Iteration": iterations,
        "Score": scores
    })

    # 그래프 출력
    st.subheader("📈 Score Improvement")
    st.line_chart(df.set_index("Iteration"))
    st.metric(label="최종 점수", value=score)
    best_score = max(scores)
    st.metric(label="최고 점수", value=best_score)

    # 결과 출력
    st.subheader("📊 개선 과정")
    for r in results:
        st.write(f"Iteration {r[0]} → Score: {r[1]}")
        st.caption(f"Feedback: {r[2]}")

    st.subheader("📄 최종 JD")
    st.write(jd)