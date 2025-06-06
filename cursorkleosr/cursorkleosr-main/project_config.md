# 프로젝트 설정

## 프로젝트 목표
- 한국 경제 관련 뉴스를 자동으로 수집하는 웹페이지 구축
- 한국 시간 기준으로 일별 뉴스 수집 및 표시
- 사용자 친화적인 인터페이스 제공

## 기술 스택
- Backend:
  - Python 3.x
  - FastAPI (웹 서버)
  - BeautifulSoup4 (웹 스크래핑)
  - SQLite (데이터 저장)
  - APScheduler (자동 수집 스케줄링)

- Frontend:
  - React.js
  - Tailwind CSS
  - Axios (API 통신)

## 주요 기능
1. 뉴스 수집
   - 주요 경제 뉴스 사이트에서 실시간 뉴스 수집
   - 한국 시간 기준으로 매일 자동 업데이트
   - 중복 뉴스 필터링

2. 데이터 저장
   - 뉴스 제목, URL, 내용 요약, 발행일, 출처 저장
   - SQLite 데이터베이스 사용

3. 웹 인터페이스
   - 반응형 디자인
   - 날짜별 뉴스 필터링
   - 키워드 검색 기능

## 제약사항
- 뉴스 사이트의 robots.txt 준수
- 적절한 요청 간격 유지 (최소 1초)
- 한국 시간대 사용 (Asia/Seoul)
- 저작권 관련 법규 준수

## 토큰화 설정
- 문자당 토큰: 2
- 최대 토큰 길이: 4000
- 요약 최대 길이: 200단어

---

## Changelog
<!-- The agent prepends the latest summary here as a new list item after each VALIDATE phase -->
