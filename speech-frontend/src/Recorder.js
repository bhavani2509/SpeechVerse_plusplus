import React, { useState, useRef, useEffect } from 'react';

function Recorder({ setLiveTranscription }) {
  const [recording, setRecording] = useState(false);
  const [recordTime, setRecordTime] = useState(0);
  const [processingTime, setProcessingTime] = useState(null);

  const timerRef = useRef(null);
  const mediaRecorder = useRef(null);
  const audioChunks = useRef([]);

  useEffect(() => {
    if (recording) {
      timerRef.current = setInterval(() => {
        setRecordTime(prev => prev + 1);
      }, 1000);
    } else {
      clearInterval(timerRef.current);
    }

    return () => clearInterval(timerRef.current);
  }, [recording]);

  const startRecording = async () => {
    console.log("🎙️ Requesting microphone access...");
    const stream = await navigator.mediaDevices.getUserMedia({ audio: true });

    audioChunks.current = [];
    mediaRecorder.current = new MediaRecorder(stream);
    setRecordTime(0);
    setProcessingTime(null);

    mediaRecorder.current.ondataavailable = (e) => {
      if (e.data.size > 0) {
        audioChunks.current.push(e.data);
      }
    };

    mediaRecorder.current.onstop = async () => {
      console.log("🛑 Recording stopped.");

      const audioBlob = new Blob(audioChunks.current, { type: 'audio/wav' });
      const formData = new FormData();
      formData.append('file', audioBlob, 'recorded_audio.wav');

      const startTime = performance.now();

      try {
        const response = await fetch("http://localhost:8000/process/", {
          method: "POST",
          body: formData
        });

        const endTime = performance.now();
        const duration = ((endTime - startTime) / 1000).toFixed(2);
        setProcessingTime(duration);

        if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);

        const result = await response.json();
        console.log("✅ Transcription response:", result);

        setLiveTranscription(
          `Processing Time: ${duration} seconds\n\n` +
          result.transcription +
          "\n\nResponse: " +
          result.response
        );
      } catch (err) {
        console.error("❌ Upload failed:", err);
        alert("Transcription failed.");
        setProcessingTime(null);
      }
    };

    mediaRecorder.current.start();
    setRecording(true);
    console.log("🔴 Recording started...");
  };

  const stopRecording = () => {
    if (mediaRecorder.current && mediaRecorder.current.state !== "inactive") {
      mediaRecorder.current.stop();
    }
    setRecording(false);
  };

  return (
    <div>
      {!recording ? (
        <button onClick={startRecording}>🎙️ Start Recording</button>
      ) : (
        <button onClick={stopRecording}>🛑 Stop Recording</button>
      )}

      {recording && (
        <p>⏱️ Recording: {recordTime} second{recordTime !== 1 ? 's' : ''}</p>
      )}

      {processingTime && (
        <p>✅ Transcription processed in {processingTime} seconds</p>
      )}
    </div>
  );
}

export default Recorder;
