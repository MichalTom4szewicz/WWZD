import "./styles/App.css";
import { useState } from "react";
import MyUploader from "./components/MyUploader.js";
import { MainChart } from "./components/MainChart";
// import fileService from "./services/file";

export const App = () => {
  const [xArray, setXArray] = useState([]);
  const [yArray, setYArray] = useState([]);
  const [zArray, setZArray] = useState([]);
  const [namesArray, setNamesArray] = useState([]);
  // const [image, setImage] = useState("");

  // const handleClick = (e) => {
  //   e.preventDefault();

  //   fileService
  //     .uploadFile({ hello: image })
  //     // .uploadFile(image)
  //     .then((r) => {
  //       console.log(r);
  //     });
  // };

  return (
    <div className="App">
      <div id="left">
        <header className="App-header">
          <MainChart
            xArray={xArray}
            setXArray={setXArray}
            yArray={yArray}
            setYArray={setYArray}
            zArray={zArray}
            setZArray={setZArray}
            namesArray={namesArray}
            setNamesArray={setNamesArray}
          />
        </header>
      </div>

      <div id="right">
        <MyUploader
          setXArray={setXArray}
          setYArray={setYArray}
          setZArray={setZArray}
          setNamesArray={setNamesArray}
        />
        {/* <MyDropzone setter={setImage} /> */}
        {/* <button onClick={handleClick}>Send</button> */}
      </div>
    </div>
  );
};
