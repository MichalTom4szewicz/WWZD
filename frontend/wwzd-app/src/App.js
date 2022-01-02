import "./styles/App.css";
import { useState } from "react";
import MyUploader from "./components/MyUploader.js";
import { MainChart } from "./components/MainChart";
import fileService from "./services/file";

const Checkbox = ({ label, value, onChange }) => {
  return (
    <label>
      <input type="checkbox" checked={value} onChange={onChange} />
      {label}
    </label>
  );
};

export const App = () => {
  const [xArray, setXArray] = useState([]);
  const [yArray, setYArray] = useState([]);
  const [zArray, setZArray] = useState([]);
  const [namesArray, setNamesArray] = useState([]);

  const [method, setMethod] = useState([1, 0]);

  const handleMethod = () => {
    let me = method;
    let met = me.map(m => Math.abs(m-1))
    setMethod(met)
    fileService.changeMethod({"method": met[0] ? "pca" : "umap"}).then((response) => {
      console.log(response)
      // let response = JSON.parse(xhr.response);

      const cords = response.data;
      setXArray(cords.map((item) => item.x));
      setYArray(cords.map((item) => item.y));
      setZArray(cords.map((item) => item.z));
      setNamesArray(cords.map((item) => item.filename));
    })
  }

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
        <p>Choose method of Dimensionality Reduction:</p>

        <Checkbox
          label="PCA"
          value = {method[0] ? true : false}
          onChange={handleMethod}
        />
        <Checkbox
          label="UMAP"
          value = {method[1] ? true : false}
          onChange={handleMethod}
        />

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
