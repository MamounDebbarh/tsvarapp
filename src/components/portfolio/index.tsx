import {
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

interface Stock {
  name: string;
  shares: number;
}

function Portfolio() {
  const [openStockDialog, setOpenStockDialog] = useState(false);
  const [openOptionDialog, setOpenOptionDialog] = useState(false);
  const [stockList, setStocklist] = useState([{} as Stock]);

  const handleAddStockDialog = () => {
    setOpenStockDialog(true);
  };

  const handleAddOptionDialog = () => {
    setOpenOptionDialog(true);
  };

  const handleCloseStockDialog = () => {
    setOpenStockDialog(false);
  };

  const handleStockSubmit = () => {
    console.log("Stock Submitted");
    setOpenStockDialog(false);
  };

  const handleCloseOptionDialog = () => {
    setOpenOptionDialog(false);
  };

  const fetchStockList = async () => {
    fetch("/stocks").then((response) =>
      response.json().then((data) => {
        setStocklist(data.stocks);
      })
    );
  };

  useEffect(() => {
    fetchStockList();
  }, []);

  return (
    <Card sx={{ minWidth: 275 }}>
      <CardContent>
        <Typography variant="h5" component="div">
          Portfolio
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
            />
            <TextField
              autoFocus
              margin="dense"
              id="name"
              label="Number of Shares"
              type="number"
              fullWidth
            />
          </DialogContent>
          <DialogActions>
            <Button onClick={handleCloseStockDialog}>Cancel</Button>
            <Button onClick={handleCloseStockDialog}>Add</Button>
          </DialogActions>
        </Dialog>

        {stockList.length < 1 ? (
          <Typography> No stocks added yet</Typography>
        ) : (
          <List>
            {stockList.map((stock, i) => (
              <ListItem key={i}>
                <Typography>
                  {stock.name} - {stock.shares}
                </Typography>
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
            />
            <TextField
              autoFocus
              margin="dense"
              id="name"
              label="Number of Contracts"
              type="number"
              fullWidth
            />
          </DialogContent>
          <DialogActions>
            <Button onClick={handleCloseOptionDialog}>Cancel</Button>
            <Button onClick={handleCloseOptionDialog}>Add</Button>
          </DialogActions>
        </Dialog>

        <List>
          <ListItem>Option 1</ListItem>
          <ListItem>Option 2</ListItem>
        </List>
      </CardContent>
    </Card>
  );
}

export default Portfolio;
