from utils.openai_utils import create_chat_completion


def generate_cover_letter(resume_text: str, jd_text: str) -> str:
    """이력서와 JD를 기반으로 자기소개서를 생성합니다."""

    prompt = f"""
이력서와 채용 공고를 기반으로 자기소개서를 작성해라.

- 한국어
- 500~800자
- 자연스럽고 설득력 있게

[이력서]
{resume_text}

[JD]
{jd_text}
"""

    return create_chat_completion(
        messages=[
            {"role": "system", "content": "자기소개서 전문가"},
            {"role": "user", "content": prompt}
        ],
        temperature=0.7,
        max_tokens=1200
    )