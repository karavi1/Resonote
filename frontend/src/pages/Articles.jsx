import React, { useEffect, useState } from "react";
import axios from "axios";

export default function Articles() {
  const [articles, setArticles] = useState([]);

  useEffect(() => {
    console.log("Fetching articles...");
  
    axios.get("/api/articles")
      .then(res => {
        console.log("Articles loaded:", res.data);
        setArticles(res.data);
      })
      .catch(err => {
        console.error("Failed to load articles", err);
      });
  }, []);


  return (
    <div>
      <h2>Articles</h2>
      <ul>
        {articles.map(article => (
          <li key={article.id}>
            <strong>{article.title}</strong> — {article.source}
          </li>
        ))}
      </ul>
    </div>
  );
}