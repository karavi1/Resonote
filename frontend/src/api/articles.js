import axios from 'axios';

const BASE_URL = 'http://localhost:5000/api';

export const fetchArticles = async () => {
  const res = await axios.get(`${BASE_URL}/articles`);
  return res.data;
};

export const ingestGuardian = async () => {
  const res = await axios.post(`${BASE_URL}/ingest/guardian`);
  return res.data;
};

export const ingestReddit = async (subreddit = "news") => {
  const res = await axios.post(`${BASE_URL}/ingest/reddit?subreddit=${subreddit}`);
  return res.data;
};

export const fetchTags = async () => {
  const res = await axios.get(`${BASE_URL}/tags`);
  return res.data;
};