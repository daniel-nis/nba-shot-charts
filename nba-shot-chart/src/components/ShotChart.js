/*import React from 'react';

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
        <p>Clutch FG %: {(statistics.clutch_fg_percentage * 100).toFixed(1)}%</p>
      </div>
    </div>
  );
}

export default ShotChart;*/

// src/components/ShotChart.js

import React from 'react';

function ShotChart({ imageBase64, playerName, statistics, favoriteShots }) {
  const imageUrl = `data:image/png;base64,${imageBase64}`;

  return (
    <div className="mt-6 w-full max-w-6xl px-4">
      <h2 className="text-3xl font-bold text-center mb-6">{playerName}'s Shot Chart</h2>
      <div className="flex flex-col md:flex-row items-center md:items-start md:space-x-6">
        <div className="w-full md:w-2/3">
          <img src={imageUrl} alt="Shot Chart" className="w-full h-auto" />
        </div>
        <div className="w-full md:w-1/3 mt-6 md:mt-0">
          <div className="p-6 pt-2 pb-2">
            <h3 className="text-2xl font-semibold mb-4 text-center">Statistics</h3>
            <ul className="space-y">
              {[
                { label: 'Total Shot Attempts', value: statistics.total_shots },
                { label: 'Field Goal Percentage', value: `${(statistics.total_make_percentage * 100).toFixed(1)}%` },
                { label: '3-Point Attempts', value: statistics.three_point_attempts },
                { label: '3-Point Percentage', value: `${(statistics.three_point_percentage * 100).toFixed(1)}%` },
                { label: '2-Point Attempts', value: statistics.two_point_attempts },
                { label: '2-Point Percentage', value: `${(statistics.two_point_percentage * 100).toFixed(1)}%` },
                { label: 'Clutch FG Percentage', value: `${(statistics.clutch_fg_percentage * 100).toFixed(1)}%` },
                { label: 'Avg. Shot Distance', value: `${statistics.average_shot_distance.toFixed(1)} ft` },
              ].map((stat, index) => (
                <li key={index} className="flex justify-between hover:bg-gray-700 p-2 rounded transition-default">
                  <span>{stat.label}:</span>
                  <span>{stat.value}</span>
                </li>
              ))}
            </ul>
          </div>
          <div className="p-6 rounded-lg">
            <h3 className="text-2xl font-semibold mb-4 text-center">Favorite Shots</h3>
            <ul className="space-y">
              {Object.entries(favoriteShots).map(([actionType, count], index) => (
                <li key={index} className="flex justify-between hover:bg-gray-700 p-2 rounded transition-default">
                  <span>{actionType}</span>
                  <span>{count}</span>
                </li>
              ))}
            </ul>
          </div>
        </div>
      </div>
    </div>
  );
}

export default ShotChart;

