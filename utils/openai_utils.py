import json
import re
from openai import OpenAI
from config import OPENAI_API_KEY, OPENAI_MODEL, OPENAI_TEMPERATURE, OPENAI_MAX_TOKENS

client = OpenAI(api_key=OPENAI_API_KEY)


def parse_json_response(content: str, fallback: dict | None = None) -> dict:
    """모델 응답에서 JSON 블록을 안전하게 추출하고 파싱합니다."""
    if fallback is None:
        fallback = {}

    if not content:
        return fallback

    content = content.strip()
    match = re.search(r"\{.*\}", content, re.DOTALL)
    if not match:
        return fallback

    try:
        return json.loads(match.group())
    except json.JSONDecodeError:
        return fallback


def create_chat_completion(messages: list[dict], model: str | None = None, temperature: float | None = None, max_tokens: int | None = None) -> str:
    """OpenAI ChatCompletion 호출을 표준화합니다."""
    response = client.chat.completions.create(
        model=model or OPENAI_MODEL,
        messages=messages,
        temperature=temperature if temperature is not None else OPENAI_TEMPERATURE,
        max_tokens=max_tokens or OPENAI_MAX_TOKENS,
    )
    return (response.choices[0].message.content or "").strip()
