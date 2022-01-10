import React, { useEffect, useState } from "react";
import axios from "axios";
import Plot from "react-plotly.js";
import "../styles/App.css";

export type Cord = {
  x: number;
  y: number;
  z: number;
  filename?: string;
  classname?: string;
};

export const MainChart = ({
  xArray,
  setXArray,
  yArray,
  setYArray,
  zArray,
  setZArray,
  namesArray,
  setNamesArray,
  axesNames,
  classesArray,
  setClassesArray,
  loading,
  setLoading,
}) => {
  const [colors, setColors] = useState<string[]>([]);
  const [loading2, setLoading2] = useState(false);
  const [image, setImage] = useState("");
  const [camera, setCamera] = useState({
    up: { x: 0, y: 0, z: 1 },
    center: { x: 0, y: 0, z: 0 },
    eye: { x: 1.25, y: 1.25, z: 1.25 },
  });

  useEffect(() => {
    setLoading2(loading);
  }, [loading]);

  useEffect(() => {
    const getImgs = async () => {
      try {
        const result = await axios.get("http://127.0.0.1:5000/imgs");
        console.log({ result });
        const cords: Cord[] = result.data?.data;
        const colorsArray = [];
        setXArray(
          cords.map((item) => {
            switch (item.classname) {
              case "pickup": {
                colorsArray.push("blue");
                break;
              }
              case "convertible": {
                colorsArray.push("orange");
                break;
              }
              case "minivan": {
                colorsArray.push("green");
                break;
              }
              case "beach_wagon": {
                colorsArray.push("yellow");
                break;
              }
              case "sports_car": {
                colorsArray.push("red");
                break;
              }
              case "limousine": {
                colorsArray.push("white");
                break;
              }
              case "racer": {
                colorsArray.push("pink");
                break;
              }
              case "jeep": {
                colorsArray.push("silver");
                break;
              }
              case "cab": {
                colorsArray.push("brown");
                break;
              }
              case "minibus": {
                colorsArray.push("purple");
                break;
              }
              case "passenger_car": {
                colorsArray.push("magenta");
                break;
              }
              case "other": {
                colorsArray.push("black");
                break;
              }
              default: {
                colorsArray.push("black");
                break;
              }
            }

            return item.x;
          })
        );
        setYArray(cords.map((item) => item.y));
        setZArray(cords.map((item) => item.z));
        setNamesArray(cords.map((item) => item.filename));
        setClassesArray(
          cords.map((item) => {
            // console.log(item.classname);
            return item.classname;
          })
        );
        setColors(colorsArray);
      } catch (e) {
        console.log({ e });
      }
      setLoading(false);
    };
    getImgs();
  }, []);

  return (
    <>
      {loading2 ? (
        <>Ładowanie...</>
      ) : (
        <>
          <img className="image" src={image} alt="..." />

          <Plot
            data={[
              {
                x: xArray,
                y: yArray,
                z: zArray,
                text: namesArray.map(
                  (item: string, i) => item + " - " + classesArray[i]
                ),
                name: "",
                mode: "markers",
                type: "scatter3d",
                marker: {
                  color: colors,
                  size: 5,
                  // symbol: ["diamond-open"],
                },
                hoverinfo: "all",
              },
            ]}
            layout={{
              scene: {
                xaxis: { title: axesNames ? axesNames[0] : "oś X" },
                yaxis: { title: axesNames ? axesNames[1] : "oś Y" },
                zaxis: { title: axesNames ? axesNames[2] : "oś Z" },
                camera: camera,
              },
              height: 800,
              width: 800,
              title: "Wizualizacja wielkich zbiorów danych",
            }}
            revision={0}
            onHover={(e: any) => {
              // console.log(e.points[0]?.text.substring(0, 9));
              setImage(e.points[0]?.text.substring(0, 9) || "");
            }}
            onRelayout={(figure: any) => {
              // console.log(figure);
              if (
                figure["scene.camera"]?.center &&
                figure["scene.camera"]?.up &&
                figure["scene.camera"]?.eye
              ) {
                setCamera({
                  center: figure["scene.camera"].center,
                  up: figure["scene.camera"].up,
                  eye: figure["scene.camera"].eye,
                });
              }
            }}
          />
        </>
      )}
    </>
  );
};

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
