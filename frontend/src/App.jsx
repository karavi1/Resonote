import React from 'react';
import { Routes, Route, Link } from 'react-router-dom';
import Articles from './pages/Articles';
import Dashboard from './pages/Dashboard';

export default function App() {
  return (
    <div className="min-h-screen bg-gray-50 text-gray-900">
      <header className="p-4 bg-white shadow flex justify-between items-center">
        <Link to="/" className="text-2xl font-bold text-blue-600">Resonote</Link>
        <nav className="space-x-4">
          <Link to="/articles" className="text-blue-500 hover:underline">Articles</Link>
          <Link to="/dashboard" className="text-blue-500 hover:underline">Dashboard</Link>
        </nav>
      </header>

      <main className="p-6">
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/articles" element={<Articles />} />
          <Route path="/dashboard" element={<Dashboard />} />
        </Routes>
      </main>
    </div>
  );
}


function Home() {
  return (
    <div className="text-center space-y-4">
      <h1 className="text-3xl font-semibold">Welcome to Resonote</h1>
      <p className="text-gray-600">Your space for curated reading, reflection, and insight.</p>
      <div className="space-x-4">
        <Link to="/articles" className="text-blue-600 underline">Explore Articles</Link>
        <Link to="/dashboard" className="text-blue-600 underline">View Knowledge Graph</Link>
      </div>
    </div>
  );
}