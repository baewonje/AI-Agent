import requests
from bs4 import BeautifulSoup
import json
from utils.logging_utils import logger


def fetch_webpage(url: str) -> str:
    """
    URL에서 HTML을 가져오는 함수
    """
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
            "Accept-Language": "ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8"
        }

        response = requests.get(url, headers=headers, timeout=15)

        if response.status_code != 200:
            logger.error(f"Failed to fetch page: {response.status_code} for URL: {url}")
            return ""

        logger.info(f"Successfully fetched {len(response.text)} characters from {url}")
        return response.text

    except Exception as e:
        logger.error(f"Exception occurred while fetching {url}: {e}")
        return ""


def extract_next_data(soup) -> str:
    """
    Next.js 기반 사이트(JSON 데이터) 추출
    """
    try:
        script = soup.find("script", {"id": "__NEXT_DATA__"})
        if not script:
            return ""

        data = json.loads(script.string)

        # 🔥 필요한 텍스트만 추출 (전체 dump X)
        texts = []

        def extract_text_recursive(obj):
            if isinstance(obj, dict):
                for v in obj.values():
                    extract_text_recursive(v)
            elif isinstance(obj, list):
                for v in obj:
                    extract_text_recursive(v)
            elif isinstance(obj, str):
                if len(obj) > 30:  # 의미 있는 문장만
                    texts.append(obj)

        extract_text_recursive(data)

        return "\n".join(texts)

    except Exception as e:
        logger.error(f"NEXT_DATA parsing failed: {e}")
        return ""


def extract_text(html: str) -> str:
    """
    HTML에서 의미 있는 텍스트만 추출
    """
    try:
        logger.debug(f"Extracting text from HTML ({len(html)} characters)")
        soup = BeautifulSoup(html, "html.parser")

        # 🔥 1️⃣ Next.js 사이트 대응 (핵심)
        next_data_text = extract_next_data(soup)
        if len(next_data_text) > 200:
            logger.info("Using NEXT.js data extraction")
            return next_data_text

        # 🔥 2️⃣ 불필요한 태그 제거
        for tag in soup(["script", "style", "header", "footer", "nav", "aside", "noscript", "iframe"]):
            tag.decompose()

        def normalize(text: str) -> str:
            lines = [line.strip() for line in text.splitlines()]
            lines = [line for line in lines if line]
            return "\n".join(lines)

        # 🔥 3️⃣ article 우선
        article = soup.find("article")
        if article:
            article_text = normalize(article.get_text(separator="\n"))
            if len(article_text) >= 200:
                return article_text

        # 🔥 4️⃣ 전체 텍스트 fallback
        page_text = normalize(soup.get_text(separator="\n"))
        if len(page_text) >= 200:
            return page_text

        # 🔥 5️⃣ 마지막 fallback (의미 있는 태그)
        elements = soup.find_all(["h1", "h2", "h3", "p", "li"])
        parts = [elem.get_text(strip=True) for elem in elements if elem.get_text(strip=True)]

        return "\n".join(parts)

    except Exception as e:
        logger.error(f"Text extraction failed: {e}")
        return ""


def crawl(url: str) -> str:
    """
    전체 크롤링 파이프라인
    """
    logger.info(f"Starting crawl for URL: {url}")
    html = fetch_webpage(url)

    if not html:
        logger.warning(f"No HTML content retrieved for {url}")
        return ""

    text = extract_text(html)

    # 🔥 최종 방어 (너 app.py랑 연결됨)
    if not text or len(text.strip()) < 100:
        logger.warning(f"Low quality or empty content extracted from {url} (length: {len(text.strip())})")
        return ""

    logger.info(f"Successfully crawled {len(text)} characters from {url}")
    return text


# 테스트용 실행
if __name__ == "__main__":
    test_url = "https://toss.im/career/job-detail?job_id=4071413003"

    result = crawl(test_url)

    print("\n[CRAWLED TEXT]\n")
    print(result[:1000])