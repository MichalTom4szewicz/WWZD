import {useCallback} from 'react'
import {useDropzone} from 'react-dropzone'

import './MyDropzone.css'

const MyDropzone = ({setter}) => {
  const onDrop = useCallback((acceptedFiles) => {
    acceptedFiles.forEach((file) => {
      const reader = new FileReader()

      reader.onabort = () => console.log('file reading was aborted')
      reader.onerror = () => console.log('file reading has failed')
      reader.onload = () => {
      }
      console.log(file.path);
      console.log(file)

      setter(file.path)
    })

  }, [])

  const {getRootProps, getInputProps} = useDropzone({onDrop})

  return (
    <div id="dropzone" {...getRootProps()}>
      <input {...getInputProps()} />
      <p id="text">Drop file or click to choose path</p>
    </div>
  )
}

export default MyDropzone;
