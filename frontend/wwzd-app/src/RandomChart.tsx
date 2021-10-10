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

  return (
    <Plot
      data={[
        {
          x: randArr(20, 3),
          y: randArr(20, 3),
          z: randArr(20, 3),
          mode: "markers",
          type: "scatter3d",
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
