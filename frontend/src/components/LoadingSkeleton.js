import React from 'react';

const LoadingSkeleton = () => {
    return (
      <div className="mt-6 w-full max-w-6xl px-4 animate-pulse">
        {/* Title */}
        <h2 className="text-3xl font-bold text-center mb-6 h-10 bg-gray-300 rounded"></h2>
  
        <div className="flex flex-col md:flex-row items-center md:items-start md:space-x-6">
          {/* Larger Shot Chart Image Placeholder */}
          <div className="w-full md:w-2/3">
            <div className="w-full h-[500px] md:h-[600px] bg-gray-300 rounded"></div> {/* Updated height */}
          </div>
  
          {/* Statistics and Favorite Shots */}
          <div className="w-full md:w-1/3 mt-6 md:mt-0">
            {/* Statistics */}
            <div className="p-6 pt-2 pb-2">
              <h3 className="text-2xl font-semibold mb-4 text-center h-8 bg-gray-300 rounded"></h3>
              <ul className="space-y-2">
                {/* Create placeholders for each stat */}
                {Array(8).fill().map((_, index) => (
                  <li
                    key={index}
                    className="flex justify-between bg-gray-300 h-8 rounded p-2"
                  ></li>
                ))}
              </ul>
            </div>
  
            {/* Favorite Shots */}
            <div className="p-6 rounded-lg">
              <h3 className="text-2xl font-semibold mb-4 text-center h-8 bg-gray-300 rounded"></h3>
              <ul className="space-y-2">
                {/* Create placeholders for each favorite shot */}
                {Array(5).fill().map((_, index) => (
                  <li
                    key={index}
                    className="flex justify-between bg-gray-300 h-8 rounded p-2"
                  ></li>
                ))}
              </ul>
            </div>
          </div>
        </div>
      </div>
    );
  };

export default LoadingSkeleton;