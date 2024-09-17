import React, { useState } from 'react';
import SearchBar from './components/SearchBar';
import ShotChart from './components/ShotChart';

function App() {
  const [playerName, setPlayerName] = useState('');
  const [imageUrl, setImageUrl] = useState('');

  const handlePlayerSelect = (name) => {
    setPlayerName(name);
    fetch(`/api/shot_chart?player_name=${encodeURIComponent(name)}`)
      .then((res) => res.json())
      .then((data) => {
        if (data.image_url) {
          setImageUrl(data.image_url);
        } else {
          alert(data.error);
        }
      })
      .catch((err) => {
        console.error(err);
        alert('Error fetching shot chart.');
      });
  };

  return (
    <div className="min-h-screen flex flex-col items-center">
      <h1 className="text-3xl font-bold mt-8">NBA Shot Chart</h1>
      <SearchBar onPlayerSelect={handlePlayerSelect} />
      {imageUrl && <ShotChart imageUrl={imageUrl} playerName={playerName} />}
    </div>
  );
}

export default App;
