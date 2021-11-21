import "./App.css";
import { RandomChart } from "./RandomChart";

import {useState} from 'react'

import MyDropzone from './MyDropzone'

import fileService from './services/file'

export const App = () => {

  const [image, setImage] = useState('')

  const handleClick = (e) => {
    e.preventDefault();

    fileService
    .uploadFile({"hello": image})
    .then(r => {
      console.log(r)
    })
  }


  return (
    <div className="App">
      <div id="left">
        <header className="App-header">
          <RandomChart />
        </header>
      </div>

      <div id="right">
        <MyDropzone setter={setImage} />
        <button onClick={handleClick}>
          Send
        </button>
      </div>
    </div>
  );
};
