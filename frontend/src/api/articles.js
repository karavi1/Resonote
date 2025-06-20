import axios from 'axios';

const BASE_URL = 'http://localhost:5000/api';

// Fetch all articles
export const fetchArticles = async () => {
    const res = await axios.get(`${BASE_URL}/articles`);
    return res.data;
};

// Fetch all tags
export const fetchTags = async () => {
    const res = await axios.get(`${BASE_URL}/tags`);
    return res.data;
};

// Ingest from Guardian with optional section and max_count
export const ingestGuardian = async (section = 'general', max_count = 5) => {
    const query = section !== 'general'
        ? `?section=${section}&max_count=${max_count}`
        : `?max_count=${max_count}`;
    const res = await axios.post(`${BASE_URL}/ingest/guardian${query}`);
    return res.data;
};

// Ingest from Reddit with optional subreddit and max_count
export const ingestReddit = async (subreddit = 'news', max_count = 5) => {
    const res = await axios.post(`${BASE_URL}/ingest/reddit?subreddit=${subreddit}&max_count=${max_count}`);
    return res.data;
};

// Toggle read/unread status for an article
export const toggleReadStatus = async (articleId) => {
    const res = await axios.post(`${BASE_URL}/articles/${articleId}/mark-read`);
    return res.data;
};

// Toggle favorite status for an article
export const toggleFavorite = async (articleId) => {
    const res = await axios.post(`${BASE_URL}/articles/${articleId}/favorite`);
    return res.data;
};

// Update an article's reflection
export const updateReflection = async (articleId, content) => {
    const res = await axios.post(`${BASE_URL}/reflect/update/${articleId}`, { content });
    return res.data;
};

// Delete an article's reflection
export const deleteReflection = async (articleId) => {
    const res = await axios.delete(`${BASE_URL}/reflect/delete/${articleId}`);
    return res.data;
};