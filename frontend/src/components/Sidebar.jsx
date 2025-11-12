// In frontend/src/components/Sidebar.jsx

import React, { useState, useEffect } from 'react';
import axios from 'axios';

export default function Sidebar() {
  const [history, setHistory] = useState([]);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    // This function runs once when the sidebar first loads
    const fetchHistory = async () => {
      // Get the token, just like in your dashboard
      const token = localStorage.getItem('token');
      if (!token) {
        setIsLoading(false);
        return;
      }

      try {
        // Fetch from the new backend endpoint we planned
        const response = await axios.get('http://localhost:8000/history', {
          headers: {
            'Authorization': `Bearer ${token}`,
          },
        });
        setHistory(response.data); // Save the history
      } catch (error) {
        console.error('Failed to fetch history:', error);
      } finally {
        setIsLoading(false);
      }
    };

    fetchHistory();
  }, []); // The empty array [] means this runs only once

  return (
    <aside className="w-64 bg-white p-4 shadow-lg hidden md:block">
      <h3 className="text-xl font-semibold text-gray-700 mb-4 pb-2 border-b">
        Past History
      </h3>
      <ul className="space-y-2">
        {isLoading && <li className="text-gray-500">Loading...</li>}
        
        {!isLoading && history.length === 0 && (
          <li className="text-gray-500 italic">No history found.</li>
        )}

        {!isLoading && history.map((item) => (
          <li 
            key={item.id} 
            className="p-2 text-gray-800 rounded-md hover:bg-gray-100 cursor-pointer truncate"
            title={item.prompt_title} // Shows full text on hover
          >
            {item.prompt_title}
          </li>
        ))}
      </ul>
    </aside>
  );
}