import os
from dotenv import load_dotenv

load_dotenv()

# OpenAI 설정
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
OPENAI_TEMPERATURE = float(os.getenv("OPENAI_TEMPERATURE", "0.3"))
OPENAI_MAX_TOKENS = int(os.getenv("OPENAI_MAX_TOKENS", "1500"))

# 검색 및 크롤링 설정
SEARCH_MAX_RESULTS = int(os.getenv("SEARCH_MAX_RESULTS", "5"))
CRAWL_TIMEOUT = int(os.getenv("CRAWL_TIMEOUT", "15"))
USER_AGENT = os.getenv("USER_AGENT", "Mozilla/5.0 (Windows NT 10.0; Win64; x64)")

# 검증
if not OPENAI_API_KEY:
    raise EnvironmentError("OPENAI_API_KEY 환경 변수가 설정되지 않았습니다.")

if not (0.0 <= OPENAI_TEMPERATURE <= 2.0):
    raise ValueError(f"OPENAI_TEMPERATURE는 0.0-2.0 범위여야 합니다. 현재: {OPENAI_TEMPERATURE}")

if not (100 <= OPENAI_MAX_TOKENS <= 4000):
    raise ValueError(f"OPENAI_MAX_TOKENS는 100-4000 범위여야 합니다. 현재: {OPENAI_MAX_TOKENS}")

if not (1 <= SEARCH_MAX_RESULTS <= 20):
    raise ValueError(f"SEARCH_MAX_RESULTS는 1-20 범위여야 합니다. 현재: {SEARCH_MAX_RESULTS}")

if not (5 <= CRAWL_TIMEOUT <= 60):
    raise ValueError(f"CRAWL_TIMEOUT은 5-60초 범위여야 합니다. 현재: {CRAWL_TIMEOUT}")
