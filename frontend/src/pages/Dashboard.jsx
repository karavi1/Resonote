import React, { useEffect, useRef, useState } from 'react';
import ForceGraph2D from 'react-force-graph-2d';
import * as d3 from 'd3-force';
import { fetchArticles } from '../api/articles';

export default function Dashboard() {
  const [allGraph, setAllGraph] = useState({ nodes: [], links: [] });
  const [readGraph, setReadGraph] = useState({ nodes: [], links: [] });
  const [tagStats, setTagStats] = useState({});
  const [summaryStats, setSummaryStats] = useState({
    total: 0,
    read: 0,
    unread: 0,
    tags: 0,
    mostCommonTag: ''
  });

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
          const shortTitle = a.title.length > 30 ? a.title.slice(0, 27) + '...' : a.title;
          nodes.push({
            id: a.id,
            label: shortTitle,
            fullTitle: a.title,
            group: 'article',
            color: '#3b82f6'
          });

          (a.tags || []).forEach(tagObj => {
            const tagName = typeof tagObj === 'string' ? tagObj : tagObj.name;
            const tagId = `tag:${tagName}`;
            tagSet.add(tagId);
            links.push({ source: a.id, target: tagId });

            tagCount[tagName] = (tagCount[tagName] || 0) + 1;
          });
        }

        for (const tagId of tagSet) {
          const tagName = tagId.replace('tag:', '');
          nodes.push({
            id: tagId,
            label: tagName,
            group: 'tag',
            color: '#9333ea'
          });
        }

        return { nodes, links };
      };

      const all = makeGraph(data);
      const read = makeGraph(data.filter(a => a.reading_status === 'read'));

      setAllGraph(all);
      setReadGraph(read);
      setTagStats(tagCount);

      const mostCommon = Object.entries(tagCount).sort((a, b) => b[1] - a[1])[0]?.[0] || '';
      setSummaryStats({
        total: data.length,
        read: data.filter(a => a.reading_status === 'read').length,
        unread: data.filter(a => a.reading_status !== 'read').length,
        tags: Object.keys(tagCount).length,
        mostCommonTag: mostCommon
      });
    };

    load();
  }, []);

  useEffect(() => {
    const centerTagNodes = (graphRef, graphData) => {
      if (!graphRef.current) return;

      const centerForce = d3.forceX().strength((node) =>
        node.group === 'tag' ? 0.3 : 0
      );
      const verticalForce = d3.forceY().strength((node) =>
        node.group === 'tag' ? 0.3 : 0
      );

      graphRef.current
        .d3Force('charge', d3.forceManyBody().strength(-180))
        .d3Force('link', d3.forceLink().distance(120))
        .d3Force('collide', d3.forceCollide(28))
        .d3Force('x', centerForce)
        .d3Force('y', verticalForce);
    };

    centerTagNodes(allRef, allGraph);
    centerTagNodes(readRef, readGraph);
  }, [allGraph, readGraph]);

  const renderGraph = (graph, ref) => (
    <ForceGraph2D
      ref={ref}
      width={window.innerWidth / 2 - 80}
      height={600}
      graphData={graph}
      nodeLabel={(node) =>
        node.group === 'tag' ? `Tag: ${node.label}` : `Article: ${node.fullTitle || node.label}`
      }
      nodeCanvasObject={(node, ctx) => {
        if (typeof node.x !== 'number' || typeof node.y !== 'number') return;

        const label = node.label;
        const fontSize = 10;
        ctx.font = `${fontSize}px Sans-Serif`;
        ctx.fillStyle = node.color;
        ctx.beginPath();
        ctx.arc(node.x, node.y, 22, 0, 2 * Math.PI);
        ctx.fill();

        ctx.fillStyle = '#fff';
        ctx.textAlign = 'center';
        ctx.textBaseline = 'middle';
        ctx.fillText(label, node.x, node.y + 1);
      }}
      nodePointerAreaPaint={(node, color, ctx) => {
        if (typeof node.x !== 'number' || typeof node.y !== 'number') return;
        ctx.fillStyle = color;
        ctx.beginPath();
        ctx.arc(node.x, node.y, 26, 0, 2 * Math.PI, false);
        ctx.fill();
      }}
      linkColor={() => '#ccc'}
      linkWidth={1}
      linkDirectionalParticles={0}
      cooldownTicks={100}
      onEngineStop={() => ref.current?.zoomToFit(400)}
      d3VelocityDecay={0.4}
      d3AlphaDecay={0.02}
    />
  );

  return (
    <div className="p-6 space-y-8 bg-gray-50 min-h-screen">
      <h2 className="text-3xl font-bold text-gray-800">🧠 Knowledge Graph Dashboard</h2>

      <div className="grid grid-cols-2 gap-4 text-sm text-gray-700">
        <div className="bg-white rounded-lg shadow p-4">
          <h4 className="font-semibold mb-2">📘 All Articles</h4>
          <ul className="space-y-1">
            <li>Total: {summaryStats.total}</li>
            <li>Read: {summaryStats.read}</li>
            <li>Unread: {summaryStats.unread}</li>
          </ul>
        </div>
        <div className="bg-white rounded-lg shadow p-4">
          <h4 className="font-semibold mb-2">🏷️ Tags</h4>
          <ul className="space-y-1">
            <li>Total Tags: {summaryStats.tags}</li>
            <li>Most Common: {summaryStats.mostCommonTag || '—'}</li>
          </ul>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div className="bg-white p-4 rounded-lg shadow border">
          <div className="flex justify-between items-center mb-2">
            <h3 className="font-semibold">All Articles</h3>
            <button
              onClick={() => setTimeout(() => allRef.current?.zoomToFit(400), 100)}
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
              onClick={() => setTimeout(() => readRef.current?.zoomToFit(400), 100)}
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