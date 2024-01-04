import { Box, Button, Grid, TextField, Typography } from "@mui/material";
import React, { useState } from "react";
import defaultUser from "../../icons/defaultUser.png";
import { useSnackbar } from "notistack";
import { getCreditScoreById } from "../../utils/api";

const UserDetails = () => {
  const [formData, setFormData] = useState({
    customer_id: "",
  });
  const [creditScore, setCreditScore] = useState();
  const [formErrors, setFormErrors] = useState({});
  const { enqueueSnackbar } = useSnackbar();
  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData((prevState) => ({
      ...prevState,
      [name]: value,
    }));
    validateInput(name, value);
  };
  const validateInput = (name, value) => {
    let errors = { ...formErrors };

    switch (name) {
      case "customer_id":
        if (!value) {
          errors.customer_id = "Customer ID is required";
        } else {
          delete errors.customer_id;
        }
        break;
      default:
        break;
    }

    setFormErrors(errors);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!Object.keys(formErrors).length) {
      console.log("Form data submitted:", formData);
      try {
        const resp = await getCreditScoreById()(formData);
        setCreditScore(resp.data);
        console.log(resp);
        enqueueSnackbar(`Credit Score retrieved for ${formData.customer_id}`, {
          variant: "success",
        });
      } catch (error) {
        enqueueSnackbar(
          error?.response?.data?.detail ||
            `Something went wrong, try again after some time`,
          {
            variant: "error",
          }
        );
      }
    } else {
      console.log("Form validation errors:", formErrors);
    }
  };

  return (
    <Grid>
      <Box
        component="form"
        autoComplete="off"
        style={{
          display: "flex",
          flexDirection: "column",
          width: "fit-content",
          placeItems: "center",
        }}
        gap={"15px"}
        onSubmit={handleSubmit}
        textAlign={"center"}
      >
        <img src={defaultUser} style={{ height: 100, width: 100 }} alt="userImage"/>
        <Typography variant="h5">Get User Credit Score</Typography>

        <TextField
          required
          label="Customer Id"
          size="small"
          name="customer_id"
          value={formData.customer_id}
          onChange={handleChange}
          error={!!formErrors.customer_id}
          helperText={formErrors.customer_id}
        />
        <Button
          type="submit"
          variant="contained"
          color="primary"
          disableElevation
          style={{ margin: "0px 0 20px" }}
        >
          Get Credit Details
        </Button>
      </Box>

      {!!creditScore && (
        <Typography variant="body1">Credit Score is {creditScore.credit_score}</Typography>
      )}
    </Grid>
  );
};

export default UserDetails;
