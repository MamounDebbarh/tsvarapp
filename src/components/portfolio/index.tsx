import ExpandMoreIcon from "@mui/icons-material/ExpandMore";
import {
  Accordion,
  AccordionDetails,
  AccordionSummary,
  Button,
  Card,
  CardContent,
  Dialog,
  DialogActions,
  DialogContent,
  DialogContentText,
  DialogTitle,
  Grid,
  List,
  ListItem,
  TextField,
  Typography,
} from "@mui/material";

import { useEffect, useState } from "react";

interface PortfolioInformation {
  choleskyDecomposition: string;
  correlationMatrix: string;
  eigenDecomposition: string;
  returnsWithWeights: string;
}

interface Stock {
  name: string;
  price: number;
  shares: number;
  weight: number;
}

interface Option {
  K: number;
  S: number;
  T: number;
  delta: number;
  gamma: number;
  name: string;
  price: number;
  rho: number;
  shares: number;
  sigma: number;
  theta: number;
  type: string;
  vega: number;
}

function Portfolio() {
  const [openStockDialog, setOpenStockDialog] = useState(false);
  const [openOptionDialog, setOpenOptionDialog] = useState(false);
  const [stockList, setStockList] = useState([{} as Stock]);
  const [optionList, setOptionList] = useState([{} as Option]);
  const [newStockName, setNewStockName] = useState("");
  const [newStockNumber, setNewStockNumber] = useState(0);
  const [newOptionName, setNewOptionName] = useState("");
  const [newOptionNumber, setNewOptionNumber] = useState(0);

  const handleAddStockDialog = () => {
    setOpenStockDialog(true);
  };

  const handleAddOptionDialog = () => {
    setOpenOptionDialog(true);
  };

  const handleCloseStockDialog = () => {
    setOpenStockDialog(false);
  };

  const handleCloseOptionDialog = () => {
    setOpenOptionDialog(false);
  };

  const handleStockSubmit = () => {
    // post to backend /stocks endpoint with newStockName and newStockNumber
    // then fetch stocks from backend and setStockList
    const requestOptions = {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ name: newStockName, shares: newStockNumber }),
    };
    fetch("/stocks", requestOptions).then((response) => response.json());
    setOpenStockDialog(false);
    fetchStockList();
    console.log("Stock Submitted");
  };

  const handleOptionSubmit = () => {
    // post to backend /options endpoint with newOptionName and newOptionNumber
    // then fetch options from backend and setOptionList
    const requestOptions = {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ name: newOptionName, shares: newOptionNumber }),
    };
    fetch("/options", requestOptions).then((response) => response.json());
    setOpenOptionDialog(false);
    fetchOptionList();
    console.log("Option Submitted");
  };

  const handleStockDelete = (name: string) => {
    // delete from backend /stocks endpoint with name
    // then fetch stocks from backend and setStockList
    const requestOptions = {
      method: "DELETE",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ name: name }),
    };
    fetch(`/stocks/${name}`, requestOptions).then((response) =>
      response.json()
    );
    fetchStockList();
    console.log("Stock Deleted");
  };

  const handleOptionDelete = (name: string) => {
    // delete from backend /options endpoint with name
    // then fetch options from backend and setOptionList
    const requestOptions = {
      method: "DELETE",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ name: name }),
    };
    fetch(`/options/${name}`, requestOptions).then((response) =>
      response.json()
    );
    fetchOptionList();
    console.log("Option Deleted");
  };

  const fetchStockList = async () => {
    fetch("/stocks").then((response) =>
      response.json().then((data) => {
        setStockList(data.stocks);
      })
    );
  };

  const fetchOptionList = async () => {
    fetch("/options").then((response) =>
      response.json().then((data) => {
        setOptionList(data.options);
      })
    );
  };

  // calculate portfolio value using stock price and stock shares and option price and option shares
  const calculatePortfolioValue = () => {
    let portfolioValue = 0;
    stockList.forEach((stock) => {
      portfolioValue += stock.price * stock.shares;
    });
    optionList.forEach((option) => {
      portfolioValue += option.price * option.shares;
    });
    return portfolioValue;
  };

  useEffect(() => {
    fetchStockList();
    fetchOptionList();
  }, []);

  return (
    <Card sx={{ minWidth: 275 }}>
      <CardContent>
        <Typography variant="h5" component="div">
          Portfolio
        </Typography>
        <Typography sx={{ mb: 1.5 }} color="text.secondary">
          Portfolio Value: ${Math.round(calculatePortfolioValue() * 100) / 100}
        </Typography>
        <Grid container spacing={2}>
          <Grid item xs={12} sm={6}>
            <Typography variant="h6" component="div">
              Stocks
            </Typography>
          </Grid>
          <Grid item xs={12} sm={6}>
            <Button variant="contained" onClick={handleAddStockDialog}>
              +
            </Button>
          </Grid>
        </Grid>

        <Dialog open={openStockDialog} onClose={handleCloseStockDialog}>
          <DialogTitle> Add a stock</DialogTitle>
          <DialogContent>
            <DialogContentText>
              Enter the stock symbol and the number of shares you own.
            </DialogContentText>
            <TextField
              autoFocus
              margin="dense"
              id="name"
              label="Stock Symbol"
              type="text"
              fullWidth
              onChange={(e) => setNewStockName(e.target.value)}
            />
            <TextField
              autoFocus
              margin="dense"
              id="name"
              label="Number of Shares"
              type="number"
              fullWidth
              onChange={(e) => setNewStockNumber(Number(e.target.value))}
            />
          </DialogContent>
          <DialogActions>
            <Button onClick={handleCloseStockDialog}>Cancel</Button>
            <Button onClick={handleStockSubmit}>Add</Button>
          </DialogActions>
        </Dialog>
        {stockList.length < 1 ? (
          <Typography> No stocks added yet</Typography>
        ) : (
          <List>
            {stockList.map((stock, i) => (
              <ListItem key={i}>
                <Accordion style={{ width: "100%" }}>
                  <AccordionSummary expandIcon={<ExpandMoreIcon />}>
                    <Grid container spacing={2}>
                      <Grid item xs={6} sm={6}>
                        <Typography>
                          {stock.name} $
                          {Math.round(stock.shares * stock.price * 100) / 100}
                        </Typography>
                      </Grid>
                      <Grid item xs={2} sm={2}>
                        <Button
                          variant="contained"
                          style={{ right: 5 }}
                          onClick={() => handleStockDelete(stock.name)}
                        >
                          -
                        </Button>
                      </Grid>
                    </Grid>
                  </AccordionSummary>
                  <AccordionDetails>
                    <Typography>Stock name: {stock.name}</Typography>
                    <Typography>Number of shares: {stock.shares}</Typography>
                    <Typography>
                      Price: ${Math.round(stock.price * 100) / 100}
                    </Typography>
                    <Typography>Weight: {stock.weight}</Typography>
                  </AccordionDetails>
                </Accordion>
              </ListItem>
            ))}
          </List>
        )}

        <Grid container spacing={2}>
          <Grid item xs={12} sm={6}>
            <Typography variant="h6" component="div">
              Options
            </Typography>
          </Grid>
          <Grid item xs={12} sm={6}>
            <Button variant="contained" onClick={handleAddOptionDialog}>
              +
            </Button>
          </Grid>
        </Grid>

        <Dialog open={openOptionDialog} onClose={handleCloseOptionDialog}>
          <DialogTitle> Add an option</DialogTitle>
          <DialogContent>
            <DialogContentText>
              Enter the option symbol and the number of contracts you own.
            </DialogContentText>
            <TextField
              autoFocus
              margin="dense"
              id="name"
              label="Option Symbol"
              type="text"
              fullWidth
              onChange={(e) => setNewOptionName(e.target.value)}
            />
            <TextField
              autoFocus
              margin="dense"
              id="name"
              label="Number of Contracts"
              type="number"
              fullWidth
              onChange={(e) => setNewOptionNumber(Number(e.target.value))}
            />
          </DialogContent>
          <DialogActions>
            <Button onClick={handleCloseOptionDialog}>Cancel</Button>
            <Button onClick={handleOptionSubmit}>Add</Button>
          </DialogActions>
        </Dialog>

        {optionList.length < 1 ? (
          <Typography> No options added yet</Typography>
        ) : (
          <List>
            {optionList.map((option, i) => (
              <ListItem key={i}>
                <Accordion style={{ width: "100%" }}>
                  <AccordionSummary expandIcon={<ExpandMoreIcon />}>
                    <Grid container spacing={2}>
                      <Grid item xs={6} sm={6}>
                        <Typography>
                          {option.name} $
                          {Math.round(option.shares * option.price * 100) / 100}
                        </Typography>
                      </Grid>
                      <Grid item xs={2} sm={2}>
                        <Button
                          variant="contained"
                          style={{ right: 5 }}
                          onClick={() => handleOptionDelete(option.name)}
                        >
                          -
                        </Button>
                      </Grid>
                    </Grid>
                  </AccordionSummary>
                  <AccordionDetails>
                    <Typography>Option name: {option.name}</Typography>
                    <Typography>
                      Number of contracts: {option.shares}
                    </Typography>
                    <Typography> Option type: {option.type}</Typography>
                    <Typography> Option price: {option.price} </Typography>
                    <Typography> Strike price: {option.S} </Typography>
                    <Typography>
                      {" "}
                      Expiration date in days: {option.T}
                    </Typography>
                    <Typography> Volatility: {option.sigma} </Typography>
                    <Typography> Delta: {option.delta} </Typography>
                    <Typography> Gamma: {option.gamma} </Typography>
                    <Typography> Theta: {option.theta} </Typography>
                    <Typography> Vega: {option.vega} </Typography>
                    <Typography> Rho: {option.rho} </Typography>
                  </AccordionDetails>
                </Accordion>
              </ListItem>
            ))}
          </List>
        )}
      </CardContent>
    </Card>
  );
}

export default Portfolio;
