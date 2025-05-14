import React, { useEffect, useRef, useState } from 'react';
import ForceGraph2D from 'react-force-graph-2d';
import { fetchArticles } from '../api/articles';

export default function Dashboard() {
  const [allGraph, setAllGraph] = useState({ nodes: [], links: [] });
  const [readGraph, setReadGraph] = useState({ nodes: [], links: [] });
  const [tagStats, setTagStats] = useState({});

  const allRef = useRef();
  const readRef = useRef();

  useEffect(() => {
    const load = async () => {
      const data = await fetchArticles();
      const tagCount = {};
      const makeGraph = (articles) => {
        const nodes = [];
        const links = [];
        const tagSet = new Set();

        for (const a of articles) {
          nodes.push({ id: a.id, label: '', group: 'article', color: '#3b82f6' }); // Blue articles

          (a.tags || []).forEach(tag => {
            const tagId = `tag:${tag}`;
            tagSet.add(tagId);
            links.push({ source: a.id, target: tagId });

            tagCount[tag] = (tagCount[tag] || 0) + 1;
          });
        }

        for (const tagId of tagSet) {
          const tagName = tagId.replace('tag:', '');
          nodes.push({
            id: tagId,
            label: tagName,
            group: 'tag',
            color: '#9333ea' // Violet tags
          });
        }

        return { nodes, links };
      };

      setAllGraph(makeGraph(data));
      setReadGraph(makeGraph(data.filter(a => a.reading_status === 'read')));
      setTagStats(tagCount);
    };

    load();
  }, []);

  const renderGraph = (graph, ref) => (
    <ForceGraph2D
      ref={ref}
      width={window.innerWidth / 2 - 80}
      height={600}
      graphData={graph}
      nodeLabel="label"
      nodeCanvasObject={(node, ctx) => {
        const label = node.label;
        const fontSize = 10;
        ctx.font = `${fontSize}px Sans-Serif`;
        ctx.fillStyle = '#fff';
        ctx.textAlign = 'center';
        ctx.textBaseline = 'middle';
        ctx.beginPath();
        ctx.arc(node.x, node.y, 16, 0, 2 * Math.PI);
        ctx.fillStyle = node.color;
        ctx.fill();
        ctx.fillStyle = '#fff';
        ctx.fillText(label, node.x, node.y);
      }}
      nodePointerAreaPaint={(node, color, ctx) => {
        ctx.fillStyle = color;
        ctx.beginPath();
        ctx.arc(node.x, node.y, 20, 0, 2 * Math.PI, false);
        ctx.fill();
      }}
      linkColor={() => '#ccc'}
      linkWidth={1}
      linkDirectionalParticles={0}
    />
  );

  return (
    <div className="p-6 space-y-8 bg-gray-50 min-h-screen">
      <h2 className="text-3xl font-bold text-gray-800">🧠 Knowledge Graph Dashboard</h2>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div className="bg-white p-4 rounded-lg shadow border">
          <div className="flex justify-between items-center mb-2">
            <h3 className="font-semibold">All Articles</h3>
            <button
              onClick={() => allRef.current.zoomToFit(400)}
              className="text-xs px-2 py-1 bg-gray-200 hover:bg-gray-300 rounded"
            >
              🔍 Fit to View
            </button>
          </div>
          {renderGraph(allGraph, allRef)}
        </div>

        <div className="bg-white p-4 rounded-lg shadow border">
          <div className="flex justify-between items-center mb-2">
            <h3 className="font-semibold">Read Articles Only</h3>
            <button
              onClick={() => readRef.current.zoomToFit(400)}
              className="text-xs px-2 py-1 bg-gray-200 hover:bg-gray-300 rounded"
            >
              🔍 Fit to View
            </button>
          </div>
          {renderGraph(readGraph, readRef)}
        </div>
      </div>

      <div className="bg-white p-4 rounded-lg shadow border mt-4">
        <h3 className="text-xl font-semibold mb-2">📊 Tag Frequency</h3>
        <div className="space-y-2">
          {Object.entries(tagStats)
            .sort((a, b) => b[1] - a[1])
            .map(([tag, count]) => (
              <div key={tag} className="flex items-center gap-2">
                <div className="w-24 text-sm font-medium">{tag}</div>
                <div className="flex-1 bg-gray-200 h-3 rounded overflow-hidden">
                  <div
                    className="bg-blue-500 h-full"
                    style={{ width: `${count * 20}px` }}
                  ></div>
                </div>
                <div className="text-sm text-gray-600 ml-2">{count}</div>
              </div>
            ))}
        </div>
      </div>
    </div>
  );
}