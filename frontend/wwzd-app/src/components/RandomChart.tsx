import React from "react";
import Plot from "react-plotly.js";

export const RandomChart = () => {
  /**
   * Create array num length with random values from 0 to mul
   */
  const randArr = (num: any, mul: any) => {
    const arr = [];
    const index = [];
    for (let i = 0; i < num; i++) {
      arr.push(Math.random() * mul);
      index.push(i);
    }
    return arr;
  };

  console.log(randArr(4, 10));

  return (
    <Plot
      data={[
        {
          x: randArr(4, 30),
          y: randArr(4, 30),
          z: randArr(4, 30),
          mode: "markers",
          type: "scatter3d",
          marker: { color: "red" },
        },
      ]}
      layout={{
        height: 800,
        width: 1200,
        title: `3D Views`,
      }}
      onRelayout={(figure) => console.log(figure)}
    />
  );
};
