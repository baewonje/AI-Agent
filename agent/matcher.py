import os
import json
import re
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def match_resume_to_jd(resume_text, jd_text):
    prompt = f"""
이력서와 채용 공고를 비교하여 적합도를 평가해라.

JSON 형식으로:
{{
  "score": 0~100,
  "reason": "한 줄 설명",
  "improvement": "개선점 한 줄"
}}

[이력서]
{resume_text}

[JD]
{jd_text}
"""

    res = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "채용 매칭 전문가"},
            {"role": "user", "content": prompt}
        ],
        temperature=0.3
    )

    content = (res.choices[0].message.content or "").strip()
    if not content:
        print("[matcher] Empty model response")
        return {
            "score": 0,
            "reason": "모델 응답이 없습니다.",
            "improvement": "다시 시도해주세요."
        }

    json_match = re.search(r"\{.*\}", content, re.DOTALL)
    if not json_match:
        print(f"[matcher] Invalid JSON response:\n{content}")
        return {
            "score": 0,
            "reason": "모델 응답이 JSON 형식이 아닙니다.",
            "improvement": "응답을 다시 확인하거나 지시문을 수정하세요."
        }

    try:
        return json.loads(json_match.group())
    except json.JSONDecodeError as e:
        print(f"[matcher] JSON decode error: {e}\nRaw response:\n{content}")
        return {
            "score": 0,
            "reason": "JSON 파싱 실패",
            "improvement": "모델 응답을 다시 확인하세요."
        }