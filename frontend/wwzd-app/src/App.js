import "./styles/App.css";
import { useState } from "react";
import MyUploader from "./components/MyUploader.js";
import { MainChart } from "./components/MainChart";
import fileService from "./services/file";

const options = [
  { value: 'pickup', label: 'pickup' },
  { value: 'convertible', label: 'convertible' },
  { value: 'sports_car', label: 'sports_car' },
  { value: 'minivan', label: 'minivan' },
  { value: 'beach_wagon', label: 'beach_wagon' },
  { value: 'limousine', label: 'limousine' },
  { value: 'racer', label: 'racer' },
  { value: 'jeep', label: 'jeep' },
  { value: 'tow_truck', label: 'tow_truck' },
  { value: 'cab', label: 'cab' },
  { value: 'minibus', label: 'minibus' },
  { value: 'passenger_car', label: 'passenger_car' },
]

const Checkbox = ({ label, value, onChange }) => {
  return (
    <label>
      <input type="checkbox" checked={value} onChange={onChange} />
      {label}
    </label>
  );
};

const Select = ({ label, value, onChange }) => {
  return (
    <label>{label}:
      <select value={value} onChange={onChange}>
        {options.map((option) => (
          <option value={option.value}>{option.label}</option>
        ))}
      </select>
    </label>
  );
};

export const App = () => {
  const [xArray, setXArray] = useState([]);
  const [yArray, setYArray] = useState([]);
  const [zArray, setZArray] = useState([]);
  const [namesArray, setNamesArray] = useState([]);

  const [method, setMethod] = useState([1, 0, 0]);
  const [ifClass, setIfClass] = useState(false);
  const [axes, setAxes] = useState(["pickup", "convertible", "sports_car"]);
  const methodsArray = ["pca", "umap", "no_whiten"]

  const handleMethod = (index) => {
    let met = method.map(m => 0)//Math.abs(m-1))
    met[index] = 1
    setMethod(met)
    fileService.changeMethod({"method": methodsArray[index]}).then((response) => {
      console.log(response)
      // let response = JSON.parse(xhr.response);

      const cords = response.data;
      setXArray(cords.map((item) => item.x));
      setYArray(cords.map((item) => item.y));
      setZArray(cords.map((item) => item.z));
      setNamesArray(cords.map((item) => item.filename));
    })
  }

  const handleAxes = (e, i) => {
    let ax = [...axes];
    ax[i] = e.target.value;
    setAxes(ax);
    if (ifClass) {
      fileService.changeAxes({"axes": ax}).then((response) => {
        console.log(response)
  
        const cords = response.data;
        setXArray(cords.map((item) => item.x));
        setYArray(cords.map((item) => item.y));
        setZArray(cords.map((item) => item.z));
        setNamesArray(cords.map((item) => item.filename));
      })
    }
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
            axesNames={ifClass ? axes : undefined}
          />
        </header>
      </div>

      <div id="right">
        <p>Choose method of Dimensionality Reduction:</p>

        <Checkbox
          label="PCA"
          value = {method[0] ? true : false}
          onChange={()=>handleMethod(0)}
        />
        <Checkbox
          label="UMAP"
          value = {method[1] ? true : false}
          onChange={()=>handleMethod(1)}
        />
        <Checkbox
          label="PCA (no whitening)"
          value = {method[2] ? true : false}
          onChange={()=>handleMethod(2)}
        />
        <Checkbox
          label="Class"
          value = {ifClass}
          onChange={()=>setIfClass(!ifClass)}
        />
        <p>
          <Select
            label="X"
            value = {axes[0]}
            onChange={(e) => handleAxes(e, 0)}
          />
          <Select
            label="Y"
            value = {axes[1]}
            onChange={(e) => handleAxes(e, 1)}
          />
          <Select
            label="Z"
            value = {axes[2]}
            onChange={(e) => handleAxes(e, 2)}
          />
        </p>

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
