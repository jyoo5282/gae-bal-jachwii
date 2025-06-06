# Frontend State Management

## Store Structure

### News Store
```typescript
interface NewsState {
  articles: Article[];
  loading: boolean;
  error: string | null;
  filters: {
    source: string | null;
    startDate: Date | null;
    endDate: Date | null;
    keyword: string;
  };
  pagination: {
    page: number;
    perPage: number;
    total: number;
  };
}
```

### Source Store
```typescript
interface SourceState {
  sources: Source[];
  loading: boolean;
  error: string | null;
  activeSource: string | null;
}
```

### UI Store
```typescript
interface UIState {
  theme: 'light' | 'dark';
  sidebarOpen: boolean;
  notifications: Notification[];
}
```

## Actions

### News Actions
- `fetchNews`: 뉴스 목록 조회
- `fetchNewsDetail`: 뉴스 상세 조회
- `setNewsFilters`: 필터 설정
- `updatePagination`: 페이지네이션 업데이트

### Source Actions
- `fetchSources`: 뉴스 소스 목록 조회
- `setActiveSource`: 활성 소스 설정
- `triggerCrawling`: 크롤링 시작

### UI Actions
- `toggleTheme`: 테마 변경
- `toggleSidebar`: 사이드바 토글
- `addNotification`: 알림 추가
- `removeNotification`: 알림 제거

## Custom Hooks

### useNewsStore
```typescript
const useNewsStore = () => {
  // 뉴스 관련 상태 및 액션
  const articles = useSelector((state) => state.news.articles);
  const loading = useSelector((state) => state.news.loading);
  const filters = useSelector((state) => state.news.filters);
  
  return { articles, loading, filters, ... };
};
```

### useSourceStore
```typescript
const useSourceStore = () => {
  // 소스 관련 상태 및 액션
  const sources = useSelector((state) => state.sources.sources);
  const activeSource = useSelector((state) => state.sources.activeSource);
  
  return { sources, activeSource, ... };
};
```

### useUIStore
```typescript
const useUIStore = () => {
  // UI 관련 상태 및 액션
  const theme = useSelector((state) => state.ui.theme);
  const notifications = useSelector((state) => state.ui.notifications);
  
  return { theme, notifications, ... };
};
``` 