import React from 'react';

function Statistic({ label, value, teamColor }) {
  return (
    <div className="text-center mb-8">
      <span className="text-l font-bold text-white">{label}</span>
      <p className="text-xl font-bold tracking-wide" style={{ color: teamColor }}>{value}</p>
    </div>
  );
}

function ShotChart({ imageBase64, playerName, statistics, favoriteShots, teamColor }) {
  const imageUrl = `data:image/png;base64,${imageBase64}`;

  return (
    <div className="mt-6 w-full max-w-screen-xl xl:max-w-6xl 2xl:max-w-screen-2xl px-4">
      <h2 className="text-3xl font-bold text-center mb-6">{playerName}'s Shot Chart</h2>
      <div className="flex flex-col md:flex-row justify-center items-center md:items-start md:space-x-6">
        <div className="w-full md:w-2/3">
          <img src={imageUrl} alt="Shot Chart" className="w-full h-auto" />
        </div>
      </div>
      {/* Statistics section */}
      <div className="pt-10 p-6 grid grid-cols-1 md:grid-cols-3 justify-items-center md:max-w-[85%] mx-auto">
        <Statistic label="Total FG" value={statistics.total_shots} teamColor={teamColor} />
        <Statistic label="FG%" value={`${(statistics.total_make_percentage * 100).toFixed(1)}`} teamColor={teamColor} />
        <Statistic label="Avg. Shot Distance" value={`${statistics.average_shot_distance.toFixed(1)} ft`} teamColor={teamColor} />
        {/* <Statistic label="3-Point Attempts" value={statistics.three_point_attempts} /> */}
        <Statistic label="3-Point Percentage" value={`${(statistics.three_point_percentage * 100).toFixed(1)}%`} teamColor={teamColor} />
        {/* <Statistic label="2-Point Attempts" value={statistics.two_point_attempts } /> */}
        <Statistic label="2-Point Percentage" value={`${(statistics.two_point_percentage * 100).toFixed(1)}%`} teamColor={teamColor} />
        <Statistic label="Clutch FG Percentage" value={`${(statistics.clutch_fg_percentage * 100).toFixed(1)}%`} teamColor={teamColor} />
      </div>
    </div>
    
  );
}

export default ShotChart;

