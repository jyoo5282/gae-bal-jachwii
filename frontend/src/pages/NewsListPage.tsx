import React, { useEffect, useState } from 'react';
import { Container } from '@mui/material';
import Header from '../components/Layout/Header';
import NewsList from '../components/News/NewsList';
import { fetchNews, triggerCrawling } from '../services/api';
import type { NewsArticle } from '../services/api';

const NewsListPage: React.FC = () => {
  const [articles, setArticles] = useState<NewsArticle[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const loadNews = async () => {
    try {
      setIsLoading(true);
      setError(null);
      const data = await fetchNews();
      setArticles(data);
    } catch (err) {
      setError('뉴스를 불러오는 중 오류가 발생했습니다.');
      console.error('Error fetching news:', err);
    } finally {
      setIsLoading(false);
    }
  };

  const handleRefresh = async () => {
    try {
      setIsLoading(true);
      setError(null);
      await triggerCrawling();
      await loadNews();
    } catch (err) {
      setError('뉴스를 새로고침하는 중 오류가 발생했습니다.');
      console.error('Error refreshing news:', err);
    }
  };

  useEffect(() => {
    loadNews();
  }, []);

  return (
    <>
      <Header onRefresh={handleRefresh} />
      <Container maxWidth="lg" sx={{ mt: 4 }}>
        <NewsList
          articles={articles}
          isLoading={isLoading}
          error={error}
        />
      </Container>
    </>
  );
};

export default NewsListPage; 