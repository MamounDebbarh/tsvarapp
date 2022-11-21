import { Button, Grid, Slider, TextField } from "@mui/material";
import { useState } from "react";

function VarCalculator() {
  const [value, setValue] = useState<number | string | Array<number | string>>(
    90
  );

  const handleSliderChange = (event: Event, newValue: number | number[]) => {
    setValue(newValue);
  };

  const handleInputChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    setValue(event.target.value === "" ? "" : Number(event.target.value));
  };

  const handleBlur = () => {
    if (value < 0) {
      setValue(0);
    } else if (value > 100) {
      setValue(100);
    }
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
          value={typeof value === "number" ? value : 90}
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
          value={value}
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
        <Button variant="contained">Calculate</Button>
      </Grid>
    </Grid>
  );
}

export default VarCalculator;
