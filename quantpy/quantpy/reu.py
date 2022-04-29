# -*- coding: utf-8 -*-
"""
Created on Tue Apr 26 13:12:31 2022

@author: sebas
"""

#Imports:
import pandas as pd
import numpy as np
import scipy.stats

def reu(ref, lcs, u_xi=0.0, k=2):
    """
    Calculates the Relative Expanded Uncertainty (REU) of a secondary instrument 
    (e.g. a Low-Cost Sensor, LCS), relative to a Reference Instrument (Ref).
    NOTE: The function presented here uses Ordinary Least Squares to parameterize
    the REU and not the Orthogonal Regression originally proposed in the document
    "Guidance for the Demonstration of Equivalence of Ambient Air Monitoring Methods"
    https://ec.europa.eu/environment/air/quality/legislation/pdf/equivalence.pdf

    Parameters
    ----------
    ref: np.array like
        Reference measurements
    lcs: np.array like
        LCS measurements. Must be same length as `ref`.
    u_xi: float
        Random uncertainty for the reference method. Defaults to 0.
    k: float
        Scaling parameter. Defaults to 2.

    Returns
    -------
    Dataframe

    Example
    --------
    #Creating a simple dataframe:
    from quantpy.reu import reu
    import pandas as pd
    import numpy as np
    #Index
    times = pd.date_range('2021-10-01', periods = 1000, freq ='60min')
    #dataframe creation with only the  reference concentration column
    df = pd.DataFrame(np.random.lognormal(mean = 3, sigma = 0.4, size = 1000),
                      columns = ['NO2'], index = times)
    #adding the LCSs data column. This example adds noise and some bias.
    df['LCS1'] = (df['NO2'] + np.random.normal(0,3,len(df.index)).tolist())*1.2

    #Testing the function
    reu(df['NO2'], df['LCS1'], u_xi = 0.0)
    """
    #masking the NaN's
    mask = ~np.isnan(ref) & ~np.isnan(lcs)
    ref = ref[mask]
    lcs = lcs[mask]

    #number of data points
    n = len(ref)

    #slope & intercept calculation (Ordinary Least Squares regression)
    b1, b0, _, _, _ = scipy.stats.linregress(ref, lcs)

    #equation error variance for y = b0 + b1*x + v_i
    rss = np.sum((lcs - b0 - b1*ref)**2)
    sigma_v_sqr = rss/(n-2)

    #error variance due to the deviation of the 1:1 line
    ec = (b0 + (b1 - 1)*ref)**2

    #Relative Expanded Uncertainty
    estimate = k*((sigma_v_sqr - u_xi**2 + ec)**(1/2))*100/lcs
    return estimate
