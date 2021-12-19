import React from "react";
import "react-dropzone-uploader/dist/styles.css";
import Dropzone from "react-dropzone-uploader";

const MyUploader = ({ setXArray, setYArray, setZArray, setNamesArray }) => {
  // specify upload params and url for your files
  const getUploadParams = ({ meta }) => {
    // console.log(meta);
    return { url: "http://127.0.0.1:5000/file" };
  };

  // called every time a file's `status` changes
  const handleChangeStatus = ({ meta, file, xhr }, status) => {
    /*console.log(status, meta, file)*/
    if (status === "done") {
      let response = JSON.parse(xhr.response);

      const cords = response.data;
      setXArray(cords.map((item) => item.x));
      setYArray(cords.map((item) => item.y));
      setZArray(cords.map((item) => item.z));
      setNamesArray(cords.map((item) => item.filename));
    }
  };

  // receives array of files that are done uploading when submit button is clicked
  const handleSubmit = (files, allFiles) => {
    // console.log(files.map((f) => f.meta));
    allFiles.forEach((f) => f.remove());
  };

  return (
    <Dropzone
      getUploadParams={getUploadParams}
      onChangeStatus={handleChangeStatus}
      onSubmit={handleSubmit}
      accept="image/*,audio/*,video/*"
    />
  );
};

export default MyUploader;
