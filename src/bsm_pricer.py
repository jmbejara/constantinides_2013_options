"""
This module contains functions for pricing European call and put options using the Black-Scholes-Merton model,
as well as calculating implied volatility.

Functions:
- european_call_price: Calculates the price of a European call option.
- european_put_price: Calculates the price of a European put option.
- norm_cdf: Calculates the cumulative distribution function (CDF) of the standard normal distribution.
- norm_pdf: Calculates the probability density function (PDF) of the standard normal distribution.
- calc_vega: Calculates the option vega using the Black-Scholes-Merton model.
- iv_objective: Calculates the difference between the market price and the theoretical price of an option.
- calc_implied_volatility: Calculates the implied volatility of an option using the bisection method.
"""

import math
import numpy as np
from scipy.stats import norm
from scipy.optimize import minimize, newton


def european_call_price(S, K,  T, r, sigma):
    """
    Calculates the price of a European call option using the Black-Scholes-Merton model.

    Parameters:
    S (float): Current price of the underlying asset
    K (float): Strike price of the option
    r (float): Risk-free interest rate
    T (float): Time to expiration of the option (in years)
    sigma (float): Volatility of the underlying asset. Can be implied or historical, with appropriate interpretation of results.

    Returns:
    float: Price of the European call option
    """
    
    d1 = (math.log(S / K) + (r + 0.5 * sigma**2) * T) / (sigma * math.sqrt(T))
    d2 = d1 - sigma * math.sqrt(T)
    
    call_price = S * norm_cdf(d1) - K * math.exp(-r * T) * norm_cdf(d2)
    return call_price


def european_put_price(S, K, T, r, sigma):
    """
    Calculates the price of a European put option using the Black-Scholes-Merton model.

    Parameters:
    S (float): The current price of the underlying asset.
    K (float): The strike price of the option.
    r (float): The risk-free interest rate.
    T (float): The time to expiration of the option in years.
    sigma (float): The volatility of the underlying asset. Can be implied or historical, with appropriate interpretation of results.

    Returns:
    float: The price of the European put option.
    """
    
    d1 = (math.log(S / K) + (r + 0.5 * sigma**2) * T) / (sigma * math.sqrt(T))
    d2 = d1 - sigma * math.sqrt(T)
    
    put_price = K * math.exp(-r * T) * norm_cdf(-d2) - S * norm_cdf(-d1)
    return put_price


def norm_cdf(x):
    """
    Calculates the cumulative distribution function (CDF) of the standard normal distribution.

    Parameters:
    x (float): The value at which to evaluate the CDF.

    Returns:
    float: The CDF value at x.
    """
    # return (1.0 + math.erf(x / math.sqrt(2.0))) / 2.0
    return norm.cdf(x)


def norm_pdf(x):
    """
    Calculates the probability density function (PDF) of the standard normal distribution.

    Parameters:
    x (float): The value at which to evaluate the PDF.

    Returns:
    float: The PDF value at x.
    """
    # return math.exp(-0.5 * x**2) / math.sqrt(2 * math.pi)
    return norm.pdf(x)


def calc_vega(S, K, T, r, sigma):
    '''Calculate option vega using Black-Scholes-Merton model.'''
    
    d1 = (np.log(S/K) + (r + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
    return S * norm_pdf(d1) * np.sqrt(T)



def iv_objective(sigma, market_price, S, K, T, r, option_type):
    """
    Objective function to calculate implied volatility for quasi-newton methods.
    """
    
    if option_type.lower() in ['call', 'c']:
        theoretical_price = european_call_price(S=S, K=K, T=T, r=r, sigma=sigma)
    else:
        theoretical_price = european_put_price(S=S, K=K, T=T, r=r, sigma=sigma)
        
    # print(option_type, 'price:',theoretical_price, sigma, market_price, (theoretical_price - market_price)**2)
    return (theoretical_price - market_price)**2



def calc_implied_volatility(market_price, S, K, T, r, option_type, method='quasi_newton', tol=1e-12, initial_guess=0.05, bounds=(0.00001, 5.0)):
    """
    Calculates the implied volatility of an option using various methods. Options for method are 'quasi_newton', 'newton_raphson', 'binary_search', and 'all'. If method=='all', the function returns a dictionary containing the implied volatilities calculated using different methods.

    Parameters:
    - market_price (float): The market price of the option.
    - S (float): The current price of the underlying asset.
    - K (float): The strike price of the option.
    - T (float): The time to expiration of the option.
    - r (float): The risk-free interest rate.
    - option_type (str): The type of the option ('call' or 'put').
    - method (str, optional): The method to use for calculating implied volatility. Defaults to 'quasi_newton'.
    - tol (float, optional): The tolerance for convergence. Defaults to 1e-12.
    - initial_guess (float, optional): The initial guess for implied volatility. Defaults to 0.05.
    - bounds (tuple, optional): The lower and upper bounds for implied volatility. Defaults to (0.00001, 5.0).

    Returns:
    - float or dict: The implied volatility of the option. If method is 'all', returns a dictionary containing the implied volatilities calculated using different methods.
    """
    
    if method == 'quasi_newton':
        return iv_quasi_newton_vectorized(market_price=market_price, S=S, K=K, T=T, r=r, option_type=option_type, tol=tol, initial_guess=initial_guess, bounds=bounds)
    elif method=='newton_raphson':
        return iv_newton_raphson(market_price=market_price, S=S, K=K, T=T, r=r, option_type=option_type, sigma_est=initial_guess)
    elif method=='binary_search':
        return iv_binary_search(market_price=market_price, S=S, K=K, T=T, r=r, option_type=option_type, sigma_low=initial_guess, sigma_high=5, tolerance=tol)
    elif method=='all':
        return {'quasi_newton': iv_quasi_newton_vectorized(market_price=market_price, S=S, K=K, T=T, r=r, option_type=option_type, tol=tol, initial_guess=initial_guess, bounds=bounds),
                'newton_raphson': iv_newton_raphson(market_price=market_price, S=S, K=K, T=T, r=r, option_type=option_type, sigma_est=initial_guess),
                'binary_search': iv_binary_search(market_price=market_price, S=S, K=K, T=T, r=r, option_type=option_type, sigma_low=initial_guess, sigma_high=5, tolerance=tol)
                }
    
    

def iv_quasi_newton_vectorized(market_price, S, K, T, r, option_type, tol=1e-15, initial_guess=0.05, bounds=(0.00001, 5.0)):
    """
    Calculates the implied volatility for each set of option parameters using a quasi-Newton optimization method.
    This function iterates over vector inputs to handle multiple calculations.
    
    Parameters are the same as the original function but can accept NumPy arrays for vectorized inputs.
    Returns a NumPy array of implied volatilities for each set of input parameters.
    """
    # Ensure inputs are NumPy arrays for vectorized operations
    market_price, S, K, T, r = map(np.asarray, (market_price, S, K, T, r))
    if isinstance(option_type, str):
        option_type = np.full(market_price.shape, option_type)  # Broadcast to full array if single value
    
    # Initialize an array to hold the implied volatility results
    iv_results = np.zeros(market_price.shape)
    
    # Iterate over each element in the input arrays
    for i in range(len(market_price)):
        # Function to minimize (objective function)
        def iv_objective(sigma, market_price, S, K, T, r, option_type):
            # Placeholder for the actual objective function calculation
            # This should return the difference between theoretical and market prices
            pass
        
        result = minimize(iv_objective, [initial_guess], args=(market_price[i], S[i], K[i], T[i], r[i], option_type[i]),
                          bounds=[bounds], method='L-BFGS-B', options={'eps': tol, 'gtol': tol})
        
        if result.success:
            iv_results[i] = result.x[0]  # Store the optimized volatility
        else:
            iv_results[i] = np.nan  # Use NaN to indicate optimization failure
    
    return iv_results 


# Function to calculate implied volatility
def iv_quasi_newton(market_price, S, K, T, r, option_type, tol=1e-15, initial_guess=0.05, bounds=(0.00001, 5.0)):
    """
    Calculates the implied volatility using a quasi-Newton optimization method with scipy.optimize.minimize.

    Parameters:
    - market_price (float): The observed market price of the option.
    - S (float): The current price of the underlying asset.
    - K (float): The strike price of the option.
    - T (float): The time to expiration of the option in years.
    - r (float): The risk-free interest rate.
    - option_type (str): The type of the option, either 'call' or 'put'.
    - tol (float, optional): The tolerance level for convergence. Defaults to 1e-12.
    - initial_guess (float, optional): The initial guess for the volatility. Defaults to 0.05.
    - bounds (tuple, optional): The lower and upper bounds for the volatility. Defaults to (0.00001, 5.0).

    Returns:
    - float: The implied volatility of the option.

    Raises:
    - ValueError: If the optimization was not successful.

    """
    
    # Initial guess for volatility
    initial_guess = [initial_guess]
    
    # Bounds for volatility (must be positive)
    bounds = [bounds]
    
    # Minimize the objective function
    result = minimize(iv_objective, initial_guess, args=(market_price, S, K, T, r, option_type),
                      bounds=bounds, method='L-BFGS-B', options={'eps': tol, 'gtol': tol})
    
    if result.success:
        return result.x[0]  # Return the optimized volatility
    else:
        raise ValueError("Optimization was not successful. Try different bounds or initial guess.")
        


def iv_newton_raphson(market_price, S, K, T, r, option_type='call', sigma_est = 0.1):
    """
    Calculate implied volatility (IV) using the Newton-Raphson method.

    Parameters:
    option_market_price (float): The market price of the option.
    S (float): The current price of the underlying asset.
    K (float): The strike price of the option.
    T (float): The time to expiration of the option.
    r (float): The risk-free interest rate.
    option_type (str, optional): The type of the option, either 'call' or 'put'. Defaults to 'call'.
    sigma_est (float, optional): An initial estimate for the volatility. Defaults to 0.1.

    Returns:
    float: The implied volatility of the option.

    Notes:
    - The function uses the Newton-Raphson method to iteratively find the implied volatility.
    - If the method fails to converge, the function returns NaN.
    """
    
    def f(sigma):
        """Function of sigma - market price."""
        if option_type.lower() in ['call', 'c']:
            return european_call_price(S, K, T, r, sigma) - market_price
        else:  # put option
            return european_put_price(S, K, T, r, sigma) - market_price

    # Calculate IV using newton method provided by scipy
    # The newton method's fprime parameter is where the derivative of the function (Vega in this case) is passed
    try:
        # Ensuring calc_vega is used correctly as the derivative of the price w.r.t. sigma
        iv = newton(f, sigma_est, fprime=lambda sigma: calc_vega(S, K, T, r, sigma))
        return iv
    except RuntimeError:
        return np.nan  # Return NaN if the method fails to converge
    

def iv_binary_search(market_price, S, K, T, r, option_type='call', sigma_low = 0.001,  sigma_high = 1, tolerance = 1e-5):
    """
    Calculate the implied volatility (IV) using binary search.
    
    Parameters:
    - option_market_price (float): The market price of the option.
    - S (float): The current price of the underlying asset.
    - K (float): The strike price of the option.
    - T (float): The time to expiration of the option.
    - r (float): The risk-free interest rate.
    - option_type (str, optional): The type of the option, either 'call' or 'put'. Defaults to 'call'.
    - sigma_low (float, optional): The lower bound of the volatility range. Defaults to 0.001.
    - sigma_high (float, optional): The upper bound of the volatility range. Defaults to 1.
    - tolerance (float, optional): The tolerance level for convergence. Defaults to 1e-5.
    
    Returns:
    - float: The implied volatility of the option.
    """
    
    while sigma_low < sigma_high:
        sigma_mid = (sigma_low + sigma_high) / 2
        price_mid = european_call_price(S, K, T, r, sigma_mid) if option_type == 'call' else european_put_price(S, K, T, r, sigma_mid)
        
        if abs(price_mid - market_price) < tolerance:
            return sigma_mid
        elif price_mid < market_price:
            sigma_low = sigma_mid
        else:
            sigma_high = sigma_mid
            
    return (sigma_low + sigma_high) / 2




def calc_option_elasticity(delta, option_price, underlying_price, option_type='call'):
    """
    Calculate the elasticity of an option.

    Parameters:
    - delta (float): The delta of the option, representing the rate of change of the option price with respect to changes in the underlying asset's price. Delta of a put must be negative. 
    - option_price (float): The current price of the option.
    - underlying_price (float): The current price of the underlying asset.

    Returns:
    - float: The elasticity of the option.
    """
    
    elasticity = delta * (underlying_price / option_price)
    return elasticity





if __name__=='__main__':
    # take inputs from user
    S = float(input("Enter the current price of the underlying asset: "))
    K = float(input("Enter the strike price of the option: "))
    r = float(input("Enter the risk-free interest rate: "))
    T = float(input("Enter the time to expiration of the option in years: "))
    sigma = float(input("Enter the volatility of the underlying asset: "))
    print('European call option price:', european_call_price(S=S, K=K, r=r, T=T, sigma=sigma))
    print('European put option price:', european_put_price(S=S, K=K, r=r, T=T, sigma=sigma))
    
    print('Implied volatility:', calc_implied_volatility(market_price=30, S=S, K=K, r=r, T=T, option_type='call'))
        
        
    # Example usage
    option_market_price = 10  # Market price of the option
    S = 100  # Underlying asset price
    K = 100  # Strike price
    T = 1  # Time to maturity (in years)
    r = 0.05  # Risk-free interest rate

    iv_nr = iv_newton_raphson(option_market_price, S, K, T, r)
    iv_bs = iv_binary_search(option_market_price, S, K, T, r)

    print(f"IV (Newton-Raphson): {iv_nr}")
    print(f"IV (Binary Search): {iv_bs}")
        
    
    
