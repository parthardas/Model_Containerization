import { Divider, Grid, styled } from "@mui/material";
import AddNewUser from "./containers/AddNewUser";
import UserDetails from "./containers/UserDetails";
import GetCreditScoreOfUnknown from "./containers/GetCreditScoreOfUnknown";
import { MaterialDesignContent, SnackbarProvider } from "notistack";

const StyledMaterialDesignContent = styled(MaterialDesignContent)(() => ({
  "&.notistack-MuiContent-success": {
    backgroundColor: "#26B56A",
  },
  "&.notistack-MuiContent-error": {
    backgroundColor: "#970C0C",
  },
}));

function App() {
  return (
    <SnackbarProvider
      maxSnack={3}
      Components={{
        success: StyledMaterialDesignContent,
        error: StyledMaterialDesignContent,
      }}
    >
      <Grid style={{ padding: "3% 5%" }}>
        <Divider />
        <Grid
          style={{ margin: "40px 0" }}
          display={"flex"}
          justifyContent={"space-between"}
        >
          <AddNewUser />
          <UserDetails />
          <GetCreditScoreOfUnknown />
        </Grid>
      </Grid>
    </SnackbarProvider>
  );
}

export default App;
