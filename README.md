# 🤖 AI JD Agent

URL 하나로 채용 공고를 분석하고 최적의 JD를 생성하는 AI 에이전트

## ✨ 주요 기능

- **📡 자동 크롤링**: 채용 공고 URL에서 텍스트 자동 추출
- **🏢 회사 분석**: 회사 정보 자동 검색 및 요약
- **🧠 AI JD 생성**: 반복 학습으로 최적의 채용 공고 생성
- **📄 이력서 분석**: PDF 이력서 텍스트 추출 및 분석
- **🎯 적합도 평가**: 이력서-JD 매칭 점수 및 개선점 제공
- **✍️ AI 자기소개서**: 반복 분석으로 개인화된 자기소개서 생성

## 🚀 설치 및 실행

### 1. 환경 설정
```bash
# Python 3.8+ 권장
pip install -r requirements.txt
```

### 2. 환경 변수 설정
`.env` 파일에 OpenAI API 키를 설정하세요:
```
OPENAI_API_KEY=your_openai_api_key_here
```

### 3. 실행
```bash
streamlit run app.py
```

## 📁 프로젝트 구조

```
ai-agent/
├── app.py                 # 메인 Streamlit 애플리케이션
├── main.py               # CLI 버전
├── config.py             # 환경 변수 및 설정
├── requirements.txt      # 의존성 패키지
├── utils/
│   ├── openai_utils.py   # OpenAI API 헬퍼
│   └── logging_utils.py  # 로깅 설정
├── tools/
│   ├── crawler.py        # 웹 크롤링
│   ├── search.py         # 정보 검색
│   ├── pdf_parser.py     # PDF 텍스트 추출
│   └── jd_generator.py   # JD 생성 및 회사 분석
├── agent/
│   ├── evaluator.py      # JD 품질 평가
│   ├── decision.py       # 개선 방향 결정
│   ├── planner.py        # 계획 수립
│   ├── matcher.py        # 이력서-JD 매칭
│   ├── memory.py         # 메모리 관리 (예정)
│   ├── executor.py       # 실행 관리 (예정)
│   ├── cover_letter.py   # 자기소개서 생성
│   └── cover_letter_evaluator.py  # 자기소개서 평가
└── logs/                 # 로그 파일 저장소
```

## 🔧 설정 옵션

`.env` 파일에서 다음 설정을 조정할 수 있습니다:

- `OPENAI_MODEL`: 사용할 GPT 모델 (기본: gpt-4o-mini)
- `OPENAI_TEMPERATURE`: 응답 창의성 (0.0-2.0, 기본: 0.3)
- `OPENAI_MAX_TOKENS`: 최대 토큰 수 (기본: 1500)
- `SEARCH_MAX_RESULTS`: 검색 결과 수 (기본: 5)
- `CRAWL_TIMEOUT`: 크롤링 타임아웃 (기본: 15초)

## 🎯 사용 방법

1. **채용 공고 URL 입력**: 분석할 채용 공고 페이지 URL
2. **이력서 업로드 (선택)**: PDF 형식의 이력서
3. **분석 시작**: AI가 자동으로 크롤링 및 분석
4. **결과 확인**: 생성된 JD, 회사 정보, 적합도, 자기소개서

## 🛠️ 기술 스택

- **Frontend**: Streamlit
- **AI**: OpenAI GPT-4
- **크롤링**: BeautifulSoup, Requests
- **PDF 처리**: PyPDF2
- **검색**: DuckDuckGo Search
- **로깅**: Python logging

## 📝 개발 노트

- AI 에이전트 패턴으로 반복 개선 알고리즘 구현
- 안전한 JSON 파싱 및 에러 처리
- 모듈화된 아키텍처로 유지보수성 향상
- 상세한 로깅으로 디버깅 지원

## 🤝 기여

기능 개선이나 버그 수정은 언제나 환영합니다!

## 📄 라이선스

MIT License