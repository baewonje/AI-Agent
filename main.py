from tools.crawler import crawl
from tools.jd_generator import generate_jd
from agent.evaluator import evaluate_jd


if __name__ == "__main__":
    url = input("URL 입력: ")

    print("\n[1] 크롤링 중...")
    content = crawl(url)

    score = 0
    feedback = ""
    max_iterations = 3

    for i in range(max_iterations):
        print(f"\n[2] JD 생성 중... (시도 {i+1})")
        jd = generate_jd(content, feedback)

        print("\n[3] JD 평가 중...")
        result = evaluate_jd(jd)

        score = result["score"]
        feedback = result["feedback"]

        print(f"\n[점수]: {score}")
        print(f"[피드백]: {feedback}")

        if score >= 90:
            print("\n✅ 충분히 좋은 JD 도달!")
            break

    print("\n======================")
    print("[최종 JD]\n")
    print(jd)