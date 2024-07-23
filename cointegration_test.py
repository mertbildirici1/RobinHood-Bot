import pandas as pd
from statsmodels.tsa.stattools import coint

def check_cointegration(series1, series2):
    """
    Perform cointegration test on two time series.
    
    Parameters:
    series1 (pd.Series): First time series.
    series2 (pd.Series): Second time series.
    
    Returns:
    tuple: Cointegration test statistic, p-value, and critical values.
    """
    coint_test = coint(series1, series2)
    return coint_test
