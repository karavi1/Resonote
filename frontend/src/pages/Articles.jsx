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
      if (source === 'guardian') {
        await ingestGuardian();
      } else if (source === 'reddit') {
        await ingestReddit();
      }
      loadArticles();
    } catch (err) {
      console.error(`Ingest failed for ${source}:`, err);
    }
  };

  useEffect(() => {
    loadArticles();
  }, []);

  const read = articles.filter((a) => a.reading_status === 'read');
  const unread = articles.filter((a) => a.reading_status === 'unread');

  return (
    <div className="space-y-6">
      <h2 className="text-2xl font-semibold">Curated Articles</h2>

      <div className="flex gap-4">
        <button
          onClick={() => handleIngest('guardian')}
          className="px-4 py-2 bg-green-600 text-white rounded"
        >
          Ingest Guardian
        </button>
        <button
          onClick={() => handleIngest('reddit')}
          className="px-4 py-2 bg-blue-600 text-white rounded"
        >
          Ingest Reddit
        </button>
      </div>

      <ArticleTable title="🆕 Unread Articles" articles={unread} />
      <ArticleTable title="📖 Read Articles" articles={read} />
    </div>
  );
}

function ArticleTable({ title, articles }) {
  return (
    <div className="mt-6">
      <h3 className="text-lg font-medium mb-2">{title}</h3>
      {articles.length === 0 ? (
        <p className="text-gray-500">No articles to show.</p>
      ) : (
        <table className="w-full table-auto border-collapse border border-gray-300">
          <thead>
            <tr className="bg-gray-100">
              <th className="border px-4 py-2 align-top">Title</th>
              <th className="border px-4 py-2 align-top">Source</th>
              <th className="border px-4 py-2 align-top">Tags</th>
              <th className="border px-4 py-2 align-top">Date</th>
              <th className="border px-4 py-2 align-top">Reflection</th>
            </tr>
          </thead>
          <tbody>
            {articles.map((a) => (
              <tr key={a.id}>
                <td className="border px-4 py-2 align-top">
                  <a
                    href={a.url}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="text-blue-600 underline"
                  >
                    {a.title}
                  </a>
                </td>
                <td className="border px-4 py-2 align-top">{a.source}</td>
                <td className="border px-4 py-2 align-top">
                  {Array.isArray(a.tags) ? a.tags.slice(0, 3).join(', ') : '—'}
                </td>
                <td className="border px-4 py-2 align-top">
                  {new Date(a.timestamp).toLocaleDateString()}
                </td>
                <td className="border px-4 py-2 align-top">
                  {a.reflection && a.reflection.content ? (
                    <div className="text-sm text-gray-700">{a.reflection.content}</div>
                  ) : (
                    <ReflectionInput articleId={a.id} onSaved={() => window.location.reload()} />
                  )}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </div>
  );
}

function ReflectionInput({ articleId, onSaved }) {
  const [content, setContent] = useState("");
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState("");

  const handleSubmit = async () => {
    if (!content.trim()) return;
    setSubmitting(true);
    try {
      const res = await fetch(`http://localhost:5000/api/reflect/make/${articleId}`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ content }),
      });

      if (!res.ok) throw new Error("Failed to save reflection");
      onSaved?.();
    } catch (err) {
      setError("Error saving reflection.");
      console.error(err);
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <div className="border rounded-md p-2 shadow-sm bg-gray-50">
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
          className="text-xs bg-blue-600 hover:bg-blue-700 text-white px-3 py-1 rounded"
        >
          {submitting ? "Saving..." : "Save"}
        </button>
        {error && <span className="text-red-500 text-xs">{error}</span>}
      </div>
    </div>
  );
}