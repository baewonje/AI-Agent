import os
from openai import OpenAI
from dotenv import load_dotenv

# 환경 변수 로드
load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


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
    



    