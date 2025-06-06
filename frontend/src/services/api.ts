import axios from 'axios';

const API_BASE_URL = 'http://localhost:8000/api';

export interface NewsArticle {
  id: number;
  title: string;
  content: string;
  url: string;
  source_name: string;
  published_at: string;
}

export interface NewsSource {
  id: number;
  name: string;
  url: string;
  is_active: boolean;
}

const api = axios.create({
  baseURL: API_BASE_URL,
});

export const fetchNews = async (): Promise<NewsArticle[]> => {
  const response = await api.get('/news');
  return response.data;
};

export const fetchSources = async (): Promise<NewsSource[]> => {
  const response = await api.get('/sources');
  return response.data;
};

export const triggerCrawling = async (): Promise<void> => {
  await api.post('/crawl');
}; 