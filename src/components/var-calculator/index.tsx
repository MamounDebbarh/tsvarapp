import { Button, Grid, Slider, TextField } from "@mui/material";

import { useState } from "react";
import VarModal from "./var-modal";

interface VarData {
  historicalVaR: number;
  historicalCVaR: number;
  normalDistributionVaR: number;
  normalDistributionCVaR: number;
  tDistributionVaR: number;
  tDistributionCVaR: number;
  monteCarloVaR: number;
  monteCarloCVaR: number;
  brownianMotionMonteCarloVaR: number;
}

function VarCalculator() {
  const [confidenceLevel, setConfidenceLevel] = useState<number>(90);
  const [timeInDays, setTimeInDays] = useState(1);
  const [varData, setVarData] = useState<VarData>({} as VarData);
  const [openVarDialog, setOpenVarDialog] = useState(false);

  const handleSliderChange = (event: Event, newValue: number | number[]) => {
    setConfidenceLevel(newValue as number);
  };

  const handleInputChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    setConfidenceLevel(Number(event.target.value));
  };

  const handleBlur = () => {
    if (confidenceLevel < 0) {
      setConfidenceLevel(0);
    } else if (confidenceLevel > 100) {
      setConfidenceLevel(100);
    }
  };

  const handleVarDialogOpen = () => {
    setOpenVarDialog(true);
  };

  const handleVarDialogClose = () => {
    setOpenVarDialog(false);
  };

  const handleVarCalculation = () => {
    // post request to backend /var endpoint with confidenceLevel
    // then fetch var from backend and setVar
    const requestOptions = {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        confidenceLevel: confidenceLevel / 100,
        timeInDays: timeInDays,
      }),
    };
    fetch(`/var`, requestOptions).then((response) => {
      response.json().then((data) => {
        setVarData(data);
        handleVarDialogOpen();
      });
    });
  };

  // useEffect(() => {
  //   setVarData(varData);
  //   console.log(varData);
  // }, [varData]);

  return (
    <Grid container spacing={2}>
      <Grid item xs={12}>
        <TextField
          id="outlined-basic"
          label="Time in Days"
          variant="outlined"
          onChange={(e) => setTimeInDays(Number(e.target.value))}
        />
      </Grid>
      <Grid item xs={8}>
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
      <Grid item xs={4}>
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
      <VarModal
        openVarDialog={openVarDialog}
        handleVarDialogClose={handleVarDialogClose}
        varData={varData}
      />
    </Grid>
  );
}

export default VarCalculator;
