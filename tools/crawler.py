import requests
from bs4 import BeautifulSoup


def fetch_webpage(url: str) -> str:
    """
    URL에서 HTML을 가져오는 함수
    """
    try:
        headers = {
            "User-Agent": "Mozilla/5.0"
        }
        response = requests.get(url, headers=headers, timeout=10)

        if response.status_code != 200:
            print(f"[ERROR] Failed to fetch page: {response.status_code}")
            return ""

        return response.text

    except Exception as e:
        print(f"[ERROR] Exception occurred: {e}")
        return ""


def extract_text(html: str) -> str:
    """
    HTML에서 의미 있는 텍스트만 추출
    """
    try:
        soup = BeautifulSoup(html, "html.parser")

        # 불필요한 태그 제거
        for tag in soup(["script", "style", "header", "footer", "nav", "aside"]):
            tag.decompose()

        text = soup.get_text(separator="\n")

        # 공백 정리
        lines = [line.strip() for line in text.splitlines()]
        lines = [line for line in lines if line]

        return "\n".join(lines)

    except Exception as e:
        print(f"[ERROR] Text extraction failed: {e}")
        return ""


def crawl(url: str) -> str:
    """
    전체 크롤링 파이프라인
    """
    html = fetch_webpage(url)

    if not html:
        return ""

    text = extract_text(html)
    return text


# 테스트용 실행
if __name__ == "__main__":
    test_url = "https://toss.im/career/job-detail?job_id=4071413003&sub_position_id=4071413003&company=%ED%86%A0%EC%8A%A4"  # 여기 원하는 URL 넣어
    result = crawl(test_url)

    print("\n[CRAWLED TEXT]\n")
    print(result[:1000])  # 너무 길어서 1000자만 출력