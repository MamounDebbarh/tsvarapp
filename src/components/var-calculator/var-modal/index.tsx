// Component used to display the modal for the var calculator
import ExpandMoreIcon from "@mui/icons-material/ExpandMore";

import {
  Accordion,
  AccordionDetails,
  AccordionSummary,
  Dialog,
  DialogContent,
  DialogTitle,
  Typography,
} from "@mui/material";

interface VarModalProps {
  openVarDialog: boolean;
  handleVarDialogClose: () => void;
  varData: VarData;
}

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

function VarModal(props: VarModalProps) {
  const { openVarDialog, handleVarDialogClose, varData } = props;

  return (
    <Dialog open={openVarDialog} onClose={handleVarDialogClose}>
      <DialogTitle>
        {" "}
        Value at risk is the maximum loss that can be expected in a given time
        period with a given probability.
      </DialogTitle>
      <DialogContent>
        <Accordion>
          <AccordionSummary expandIcon={<ExpandMoreIcon />}>
            <Typography>
              Historical Value at risk: {varData.historicalVaR}
            </Typography>
          </AccordionSummary>
          <AccordionDetails>
            <Typography>
              Historical VaR is calculated using a portfolio's daily returns
              over a certain period of time. The portfolio's daily returns are
              used to calculate the portfolio's volatility and expected returns.
              The volatility of the portfolio's returns is then used to
              calculate the portfolio's VaR.{" "}
            </Typography>
          </AccordionDetails>
        </Accordion>
        <Accordion>
          <AccordionSummary expandIcon={<ExpandMoreIcon />}>
            <Typography>
              Historical Conditional value at risk: {varData.historicalCVaR}
            </Typography>
          </AccordionSummary>
          <AccordionDetails>
            <Typography>
              The difference between Historical VaR and Historical CVaR is that
              VaR looks at the probability of a loss over a certain period of
              time, while CVaR looks at the average losses that would occur if a
              loss occurred at that time. VaR is calculated using the historical
              returns of the portfolio, while CVaR is calculated using the
              expected returns of the portfolio.
            </Typography>
          </AccordionDetails>
        </Accordion>
        <Accordion>
          <AccordionSummary expandIcon={<ExpandMoreIcon />}>
            <Typography>
              Normal distribution VaR: {varData.normalDistributionVaR}
            </Typography>
          </AccordionSummary>
          <AccordionDetails>
            <Typography>
              Normal distribution VaR is calculated using the inverse of the
              normal cumulative distribution function. The normal distribution
              VaR is based on the assumption that the portfolio returns follow a
              normal distribution or bell curve.
            </Typography>
          </AccordionDetails>
        </Accordion>
        <Accordion>
          <AccordionSummary expandIcon={<ExpandMoreIcon />}>
            <Typography>
              Normal distribution CVaR: {varData.normalDistributionCVaR}
            </Typography>
          </AccordionSummary>
          <AccordionDetails>
            <Typography>
              CVaR, on the other hand, takes into account the entire
              distribution of potential losses, rather than just the worst
              losses. It is calculated by taking the average of the worst losses
              of the portfolio and then multiplying that percentile by the
              standard deviation of the portfolio.
            </Typography>
          </AccordionDetails>
        </Accordion>
        <Accordion>
          <AccordionSummary expandIcon={<ExpandMoreIcon />}>
            <Typography>
              t distribution VaR: {varData.tDistributionVaR}
            </Typography>
          </AccordionSummary>
          <AccordionDetails>
            <Typography>
              t distribution VaR is calculated by first calculating the expected
              loss and then using the t-distribution to determine the
              probability of a given loss occurring. The expected loss is then
              multiplied by the probability to create the CVaR.
            </Typography>
          </AccordionDetails>
        </Accordion>
        <Accordion>
          <AccordionSummary expandIcon={<ExpandMoreIcon />}>
            <Typography>
              t distribution CVaR: {varData.tDistributionCVaR}
            </Typography>
          </AccordionSummary>
          <AccordionDetails>
            <Typography>
              The key advantage of using CVaR is that it is able to measure the
              expected losses of a portfolio beyond the point of VaR. This makes
              it a more accurate measure of risk than VaR, as it takes into
              account the potential for losses that may be greater than those
              indicated by the VaR measure. This is especially important when
              dealing with a highly volatile portfolio, as it can provide
              insight into the potential magnitude of losses that may be
              experienced.
            </Typography>
          </AccordionDetails>
        </Accordion>
        <Accordion>
          <AccordionSummary expandIcon={<ExpandMoreIcon />}>
            <Typography>Monte Carlo VaR: {varData.monteCarloVaR}</Typography>
          </AccordionSummary>
          <AccordionDetails>
            <Typography>
              Monte Carlo VaR is calculated by simulating many different
              scenarios and then calculating the VaR of each scenario. This
              approach can produce a more accurate VaR figure, as it considers
              the distribution of possible outcomes and the probability of each
              one occurring.
            </Typography>
          </AccordionDetails>
        </Accordion>
        <Accordion>
          <AccordionSummary expandIcon={<ExpandMoreIcon />}>
            <Typography>Monte Carlo CVaR: {varData.monteCarloCVaR}</Typography>
          </AccordionSummary>
          <AccordionDetails>
            <Typography>
              CVaR can be calculated in a similar fashion. Monte Carlo CVaR
              differs from traditional CVaR in that it uses a Monte Carlo
              simulation to simulate multiple scenarios and calculate the CVaR
              for each one. This approach can provide a more accurate measure of
              portfolio risk as it takes into account the probability of
              different potential outcomes.
            </Typography>
          </AccordionDetails>
        </Accordion>
        <Accordion>
          <AccordionSummary expandIcon={<ExpandMoreIcon />}>
            <Typography>
              Monte Carlo VaR (Brownian): {varData.brownianMotionMonteCarloVaR}
            </Typography>
          </AccordionSummary>
          <AccordionDetails>
            <Typography>
              Geometric brownian motion is used in VaR calculations to model the
              behavior of a stock price over time. A stock price is assumed to
              follow a random walk, meaning that the change in the value of the
              stock over time is assumed to be random and independent of the
              previous values. The geometric brownian motion model is also used
              to calculate the expected return of a portfolio.
            </Typography>
          </AccordionDetails>
        </Accordion>
      </DialogContent>
    </Dialog>
  );
}
export default VarModal;
