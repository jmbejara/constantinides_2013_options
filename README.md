# SPX Option Portfolio Construction Workflow

**Based on:**  
- Constantinides, Jackwerth, Savov (2013) — *The Puzzle of Index Option Returns*  
- He, Kelly, Manela (2017) — *Intermediary Asset Pricing*

---

## Overview

This workflow builds portfolios of S&P 500 index options to replicate and extend results in CJS (2013) and HKM (2017). The goal is to reconstruct the time series of returns for option portfolios used in HKM on cross-sectional asset pricing. The primary difference between the CJS and HKM papers is that the HKM study utilizes 18 portfolios instead of 54 in CJS, by taking an equal-weighted average across the 3 maturities utilized in CJS (i.e. 30, 60, and 90 days).

---

## Data Utilized

- SPX options data from WRDS / OptionMetrics, from January 1996 - December 2019. 


---

## Step 2: SPX Option Data Filtration Protocol
*Based on Constantinides, Jackwerth, and Savov (2013), Appendix B*

### Level 1 Filters — Data Deduplication and Quote Reliability

These filters remove redundant quotes and structurally unreliable observations.

- **Identical Filter**  
  Drop duplicate entries with the same option type, strike, expiration, and price. Retain only one instance per combination.

- **Identical Except Price Filter**  
  For quotes with identical terms (option type, strike, expiration) but different prices, retain the quote whose T-bill-implied volatility is closest to that of its neighbors in moneyness. Remove the rest.

- **Bid = 0 Filter**  
  Eliminate quotes with zero bid price to avoid stale or low-value options. Zero bids may also reflect censoring, as negative bids are not recordable.

- **Volume = 0 Filter**  
  Although not discussed in Appendix B, CJS Table B.1 lists this filter. We acknowledge its presence but exclude it from our protocol, as applying it drops over 70% of the remaining records and is not described in the methodology text.

---

### Level 2 Filters — Economic Plausibility and Pricing Consistency

These filters enforce basic economic logic, plausible moneyness, and valid interest rate inference from market prices.

- **Days to Maturity < 7 or > 180**  
  Drop options with fewer than 7 or more than 180 calendar days to expiration. Very short-dated options behave erratically, and long-dated options are often illiquid.

- **Implied Volatility < 5% or > 100%**  
  Remove options with extreme implied volatility values, using T-bill rates. Such extremes are likely due to stale quotes or poor fits.

- **Moneyness < 0.8 or > 1.2**  
  Eliminate deep ITM or OTM options where pricing is dominated by intrinsic value or illiquidity, limiting informativeness for IV surface construction.

- **Implied Interest Rate < 0**  
  Use put-call parity to back out the implied interest rate from matched quotes. Drop any options for which the implied interest rate is negative. Remaining quotes are assigned the median implied rate by maturity (for moneyness 0.95–1.05), and the rest are interpolated across maturities and days.

- **Unable to Compute IV (Negative Time Value)**  
  Discard quotes that imply negative time value, indicating arbitrage violations or pricing errors that invalidate IV computation.

---

### Level 3 Filters — Surface Fit Outlier Removal and Arbitrage Constraints

These filters ensure internal consistency across the implied volatility surface and enforce no-arbitrage conditions.

- **Implied Volatility Filter**  
  For each date and maturity, fit a quadratic curve to the log-implied volatilities of calls and puts separately. Remove options that deviate substantially from the fitted curve, as these are likely mispriced or stale quotes.

- **Put-Call Parity Filter**  
  Match put-call pairs by date, strike, and expiration. Compute a put-call parity-implied interest rate, and drop quotes where the implied rate deviates significantly from the daily median, suggesting violations of parity or data inconsistency.



---

## Step 3: Define Portfolio Grid

- Construct **54 portfolios**:
  - **Moneyness bins (9):** 0.90, 0.925, ..., 1.10
  - **Maturities (3):** 30, 60, 90 days
  - **Option types (2):** Calls and Puts
- For HKM: Collapse to **18 portfolios** by averaging across maturities

---

## Step 4: Compute Option Returns (HKM Methodology)

- **Daily return:** Use midpoint of bid and ask
- **Leverage adjustment:** Scale to β = 1 using Black-Scholes elasticity:
  - Call: ∂C/∂S × S/C > 1  
  - Put: ∂P/∂S × S/P < -1
- **Capital allocation:** Hold fractional options; remainder in risk-free asset

---

## Step 5: Cleaning and Weighting

- Exclude options with:
  - Invalid or extreme implied vols
  - Missing return inputs (unless interpolated)
- No kernel smoothing (unlike CJS)
- If data missing:
  - Interpolate IV or carry forward price
  - Rescale portfolio weights to preserve capital

---

## Step 6: Return Aggregation

- **Daily to Monthly:** Compound daily β-adjusted returns
- **Per Portfolio:** Maintain separate return series for each defined portfolio

---

## Step 7: Final Dataset Structure

- **Panel format:**
  - **Rows:** Date × Portfolio ID
  - **Columns:** Return, moneyness, maturity, option type, elasticity, leverage-adjusted return

---

## Step 8: Downstream Usage

- Ready for:
  - Fama-MacBeth regressions
  - Intermediary factor model testing
  - Cross-asset comparison (if combining with HKM asset set)

---

## Notes on Robustness

- Filtration + elasticity adjustment yields cleaner return series
- Design enables beta normalization across option portfolios
- Reduced skewness and kurtosis allows use of linear factor pricing models