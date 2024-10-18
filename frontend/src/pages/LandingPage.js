import React from "react";
import {
  Box,
  Button,
  Typography,
  Grid,
  Card,
  CardMedia,
  CardContent,
} from "@mui/material";
import { useNavigate } from "react-router-dom";
import Slider from "react-slick";
import "slick-carousel/slick/slick.css";
import "slick-carousel/slick/slick-theme.css";

const LandingPage = () => {
  const navigate = useNavigate();

  // Carousel settings with smaller size and no arrows
  const settings = {
    infinite: true,
    speed: 500,
    slidesToShow: 1,
    slidesToScroll: 1,
    autoplay: true,
    autoplaySpeed: 3000,
    arrows: false, // Remove the arrows from the carousel
    dots: false, // Optionally remove the dots as well
  };

  return (
    <Box
      sx={{
        minHeight: "100vh",
        backgroundColor: "#1E1E2F",
        display: "flex",
        flexDirection: "column",
      }}
    >
      {/* Navbar with Sidebar, Title, and Buttons */}
      <Box
        sx={{
          display: "flex",
          alignItems: "center",
          justifyContent: "space-between",
          padding: 2,
          backgroundColor: "black",
        }}
      >
        {/* Sidebar and Title in a row */}
        <Box
          sx={{
            display: "flex",
            alignItems: "center",
            flex: 1,
          }}
        >
          {/* Title */}
          <Typography variant="h4" sx={{ color: "#D359FF", paddingLeft: 20 }}>
            Data Uploader
          </Typography>
        </Box>

        {/* Buttons on the right */}
        <Box
          sx={{
            display: "flex",
            alignItems: "center",
            gap: 2, // Add some space between the buttons
          }}
        >
          <Button
            variant="contained"
            onClick={() => navigate("/upload-csv")}
            sx={{ backgroundColor: "primary.main" }}
          >
            Upload CSV
          </Button>
          <Button
            variant="contained"
            onClick={() => navigate("/upload-excel")}
            sx={{ backgroundColor: "primary.main" }}
          >
            Upload Excel
          </Button>
          <Button
            variant="contained"
            onClick={() => navigate("/upload-mssql")}
            sx={{ backgroundColor: "primary.main" }}
          >
            Connect to MSSQL
          </Button>
        </Box>
      </Box>

      {/* Grid Layout with Smaller Carousel (60%) and Info Card (40%) */}
      <Grid container spacing={2} sx={{ marginTop: 2, flex: 1 }}>
        {/* Carousel on the left side (60%) */}
        <Grid item xs={12} md={7}>
          <Box sx={{ position: "relative", height: "100%" }}>
            <Slider {...settings}>
              {/* First Slide */}
              <Card sx={{ backgroundColor: "transparent", boxShadow: "none" }}>
                <CardMedia
                  component="img"
                  alt="CSV to PostgreSQL"
                  image={`${process.env.PUBLIC_URL}/csv_pg.png`} // Path to the first image
                  title="CSV to PostgreSQL"
                  sx={{
                    height: "300px", // Reduced height for a smaller carousel
                    width: "100%",
                    objectFit: "contain",
                  }}
                />
              </Card>

              {/* Second Slide */}
              <Card sx={{ backgroundColor: "transparent", boxShadow: "none" }}>
                <CardMedia
                  component="img"
                  alt="MSSQL to PostgreSQL"
                  image={`${process.env.PUBLIC_URL}/mssql_pgadmin.png`} // Path to the second image
                  title="MSSQL to PostgreSQL"
                  sx={{
                    height: "300px", // Reduced height for a smaller carousel
                    width: "100%",
                    objectFit: "contain",
                  }}
                />
              </Card>
            </Slider>
          </Box>
        </Grid>

        {/* Info Card on the right side (40%) */}
        <Grid item xs={12} md={5}>
          <Card
            sx={{
              backgroundColor: "#D359FF",
              color: "#1e1e2f",
              padding: 3,
              boxShadow: 3,
              height: "300px", // Adjusted height to match the smaller carousel
            }}
          >
            <CardContent>
              <Typography variant="h5" sx={{ marginBottom: 2 }}>
                Important Information
              </Typography>
              <Typography variant="body1">
                This section can display additional information such as guides
                on how to upload files, connection statuses, and more details
                about the app functionalities.
              </Typography>
            </CardContent>
          </Card>
        </Grid>
      </Grid>
    </Box>
  );
};

export default LandingPage;
