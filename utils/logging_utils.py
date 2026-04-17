import logging
import sys
from pathlib import Path

# 로그 설정
def setup_logging():
    """애플리케이션 로깅 설정"""

    # 로그 디렉토리 생성
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)

    # 로거 설정
    logger = logging.getLogger("ai_agent")
    logger.setLevel(logging.INFO)

    # 포맷터
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

    # 콘솔 핸들러
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)

    # 파일 핸들러
    file_handler = logging.FileHandler(log_dir / "ai_agent.log", encoding='utf-8')
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)

    # 핸들러 추가
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

    return logger

# 전역 로거
logger = setup_logging()