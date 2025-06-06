import React from 'react';
import { Box, Container, Typography } from '@mui/material';
import NewsCard from './NewsCard';
import LoadingSpinner from '../Common/LoadingSpinner';
import ErrorMessage from '../Common/ErrorMessage';

interface NewsArticle {
  id: number;
  title: string;
  content: string;
  url: string;
  source_name: string;
  published_at: string;
}

interface NewsListProps {
  articles: NewsArticle[];
  isLoading: boolean;
  error: string | null;
}

const NewsList: React.FC<NewsListProps> = ({ articles, isLoading, error }) => {
  if (isLoading) {
    return <LoadingSpinner />;
  }

  if (error) {
    return <ErrorMessage message={error} />;
  }

  if (articles.length === 0) {
    return (
      <Box textAlign="center" py={4}>
        <Typography variant="h6" color="text.secondary">
          표시할 뉴스가 없습니다.
        </Typography>
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