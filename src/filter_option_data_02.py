"""
This module contains functions to filter options data based on time to maturity, implied volatility, moneyness, and implied interest rate.
"""

import pandas as pd
import numpy as np
from datetime import datetime,timedelta
import bsm_pricer as bsm
import load_option_data_01 as l1
import filter_option_data_01 as f1
import filter_option_data_03 as f3
from pathlib import Path
import config

DATA_DIR = Path(config.DATA_DIR)


def calc_days_to_maturity(df):
    # calc days to maturity
    df = df.assign(days_to_maturity = df['exdate'].subtract(df['date']))
    return df

def days_to_maturity_filter(df, min_days=7, max_days=180):
    df = calc_days_to_maturity(df)
    df = df[(df['days_to_maturity'] >= pd.Timedelta(days=min_days)) & (df['days_to_maturity'] <= pd.Timedelta(days=max_days))]
    return df

def iv_range_filter(df, min_iv=0.05, max_iv=1.00):
    """Filter options based on implied volatility range.
       Default is 5% to 100% (0.05 to 1.00).
    """
    df = df[(df['IV'] >= min_iv) & (df['IV'] <= max_iv)]
    return df


def filter_moneyness(df):
    """Moneyness <0.8 or >1.2 Filter: Filter options based on moneyness.
       We define moneyness as the ratio of the option's strike price to 
       the stock underlying price. Moneyness field must be defined before 
       running this function
    """
    # check if moneyness (mnyns) is already in the dataframe
    if 'mnyns' not in df.columns:
        # if not, calculate moneyness
        df = f1.calc_moneyness(df)
    # remove options with moneyness less than 0.8 or greater than 1.2
    df = df.loc[(df['mnyns']>=0.8) & (df['mnyns']<=1.2)].reset_index(drop=True)
    return df

def filter_implied_interest_rate(optm_l2_mny):
    """Implied Interest Rate <0% Filter: Filter options based on implied interest rate.
       Implied interest rate field must be defined before running this function.
    """
    optm_l2_mny['mid_price'] = (optm_l2_mny['best_bid'] + optm_l2_mny['best_offer']) / 2

    call_options = optm_l2_mny.loc[optm_l2_mny['cp_flag'] == 'C'].reset_index(drop=True)
    put_options = optm_l2_mny.loc[optm_l2_mny['cp_flag'] == 'P'].reset_index(drop=True)

    matching_calls, matching_puts = f3.build_put_call_pairs(call_options, put_options)
    # reset index to merge
    matching_calls.reset_index(inplace=True)
    matching_puts.reset_index(inplace=True)
    
    matched_options = pd.merge(matching_calls, matching_puts, on=['date', 'exdate', 'strike_price', 'sec_price'], suffixes=('_C', '_P')).reset_index()
    
    matched_options = f3.calc_implied_interest_rate(matched_options)
    
    neg_int = matched_options.loc[matched_options['pc_parity_int_rate'] < 0][['date', 'exdate', 'strike_price', 'sec_price']].drop_duplicates()

    optm_l2_int = pd.merge(optm_l2_mny, neg_int, on=['date', 'exdate', 'strike_price', 'sec_price'], how='outer', indicator=True)
    optm_l2_int = optm_l2_int.loc[optm_l2_int['_merge'] == 'left_only'].drop(columns='_merge')  

    med_impl_int = matched_options.loc[(matched_options['mnyns_C']>=0.95) & (matched_options['mnyns_C']<=1.05)].groupby(['time_to_maturity_C'])['pc_parity_int_rate'].median().reset_index()
    med_impl_int = med_impl_int.loc[med_impl_int['pc_parity_int_rate']>=0]

    optm_l2_int = pd.merge(optm_l2_int, med_impl_int, left_on='time_to_maturity', right_on='time_to_maturity_C', how='left', indicator=True)
    optm_l2_int['pc_parity_int_rate'] = optm_l2_int['pc_parity_int_rate'].ffill()
    
    return optm_l2_int


def filter_unable_compute_iv(df):
    """Unable to Compute IV Filter: Filter options where implied volatility cannot be computed.
    """
    df = df.loc[df['impl_volatility'].notna()]
    return df


def apply_l2_filters(df):
    """Apply all level 2 filters to the dataframe.
    """
    df = filter_time_to_maturity(df)
    df = filter_iv(df)
    df = filter_moneyness(df)
    df = filter_implied_interest_rate(df)
    df = filter_unable_compute_iv(df)
    return df

# if __name__ == "__main__": 