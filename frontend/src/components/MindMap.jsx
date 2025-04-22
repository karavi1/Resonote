import React, { useEffect, useState } from "react";
import ForceGraph2D from "react-force-graph-2d";
import axios from "axios";

export default function MindMap() {
  const [graphData, setGraphData] = useState({ nodes: [], links: [] });

  useEffect(() => {
    // Example: get articles and reflections and turn into graph
    axios.get("/api/articles").then((res) => {
      const articles = res.data;

      const nodes = [];
      const links = [];

      articles.forEach((article) => {
        const articleNodeId = `article-${article.id}`;

        nodes.push({ id: articleNodeId, name: article.title, group: "article" });

        // Link to tags
        if (article.tags) {
          article.tags.split(",").forEach((tag) => {
            const tagId = `tag-${tag.trim().toLowerCase()}`;
            if (!nodes.find((n) => n.id === tagId)) {
              nodes.push({ id: tagId, name: tag.trim(), group: "tag" });
            }
            links.push({ source: articleNodeId, target: tagId });
          });
        }

        // Optional: link reflections when available (pseudo-code example)
        // You can make an API call to /reflections here if needed
      });

      setGraphData({ nodes, links });
    });
  }, []);

  return (
    <div>
      <h3>Knowledge Graph</h3>
      <ForceGraph2D
        graphData={graphData}
        nodeLabel="name"
        nodeAutoColorBy="group"
        linkDirectionalParticles={2}
        width={800}
        height={600}
      />
    </div>
  );
}