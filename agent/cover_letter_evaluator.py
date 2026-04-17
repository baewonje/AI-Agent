import json
import re
from utils.openai_utils import create_chat_completion, parse_json_response


def evaluate_cover_letter(cover_letter_text: str, resume_text: str, jd_text: str) -> dict:
    """자기소개서의 품질을 평가합니다."""

    prompt = f"""
아래 자기소개서를 평가해라.

[평가 기준]
1. 내용의 구체성 (0~25) - 구체적인 사례와 성과 포함
2. JD 연관성 (0~25) - 채용 공고 요구사항과의 연결성
3. 구조 및 가독성 (0~25) - 논리적 구성과 자연스러운 흐름
4. 설득력 (0~25) - 지원자의 강점과 열정 표현

총점 100점 기준으로 평가하라.

[출력 형식]
반드시 JSON 형식으로만 답해라:
{{
    "score": 점수,
    "feedback": "한 문장, 최대 20자 이내"
}}

[자기소개서]
{cover_letter_text}

[이력서]
{resume_text}

[JD]
{jd_text}
"""

    content = create_chat_completion(
        messages=[
            {"role": "system", "content": "너는 자기소개서 평가 전문가다."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.2
    )

    return parse_json_response(content, fallback={"score": 0, "feedback": "parse error"})


def decide_cover_letter_action(state: dict) -> dict:
    """자기소개서 개선을 위한 다음 행동을 결정합니다."""

    prompt = f"""
자기소개서 개선을 위한 다음 행동을 결정해라.

현재 상태:
{json.dumps(state, ensure_ascii=False)}

행동 옵션:
- "improve" : 내용 개선
- "expand" : 길이 늘리기
- "refine" : 세부 사항 다듬기
- "stop" : 완료

규칙:
- 점수가 85점 이상이면 중단
- 내용이 너무 짧으면 확장
- 구조가 좋지 않으면 개선

Return ONLY JSON:
{{
  "action": "improve | expand | refine | stop",
  "reason": "max 10 words"
}}
"""

    content = create_chat_completion(
        messages=[
            {"role": "system", "content": "너는 자기소개서 개선 전문가다."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.3
    )

    return parse_json_response(content, fallback={"action": "stop", "reason": "parsing failed"})