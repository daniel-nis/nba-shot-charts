// src/components/ShotChart.js

import React from 'react';

function ShotChart({ imageBase64, playerName, statistics }) {
  const imageUrl = `data:image/png;base64,${imageBase64}`;
  return (
    <div className="mt-6 w-full max-w-3xl">
      <h2 className="text-2xl font-semibold text-center mb-4">{playerName}'s Shot Chart</h2>
      <img src={imageUrl} alt="Shot Chart" className="w-full h-auto pb-8" />
      <div className="mt-4 text-center">
        <h3 className="text-xl font-semibold mb-2">Statistics</h3>
        <p>Total Shot Attempts: {statistics.total_shots}</p>
        <p>Total Make %: {(statistics.total_make_percentage * 100).toFixed(1)}%</p>
        <p>3-Point Attempts: {statistics.three_point_attempts}</p>
        <p>3-Point %: {(statistics.three_point_percentage * 100).toFixed(1)}%</p>
        <p>2-Point Attempts: {statistics.two_point_attempts}</p>
        <p>2-Point %: {(statistics.two_point_percentage * 100).toFixed(1)}%</p>
        <p>Average Shot Distance: {statistics.average_shot_distance.toFixed(1)} ft.</p>
      </div>
    </div>
  );
}

export default ShotChart;
