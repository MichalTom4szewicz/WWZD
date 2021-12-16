import "./styles/App.css";
// import { useState } from "react";
import { RandomChart } from "./components/RandomChart";
import MyUploader from "./components/MyUploader";
// import fileService from "./services/file";

export const App = () => {
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
          <RandomChart />
        </header>
      </div>

      <div id="right">
        <MyUploader />
        {/* <MyDropzone setter={setImage} /> */}
        {/* <button onClick={handleClick}>Send</button> */}
      </div>
    </div>
  );
};
