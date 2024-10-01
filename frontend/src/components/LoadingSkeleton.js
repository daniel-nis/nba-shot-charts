import React from 'react';

const LoadingSkeleton = () => {
    return (
      <div className="mt-6 w-full max-w-screen-xl xl:max-w-6xl 2xl:max-w-screen-2xl px-4 animate-pulse">
        {/* Title Placeholder */}
        <div className="w-full md:w-2/3 mx-auto">
          <h2 className="w-full h-10 bg-gray-700 rounded mb-6">
            <span className="sr-only">Loading player shot chart...</span>
          </h2> 
        </div>

        {/* Shot Chart Image Placeholder */}
        <div className="flex flex-col md:flex-row justify-center items-center md:items-start md:space-x-6">
          <div className="w-full md:w-2/3">
            <div className="w-full h-[800px] md:h-[900px] bg-gray-700 rounded"></div> {/* Shot chart loading placeholder */}
          </div>
        </div>
      </div>
    );
};

export default LoadingSkeleton;
