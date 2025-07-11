import axios from 'axios';
import axiosRetry from 'axios-retry';

const BASE_URL = 'http://localhost:5000/api';

axiosRetry(axios, {
  retries: 3,
  retryDelay: axiosRetry.exponentialDelay,
  retryCondition: (error) =>
    axiosRetry.isNetworkOrIdempotentRequestError(error) ||
    error.response?.status >= 500
});

export const fetchArticles = async () => {
  const res = await axios.get(`${BASE_URL}/articles`);
  return res.data;
};

export const ingestGuardian = async (section = "general", maxCount = 5) => {
  const query = section !== "general" ? `?section=${section}&max_count=${maxCount}` : `?max_count=${maxCount}`;
  const res = await axios.post(`${BASE_URL}/ingest/guardian${query}`);
  return res.data;
};

export const ingestReddit = async (subreddit = "news", maxCount = 5) => {
  const res = await axios.post(`${BASE_URL}/ingest/reddit?subreddit=${subreddit}&max_count=${maxCount}`);
  return res.data;
};

export const fetchTags = async () => {
  const res = await axios.get(`${BASE_URL}/tags`);
  return res.data;
};

export const toggleReadStatus = async (articleId) => {
  const res = await axios.post(`${BASE_URL}/articles/${articleId}/mark-read`);
  return res.data;
};

export const toggleFavorite = async (articleId) => {
  const res = await axios.post(`${BASE_URL}/articles/${articleId}/favorite`);
  return res.data;
};

export const deleteArticle = async (articleId) => {
  const res = await axios.delete(`${BASE_URL}/articles/${articleId}/delete`);
  return res.data;
}

export const updateReflection = async (articleId, content) => {
  const res = await axios.post(`${BASE_URL}/reflect/update/${articleId}`, { content });
  return res.data;
};

export const deleteReflection = async (articleId) => {
  const res = await axios.delete(`${BASE_URL}/reflect/delete/${articleId}`);
  return res.data;
};