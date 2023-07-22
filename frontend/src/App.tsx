import React from "react";

function randomNumberInRange(min: number, max: number) {
  return Math.floor(Math.random() * (max - min + 1)) + min;
}

function App() {
  const nums: number[] = Array(50)
    .fill(undefined)
    .map(() => randomNumberInRange(0, 100));

  return (
    <div className="min-h-screen bg-slate-800 text-slate-100 p-4 text-xl">
      <h1>hello world</h1>

      {nums.map((num) => (
        <p>{num}</p>
      ))}
    </div>
  );
}

export default App;
