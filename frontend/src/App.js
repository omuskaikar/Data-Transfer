// src/App.js
import React from 'react';
import { ThemeProvider } from '@mui/material/styles';
import SidebarComponent from "./components/Sidebar";
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import UploadCsv from './pages/UploadCsv';
import LandingPage from './pages/LandingPage';
import UploadMSSQL from './pages/UploadMSSQL';
import UploadExcel from "./pages/UploadExcel";
import theme from './theme';


function App() {
  return (
    <ThemeProvider theme={theme}>
      <Router>
        <SidebarComponent /> 
        <Routes>
          <Route path="/" element={<LandingPage />} />
          <Route path="/upload-csv" element={<UploadCsv />} />
          <Route path="/upload-excel" element={<UploadExcel />} />
          <Route path="/upload-mssql" element={<UploadMSSQL />} />
        </Routes>
      </Router>
    </ThemeProvider>
  );
}

export default App;
