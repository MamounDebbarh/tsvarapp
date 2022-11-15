// @ts-check
import { Grid, Typography } from "@mui/material";
import MainMenu from "./components/main-menu";
import Portfolio from "./components/portfolio";

function MainPage() {
  return (
    <Grid container spacing={2}>
      <Grid item xs={12}>
        <Typography
          variant="h4"
          component="header"
          style={{ padding: 5, paddingBottom: 15 }}
          align="center"
        >
          Value at Risk (VaR) Calculator
        </Typography>
      </Grid>
      <Grid item xs={4}>
        <Portfolio />
      </Grid>
      <Grid item xs={8}>
        <MainMenu />
      </Grid>
    </Grid>
  );
}

export default MainPage;
