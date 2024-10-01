import React, { useState, useEffect, useRef } from 'react';

function SearchBar({ onPlayerSelect }) {
  const [query, setQuery] = useState('');
  const [suggestions, setSuggestions] = useState([]);
  const [showSuggestions, setShowSuggestions] = useState(false);
  const suggestionBoxRef = useRef();
  const inputRef = useRef();

  const API_BASE_URL = process.env.REACT_APP_API_BASE_URL;

  useEffect(() => {
    if (query.length > 0) {
      fetch(`/api/players?q=${encodeURIComponent(query)}`)
      // fetch(`${API_BASE_URL}/api/players?q=${encodeURIComponent(query)}`)
        .then((res) => {
          if (!res.ok) {
            throw new Error(`HTTP error! status: ${res.status}`);
          }
          return res.json();
        })
        .then((data) => {
          setSuggestions(data);
          if (data.length > 0) {
            setShowSuggestions(true);
          } else {
            setShowSuggestions(false);
          }
        })
        .catch((err) => {
          console.error('Fetch error:', err);
          setSuggestions([]);
          setShowSuggestions(false);
        });
    } else {
      setSuggestions([]);
      setShowSuggestions(false);
    }
  }, [query, API_BASE_URL]);

  // Close suggestions when clicking outside or on the input
  useEffect(() => {
    const handleClick = (event) => {
      if (
        suggestionBoxRef.current &&
        !suggestionBoxRef.current.contains(event.target) &&
        inputRef.current &&
        !inputRef.current.contains(event.target)
      ) {
        setShowSuggestions(false);
      }
      // If clicked on the input, close suggestions
      if (inputRef.current && inputRef.current.contains(event.target)) {
        setShowSuggestions(false);
      }
    };
    document.addEventListener('mousedown', handleClick);
    return () => document.removeEventListener('mousedown', handleClick);
  }, []);

  const handleSelect = (name) => {
    setQuery(name);
    setShowSuggestions(false);
    onPlayerSelect(name);
  };

  return (
    <div className="relative mt-6 w-full max-w-md">
      <input
        ref={inputRef}
        type="text"
        className="w-full px-4 py-2 rounded-lg bg-gray-800 text-white focus:outline-none focus:ring-1 focus:ring-stone-50 border border-white"
        placeholder="Search for a player..."
        value={query}
        onChange={(e) => setQuery(e.target.value)}
        onFocus={() => {
          // Do not show suggestions on focus
        }}
      />
      {showSuggestions && (
        <ul
          ref={suggestionBoxRef}
          className="absolute z-10 w-full bg-gray-800 mt-1 rounded-lg overflow-hidden shadow-lg"
        >
          {suggestions.map((suggestion, index) => (
            <li
              key={index}
              className="px-4 py-2 hover:bg-gray-700 cursor-pointer"
              onClick={() => handleSelect(suggestion)}
            >
              {suggestion}
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}

export default SearchBar;
