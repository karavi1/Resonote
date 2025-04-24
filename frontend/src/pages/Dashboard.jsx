import React, { useEffect, useState } from 'react';
import ForceGraph2D from 'react-force-graph-2d';
import { fetchArticles } from '../api/articles';

export default function Dashboard() {
  const [nodes, setNodes] = useState([]);
  const [links, setLinks] = useState([]);

  useEffect(() => {
    const loadData = async () => {
      const articles = await fetchArticles();

      const tagSet = new Set();
      const nodeList = [];
      const linkList = [];

      for (const article of articles) {
        nodeList.push({
          id: article.id,
          name: article.title,
          group: 'article',
        });

        for (const tag of article.tags || []) {
          const tagId = `tag:${tag}`;
          tagSet.add(tagId);
          linkList.push({ source: article.id, target: tagId });
        }
      }

      for (const tagId of tagSet) {
        nodeList.push({
          id: tagId,
          name: tagId.replace('tag:', ''),
          group: 'tag',
        });
      }

      setNodes(nodeList);
      setLinks(linkList);
    };

    loadData();
  }, []);

  return (
    <div className="space-y-6">
      <h2 className="text-2xl font-semibold mb-4">Knowledge Graph</h2>
      <div className="h-[600px] border rounded bg-white shadow">
        <ForceGraph2D
          graphData={{ nodes, links }}
          nodeAutoColorBy="group"
          nodeLabel="name"
        />
      </div>
    </div>
  );
}