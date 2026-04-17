import streamlit as st
import time
import pandas as pd

from tools.crawler import crawl
from tools.jd_generator import generate_jd, summarize_company
from tools.search import search
from tools.pdf_parser import extract_text_from_pdf

from agent.evaluator import evaluate_jd
from agent.decision import decide_action
from agent.planner import create_plan
from agent.matcher import match_resume_to_jd
from agent.cover_letter import generate_cover_letter


st.set_page_config(page_title="AI JD Agent", layout="wide")

st.title("🤖 AI JD Generator Agent")
st.markdown("URL 하나로 채용 공고를 분석하고 최적의 JD를 생성합니다.")

url = st.text_input("🔗 채용 공고 URL 입력")
uploaded_file = st.file_uploader("📄 이력서 PDF 업로드 (선택)", type=["pdf"])


if st.button("🚀 분석 시작"):

    if not url:
        st.warning("URL을 입력해주세요")
        st.stop()

    progress = st.progress(0)
    status = st.empty()

    # 1. 크롤링
    status.text("📡 데이터 수집 중...")
    content = crawl(url)

    # 🔥 텍스트 검증
    if not content or len(content.strip()) < 100:
        st.error("❌ 텍스트 기반 채용공고만 지원됩니다. 이 페이지는 JavaScript 렌더링이 필요하거나 크롤링에 실패했을 수 있습니다.")
        st.markdown("**추출된 텍스트 길이:** {}자".format(len(content.strip())))
        if content:
            st.code(content[:1000])
        st.stop()

    progress.progress(20)

    # 🔥 회사 정보 검색
    status.text("🏢 회사 정보 분석 중...")
    company_query = f"{url} 회사 인원수 매출 평균연봉"
    company_info = search(company_query)

    company_context = "\n".join([
        f"{r['title']} - {r['body']}"
        for r in company_info
    ])

    company_summary = summarize_company(company_context)

    # 🔥 PDF 있을 경우만 처리
    if uploaded_file is not None:
        resume_text = extract_text_from_pdf(uploaded_file)
        tab1, tab2, tab3 = st.tabs(["📊 직무 분석", "🎯 적합도", "✍️ 자기소개서"])
    else:
        tab1 = st.tabs(["📊 직무 분석"])[0]

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

    # 🔥 Agent Loop
    for i in range(max_iterations):
        status.text(f"🧠 JD 생성 및 개선 중... ({i+1}/{max_iterations})")
        state["iteration"] = i

        jd_input = content + "\n\n[회사 정보]\n" + company_context

        jd = generate_jd(jd_input, feedback)
        result = evaluate_jd(jd)

        score = result["score"]

        if score > best_score:
            best_score = score
            best_jd = jd

        feedback = result["feedback"]

        results.append((i+1, score, feedback))

        progress.progress(int((i+1) / max_iterations * 100))
        time.sleep(1)

        decision = decide_action(state)

        action = decision["action"]
        reason = decision["reason"]

        st.caption(f"🧠 {action.upper()} - {reason}")

        if action == "search":
            status.text("🔍 추가 정보 검색 중...")

            search_results = search(url)

            search_context = "\n".join([
                r["title"] + " " + r["body"]
                for r in search_results
            ])

            content += "\n\n[SEARCH]\n" + search_context

        elif action == "stop":
            break

    progress.progress(100)
    status.text("✅ 완료!")

    # 데이터 정리
    iterations = [r[0] for r in results]
    scores = [r[1] for r in results]

    df = pd.DataFrame({
        "Iteration": iterations,
        "Score": scores
    })

    # =========================
    # 📊 TAB 1: 직무 분석
    # =========================
    with tab1:
        st.subheader("📊 JD 분석")

        col1, col2, col3 = st.columns(3)
        col1.metric("최고 점수", best_score)
        col2.metric("반복 횟수", len(results))
        col3.metric("최종 점수", scores[-1])

        st.line_chart(df.set_index("Iteration"))

        st.subheader("🏢 회사 정보")
        st.info(company_summary)

        st.subheader("🏆 Best JD")
        st.success(best_jd)

        st.subheader("📊 개선 과정")
        for r in results:
            st.write(f"Iteration {r[0]} → Score: {r[1]}")
            st.caption(f"{r[2]}")

    # =========================
    # 🎯 TAB 2: 적합도 (PDF 있을 때만)
    # =========================
    if uploaded_file is not None:
        with tab2:
            st.subheader("🎯 이력서 적합도")

            match_result = match_resume_to_jd(resume_text, best_jd)

            st.metric("적합도", f"{match_result['score']}%")
            st.info(match_result["reason"])
            st.warning("개선점: " + match_result["improvement"])

    # =========================
    # ✍️ TAB 3: 자기소개서
    # =========================
    if uploaded_file is not None:
        with tab3:
            st.subheader("✍️ 자기소개서")

            cover_letter = generate_cover_letter(resume_text, best_jd)
            st.write(cover_letter)