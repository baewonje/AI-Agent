from utils.openai_utils import create_chat_completion
from agent.cover_letter_evaluator import evaluate_cover_letter, decide_cover_letter_action


def extract_resume_strengths(resume_text: str) -> str:
    """이력서에서 주요 강점과 키워드를 추출합니다."""
    prompt = f"""
이력서 내용을 분석하여 지원자의 주요 강점과 핵심 키워드를 1-2줄로 요약해라.

[요구사항]
- 언어: 한국어
- 형식: "이력서의 강점은 [키워드1, 키워드2, 키워드3]이며, 이를 살려서 더 수정하면 좋다."
- 길이: 50자 이내
- 내용: 실제 이력서에서 나온 구체적인 역량이나 경험 기반

[이력서 내용]
{resume_text}
"""

    return create_chat_completion(
        messages=[
            {"role": "system", "content": "당신은 HR 전문가로, 이력서의 강점을 간결하게 요약합니다."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.3,
        max_tokens=100
    )


def generate_cover_letter(resume_text: str, jd_text: str, feedback: str = "") -> str:
    """이력서와 JD를 기반으로 고품질 자기소개서를 생성합니다."""

    prompt = f"""
이력서와 채용 공고를 기반으로 전문적인 자기소개서를 작성해라.

[요구사항]
- 언어: 한국어 (격식 있고 전문적인 톤)
- 길이: 800~1200자 (충분한 내용 포함)
- 구조: 서론 + 본론(경험/역량) + 결론 + 마무리
- 스타일: 자연스럽고 설득력 있게, 구체적인 사례 포함

[자기소개서 구조]
1. 서론 (150-200자)
   - 인사 및 지원 동기
   - 해당 포지션에 대한 관심 표현

2. 본론 (500-800자)
   - 관련 경험 및 성과 (구체적인 사례 2-3개)
   - 보유 역량 및 강점
   - 회사/직무에 대한 이해도
   - 기여할 수 있는 부분

3. 결론 (150-200자)
   - 포부 및 비전
   - 마무리 인사

[중요 포인트]
- 구체적인 숫자나 성과를 포함 (예: "프로젝트 완료율 95% 달성")
- JD의 요구사항과 본인의 역량을 연결
- 열정과 성장 가능성을 강조
- 문법적으로 완벽하고 자연스러운 한국어 사용

[개선 피드백]
{feedback}

[이력서 내용]
{resume_text}

[채용 공고 내용]
{jd_text}
"""

    return create_chat_completion(
        messages=[
            {"role": "system", "content": "당신은 10년 경력의 HR 전문가이자 자기소개서 컨설턴트입니다. 지원자의 강점을 최대한 부각시키고, 채용 담당자를 설득할 수 있는 자기소개서를 작성합니다."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.7,
        max_tokens=2000
    )


def generate_cover_letter_with_agent(resume_text: str, jd_text: str, max_iterations: int = 3) -> tuple[str, list, str]:
    """AI 에이전트 방식으로 자기소개서를 반복 개선합니다."""

    # 이력서 강점 추출
    resume_strengths = extract_resume_strengths(resume_text)

    score = 0
    feedback = ""
    results = []
    best_score = 0
    best_cover_letter = ""

    for i in range(max_iterations):
        # 자기소개서 생성
        cover_letter = generate_cover_letter(resume_text, jd_text, feedback)

        # 평가
        result = evaluate_cover_letter(cover_letter, resume_text, jd_text)
        score = result["score"]

        if score > best_score:
            best_score = score
            best_cover_letter = cover_letter

        feedback = result["feedback"]
        results.append((i+1, score, feedback))

        # 개선 결정
        state = {
            "score": score,
            "iteration": i+1,
            "content_length": len(cover_letter),
            "feedback": feedback
        }

        decision = decide_cover_letter_action(state)
        action = decision["action"]

        if action == "stop" or score >= 90:
            break

    return best_cover_letter, results, resume_strengths