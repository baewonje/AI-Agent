import os
from openai import OpenAI
from dotenv import load_dotenv
import json

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def decide_action(state: dict):
    """
    state = {
        "score": 현재 점수,
        "iteration": 몇 번째 반복,
        "content": JD 내용 요약
    }
    """

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

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "너는 한국어로만 답하는 채용 공고 분석 AI다."},
            {"role": "user", "content": prompt}
        ],
        temperature=0
    )

    return json.loads(response.choices[0].message.content)