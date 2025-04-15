    """
    !!
    
    This is some trial code for the portfolio construction process. Expect dummy functionality and code changes.
    
    !!
    
    """


import numpy as np
import pandas as pd
from scipy.stats import norm
from scipy.spatial.distance import cdist

# --- Black-Scholes elasticity ---
def bs_elasticity(S, K, T, r, sigma, option_type='call'):
    d1 = (np.log(S / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
    if option_type == 'call':
        price = S * norm.cdf(d1) - K * np.exp(-r * T) * norm.cdf(d1 - sigma * np.sqrt(T))
        delta = norm.cdf(d1)
    else:
        price = K * np.exp(-r * T) * norm.cdf(-d1 + sigma * np.sqrt(T)) - S * norm.cdf(-d1)
        delta = -norm.cdf(-d1)
    return (delta * S / price), price

# --- Kernel Weights ---
def kernel_weights(moneyness_grid, maturity_grid, k_s, ttm, bw_m=0.0125, bw_t=10):
    grid = np.column_stack((moneyness_grid, maturity_grid))
    point = np.array([[k_s, ttm]])
    dists = cdist(grid, point, 'euclidean')[:, 0]
    weights = np.exp(-0.5 * (dists / np.array([bw_m, bw_t])).sum())
    return weights / weights.sum()

# --- Construct a single day portfolio ---
def construct_portfolio(data, k_s_target, ttm_target, option_type='call', r=0.01):
    subset = data[(data['option_type'] == option_type)]
    weights = kernel_weights(subset['moneyness'], subset['ttm'], k_s_target, ttm_target)
    subset = subset.assign(weight=weights)
    subset = subset[subset['weight'] > 0.01]
    subset['weight'] /= subset['weight'].sum()

    # Leverage-adjusted returns
    elast, price = bs_elasticity(
        S=subset['underlying'], K=subset['strike'], T=subset['ttm']/365,
        r=r, sigma=subset['iv'], option_type=option_type
    )
    subset['leverage_return'] = subset['daily_return'] / elast

    return (subset['leverage_return'] * subset['weight']).sum()

# --- Main Loop (simplified) ---
def build_portfolios(option_data, m_grid, ttm_grid, option_types=['call', 'put']):
    portfolios = []
    for opt_type in option_types:
        for k_s in m_grid:
            for ttm in ttm_grid:
                ret = construct_portfolio(option_data, k_s, ttm, option_type=opt_type)
                portfolios.append({
                    'type': opt_type,
                    'moneyness': k_s,
                    'ttm': ttm,
                    'return': ret
                })
    return pd.DataFrame(portfolios)
