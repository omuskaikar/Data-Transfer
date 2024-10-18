import React, { useState } from "react";
import axios from "axios";
import { Box, Grid, MenuItem, Select, Typography } from "@mui/material";
import FormInput from "../components/FormInput";
import FileUpload from "../components/FileUpload";
import { toast, ToastContainer } from "react-toastify";
import "react-toastify/dist/ReactToastify.css";

const UploadCsv = () => {
  const [dbDetails, setDbDetails] = useState({
    host: "",
    user: "",
    password: "",
  });

  const [connected, setConnected] = useState(false);
  const [databases, setDatabases] = useState([]);
  const [selectedDatabase, setSelectedDatabase] = useState("");
  const [tables, setTables] = useState([]);
  const [selectedTable, setSelectedTable] = useState("");

  const handleConnect = async () => {
    try {
      const response = await axios.post(
        "http://localhost:8000/dbmanager/connect-postgres/",
        dbDetails
      );
      if (response.data.status === "success") {
        setDatabases(response.data.databases);
        setConnected(true);
        toast.success("Connected to the database");
      } else {
        toast.error("Failed to connect to the database");
      }
    } catch (error) {
      console.error("Error connecting to database:", error);
      toast.error("Error connecting to the database.");
    }
  };

  const handleDatabaseSelect = async (e) => {
    setSelectedDatabase(e.target.value);
    try {
      const response = await axios.post(
        "http://localhost:8000/dbmanager/fetch-tables-postgres/",
        { dbName: e.target.value, ...dbDetails }
      );
      setTables(response.data.tables);
    } catch (error) {
      console.error("Error fetching tables:", error);
      toast.error("Error fetching tables.");
    }
  };

  const handleFileUpload = async (file) => {
    const formData = new FormData();
    formData.append("file", file);
    formData.append("table_name", selectedTable);
    formData.append("host", dbDetails.host);
    formData.append("dbname", selectedDatabase);
    formData.append("user", dbDetails.user);
    formData.append("password", dbDetails.password);

    try {
      const response = await axios.post(
        "http://localhost:8000/dbmanager/upload-csv-postgres/",
        formData,
        {
          headers: { "Content-Type": "multipart/form-data" },
        }
      );
      if (response.data.status === "success") {
        toast.success("File uploaded and data inserted successfully");
      } else {
        toast.error("File upload failed");
      }
    } catch (error) {
      console.error("Error uploading file:", error);
      toast.error("Error uploading the file.");
    }
  };

  return (
    <Box
      sx={{
        padding: 4,
        minHeight: "100vh",
        backgroundColor: "#1e1e2f",
        display: "flex",
        justifyContent: "center",
        alignItems: "center",
      }}
    >
      <Box
        sx={{
          width: "100%",
          maxWidth: 600,
          padding: 3,
          backgroundColor: "#282c34",
          borderRadius: 2,
          boxShadow: 3,
        }}
      >
        <ToastContainer />
        {!connected ? (
          <FormInput
            dbDetails={dbDetails}
            setDbDetails={setDbDetails}
            onConnect={handleConnect}
          />
        ) : (
          <Grid container spacing={4}>
            <Grid item xs={12} md={6}>
              <Typography
                variant="h5"
                sx={{ fontWeight: "bold", color: "white", textAlign: "center" }}
              >
                Select a Database
              </Typography>
              <Select
                fullWidth
                value={selectedDatabase}
                onChange={handleDatabaseSelect}
                sx={{
                  marginTop: 2,
                  backgroundColor: "#3c4047",
                  color: "white",
                }}
              >
                {databases.map((db, index) => (
                  <MenuItem key={index} value={db}>
                    {db}
                  </MenuItem>
                ))}
              </Select>
            </Grid>

            {selectedDatabase && (
              <Grid item xs={12} md={6}>
                <Typography
                  variant="h5"
                  sx={{
                    fontWeight: "bold",
                    color: "white",
                    textAlign: "center",
                  }}
                >
                  Select a Table
                </Typography>
                <Select
                  fullWidth
                  value={selectedTable}
                  onChange={(e) => setSelectedTable(e.target.value)}
                  sx={{
                    marginTop: 2,
                    backgroundColor: "#3c4047",
                    color: "white",
                  }}
                >
                  {tables.map((table, index) => (
                    <MenuItem key={index} value={table}>
                      {table}
                    </MenuItem>
                  ))}
                </Select>
              </Grid>
            )}

            {selectedTable && (
              <Grid item xs={12}>
                <FileUpload
                  dbDetails={dbDetails}
                  fileType="CSV"
                  onFileUpload={handleFileUpload}
                />
              </Grid>
            )}
          </Grid>
        )}
      </Box>
    </Box>
  );
};

export default UploadCsv;
