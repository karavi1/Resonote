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
              <th className="border px-4 py-2">Title</th>
              <th className="border px-4 py-2">Source</th>
              <th className="border px-4 py-2">Tags</th>
              <th className="border px-4 py-2">Date</th>
              <th className="border px-4 py-2">Reflection</th>
            </tr>
          </thead>
          <tbody>
            {articles.map((a) => (
              <tr key={a.id}>
                <td className="border px-4 py-2">
                  <a
                    href={a.url}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="text-blue-600 underline"
                  >
                    {a.title}
                  </a>
                </td>
                <td className="border px-4 py-2">{a.source}</td>
                <td className="border px-4 py-2">
                  {Array.isArray(a.tags) ? a.tags.slice(0, 3).join(', ') : '—'}
                </td>
                <td className="border px-4 py-2">
                  {new Date(a.timestamp).toLocaleDateString()}
                </td>
                <td className="border px-4 py-2">
                  {a.reflection && a.reflection.content ? (
                    <div className="text-sm text-gray-700">{a.reflection.content}</div>
                  ) : (
                    <span className="text-gray-500 italic">No reflection</span>
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