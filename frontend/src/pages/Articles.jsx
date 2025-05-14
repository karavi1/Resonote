import React, { useEffect, useState } from 'react';
import { fetchArticles, ingestGuardian, ingestReddit } from '../api/articles';

export default function Articles() {
  const [articles, setArticles] = useState([]);
  const [loading, setLoading] = useState(false);

  const loadArticles = async () => {
    setLoading(true);
    try {
      const data = await fetchArticles();
      setArticles(data || []);
    } catch (err) {
      console.error('Error loading articles:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleIngest = async (source) => {
    try {
      if (source === 'guardian') await ingestGuardian();
      else if (source === 'reddit') await ingestReddit();
      loadArticles();
    } catch (err) {
      console.error(`Ingest failed for ${source}:`, err);
    }
  };

  const toggleReadStatus = async (articleId, currentStatus) => {
    const newStatus = currentStatus === 'read' ? 'unread' : 'read';
    try {
      await fetch(`http://localhost:5000/api/articles/${articleId}/status`, {
        method: 'PATCH',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ reading_status: newStatus })
      });
      loadArticles();
    } catch (err) {
      console.error('Error updating read status:', err);
    }
  };

  useEffect(() => {
    loadArticles();
  }, []);

  const read = articles.filter((a) => a.reading_status === 'read');
  const unread = articles.filter((a) => a.reading_status === 'unread');

  return (
    <div className="px-6 py-10 space-y-8">
      <h2 className="text-3xl font-bold">🧠 Curated Articles</h2>

      <div className="flex gap-4">
        <button
          onClick={() => handleIngest('guardian')}
          className="bg-green-600 text-white px-4 py-2 rounded hover:bg-green-700"
        >
          Ingest Guardian
        </button>
        <button
          onClick={() => handleIngest('reddit')}
          className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700"
        >
          Ingest Reddit
        </button>
      </div>

      <ArticleGrid title="🆕 Unread Articles" articles={unread} onToggleStatus={toggleReadStatus} />
      <ArticleGrid title="📖 Read Articles" articles={read} onToggleStatus={toggleReadStatus} />
    </div>
  );
}

function getGradientForTags(tags) {
  const TAG_COLORS = {
    science: '#60A5FA',
    tech: '#6366F1',
    health: '#34D399',
    politics: '#F87171',
    finance: '#FBBF24',
    education: '#A78BFA',
    culture: '#F472B6',
    world: '#F97316',
    story: '#f9a8d4',
    news: '#7dd3fc',
    may: '#d8b4fe',
    sport: '#fca5a5',
    default: '#D1D5DB'
  };

  const selected = [...new Set((tags || []).map(t => TAG_COLORS[t.toLowerCase()] || TAG_COLORS.default))].slice(0, 3);
  const gradient = `linear-gradient(135deg, ${selected.join(', ')})`;
  return { backgroundImage: gradient };
}

function ArticleGrid({ title, articles, onToggleStatus }) {
  return (
    <div>
      <h3 className="text-2xl font-semibold mb-4">{title}</h3>
      {articles.length === 0 ? (
        <p className="text-gray-500">No articles to show.</p>
      ) : (
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
          {articles.map((a) => (
            <div
              key={a.id}
              className="border border-gray-200 rounded-xl shadow-md p-5 flex flex-col justify-between"
              style={getGradientForTags(a.tags)}
            >
              <div className="space-y-2">
                <a
                  href={a.url}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="text-blue-800 font-semibold text-lg hover:underline"
                >
                  {a.title}
                </a>

                <div className="text-sm text-gray-700">
                  {a.source} • {new Date(a.timestamp).toLocaleDateString()}
                </div>

                {Array.isArray(a.tags) && a.tags.length > 0 && (
                  <div className="flex flex-wrap gap-2 mt-2">
                    {a.tags.map((tag, i) => (
                      <span
                        key={i}
                        className="bg-white bg-opacity-30 text-gray-900 text-xs px-2 py-1 rounded-full"
                      >
                        {tag}
                      </span>
                    ))}
                  </div>
                )}
              </div>

              <div className="mt-4 space-y-2">
                <button
                  onClick={() => onToggleStatus(a.id, a.reading_status)}
                  className="text-xs bg-white bg-opacity-40 hover:bg-opacity-60 text-gray-900 px-2 py-1 rounded"
                >
                  Mark as {a.reading_status === 'read' ? 'Unread' : 'Read'}
                </button>

                {a.reflection && a.reflection.content ? (
                  <ReflectionEditor
                    articleId={a.id}
                    existingContent={a.reflection.content}
                    onSaved={() => window.location.reload()}
                  />
                ) : (
                  <ReflectionInput articleId={a.id} onSaved={() => window.location.reload()} />
                )}
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

function ReflectionInput({ articleId, onSaved }) {
  const [content, setContent] = useState('');
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState('');

  const handleSubmit = async () => {
    if (!content.trim()) return;
    setSubmitting(true);
    try {
      const res = await fetch(`http://localhost:5000/api/reflect/make/${articleId}`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ content }),
      });
      if (!res.ok) throw new Error('Failed to save reflection');
      onSaved?.();
    } catch (err) {
      setError('Error saving reflection.');
      console.error(err);
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <div className="mt-3 border-t pt-3">
      <textarea
        rows="3"
        className="w-full border border-gray-300 rounded px-2 py-1 text-sm mb-2"
        value={content}
        onChange={(e) => setContent(e.target.value)}
        placeholder="Write your reflection..."
      />
      <div className="flex justify-between items-center">
        <button
          onClick={handleSubmit}
          disabled={submitting}
          className="text-sm bg-blue-600 hover:bg-blue-700 text-white px-3 py-1 rounded"
        >
          {submitting ? 'Saving...' : 'Save'}
        </button>
        {error && <span className="text-red-500 text-xs">{error}</span>}
      </div>
    </div>
  );
}

function ReflectionEditor({ articleId, existingContent, onSaved }) {
  const [content, setContent] = useState(existingContent);
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState('');

  const handleUpdate = async () => {
    if (!content.trim()) return;
    setSubmitting(true);
    try {
      const res = await fetch(`http://localhost:5000/api/reflect/make/${articleId}`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ content }),
      });
      if (!res.ok) throw new Error('Failed to update reflection');
      onSaved?.();
    } catch (err) {
      setError('Error updating reflection.');
      console.error(err);
    } finally {
      setSubmitting(false);
    }
  };

  const handleDelete = async () => {
    try {
      const res = await fetch(`http://localhost:5000/api/reflect/delete/${articleId}`, {
        method: 'DELETE',
      });
      if (!res.ok) throw new Error('Failed to delete reflection');
      onSaved?.();
    } catch (err) {
      setError('Error deleting reflection.');
      console.error(err);
    }
  };

  return (
    <div className="mt-3 border-t pt-3">
      <textarea
        rows="3"
        className="w-full border border-gray-300 rounded px-2 py-1 text-sm mb-2"
        value={content}
        onChange={(e) => setContent(e.target.value)}
        placeholder="Update your reflection..."
      />
      <div className="flex justify-between items-center gap-2">
        <button
          onClick={handleUpdate}
          disabled={submitting}
          className="text-sm bg-blue-600 hover:bg-blue-700 text-white px-3 py-1 rounded"
        >
          {submitting ? 'Saving...' : 'Update'}
        </button>
        <button
          onClick={handleDelete}
          disabled={submitting}
          className="text-sm bg-red-600 hover:bg-red-700 text-white px-3 py-1 rounded"
        >
          Delete
        </button>
        {error && <span className="text-red-500 text-xs">{error}</span>}
      </div>
    </div>
  );
}