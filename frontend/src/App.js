import React, { useState } from 'react';
import SearchBar from './components/SearchBar';
import ShotChart from './components/ShotChart';
import LoadingSkeleton from './components/LoadingSkeleton';

const API_BASE_URL = process.env.REACT_APP_API_BASE_URL;

function App() {
  const [playerName, setPlayerName] = useState('');
  const [imageBase64, setImageBase64] = useState('');
  const [statistics, setStatistics] = useState(null);
  const [favoriteShots, setFavoriteShots] = useState(null);
  const [teamColor, setTeamColor] = useState('');
  const [loading, setLoading] = useState(false);

  const handlePlayerSelect = (name) => {
    setPlayerName(name);
    setLoading(true);
    // fetch(`/api/shot_chart?player_name=${encodeURIComponent(name)}`)
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
        setLoading(false);
        if (data.image_base64 && data.statistics && data.favorite_shots && data.team_color) {
          setImageBase64(data.image_base64);
          setStatistics(data.statistics);
          setFavoriteShots(data.favorite_shots);
          setTeamColor(data.team_color);
        } else {
          alert(data.error);
        }
      })
      .catch((err) => {
        setLoading(false);
        console.error('Fetch error:', err);
        alert('Error fetching shot chart.');
      });
  };

  return (
    <div className="min-h-screen flex flex-col items-center">
      <h1 className="text-4xl font-bold mt-8">NBA Shot Chart</h1>
      <SearchBar onPlayerSelect={handlePlayerSelect} />
      {loading ? (
        <LoadingSkeleton />
      ) : (
        imageBase64 && statistics && favoriteShots && (
          <ShotChart
            imageBase64={imageBase64}
            playerName={playerName}
            statistics={statistics}
            favoriteShots={favoriteShots}
            teamColor={teamColor}
          />
        )
      )}
      <footer className="p-12 mt-auto text-center text-gray-500 text-sm pb-4">
        <p>2023-2024 NBA Shot Chart. Not affiliated with the NBA.</p>
        <p>
          Made by 
          <a 
            href="https://twitter.com/dotproductt" 
            target="_blank" 
            rel="noopener noreferrer" 
            className="text-blue-500 hover:underline"
          > @dotproductt
          </a>
        </p>
      </footer>
    </div>
  );
}

export default App;
