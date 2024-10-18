import React, { useState } from "react";
import { Box, Button, Typography, Input } from '@mui/material';

const FileUpload = ({ fileType, onFileUpload }) => {
  const [file, setFile] = useState(null);

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    if (file) {
      onFileUpload(file);
    } else {
      alert("Please select a file first.");
    }
  };

  return (
    <Box 
      sx={{ 
        maxWidth: 600, 
        margin: 'auto', 
        padding: 4, 
        backgroundColor: 'background.paper', 
        borderRadius: 2, 
        boxShadow: 3, 
        textAlign: 'center',
      }}
    >
      <Typography variant="h5" gutterBottom>
        Upload {fileType}
      </Typography>
      <Input 
        type="file" 
        onChange={handleFileChange} 
        sx={{ marginTop: 2 }} 
      />
      <Button 
        variant="contained" 
        sx={{ marginTop: 2 }} 
        onClick={handleSubmit}
      >
        Upload
      </Button>
    </Box>
  );
};

export default FileUpload;
