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
from agent.cover_letter import generate_cover_letter_with_agent


st.set_page_config(page_title="AI JD Agent", layout="wide")

st.title("🤖 AI JD Generator Agent")
st.markdown("URL 하나로 채용 공고를 분석하고 최적의 JD를 생성합니다.")

url = st.text_input("🔗 채용 공고 URL 입력")
uploaded_file = st.file_uploader("📄 이력서 PDF 업로드 (선택)", type=["pdf"])

if "analysis_started" not in st.session_state:
    st.session_state.analysis_started = False

if "analysis_result" not in st.session_state:
    st.session_state.analysis_result = {}

start_analysis = st.button("🚀 분석 시작")
if start_analysis:
    st.session_state.analysis_started = True
    st.session_state.analysis_result = {}


if st.session_state.analysis_started:

    if not url:
        st.warning("URL을 입력해주세요")
        st.stop()

    progress = st.progress(0)
    status = st.empty()

    if not st.session_state.analysis_result:
        # 1. 크롤링
        status.text("📡 데이터 수집 중...")
        try:
            content = crawl(url)
        except Exception as e:
            st.error(f"❌ 크롤링 중 오류가 발생했습니다: {str(e)}")
            st.info("💡 다른 URL을 시도하거나 페이지를 새로고침해 보세요.")
            st.stop()

        # 🔥 텍스트 검증
        if not content or len(content.strip()) < 100:
            st.error("❌ 텍스트 기반 채용공고만 지원됩니다. 이 페이지는 JavaScript 렌더링이 필요하거나 크롤링에 실패했을 수 있습니다.")
            st.markdown("**추출된 텍스트 길이:** {}자".format(len(content.strip())))
            if content:
                with st.expander("추출된 텍스트 미리보기"):
                    st.code(content[:1000])
            st.info("💡 다른 채용 사이트나 더 간단한 페이지를 시도해 보세요.")
            st.stop()

        progress.progress(20)

        # 🔥 회사 정보 검색
        status.text("🏢 회사 정보 분석 중...")
        try:
            company_query = f"{url} 회사 인원수 매출 평균연봉"
            company_info = search(company_query)

            company_context = "\n".join([
                f"{r['title']} - {r['body']}"
                for r in company_info
            ])

            company_summary = summarize_company(company_context)
        except Exception as e:
            st.warning(f"⚠️ 회사 정보 검색 중 오류가 발생했습니다: {str(e)}")
            company_summary = "회사 정보를 가져올 수 없습니다."
            company_context = ""

        progress.progress(30)

        # 🔥 PDF 처리
        resume_text = ""
        if uploaded_file is not None:
            status.text("📄 이력서 분석 중...")
            try:
                resume_text = extract_text_from_pdf(uploaded_file)
                if not resume_text or len(resume_text.strip()) < 50:
                    st.warning("⚠️ PDF에서 텍스트를 충분히 추출하지 못했습니다. 스캔된 이미지나 복잡한 레이아웃의 PDF는 지원되지 않을 수 있습니다.")
                    resume_text = ""
            except Exception as e:
                st.error(f"❌ PDF 처리 중 오류가 발생했습니다: {str(e)}")
                st.info("💡 다른 PDF 파일을 시도하거나 텍스트 기반 이력서를 사용해 보세요.")
                resume_text = ""

            progress.progress(40)

        # 탭 설정
        if uploaded_file is not None and resume_text:
            tab1, tab2, tab3 = st.tabs(["📊 직무 분석", "🎯 이력서 적합도", "✍️ 자기소개서"])
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

        st.session_state.analysis_result = {
            "content": content,
            "company_summary": company_summary,
            "company_context": company_context,
            "resume_text": resume_text,
            "best_score": best_score,
            "best_jd": best_jd,
            "results": results,
            "iterations": [r[0] for r in results],
            "scores": [r[1] for r in results]
        }

        iterations = st.session_state.analysis_result["iterations"]
        scores = st.session_state.analysis_result["scores"]

        df = pd.DataFrame({
            "Iteration": iterations,
            "Score": scores
        })
    else:
        content = st.session_state.analysis_result["content"]
        company_summary = st.session_state.analysis_result["company_summary"]
        company_context = st.session_state.analysis_result["company_context"]
        resume_text = st.session_state.analysis_result["resume_text"]
        best_score = st.session_state.analysis_result["best_score"]
        best_jd = st.session_state.analysis_result["best_jd"]
        results = st.session_state.analysis_result["results"]
        iterations = st.session_state.analysis_result["iterations"]
        scores = st.session_state.analysis_result["scores"]

        if uploaded_file is not None and resume_text:
            tab1, tab2, tab3 = st.tabs(["📊 직무 분석", "🎯 이력서 적합도", "✍️ 자기소개서"])
        else:
            tab1 = st.tabs(["📊 직무 분석"])[0]

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
    # ✍️ TAB 3: 자기소개서 (PDF 있을 때만)
    # =========================
    if uploaded_file is not None:
        with tab3:
            st.subheader("✍️ AI 자기소개서 생성")

            # 자기소개서 생성 버튼
            if st.button("🤖 AI 분석으로 자기소개서 생성", key="generate_cl"):
                with st.spinner("AI가 이력서를 분석하고 최적의 자기소개서를 생성하는 중..."):
                    cover_letter, cl_results = generate_cover_letter_with_agent(resume_text, best_jd)

                # 결과 표시
                st.success("✅ 최적의 자기소개서가 생성되었습니다!")

                # 평가 결과 요약
                if cl_results:
                    col1, col2, col3 = st.columns(3)
                    best_cl_score = max(r[1] for r in cl_results)
                    col1.metric("최고 점수", best_cl_score)
                    col2.metric("반복 횟수", len(cl_results))
                    col3.metric("최종 점수", cl_results[-1][1])

                    # 개선 과정 차트
                    cl_iterations = [r[0] for r in cl_results]
                    cl_scores = [r[1] for r in cl_results]
                    cl_df = pd.DataFrame({"Iteration": cl_iterations, "Score": cl_scores})
                    st.line_chart(cl_df.set_index("Iteration"))

                # 최종 자기소개서
                st.subheader("📝 최종 자기소개서")
                st.write(cover_letter)

                # 개선 과정 상세
                with st.expander("📊 자기소개서 개선 과정"):
                    for r in cl_results:
                        st.write(f"Iteration {r[0]} → Score: {r[1]}")
                        st.caption(f"{r[2]}")