import React, { useState } from 'react';
import axios from 'axios';

const App = () => {
  const [file, setFile] = useState(null);

  const downloadFile = async (filename) => {
    try {
      const response = await axios.get(`http://your-backend-url.com/uploads/${filename}`, {
        responseType: 'blob'
      });

      const blob = new Blob([response.data]);
      const url = window.URL.createObjectURL(blob);
      setFile(url);

      // Automatically trigger download
      const a = document.createElement('a');
      a.href = url;
      a.download = filename;
      document.body.appendChild(a);
      a.click();
      document.body.removeChild(a);
    } catch (error) {
      console.error('Error downloading file:', error);
    }
  };

  return (
    <div>
      <button onClick={() => downloadFile('file1.jpg')}>Download File 1</button>
      <button onClick={() => downloadFile('file2.pdf')}>Download File 2</button>
      {file && (
        <div>
          <h2>Downloaded File:</h2>
          <a href={file} download>Downloaded File</a>
        </div>
      )}
    </div>
  );
};

export default App;
