import React from "react";
import Plot from "react-plotly.js";

export type Cord = [x: number, y: number, z: number, objectClass: string];

export const RandomChart = () => {
  const generateRandomCords = () => {
    const classes = [
      "car",
      "bus",
      "jeep",
      "truck",
      "minibus",
      "plane",
      "sportscar",
      "pickup",
      "minivan",
      "limousine",
      "train",
    ];
    const randomCords: Cord[] = [];
    for (let i = 0; i < 30; i++) {
      const randClass = Math.floor(Math.random() * 11);
      randomCords.push([
        Math.random() * 40,
        Math.random() * 40,
        Math.random() * 40,
        classes[randClass],
      ]);
    }
    return randomCords;
  };

  const cords = generateRandomCords();
  // console.log({ cords });

  const xArray = cords.map((item) => item[0]);
  const yArray = cords.map((item) => item[1]);
  const zArray = cords.map((item) => item[2]);
  const classesArray = cords.map((item) => item[3]);

  return (
    <Plot
      data={[
        {
          x: xArray,
          y: yArray,
          z: zArray,
          text: classesArray,
          // name: "name",
          mode: "markers",
          type: "scatter3d",
          marker: { color: "red", size: 5 },
          hoverinfo: "x+y+z+text",
        },
      ]}
      layout={{
        scene: {
          xaxis: { title: "oś X" },
          yaxis: { title: "oś Y" },
          zaxis: { title: "oś Z" },
        },
        height: 800,
        width: 800,
        title: "Wizualizacja wielkich zbiorów danych",
      }}
      // onHover={() => console.log("zz")}
      onRelayout={(figure) => console.log(figure)}
    />
  );
};
