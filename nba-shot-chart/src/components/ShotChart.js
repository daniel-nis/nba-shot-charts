// src/components/ShotChart.js
import React from 'react';

function ShotChart({ imageUrl, playerName }) {
  return (
    <div className="mt-6 w-full max-w-3xl">
      <img src={imageUrl} alt="Shot Chart" className="w-full h-auto rounded-lg pb-8" />
    </div>
    
  );
}

export default ShotChart;
