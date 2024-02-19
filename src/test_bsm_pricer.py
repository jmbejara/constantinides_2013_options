import pandas as pd
from pandas.testing import assert_frame_equal
from functools import partial

import config
DATA_DIR = config.DATA_DIR

import bsm_pricer

def test_bsm_call_price():
    """
    Test the bsm_pricer.european_call_price() function.
    """

    kwargs = {
        "S": 100,
        "K": 120,
        "r": 0.05,
        "T": 1.75,
        "sigma": 0.65,
    }

    # Expected output:
    # European call option price: 30.156619040994123
    expected_output = 30.156619040994123
    
    assert abs(bsm_pricer.european_call_price(**kwargs) - expected_output) < 1e-10
    
def test_bsm_put_price():
    """
    Test the bsm_pricer.european_put_price() function.
    """

    kwargs = {
        "S": 100,
        "K": 120,
        "r": 0.05,
        "T": 1.75,
        "sigma": 0.65,
    }

    # Expected output:
    # European put option price: 40.102883639099424
    expected_output = 40.102883639099424
    
    assert abs(bsm_pricer.european_put_price(**kwargs) - expected_output) < 1e-10
    
    
def test_calc_implied_volatility():
    """
    Test the bsm_pricer.calc_implied_volatility() function.
    """

    kwargs = {
        "market_price": 30,
        "S": 100,
        "K": 120,
        "r": 0.05,
        "T": 1.75,
        "option_type": "call",
    }

    # Expected output:
    # Implied volatility: 0.6468780610638603
    expected_output = 0.6468780610638603
    
    assert abs(bsm_pricer.calc_implied_volatility(**kwargs) - expected_output) < 1e-10