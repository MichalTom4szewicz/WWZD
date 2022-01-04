import axios from "axios";

const serverUrl = "http://127.0.0.1:5000";

const FormData = require("form-data");

const uploadFile = (file) => {
  const request = axios.post(`${serverUrl}/file`, file);
  // const form = new FormData();
  // form.append('file', {'object': file}, 'stickers.jpg');

  // const request = axios.post(`${serverUrl}/file`, form, {
  //   // headers: {
  //   //   ...form.getHeaders(),
  //   //   Authentication: 'Bearer ...',
  //   // },
  //   headers: {
  //     'Content-Type': 'multipart/form-data',
  //     'Access-Control-Allow-Origin': '*'
  //   }
  // })

  // const request = axios.post(`${serverUrl}/file`, file, {
  //   headers: {
  //     'Content-Type': 'multipart/form-data'
  //   }
  // })
  return request.then((response) => response.data);
};

const changeMethod = (method) => {
  const request = axios.post(`${serverUrl}/method`, method);
  return request.then((response) => response.data);
};

const changeAxes = (axes) => {
  const request = axios.post(`${serverUrl}/axes`, axes);
  return request.then((response) => response.data);
};

export default {
  uploadFile,
  changeMethod,
  changeAxes
};
