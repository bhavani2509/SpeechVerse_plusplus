import React, { useState } from 'react';
import axios from 'axios';

function FileUpload({ setFullTranscription }) {
  const [file, setFile] = useState(null);

  const uploadFile = async () => {
    if (!file) return alert("Please select a file!");

    const formData = new FormData();
    formData.append("file", file);

    try {
        const response = await axios.post('http://127.0.0.1:8000/process/', formData, {
        headers: { 'Content-Type': 'multipart/form-data' }
      });
      console.log(response);
      setFullTranscription(response.data.transcription + "\n\nResponse: " + response.data.response);
    } catch (err) {
      console.error(err);
      alert("Upload failed!");
    }
  };

  return (
    <div>
      <input type="file" accept="audio/*" onChange={e => setFile(e.target.files[0])} />
      <button onClick={uploadFile}>Upload and Transcribe</button>
    </div>
  );
}

export default FileUpload;
