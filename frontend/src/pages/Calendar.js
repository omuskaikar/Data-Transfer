// src/pages/Calendar.js
import React, { useState } from "react";
import FormInput from "../components/FormInput";
import FileUpload from "../components/FileUpload";

const Calendar = () => {
  const [dbDetails, setDbDetails] = useState({
    ip: "",
    dbname: "",
    user: "",
    password: "",
  });

  return (
    <div style={{ display: "flex" }}>
      <FormInput dbDetails={dbDetails} setDbDetails={setDbDetails} />
      <FileUpload dbDetails={dbDetails} fileType="CSV" />
    </div>
  );
};

export default Calendar;
