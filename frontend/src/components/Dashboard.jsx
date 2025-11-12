// In frontend/src/components/Dashboard.jsx

import React, { useState } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';
import Sidebar from './Sidebar'; // <-- 1. IMPORT THE SIDEBAR

export default function Dashboard() {
  const [text, setText] = useState('');
  const [result, setResult] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState('');
  const navigate = useNavigate();

  const handleLogout = () => {
    localStorage.removeItem('accessToken');
    navigate('/login');
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setIsLoading(true);
    setError('');
    setResult(null);
    const token = localStorage.getItem('token');

    try {
      const response = await axios.post('http://localhost:8000/analyze-text/', { text }, {
        headers: { 'Authorization': `Bearer ${token}` }
      });
      setResult(response.data);
      // NOTE: We'll need to make this reload the sidebar later
    } catch (err) {
      setError('An error occurred during analysis. Please try again.');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="flex h-screen bg-gray-100"> {/* <-- 2. CHANGED to flex and h-screen */}
      
      {/* --- Sidebar --- */}
      {/* This is our new component */}
      <Sidebar />

      {/* --- Main Content Area (wrapper) --- */}
      <div className="flex-1 flex flex-col overflow-hidden"> {/* <-- 3. ADDED this wrapper */}
        
        {/* Navigation Bar (Stays the same) */}
        <nav className="flex justify-between items-center p-4 bg-white shadow-md">
          <h1 className="text-xl font-bold text-gray-800">Legal AI Advisor</h1>
          <button 
            onClick={handleLogout} 
            className="px-4 py-2 font-semibold text-white bg-blue-600 rounded-lg shadow hover:bg-blue-700 transition-colors"
          >
            Logout
          </button>
        </nav>

        {/* Main Content (with scrolling) */}
        <main className="p-4 sm:p-8 flex-1 overflow-y-auto"> {/* <-- 4. CHANGED to be scrollable */}
          <div className="max-w-4xl mx-auto">
            {/* Input Form Card (Stays the same) */}
            <form onSubmit={handleSubmit} className="p-6 bg-white rounded-lg shadow-lg">
              {/* ...all your form content... */}
              <h2 className="text-2xl font-semibold mb-4 text-gray-700">Analyze Document Text</h2>
              <textarea
                className="w-full p-4 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 transition-shadow"
                rows="15"
                value={text}
                onChange={(e) => setText(e.target.value)}
                placeholder="Paste your legal document text here..."
                required
              />
              <button 
                type="submit" 
                disabled={isLoading} 
                className="w-full mt-4 py-3 font-semibold text-white bg-blue-600 rounded-lg shadow hover:bg-blue-700 disabled:bg-gray-400 disabled:cursor-not-allowed transition-colors"
              >
                {isLoading ? 'Analyzing...' : 'Analyze Text'}
              </button>
            </form>

            {/* Error Display (Stays the same) */}
            {error && <p className="mt-4 text-center text-red-600 font-medium">{error}</p>}

            {/* Results Display Card (Stays the same) */}
            {result && (
              <div className="mt-8 p-6 bg-white rounded-lg shadow-lg animate-fade-in">
                {/* ...all your result content... */}
                <h3 className="text-xl font-semibold mb-4 pb-2 border-b border-gray-200 text-gray-800">Analysis Results</h3>
                <div className="space-y-6">
                  <div>
                    <h4 className="font-bold text-gray-600">Summary:</h4>
                    <p className="mt-2 text-gray-700 whitespace-pre-wrap leading-relaxed">{result.summary}</p>
                  </div>
                  <div>
                    <h4 className="font-bold text-gray-600">Citations Found:</h4>
                    <ul className="mt-2 space-y-2 list-disc list-inside">
                      {result.hyperlinks.length > 0 ? (
                        result.hyperlinks.map((link, index) => (
                          <li key={index} className="text-gray-700">
                            <a href={link.url} target="_blank" rel="noopener noreferrer" className="text-blue-600 hover:underline hover:text-blue-800 transition-colors">
                              {link.citation_text}
                            </a>
                          </li>
                        ))
                      ) : (
                        <li className="text-gray-500">No citations were found.</li>
                      )}
                    </ul>
                  </div>
                </div>
              </div>
            )}
          </div>
        </main>
      </div>
    </div>
  );
}