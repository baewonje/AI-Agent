import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def evaluate_jd(jd_text: str) -> dict:
    """
    JD 품질을 평가하고 점수를 반환
    """

    if not jd_text:
        return {"score": 0, "feedback": "No JD provided"}

    prompt = f"""
    아래 채용 공고(Job Description)를 평가해줘.

    [평가 기준]
    1. 직무 설명이 명확한가 (0~25)
    2. 주요 업무가 구체적인가 (0~25)
    3. 자격 요건이 현실적인가 (0~25)
    4. 전체적으로 완성도가 높은가 (0~25)

    총점 100점 기준으로 점수를 매기고,
    부족한 점을 간단히 피드백으로 작성해줘.

    반드시 아래 JSON 형식으로만 답해:
    {{
        "score": 점수,
        "feedback": "피드백 내용"
    }}

    [JD]
    {jd_text}
    """

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "너는 채용 공고를 평가하는 전문가다."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3
        )

        content = response.choices[0].message.content

        # JSON 파싱
        import json
        return json.loads(content)

    except Exception as e:
        return {"score": 0, "feedback": f"Evaluation failed: {e}"}