import { Box, Card, CardContent, Tab, Tabs, Typography } from "@mui/material";
import React from "react";
import VarCalculator from "../var-calculator";

interface TabPanelProps {
  children?: React.ReactNode;
  index: number;
  value: number;
}

function TabPanel(props: TabPanelProps) {
  const { children, value, index, ...other } = props;

  return (
    <div
      role="tabpanel"
      hidden={value !== index}
      id={`simple-tabpanel-${index}`}
      aria-labelledby={`simple-tab-${index}`}
      {...other}
    >
      {value === index && (
        <Box sx={{ p: 3 }}>
          <Typography component="div">{children}</Typography>
        </Box>
      )}
    </div>
  );
}

function a11yProps(index: number) {
  return {
    id: `simple-tab-${index}`,
    "aria-controls": `simple-tabpanel-${index}`,
  };
}

export default function MainMenu() {
  const [value, setValue] = React.useState(0);

  const handleChange = (event: React.SyntheticEvent, newValue: number) => {
    setValue(newValue);
  };

  return (
    <Card sx={{ minWidth: 275 }}>
      <CardContent>
        <Box sx={{ width: "100%" }}>
          <Box sx={{ borderBottom: 1, borderColor: "divider" }}>
            <Tabs
              value={value}
              onChange={handleChange}
              aria-label="basic tabs example"
            >
              <Tab label="Value at Risk calculator" {...a11yProps(0)} />
              <Tab label="Monte Carlo simulation" {...a11yProps(1)} />
              <Tab label="Linear model" {...a11yProps(2)} />
            </Tabs>
          </Box>
          <TabPanel value={value} index={0}>
            <VarCalculator />
          </TabPanel>
          <TabPanel value={value} index={1}>
            Monte Carlo simulation Component
          </TabPanel>
          <TabPanel value={value} index={2}>
            Linear model Component
          </TabPanel>
        </Box>
      </CardContent>
    </Card>
  );
}
