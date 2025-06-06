import React from 'react';
import { 
  Card, 
  CardContent, 
  Typography, 
  Link, 
  Box,
  Chip
} from '@mui/material';
import { format } from 'date-fns';
import { ko } from 'date-fns/locale';

interface NewsCardProps {
  title: string;
  content: string;
  url: string;
  sourceName: string;
  publishedAt: string;
}

const NewsCard: React.FC<NewsCardProps> = ({
  title,
  content,
  url,
  sourceName,
  publishedAt,
}) => {
  const formattedDate = format(
    new Date(publishedAt),
    'PPP p',
    { locale: ko }
  );

  return (
    <Card sx={{ mb: 2 }}>
      <CardContent>
        <Box display="flex" justifyContent="space-between" alignItems="flex-start" mb={1}>
          <Typography variant="h6" component="h2" gutterBottom>
            <Link 
              href={url} 
              target="_blank" 
              rel="noopener noreferrer"
              color="inherit"
              underline="hover"
            >
              {title}
            </Link>
          </Typography>
          <Chip 
            label={sourceName} 
            size="small" 
            color="primary" 
            sx={{ ml: 1 }}
          />
        </Box>
        <Typography 
          variant="body2" 
          color="text.secondary" 
          sx={{
            display: '-webkit-box',
            WebkitLineClamp: 3,
            WebkitBoxOrient: 'vertical',
            overflow: 'hidden',
            mb: 1
          }}
        >
          {content}
        </Typography>
        <Typography variant="caption" color="text.secondary">
          {formattedDate}
        </Typography>
      </CardContent>
    </Card>
  );
};

export default NewsCard; 