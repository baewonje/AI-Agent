import streamlit as st
import time
from tools.crawler import crawl
from tools.jd_generator import generate_jd
from agent.evaluator import evaluate_jd
import pandas as pd
from agent.decision import decide_action
from tools.search import search
from agent.planner import create_plan

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

    # 🔥 1. 회사 정보 추가 (NEW)
    status.text("🏢 회사 정보 분석 중...")

    company_query = f"{url} 회사 인원수 매출 평균연봉"
    company_info = search(company_query)

    company_context = "\n".join([
        f"{r['title']} - {r['body']}"
        for r in company_info
    ])

    st.subheader("🏢 회사 정보")
    st.write(company_context)

    score = 0
    feedback = ""

    results = []
    max_iterations = 3

    state = {
        "score": score,
        "iteration": 1,
        "content": content[:1000]
    }

    best_score = 0
    best_jd = ""

    # 2. Agent Loop
    for i in range(max_iterations):
        status.text(f"🧠 JD 생성 및 개선 중... ({i+1}/{max_iterations})")
        state["iteration"] = i

        # 🔥 회사 정보 포함해서 JD 생성
        jd_input = content + "\n\n[회사 정보]\n" + company_context

        jd = generate_jd(jd_input, feedback)
        result = evaluate_jd(jd)

        score = result["score"]

        if score > best_score:
            best_score = score
            best_jd = jd

        plan = create_plan(state)

        st.write("📋 Plan")
        st.write(plan["goal"])
        st.write(plan["plan"])

        feedback = result["feedback"]

        results.append((i+1, score, feedback))

        progress.progress(int((i+1) / max_iterations * 100))
        time.sleep(1)

        decision = decide_action(state)

        action = decision["action"]
        reason = decision["reason"]

        st.info(f"🧠 {action.upper()}")
        st.caption(reason)

        if action == "search":
            status.text("🔍 검색 중...")

            search_results = search(url)

            search_context = "\n".join([
                r["title"] + " " + r["body"]
                for r in search_results
            ])

            content += "\n\n[SEARCH]\n" + search_context


        elif action == "stop":
            st.success("Agent 종료 (품질 충분)")
            break

    progress.progress(100)
    status.text("✅ 완료!")

    st.success("분석 완료!")

    # 데이터 준비
    iterations = [r[0] for r in results]
    scores = [r[1] for r in results]

    df = pd.DataFrame({
        "Iteration": iterations,
        "Score": scores
    })

    st.subheader("📈 Score Improvement")
    st.line_chart(df.set_index("Iteration"))

    st.metric(label="최고 점수", value=best_score)

    # 결과 출력
    st.subheader("📊 개선 과정")
    for r in results:
        st.write(f"Iteration {r[0]} → Score: {r[1]}")
        st.caption(f"Feedback: {r[2]}")

    st.subheader("🏆 최고 JD (Best Result)")
    st.write(best_jd)

    st.subheader("📄 최종 JD (Last Result)")
    st.write(jd)