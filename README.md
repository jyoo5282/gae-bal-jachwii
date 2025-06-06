# 🌐 한국 경제 뉴스자동 수집 시스템 (Korean Economic News Collector)

![Python](https://img.shields.io/badge/Python-3776AB?style=flat-square&logo=Python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=flat-square&logo=FastAPI&logoColor=white)
![TypeScript](https://img.shields.io/badge/TypeScript-3178C6?style=flat-square&logo=TypeScript&logoColor=white)
![MongoDB](https://img.shields.io/badge/MongoDB-47A248?style=flat-square&logo=MongoDB&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-2496ED?style=flat-square&logo=Docker&logoColor=white)

🚀 한국 경제 관련 뉴스 사이트에서 실시간으로 뉴스를 수집하고 분석하는 현대적인 웹 애플리케이션입니다.

## ✨ 주요 기능

### 📰 스마트 뉴스 크롤링
- 한국경제, 매일경제, 조선비즈 등 주요 경제 뉴스 사이트 지원
- 중복 뉴스 자동 필터링 (URL 및 제목 기반)
- 실시간 뉴스 모니터링 및 수집

### 🔄 고급 데이터 관리
- RESTful API를 통한 뉴스데이터 접근
- 페이지네이션, 필터링, 검색 기능
- 뉴스 통계 및 분석 대시보드

### 🎯 현대적인 사용자 인터페이스
- React 기반 반응형 웹 인터페이스
- 한국 표준(KST) 기준 뉴스 표시
- 지표적인 뉴스 트렌드/랭킹 정보

## 🛠 구현된 핵심 요소
- TypeScript + MongoDB DB (로직 백엔드)
- JavaScript 간단 검색 (빠른 처리)
- Docker 컨테이너 지원

## 🚀 시작하기

### 필수 요구사항
- Python 3.8+
- Node.js 14+
- MongoDB

### 설치 방법
```bash
# 저장소 클론
git clone https://github.com/[your-username]/gae-bal-jachwi.git
cd gae-bal-jachwi

# 백엔드 설정
cd backend
pip install -r requirements.txt
uvicorn main:app --reload

# 프론트엔드 설정
cd ../frontend
npm install
npm start
```

### 환경 변수 설정
`.env` 파일을 생성하고 다음 변수들을 설정하세요:
```env
MONGODB_URL=mongodb://localhost:27017
DATABASE_NAME=news_collector
API_KEY=your_api_key
```

## 📝 라이선스
이 프로젝트는 MIT 라이선스 하에 있습니다. 자세한 내용은 [LICENSE](LICENSE) 파일을 참조하세요.

## 🤝 기여하기
프로젝트 기여는 언제나 환영합니다! [CONTRIBUTING.md](CONTRIBUTING.md)를 참조하세요.

## 📞 문의하기
문제가 발생하거나 제안사항이 있으시다면 이슈를 생성해주세요.

## 🤝 기여하기
버그 리포트, 기능 제안, 풀 리퀘스트 모두 환영합니다! 
프로젝트 개선에 참여하고 싶으시다면 언제든 이슈를 열어주세요.

## 👨‍💻 개발자

- [@jyoo5282](https://github.com/jyoo5282) - 프로젝트 개발 및 유지보수

---

⭐️ 이 프로젝트가 도움이 되었다면 스타를 눌러주세요! 