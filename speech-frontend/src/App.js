import React, { useState } from 'react';
import FileUpload from './FileUpload';
import Recorder from './Recorder';

function App() {
  const [fullTranscription, setFullTranscription] = useState("");
  const [liveTranscription, setLiveTranscription] = useState("");

  return (
    <div style={{ padding: 20 }}>
      <h1>🎤 VoiceWave Frontend</h1>

      <h2>📂 Upload Audio File (Full Transcription)</h2>
      <FileUpload setFullTranscription={setFullTranscription} />

      <div style={{ marginTop: 20 }}>
        <h3>Full Transcription:</h3>
        <textarea rows={6} cols={80} value={fullTranscription} readOnly />
      </div>

      <hr style={{ margin: '40px 0' }} />

      <h2>🎙️ Record and Get Real-Time Transcription</h2>
      <Recorder setLiveTranscription={setLiveTranscription} />

      <div style={{ marginTop: 20 }}>
        <h3>Live Transcription:</h3>
        <textarea rows={6} cols={80} value={liveTranscription} readOnly />
      </div>
    </div>
  );
}

export default App;
