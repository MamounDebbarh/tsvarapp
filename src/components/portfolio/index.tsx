import {
  Accordion,
  AccordionDetails,
  AccordionSummary,
  Card,
  CardContent,
  List,
  ListItem,
  Typography,
} from "@mui/material";

function Portfolio() {
  return (
    <Card sx={{ minWidth: 275 }}>
      <CardContent>
        <Typography variant="h5" component="div">
          Portfolio
        </Typography>
        <Typography variant="h6" component="div">
          Stocks
        </Typography>
        <List>
          <ListItem>
            <Accordion>
              <AccordionSummary>
                <Typography>Stock 1</Typography>
              </AccordionSummary>
              <AccordionDetails>
                <Typography>
                  Lorem ipsum dolor sit amet, consectetur adipiscing
                </Typography>
              </AccordionDetails>
            </Accordion>
          </ListItem>
          <ListItem>
            <Accordion>
              <AccordionSummary>
                <Typography>Stock 2</Typography>
              </AccordionSummary>
              <AccordionDetails>
                <Typography>
                  Lorem ipsum dolor sit amet, consectetur adipiscing
                </Typography>
              </AccordionDetails>
            </Accordion>
          </ListItem>
        </List>
        <Typography variant="h6" component="div">
          Options
        </Typography>
        <List>
          <ListItem>
            <Accordion>
              <AccordionSummary>
                <Typography>Option 1</Typography>
              </AccordionSummary>
              <AccordionDetails>
                <Typography>
                  Lorem ipsum dolor sit amet, consectetur adipiscing
                </Typography>
              </AccordionDetails>
            </Accordion>
          </ListItem>
          <ListItem>
            <Accordion>
              <AccordionSummary>
                <Typography>Option 2</Typography>
              </AccordionSummary>
              <AccordionDetails>
                <Typography>
                  Lorem ipsum dolor sit amet, consectetur adipiscing
                </Typography>
              </AccordionDetails>
            </Accordion>
          </ListItem>
        </List>
      </CardContent>
    </Card>
  );
}

export default Portfolio;
