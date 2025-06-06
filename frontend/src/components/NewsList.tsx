import React from 'react';
import { Box, Container, Typography } from '@mui/material';
import NewsCard from './NewsCard';
import { NewsArticle } from '../services/api';

interface NewsListProps {
  articles: NewsArticle[];
  isLoading: boolean;
  error: string | null;
}

const NewsList: React.FC<NewsListProps> = ({ articles, isLoading, error }) => {
  if (isLoading) {
    return (
      <Box textAlign="center" py={4}>
        <Typography>명언을 가져오는 중...</Typography>
      </Box>
    );
  }

  if (error) {
    return (
      <Box textAlign="center" py={4}>
        <Typography color="error">{error}</Typography>
      </Box>
    );
  }

  if (articles.length === 0) {
    return (
      <Box textAlign="center" py={4}>
        <Typography>표시할 명언이 없습니다.</Typography>
      </Box>
    );
  }

  return (
    <Container maxWidth="md">
      <Box py={3}>
        {articles.map((article) => (
          <NewsCard
            key={article.id}
            title={article.title}
            content={article.content}
            url={article.url}
            sourceName={article.source_name}
            publishedAt={article.published_at}
          />
        ))}
      </Box>
    </Container>
  );
};

export default NewsList; 