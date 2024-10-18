import React from "react";
import { Box, TextField, Button, Typography } from '@mui/material';

const FormInput = ({ dbDetails, setDbDetails, onConnect }) => {
  const handleInputChange = (e) => {
    setDbDetails({ ...dbDetails, [e.target.name]: e.target.value });
  };

  return (
    <Box
      sx={{
        maxWidth: 400,
        margin: "auto",
        padding: 3,
        backgroundColor: "background.paper",
        borderRadius: 2,
        boxShadow: 3,
        textAlign: "center",
      }}
    >
      <Typography
        variant="h5"
        sx={{
          fontWeight: "bold",
          color: "white",
          textAlign: "center",
        }} // Bold white text
      >
        Database Connection
      </Typography>
      <TextField
        fullWidth
        margin="normal"
        label="Host"
        variant="outlined"
        name="host"
        value={dbDetails.host}
        onChange={handleInputChange}
        InputLabelProps={{ style: { color: "white" } }}
        sx={{
          "& .MuiOutlinedInput-root": {
            "& fieldset": { borderColor: "#ddd" },
            "&:hover fieldset": { borderColor: "primary.main" },
            "&.Mui-focused fieldset": { borderColor: "primary.main" },
          },
          "& input": { color: "white" },
        }}
      />
      <TextField
        fullWidth
        margin="normal"
        label="Username"
        variant="outlined"
        name="user"
        value={dbDetails.user}
        onChange={handleInputChange}
        InputLabelProps={{ style: { color: "white" } }}
        sx={{
          "& .MuiOutlinedInput-root": {
            "& fieldset": { borderColor: "#ddd" },
            "&:hover fieldset": { borderColor: "primary.main" },
            "&.Mui-focused fieldset": { borderColor: "primary.main" },
          },
          "& input": { color: "white" },
        }}
      />
      <TextField
        fullWidth
        margin="normal"
        label="Password"
        variant="outlined"
        name="password"
        type="password"
        value={dbDetails.password}
        onChange={handleInputChange}
        InputLabelProps={{ style: { color: "white" } }}
        sx={{
          "& .MuiOutlinedInput-root": {
            "& fieldset": { borderColor: "#ddd" },
            "&:hover fieldset": { borderColor: "primary.main" },
            "&.Mui-focused fieldset": { borderColor: "primary.main" },
          },
          "& input": { color: "white" },
        }}
      />
      <Button
        fullWidth
        variant="contained"
        sx={{ marginTop: 2 }}
        onClick={onConnect}
      >
        Connect
      </Button>
    </Box>
  );
};

export default FormInput;
