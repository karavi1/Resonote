// src/App.js
import React from "react";
import { BrowserRouter as Router, Route, Routes } from "react-router-dom";
import Articles from "./pages/Articles.jsx";
import Home from "./pages/Home.jsx";
import Reflection from "./pages/Reflection.jsx";

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/articles" element={<Articles />} />
        <Route path="/reflect/:articleId" element={<Reflection />} />
      </Routes>
    </Router>
  );
}

export default App;