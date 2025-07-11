import React, { useEffect, useState } from 'react';
import {
  fetchArticles,
  ingestGuardian,
  ingestReddit,
  toggleReadStatus,
  toggleFavorite,
  updateReflection,
  deleteReflection,
  fetchTags,
  deleteArticle
} from '../api/articles';
import Toast from 'react-bootstrap/Toast';
import ToastContainer from 'react-bootstrap/ToastContainer';

export default function Articles() {
  const [articles, setArticles] = useState([]);
  const [loading, setLoading] = useState(false);
  const [redditSub, setRedditSub] = useState('news');
  const [guardianSec, setGuardianSec] = useState('general');
  const [maxCount, setMaxCount] = useState(5);
  const [reflectionEdits, setReflectionEdits] = useState({});
  const [filterTag, setFilterTag] = useState('');
  const [toast, setToast] = useState({ show: false, message: '', variant: 'success' });

  const showToast = (message, variant = 'success') => {
    setToast({ show: true, message, variant });
    setTimeout(() => setToast({ show: false, message: '', variant: 'success' }), 3000);
  };

  const loadArticles = async () => {
    setLoading(true);
    try {
      const data = await fetchArticles();
      setArticles(data || []);
    } catch (err) {
      console.error('Error loading articles:', err);
      showToast('Failed to load articles', 'danger');
    } finally {
      setLoading(false);
    }
  };

  const handleDeleteArticle = async (id) => {
    try {
      await deleteArticle(id);
      setArticles(prev => prev.filter(a => a.id !== id));
      showToast('Article deleted', 'danger');
    } catch (err) {
      console.error('Error deleting article:', err);
      showToast('Failed to delete article', 'danger');
    }
  };

  const handleRedditIngest = async () => {
    try {
      await ingestReddit(redditSub, maxCount);
      await loadArticles();
      showToast('Reddit ingestion successful');
    } catch (err) {
      console.error('Reddit ingestion error:', err);
      showToast('Reddit ingestion failed', 'danger');
    }
  };

  const handleGuardianIngest = async () => {
    try {
      await ingestGuardian(guardianSec, maxCount);
      await loadArticles();
      showToast('Guardian ingestion successful');
    } catch (err) {
      console.error('Guardian ingestion error:', err);
      showToast('Guardian ingestion failed', 'danger');
    }
  };

  const handleToggleStatus = async (id) => {
    try {
      await toggleReadStatus(id);
      setArticles(prev =>
        prev.map(a =>
          a.id === id
            ? { ...a, reading_status: a.reading_status === 'read' ? 'unread' : 'read' }
            : a
        )
      );
      showToast('Toggled read status');
    } catch (err) {
      console.error('Error toggling read status:', err);
      showToast('Failed to toggle read status', 'danger');
    }
  };

  const handleToggleFavorite = async (id) => {
    try {
      await toggleFavorite(id);
      setArticles(prev =>
        prev.map(a => (a.id === id ? { ...a, favorite: !a.favorite } : a))
      );
      showToast('Toggled favorite status');
    } catch (err) {
      console.error('Error toggling favorite status:', err);
      showToast('Failed to toggle favorite status', 'danger');
    }
  };

  const handleSaveReflection = async (id, content) => {
    try {
      await updateReflection(id, content);
      setArticles(prev =>
        prev.map(a => (a.id === id ? { ...a, reflection: { content } } : a))
      );
      setReflectionEdits(prev => ({ ...prev, [id]: false }));
      showToast('Reflection saved');
    } catch (err) {
      console.error('Error saving reflection:', err);
      showToast('Failed to save reflection', 'danger');
    }
  };

  const handleDeleteReflection = async (id) => {
    try {
      await deleteReflection(id);
      setArticles(prev =>
        prev.map(a => (a.id === id ? { ...a, reflection: null } : a))
      );
      showToast('Reflection deleted');
    } catch (err) {
      console.error('Error deleting reflection:', err);
      showToast('Failed to delete reflection', 'danger');
    }
  };

  useEffect(() => {
    loadArticles();
  }, []);

  return (
    <div className="px-4 py-8 space-y-6">
      <h2 className="text-3xl font-bold">🧠 Curated Articles</h2>

      <IngestionControls
        redditSub={redditSub}
        setRedditSub={setRedditSub}
        guardianSec={guardianSec}
        setGuardianSec={setGuardianSec}
        maxCount={maxCount}
        setMaxCount={setMaxCount}
        ingestReddit={handleRedditIngest}
        ingestGuardian={handleGuardianIngest}
      />

      <div className="flex gap-2 items-center">
        <label className="text-sm font-medium">Filter by Tag:</label>
        <input
          type="text"
          placeholder="e.g. technology"
          className="border rounded px-2 py-1"
          value={filterTag}
          onChange={(e) => setFilterTag(e.target.value.toLowerCase())}
        />
      </div>

      {loading ? (
        <p className="text-gray-500">Loading articles...</p>
      ) : (
        <ArticleSections
          articles={articles.filter(
            (a) => filterTag === '' || a.tags.some((t) => t.name.toLowerCase().includes(filterTag))
          )}
          onToggleStatus={handleToggleStatus}
          onToggleFavorite={handleToggleFavorite}
          onDeleteArticle={handleDeleteArticle}
          reflectionEdits={reflectionEdits}
          setReflectionEdits={setReflectionEdits}
          saveReflection={handleSaveReflection}
          deleteReflection={handleDeleteReflection}
        />
      )}

      <ToastContainer position="bottom-end" className="p-3">
        <Toast show={toast.show} bg={toast.variant}>
          <Toast.Body>{toast.message}</Toast.Body>
        </Toast>
      </ToastContainer>
    </div>
  );
}

function IngestionControls({
  redditSub,
  setRedditSub,
  guardianSec,
  setGuardianSec,
  maxCount,
  setMaxCount,
  ingestReddit,
  ingestGuardian
}) {
  const redditSubs = ['news', 'technology', 'health', 'worldnews', 'science'];
  const guardianSecs = ['general', 'technology', 'world'];

  return (
    <div className="flex flex-col gap-4 sm:flex-row sm:items-center sm:gap-6">
      <div className="flex flex-wrap items-center gap-2">
        <label className="text-sm font-medium">Reddit:</label>
        <select
          value={redditSub}
          onChange={(e) => setRedditSub(e.target.value)}
          className="border rounded px-2 py-1 bg-gray-100"
        >
          {redditSubs.map((s, i) => (
            <option key={i} value={s}>
              {s}
            </option>
          ))}
        </select>
        <input
          type="number"
          value={maxCount}
          min={1}
          max={20}
          onChange={(e) => setMaxCount(Number(e.target.value))}
          className="w-16 border rounded px-2 py-1"
        />
        <button
          onClick={ingestReddit}
          className="bg-blue-600 text-white font-medium px-3 py-1.5 rounded hover:bg-blue-700"
        >
          Ingest Reddit
        </button>
      </div>

      <div className="flex flex-wrap items-center gap-2">
        <label className="text-sm font-medium">Guardian:</label>
        <select
          value={guardianSec}
          onChange={(e) => setGuardianSec(e.target.value)}
          className="border rounded px-2 py-1 bg-gray-100"
        >
          {guardianSecs.map((s, i) => (
            <option key={i} value={s}>
              {s}
            </option>
          ))}
        </select>
        <input
          type="number"
          value={maxCount}
          min={1}
          max={20}
          onChange={(e) => setMaxCount(Number(e.target.value))}
          className="w-16 border rounded px-2 py-1"
        />
        <button
          onClick={ingestGuardian}
          className="bg-green-600 text-white font-medium px-3 py-1.5 rounded hover:bg-green-700"
        >
          Ingest Guardian
        </button>
      </div>
    </div>
  );
}

function ArticleSections({
  articles,
  onToggleStatus,
  onToggleFavorite,
  onDeleteArticle,
  reflectionEdits,
  setReflectionEdits,
  saveReflection,
  deleteReflection
}) {
  // 1. Sort newest → oldest
  const sorted = [...articles].sort(
    (a, b) => new Date(b.timestamp) - new Date(a.timestamp)
  );

  // 2. Group by Read/Unread and primary tag
  const grouped = sorted.reduce((acc, article) => {
    const status = article.reading_status === 'read' ? 'Read' : 'Unread';
    const primaryTag = article.tags?.[0]?.name?.toLowerCase() ?? 'general';

    acc[status] = acc[status] || {};
    acc[status][primaryTag] = acc[status][primaryTag] || [];
    acc[status][primaryTag].push(article);
    return acc;
  }, {});

  // 3. Compute counts
  const statuses = ['Unread', 'Read'];
  const statusCounts = statuses.reduce((counts, status) => {
    const total = Object.values(grouped[status] || {}).reduce((sum, list) => sum + list.length, 0);
    counts[status] = total;
    return counts;
  }, {});

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
      {statuses.map((status) => (
        <div key={status}>
          <h3 className="text-xl font-bold mb-2">
            {status} Articles ({statusCounts[status] || 0})
          </h3>
          {grouped[status] ? (
            Object.entries(grouped[status]).map(([tag, list]) => (
              <div key={tag} className="mb-6">
                <h4 className="text-md font-semibold text-gray-600 mb-2 capitalize">
                  {tag} ({list.length})
                </h4>
                <ul className="space-y-4">
                  {list.map((article) => (
                    <li
                      key={article.id}
                      className="relative border border-gray-300 rounded p-4 bg-white shadow"
                    >
                      <a
                        href={article.url}
                        target="_blank"
                        rel="noopener noreferrer"
                        className="font-medium text-blue-700 hover:underline"
                      >
                        {article.title}
                      </a>
                      <p className="text-sm text-gray-600">
                        {article.source} • {new Date(article.timestamp).toLocaleDateString()}
                      </p>

                      {/* reflection UI unchanged */}

                      <div className="mt-2 flex gap-2">
                        <button
                          onClick={() => onToggleStatus(article.id)}
                          className="text-xs px-2 py-1 border border-black rounded"
                        >
                          Mark as {article.reading_status === 'read' ? 'Unread' : 'Read'}
                        </button>
                        <button
                          onClick={() => onToggleFavorite(article.id)}
                          className="text-xs px-2 py-1 border border-black rounded"
                        >
                          {article.favorite ? 'Unfavorite' : 'Favorite'}
                        </button>
                      </div>

                      {/* Delete button */}
                      <button
                        onClick={() => onDeleteArticle(article.id)}
                        className="absolute bottom-2 right-2 text-xs font-medium px-2 py-1 bg-red-600 text-white rounded hover:bg-red-700"
                      >
                        Delete
                      </button>
                    </li>
                  ))}
                </ul>
              </div>
            ))
          ) : (
            <p className="text-sm text-gray-500">
              No {status.toLowerCase()} articles found.
            </p>
          )}
        </div>
      ))}
    </div>
  );
}