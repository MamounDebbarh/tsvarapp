import { Button, Grid, Slider, TextField } from "@mui/material";
import { useState } from "react";

function VarCalculator() {
  const [confidenceLevel, setConfidenceLevel] = useState<
    number | string | Array<number | string>
  >(90);
  const [varValue, setVarValue] = useState(0);
  const [portfolioValue, setPortfolioValue] = useState(0);
  const [portfolioRisk, setPortfolioRisk] = useState(0);
  const [portfolioReturns, setPortfolioReturns] = useState(0);

  const handleSliderChange = (event: Event, newValue: number | number[]) => {
    setConfidenceLevel(newValue);
  };

  const handleInputChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    setConfidenceLevel(
      event.target.value === "" ? "" : Number(event.target.value)
    );
  };

  const handleBlur = () => {
    if (confidenceLevel < 0) {
      setConfidenceLevel(0);
    } else if (confidenceLevel > 100) {
      setConfidenceLevel(100);
    }
  };

  const handleVarCalculation = () => {
    // post request to backend /var endpoint with confidenceLevel
    // then fetch var from backend and setVar
    const requestOptions = {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ confidenceLevel: confidenceLevel }),
    };
    fetch(`/var`, requestOptions).then((response) => {
      response.json();
      console.log(response.json());
    });
    console.log("Var Calculated");
  };

  const handlePortfolioReturns = () => {
    // get request to backend /portfolioReturns endpoint
    // then fetch portfolioReturns from backend and setPortfolioReturns
    fetch(`/portfolioReturns`).then((response) => {
      response.json();
      console.log(response.json());
    });
    console.log("Portfolio Returns Calculated");
  };

  return (
    <Grid container spacing={2}>
      <Grid item xs={6}>
        <TextField
          id="outlined-basic"
          label="Position Amount"
          variant="outlined"
        />
      </Grid>
      <Grid item xs={6}>
        <TextField
          id="outlined-basic"
          label="Asset Volatility (%)"
          variant="outlined"
        />
      </Grid>
      <Grid item xs={6}>
        <TextField
          id="outlined-basic"
          label="Time in Days"
          variant="outlined"
        />
      </Grid>
      <Grid item xs={6}>
        <TextField
          id="outlined-basic"
          label="Confidence Interval (%)"
          variant="outlined"
        />
      </Grid>
      <Grid item xs={6}>
        <Slider
          value={typeof confidenceLevel === "number" ? confidenceLevel : 90}
          onChange={handleSliderChange}
          aria-labelledby="input-slider"
          valueLabelDisplay="auto"
          min={90}
          max={100}
          step={0.1}
        />
      </Grid>
      <Grid item xs={3}>
        <TextField
          value={confidenceLevel}
          size="small"
          onChange={handleInputChange}
          onBlur={handleBlur}
          inputProps={{
            step: 0.1,
            min: 90,
            max: 99.9,
            type: "number",
            "aria-labelledby": "input-slider",
          }}
        />
      </Grid>
      <Grid item xs={3}>
        <Button variant="contained" onClick={handleVarCalculation}>
          Calculate
        </Button>
      </Grid>
      <Grid item xs={3}>
        <Button variant="contained" onClick={handlePortfolioReturns}>
          handlePortfolioReturns
        </Button>
      </Grid>
    </Grid>
  );
}

export default VarCalculator;
