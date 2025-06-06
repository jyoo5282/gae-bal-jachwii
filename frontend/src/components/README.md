# Frontend Component Structure

## Core Components

### Layout Components
- `Layout/`: 전체 레이아웃 컴포넌트
  - `Header.tsx`: 상단 헤더 컴포넌트
  - `Sidebar.tsx`: 사이드바 컴포넌트
  - `Footer.tsx`: 하단 푸터 컴포넌트

### News Components
- `News/`: 뉴스 관련 컴포넌트
  - `NewsList.tsx`: 뉴스 목록 컴포넌트
  - `NewsCard.tsx`: 개별 뉴스 카드 컴포넌트
  - `NewsDetail.tsx`: 뉴스 상세 보기 컴포넌트
  - `NewsFilter.tsx`: 뉴스 필터링 컴포넌트

### Source Components
- `Source/`: 뉴스 소스 관련 컴포넌트
  - `SourceList.tsx`: 뉴스 소스 목록 컴포넌트
  - `SourceCard.tsx`: 개별 소스 카드 컴포넌트

### Common Components
- `Common/`: 공통 컴포넌트
  - `LoadingSpinner.tsx`: 로딩 스피너 컴포넌트
  - `ErrorMessage.tsx`: 에러 메시지 컴포넌트
  - `Button.tsx`: 공통 버튼 컴포넌트
  - `Card.tsx`: 공통 카드 컴포넌트

## Pages
- `pages/`: 페이지 컴포넌트
  - `HomePage.tsx`: 메인 페이지
  - `NewsListPage.tsx`: 뉴스 목록 페이지
  - `NewsDetailPage.tsx`: 뉴스 상세 페이지
  - `SourcesPage.tsx`: 뉴스 소스 관리 페이지

## Hooks
- `hooks/`: 커스텀 훅
  - `useNews.ts`: 뉴스 데이터 관리 훅
  - `useSources.ts`: 뉴스 소스 관리 훅
  - `useFilter.ts`: 필터링 상태 관리 훅

## Services
- `services/`: API 서비스
  - `api.ts`: API 호출 함수들
  - `types.ts`: 타입 정의 