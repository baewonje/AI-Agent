import os
from openai import OpenAI
from dotenv import load_dotenv

# 환경 변수 로드
load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def summarize_company(info_text):
    prompt = f"""
다음 회사 검색 결과를 기반으로 한국어로 정리해줘.

항목:
- 회사 개요
- 예상 규모 (직원수)
- 매출 정보 (있으면)
- 평균 연봉 (있으면)

반드시 한국어로 짧게 정리해라.

[데이터]
{info_text}
"""

    res = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "너는 기업 분석 전문가다."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.3
    )

    return res.choices[0].message.content

def generate_jd(content: str, feedback: str = "") -> str:
    """
    크롤링된 텍스트를 기반으로 JD 생성
    """

    if not content:
        return "[ERROR] No content provided."

    prompt = f"""
    아래 내용을 기반으로 채용 공고(Job Description)를 작성해줘.

    [요구사항]
    - 직무 개요
    - 주요 업무
    - 자격 요건
    - 우대 사항

    [개선 피드백]
    {feedback}

    [내용]
    {content[:3000]}
    """

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "너는 채용 공고를 잘 작성하는 HR 전문가다."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7
        )

        return response.choices[0].message.content

    except Exception as e:
        return f"[ERROR] JD generation failed: {e}"
    



    