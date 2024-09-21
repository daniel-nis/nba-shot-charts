import React, { useState } from 'react';
import SearchBar from './components/SearchBar';
import ShotChart from './components/ShotChart';

const API_BASE_URL = process.env.REACT_APP_API_BASE_URL;

function App() {
  const [playerName, setPlayerName] = useState('');
  const [imageBase64, setImageBase64] = useState('');
  const [statistics, setStatistics] = useState(null);
  const [favoriteShots, setFavoriteShots] = useState(null);

  const handlePlayerSelect = (name) => {
    setPlayerName(name);
    fetch(`${API_BASE_URL}/api/shot_chart?player_name=${encodeURIComponent(name)}`)
      .then((res) => {
        if (!res.ok) {
          return res.text().then((text) => {
            throw new Error(`HTTP error! status: ${res.status}\n${text}`);
          });
        }
        return res.json();
      })
      .then((data) => {
        if (data.image_base64 && data.statistics && data.favorite_shots) {
          setImageBase64(data.image_base64);
          setStatistics(data.statistics);
          setFavoriteShots(data.favorite_shots);
        } else {
          alert(data.error);
        }
      })
      .catch((err) => {
        console.error('Fetch error:', err);
        alert('Error fetching shot chart.');
      });
  };

  return (
    <div className="min-h-screen flex flex-col items-center">
      <h1 className="text-4xl font-bold mt-8">NBA Shot Chart</h1>
      <SearchBar onPlayerSelect={handlePlayerSelect} />
      {imageBase64 && statistics && favoriteShots && (
        <ShotChart
          imageBase64={imageBase64}
          playerName={playerName}
          statistics={statistics}
          favoriteShots={favoriteShots}
        />
      )}
      <footer className="p-12 mt-auto text-center text-gray-500 text-sm pb-4">
        <p>2023-2024 NBA Shot Chart. Not affiliated with the NBA.</p>
      </footer>
    </div>
  );
}

export default App;
