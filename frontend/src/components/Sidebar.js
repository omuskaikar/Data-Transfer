import React, { useState } from "react";
import {
  Drawer,
  List,
  ListItem,
  ListItemIcon,
  ListItemText,
  IconButton,
} from "@mui/material";
import { FaFileCsv, FaFileExcel, FaDatabase, FaBars } from "react-icons/fa";
import { Link, useLocation } from "react-router-dom";

const SidebarComponent = () => {
  const [open, setOpen] = useState(false);
  const location = useLocation(); // Get the current route to track the selected item

  const toggleDrawer = () => {
    setOpen(!open);
  };

  return (
    <>
      <IconButton
        onClick={toggleDrawer}
        sx={{ color: "#d359ff", position: "absolute", top: 10, left: 10 }} // Set button to purple
      >
        <FaBars />
      </IconButton>
      <Drawer
        open={open}
        onClose={toggleDrawer}
        sx={{
          "& .MuiDrawer-paper": {
            width: 240,
            backgroundColor: "#000000", // Background color black
            color: "#000000", // Text color black for general contrast
          },
        }}
      >
        <List>
          <ListItem
            button
            component={Link}
            to="/upload-csv"
            sx={{
              backgroundColor:
                location.pathname === "/upload-csv" ? "#3e3e3e" : "inherit", // Highlight selected with gray
              "&:hover": {
                backgroundColor: "#3e3e3e", // Gray on hover
              },
            }}
          >
            <ListItemIcon>
              <FaFileCsv color="#d359ff" /> {/* Set icon color to purple */}
            </ListItemIcon>
            <ListItemText primary="Upload CSV" sx={{ color: "#d359ff" }} />
          </ListItem>

          <ListItem
            button
            component={Link}
            to="/upload-excel"
            sx={{
              backgroundColor:
                location.pathname === "/upload-excel" ? "#3e3e3e" : "inherit", // Highlight selected with gray
              "&:hover": {
                backgroundColor: "#3e3e3e", // Gray on hover
              },
            }}
          >
            <ListItemIcon>
              <FaFileExcel color="#d359ff" /> {/* Set icon color to purple */}
            </ListItemIcon>
            <ListItemText primary="Upload Excel" sx={{ color: "#d359ff" }} />
          </ListItem>

          <ListItem
            button
            component={Link}
            to="/upload-mssql"
            sx={{
              backgroundColor:
                location.pathname === "/upload-mssql" ? "#3e3e3e" : "inherit", // Highlight selected with gray
              "&:hover": {
                backgroundColor: "#3e3e3e", // Gray on hover
              },
            }}
          >
            <ListItemIcon>
              <FaDatabase color="#d359ff" /> {/* Set icon color to purple */}
            </ListItemIcon>
            <ListItemText primary="Upload MSSQL" sx={{ color: "#d359ff" }} />
          </ListItem>
        </List>
      </Drawer>
    </>
  );
};

export default SidebarComponent;
