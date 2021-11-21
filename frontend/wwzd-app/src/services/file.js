import axios from 'axios'

const serverUrl = 'http://127.0.0.1:5000'

const uploadFile = (file) => {
  const request = axios.post(`${serverUrl}/file`, file)
  return request.then(response => response.data)
}

export default {
  uploadFile,
}