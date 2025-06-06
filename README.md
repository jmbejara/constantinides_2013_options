# Portfolio Returns Reproduction
##  Based on Constantinides, George M., Jens Carsten Jackwerth, and Alexi Savov. “The puzzle of index option returns.” Review of Asset Pricing Studies 3, no. 2 (2013): 229-257.


### SPX Option Portfolio Construction Process

1. Utilize 3-tiered options data filtration process outlined in *Constantinides, Jackwerth, Savov (2013)* ("**CJS**").

2. Construct option portfolios using the process outlined in *He, Kelly, Manela (2017)* ("**HKM**").



## SPX Option Portfolio Construction — Work Process

### Step 1: Data
- SPX index options data from WRDS / OptionMetrics:
    -- Do we want this code to be flexible to any timeframe? 
    -- Do we ignore the time period replication issues raised in the final project last year? 
- Required fields: strike, maturity, bid/ask, implied vol, underlying index level, option type (call/put)

---

### Step 2: Data Filtering (per Constantinides, Jackwerth, Savov 2013)
- Apply 3-step filtration process:
  1. Retain only reliable quotes based on bid-ask and quote conditions
  2. Apply stricter filters to the buy-side of the market
  3. For missing quotes:
     - Use raw quote if available
     - Use payoff if expiration is near
     - Otherwise interpolate **implied vol** using fitted surface and reconstruct price

---

### Step 3: Define Portfolio Bins
- Create 54 distinct portfolios (***or 18 per HKM??***):
  - 9 moneyness bins: [0.90, 0.925, ..., 1.10]
  - 3 time-to-maturity buckets: 30, 60, 90 days
  - 2 option types: call and put

---

### Step 4: Return Computation (per He, Kelly, Manela 2017)
- For each option in each portfolio:
  - Compute one-day arithmetic return using midpoint of bid-ask
  - Apply leverage adjustment to achieve beta = 1 using Black-Scholes elasticity:
    - Call: $\frac{\partial C}{\partial S} \cdot \frac{S}{C} > 1$
    - Put: $\frac{\partial P}{\partial S} \cdot \frac{S}{P} < -1$
  - Hold fractional option positions; invest remaining capital in the risk-free asset

---

### Step 5: Weighting and Cleaning
- No kernel smoothing is applied (unlike Constantinides et al.)
- Use filtered options only
- Interpolate implied vol surface as needed for missing contracts
- If price still missing, carry forward last known price and rescale weights

---

### Step 6: Aggregation and Output -- DISCUSS
- Compute leverage-adjusted returns daily
- Compound daily returns into monthly returns per portfolio
- Optional: collapse 54 portfolios into 18 by averaging over maturities for each moneyness and option type

---

### Step 7: Panel Data Formatting -- DISCUSS
- Structure final dataset as panel data:
  - Dimensions: Date × Portfolio ID
  - Variables: return, moneyness, maturity, option type

---

### Step 8: Downstream Use ??
- Use portfolio returns in cross-sectional asset pricing models
- Compatible with Fama-MacBeth regressions and intermediary factor models


---

### Portfolio Construction in He, Kelly, Manela (2017)

#### 1. Objective
To create representative test portfolios across various asset classes (including options), enabling cross-sectional asset pricing tests of intermediary capital risk.

---

#### 2. Option Portfolio Structure
- **54 portfolios**: S&P 500 index options, sorted by:
  - **Moneyness (strike/index)**: 9 levels  
  - **Maturity**: 30, 60, or 90 days  
  - **Type**: Separate portfolios for **calls** and **puts**
- **Final form for testing**: HKM reduced the 54 to **18 portfolios** by averaging across maturities with the same moneyness.

---

#### 3. Return Computation
- **Daily arithmetic return**, based on the **midpoint of bid-ask prices**
- **Leverage-adjusted** to achieve a **market beta of 1** using Black-Scholes **elasticity**:
  - Call elasticity = $\frac{\partial C}{\partial S} \cdot \frac{S}{C} > 1$  
  - Put elasticity = $\frac{\partial P}{\partial S} \cdot \frac{S}{P} < -1$
- Fractional option holdings + remainder in **risk-free asset**

---

#### 4. Weighting and Cleaning
- No **kernel weighting** like Constantinides et al.
- Use of **filtered data** with interpolated **implied volatility surface**
- **Missing data** handled via interpolation or holding asset at previous price

---

#### 5. Aggregation
- Daily leverage-adjusted returns → **monthly compounded returns**
- Each


----


### **Portfolio Construction in Constantinides (2013)**
- **Number of Portfolios**: 54 total, split into:
  - 27 call option portfolios  
  - 27 put option portfolios
- **Design Grid**: Each portfolio is defined by a specific:
  - **Time to maturity**: 30, 60, or 90 days  
  - **Moneyness**: 9 levels:  
    `0.90, 0.925, 0.95, 0.975, 1.00, 1.025, 1.05, 1.075, 1.10`  
    - *Moneyness = strike price / index level*

---

### **Data and Filters**
- **Sources**:
  - Berkeley Options Database (1986–1995)  
  - OptionMetrics (1996–2012)
- **Filtering**:
  - Only reliable quotes are used  
  - 173,125 (Berkeley) and 824,397 (OptionMetrics) observations after filtering  
  - Filters are applied more strictly on the buy side; missing quotes are interpolated using a fitted implied volatility surface

---

### **Weighting and Construction**
- **Weighting Kernel**:
  - Bivariate Gaussian kernel on moneyness and days to maturity  
  - Bandwidths: 0.0125 (moneyness), 10 days (maturity)  
  - Options with weights < 1% are dropped
- **Normalization**:
  - Weights are normalized to sum to 1  
  - Recomputed daily

---

### **Return Calculation**
- **Return Basis**:
  - One-day arithmetic return based on midpoint of bid-ask
- **Leverage Adjustment**:
  - Portfolios are adjusted to unit market beta (β = 1) daily using Black-Scholes elasticity:  
    - Call elasticity: ∂C/∂S × S/C > 1  
    - Put elasticity: ∂P/∂S × S/P < –1  
  - This results in holding fractional option positions and investing the rest in the risk-free asset
- **Final Return Series**:
  - Daily leverage-adjusted returns are compounded into monthly returns

---

### **Robustness and Treatment of Missing Data**
- **Handling Missing Options**:
  - If quote is unavailable:
    - Use unfiltered data if possible  
    - Use payoff at expiry if expiration is imminent  
    - Otherwise, interpolate using a surface fit to implied volatility
  - During missing periods, options are held at purchase price and weights rescaled to maintain portfolio integrity

---

### **Statistical Rationale**
- This process significantly reduces skewness and kurtosis, enabling:
  - Application of linear factor pricing models  
  - Direct comparison with models using Fama-French 25 portfolios




