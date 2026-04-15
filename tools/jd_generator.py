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
    



    