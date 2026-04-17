import json
from utils.openai_utils import create_chat_completion, parse_json_response


def decide_action(state: dict) -> dict:
    """현재 상태를 기반으로 다음 행동을 결정합니다."""

    prompt = f"""
You are an AI agent controller.

Based on the current state, decide the NEXT action.

Actions:
- "generate" : improve JD
- "search" : gather external information
- "stop" : finish process

Rules:
- Be strict about efficiency.
- Avoid unnecessary search.
- Stop if quality is good enough.

State:
{json.dumps(state, ensure_ascii=False)}

Return ONLY JSON:
{{
  "action": "generate | search | stop",
  "reason": "max 10 words"
}}
"""

    content = create_chat_completion(
        messages=[
            {"role": "system", "content": "너는 한국어로만 답하는 채용 공고 분석 AI다."},
            {"role": "user", "content": prompt}
        ],
        temperature=0
    )

    return parse_json_response(content, fallback={"action": "stop", "reason": "parsing failed"})