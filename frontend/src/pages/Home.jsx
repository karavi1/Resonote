import { Link } from "react-router-dom";
import MindMap from "../components/MindMap.jsx";
import React from "react";

export default function Home() {
  return (
    <div>
      <Link to="/articles">View Articles</Link>
      <h1>Resonote Dashboard</h1>
      <p>Visualize your knowledge network below:</p>
      <MindMap />
    </div>
  );
}