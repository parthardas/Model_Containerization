import { Box, Button, Grid, TextField, Typography } from "@mui/material";
import React, { useState } from "react";
import { useSnackbar } from "notistack";
import { getCreditScore } from "../../utils/api";

const GetCreditScoreOfUnknown = () => {
  const [formData, setFormData] = useState({
    credit_history_age: "",
    monthly_balance: "",
    annual_income: "",
    changed_credit_limit: "",
    outstanding_debt: "",
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
      case "credit_history_age":
        if (value < 0) {
          errors.credit_history_age =
            "Credit history age must be a positive integer";
        } else {
          delete errors.credit_history_age;
        }
        break;
      case "monthly_balance":
      case "annual_income":
      case "changed_credit_limit":
      case "outstanding_debt":
        if (value < 0 || isNaN(value)) {
          errors[name] = "Value must be a non-negative number";
        } else {
          delete errors[name];
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
        const resp = await getCreditScore()(formData);
        console.log(resp);
        setCreditScore(resp.data);
        enqueueSnackbar(`Credit Score retrieved`, {
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
        }}
        gap={"10px"}
        onSubmit={handleSubmit}
        textAlign={"center"}
      >
        <Typography variant="h5">Get Credit Score Details</Typography>
        <TextField
          required
          label="Credit History Age"
          type="number"
          size="small"
          name="credit_history_age"
          value={formData.credit_history_age}
          onChange={handleChange}
          error={!!formErrors.credit_history_age}
          helperText={formErrors.credit_history_age}
        />
        <TextField
          required
          label="Monthly Balance"
          type="number"
          size="small"
          name="monthly_balance"
          value={formData.monthly_balance}
          onChange={handleChange}
          error={!!formErrors.monthly_balance}
          helperText={formErrors.monthly_balance}
        />
        <TextField
          required
          label="Annual Income"
          type="number"
          size="small"
          name="annual_income"
          value={formData.annual_income}
          onChange={handleChange}
          error={!!formErrors.annual_income}
          helperText={formErrors.annual_income}
        />
        <TextField
          required
          label="Changed Credit Limit"
          type="number"
          size="small"
          name="changed_credit_limit"
          value={formData.changed_credit_limit}
          onChange={handleChange}
          error={!!formErrors.changed_credit_limit}
          helperText={formErrors.changed_credit_limit}
        />
        <TextField
          required
          label="Outstanding Debt"
          type="number"
          size="small"
          name="outstanding_debt"
          value={formData.outstanding_debt}
          onChange={handleChange}
          error={!!formErrors.outstanding_debt}
          helperText={formErrors.outstanding_debt}
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
        <Typography variant="p">
          Credit Score is {creditScore.credit_score}
        </Typography>
      )}
    </Grid>
  );
};

export default GetCreditScoreOfUnknown;
