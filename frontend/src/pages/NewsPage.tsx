import React, { useEffect, useState } from 'react';
import { Container, Typography } from '@mui/material';
import NewsList from '../components/NewsList';
import { fetchNews } from '../services/api';
import type { NewsArticle } from '../services/api';

const NewsPage: React.FC = () => {
  const [articles, setArticles] = useState<NewsArticle[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const loadNews = async () => {
      try {
        setIsLoading(true);
        setError(null);
        const data = await fetchNews();
        setArticles(data);
      } catch (err) {
        setError('명언을 불러오는 중 오류가 발생했습니다.');
        console.error('Error fetching quotes:', err);
      } finally {
        setIsLoading(false);
      }
    };

    loadNews();
  }, []);

  return (
    <Container maxWidth="lg">
      <Typography variant="h4" component="h1" gutterBottom sx={{ my: 4, textAlign: 'center', color: '#1976d2' }}>
        성공한 사람들의 명언
      </Typography>
      <Typography variant="subtitle1" gutterBottom sx={{ textAlign: 'center', mb: 4, color: 'text.secondary' }}>
        당신의 성공을 위한 영감의 한 조각
      </Typography>
      <NewsList
        articles={articles}
        isLoading={isLoading}
        error={error}
      />
    </Container>
  );
};

export default NewsPage; 