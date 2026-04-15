from ddgs import DDGS

def search(query: str, max_results: int = 5):
    results = []

    with DDGS() as ddgs:
        for r in ddgs.text(query, max_results=max_results):
            results.append({
                "title": r["title"],
                "body": r["body"],
                "url": r["href"]
            })

    return results