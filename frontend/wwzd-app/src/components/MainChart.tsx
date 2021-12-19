import axios from "axios";
import React, { useEffect, useState } from "react";
import Plot from "react-plotly.js";

export type Cord = [x: number, y: number, z: number, objectClass: string];

export const MainChart = () => {
  const [xArray, setXArray] = useState<number[]>([]);
  const [yArray, setYArray] = useState<number[]>([]);
  const [zArray, setZArray] = useState<number[]>([]);
  const [classesArray, setClassesArray] = useState<string[]>([]);
  const [initLength, setInitLength] = useState(0);
  const [colors, setColors] = useState([]);

  useEffect(() => {
    const getRandomCordsFromServer = async () => {
      const result = await axios.get("http://127.0.0.1:5000/testInit");
      console.log({ result });
      const cords: Cord[] = result.data;

      setXArray(cords.map((item) => item[0]));
      setYArray(cords.map((item) => item[1]));
      setZArray(cords.map((item) => item[2]));
      setClassesArray(cords.map((item) => item[3]));
      setInitLength(cords.length);
      const colorsArray = [];
      for (let i = 0; i < 20; i++) {
        colorsArray.push("red");
      }
      setColors(colorsArray);
    };
    getRandomCordsFromServer();
  }, []);

  // const generateRandomCords = () => {
  //   const classes = [
  //     "car",
  //     "bus",
  //     "jeep",
  //     "truck",
  //     "minibus",
  //     "plane",
  //     "sportscar",
  //     "pickup",
  //     "minivan",
  //     "limousine",
  //     "train",
  //   ];
  //   const randomCords: Cord[] = [];
  //   for (let i = 0; i < 30; i++) {
  //     const randClass = Math.floor(Math.random() * 11);
  //     randomCords.push([
  //       Math.random() * 40,
  //       Math.random() * 40,
  //       Math.random() * 40,
  //       classes[randClass],
  //     ]);
  //   }
  //   return randomCords;
  // };

  // const cords = generateRandomCords();
  // // console.log({ cords });

  // const xArray = cords.map((item) => item[0]);
  // const yArray = cords.map((item) => item[1]);
  // const zArray = cords.map((item) => item[2]);
  // const classesArray = cords.map((item) => item[3]);

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
          marker: {
            color: colors,
            // color: ["red", "blue"],
            size: 5,
            // symbol: ["diamond-open"],
          },
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
