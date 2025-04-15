### **Portfolio Structure**
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
