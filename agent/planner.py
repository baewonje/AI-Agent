import json
from utils.openai_utils import create_chat_completion, parse_json_response


def create_plan(state: dict):
    """
    state = {
        "score": 현재 점수,
        "iteration": 몇 번째 loop,
        "content": JD 요약
    }
    """

    prompt = f"""
You are a planning agent.

Your job is to create a step-by-step plan to improve a Job Description.

Current state:
{json.dumps(state, ensure_ascii=False)}

You must decide:
- what to improve
- whether to use search
- what to focus on next

Return ONLY JSON:

{{
  "plan": [
    "step 1",
    "step 2",
    "step 3"
  ],
  "goal": "short goal for this iteration"
}}
"""

    content = create_chat_completion(
        messages=[
            {"role": "system", "content": "너는 한국어로만 답하는 채용 공고 분석 AI다."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.3
    )

    return parse_json_response(content, fallback={"plan": [], "goal": "plan parsing failed"})