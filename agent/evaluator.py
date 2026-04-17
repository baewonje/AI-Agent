import json
import re
from utils.openai_utils import create_chat_completion, parse_json_response


def evaluate_jd(jd_text: str):
    

    prompt = f"""
    아래 채용 공고(Job Description)를 평가해라.

    [평가 기준]
    1. 직무 설명 명확성 (0~25)
    2. 주요 업무 구체성 (0~25)
    3. 자격 요건 현실성 (0~25)
    4. 전체 완성도 (0~25)

    총점 100점 기준으로 평가하라.

    [출력 형식]
    반드시 JSON 형식으로만 답해라:
    {{
        "score": 점수,
        "feedback": "한 문장, 최대 20자 이내"
    }}

    [JD]
    {jd_text}
    """

    content = create_chat_completion(
        messages=[
            {"role": "system", "content": "너는 JD 평가 전문가다."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.2
    )
    

    return parse_json_response(content, fallback={"score": 0, "feedback": "parse error"})