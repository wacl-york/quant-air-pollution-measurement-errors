# -*- coding: utf-8 -*-
"""
Created on Wed Apr 27 10:41:12 2022

@author: sebas
"""

import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.ticker as ticker
import numpy as np
import scipy.stats
from sklearn.metrics import mean_squared_error, mean_absolute_error
from quantpy.reu import reu

def bland_altman(data,
                 ref,
                 lcs,
                 figsize=None,
                 xlim=None,
                 ylim=None,
                 xticks=None,
                 yticks=None
                ):
    """
    Creates a Bland-Altman plot of a secondary instrument (e.g. a Low-Cost Sensor)
    and a Reference Instrument.

    Parameters
    ----------
    data: pandas.DataFrame
        The dataframe containing the Reference and LCS time series
    ref: string
        Name of the column containing the reference data (e.g. 'NO2').
    lcs: string
        Name of the column containing the LCS data (e.g. 'LCS1').
    figsize: A 2 element list
         Figure dimensions (width, height) in inches
    xlim: List of 2 elements
        x-axis limits
    ylim: List of 2 elements
        y-axis limits
    xticks: Iterable
        x-ticks values
    yticks: Iterable
        y-ticks values

    Returns
    -------
    Figure object

    Examples
    --------
    import quantpy.plots as plots
    import pandas as pd
    import numpy as np
    import matplotlib.pyplot as plt

    # Creating a simple dataframe with random reference data
    times = pd.date_range('2021-10-01', periods = 1000, freq ='60min')
    df = pd.DataFrame(np.random.lognormal(mean = 3, sigma = 0.4, size = 1000),
                      columns = ['NO2'], index = times)
    # Simulate a LCS with noise and bias
    df['LCS1'] = (df['NO2'] + np.random.normal(0,3,len(df.index)).tolist())*1.2

    plots.bland_altman(df, 'NO2', 'LCS1')
    plt.show()
    """
    #initialise the figure
    fig, ax = plt.subplots(1, 1,figsize = figsize, dpi = 200)

    #inputs
    x = data[ref]
    y = data[lcs]

    #masking the NaN's
    mask = ~np.isnan(x) & ~np.isnan(y)
    x = x[mask]
    y = y[mask]

    #mean between Ref and LCS
    mean = np.mean([x, y], axis = 0)

    #difference between Ref and LCS
    diff = y - x

    #data points density
    xy = np.vstack([x,y])
    z = scipy.stats.gaussian_kde(xy)(xy)

    #scatter plot diff vs mean
    ax.scatter(mean, diff, c = z, s = 14, alpha = 1, linewidth = 1)

    #mean of the differences
    md = np.mean(diff)

    #add the mean of the differences line
    ax.axline((0, md), slope=0, color="blue", linewidth=2, alpha=0.8, linestyle='-')

    #standard deviation of the differences
    sd = np.std(diff, axis = 0)

    #add lines at 1.96 standard dev
    ax.axline((0, md + 1.96*sd), slope=0, color="red", linewidth=2, alpha=0.8,
              linestyle='-')
    ax.axline((0, md - 1.96*sd), slope=0, color="red", linewidth=2, alpha=0.8,
              linestyle='-')

    #'x' and 'y' axis title
    ax.set_ylabel('Sensor — Reference', labelpad = 5, fontsize = 16)
    ax.set_xlabel('Mean of Ref & Sensor', labelpad = 10, fontsize = 16)

    #'x' and 'y' ticks
    if xticks is not None:
        ax.set_xticks(xticks)
    if yticks is not None:
        ax.set_yticks(yticks)

    #'y' and 'x' axis limits
    if xlim is not None:
        ax.set_xlim(xlim)
    if ylim is not None:
        ax.set_ylim(ylim)

    #annotations
    annot_x_location = 0.67 * np.max(mean)

    annotation_string = 'Mean + 1.96 SD'
    ax.annotate(annotation_string, xy = (annot_x_location, md + 1.96*sd + 1), xycoords = 'data',fontsize = 11)

    annotation_string = 'Mean Diff'
    ax.annotate(annotation_string, xy = (annot_x_location, md + 0.5), xycoords = 'data',fontsize = 11)

    annotation_string = 'Mean - 1.96 SD'
    ax.annotate(annotation_string, xy = (annot_x_location, md - 1.96*sd - 2), xycoords = 'data',fontsize = 11)


def scatter(data,
            ref,
            lcs,
            figsize=None,
            xlim=None,
            ylim=None,
            xticks=None,
            yticks=None
           ):
    """
    Creates a regression plot of a secondary instrument (e.g. a Low-Cost Sensor)
    against a Reference Instrument.

    Parameters
    ----------
    data: pandas.DataFrame
        The dataframe containing the Reference and LCS time series
    ref: string
        Name of the column containing the reference data (e.g. 'NO2').
    lcs: string
        Name of the column containing the LCS data (e.g. 'LCS1').
    figsize: A 2 element list
         Figure dimensions (width, height) in inches
    xlim: List of 2 elements
        x-axis limits
    ylim: List of 2 elements
        y-axis limits
    xticks: Iterable
        x-ticks values
    yticks: Iterable
        y-ticks values

    Returns
    -------
    Figure object

    Example
    --------
    import quantpy.plots as plots
    import pandas as pd
    import numpy as np
    import matplotlib.pyplot as plt

    # Creating a simple dataframe with random reference data
    times = pd.date_range('2021-10-01', periods = 1000, freq ='60min')
    df = pd.DataFrame(np.random.lognormal(mean = 3, sigma = 0.4, size = 1000),
                      columns = ['NO2'], index = times)
    # Simulate a LCS with noise and bias
    df['LCS1'] = (df['NO2'] + np.random.normal(0,3,len(df.index)).tolist())*1.2

    plots.scatter(df, 'NO2', 'LCS1')
    plt.show()
    """
    #initialise the figure
    fig, ax = plt.subplots(1, 1,figsize = figsize, dpi = 200)

    #inputs
    x = data[ref]
    y = data[lcs]

    #masking the NaN's
    mask = ~np.isnan(x) & ~np.isnan(y)
    x = x[mask]
    y = y[mask]

    #number of data points
    n = len(x)

    # Calculate summary metrics
    slope, intercept, r, _, _ = scipy.stats.linregress(x, y)
    r2 = r*r
    rmse = mean_squared_error(y, x, squared = False)
    mae = mean_absolute_error(y, x)

    #data points density
    xy = np.vstack([x,y])
    z = scipy.stats.gaussian_kde(xy)(xy)
        
    #scatter plot LCS vs Ref
    ax.scatter(x, y, c = z, s = 14, alpha = 1, linewidth = 1)

    #fitted line
    ax.axline((0, intercept), slope=slope, color='red', linewidth=2, alpha=1,
              linestyle='--')

    #1:1 line
    ax.axline((0, 0), slope=1, color='black', linewidth=2, alpha=0.8,
              linestyle='-')

    #'x' and 'y' axis title
    ax.set_ylabel(lcs + ' $[units]}$', labelpad = 5, fontsize = 16)
    ax.set_xlabel(ref + ' $[units]}$', labelpad = 10, fontsize = 16)
        
    #'x' and 'y' ticks
    if xticks is not None:
        ax.set_xticks(xticks)
    if yticks is not None:
        ax.set_yticks(yticks)
                
    #'y' and 'x' axis limits
    if xlim is not None:
        ax.set_xlim(xlim)
    if ylim is not None:
        ax.set_ylim(ylim)

    #annotation1: regression equation & total data points 'n'
    if intercept > 0:
        annotation_string1 = f'y = {slope:.2f}x + {intercept:.2f}'
    elif intercept == 0:
        annotation_string1 = f'y = {slope:.2f}x'
    else:
        annotation_string1 = f'y = {slope:.2f}x - {-intercept:.2f}'
    annotation_string1 = annotation_string1
    annotation_string1 += "\n"
    annotation_string1 += "\n"
    annotation_string1 += r"n = %.f" % n

    #annotation2: R2, RMSE & MAE
    annotation_string2 = R"R$^\mathsf{2}$ = %.2f" % r2
    annotation_string2 += "\n"
    annotation_string2 += "\n"
    annotation_string2 += r"RMSE = %.1f" % rmse
    annotation_string2 += "\n"
    annotation_string2 += "\n"
    annotation_string2 += r"MAE = %.1f" % mae

    #position of annotation 1 & 2
    ax.annotate(annotation_string1, (0.05, 0.75), xycoords ='axes fraction', fontsize = 12)
    ax.annotate(annotation_string2, (0.75, 0.05), xycoords ='axes fraction', fontsize = 12)


def reu_plot(data,
             ref,
             lcs,
             u_xi=0,
             k=2,
             DQO=None,
             figsize=None,
             xlim=None,
             ylim=None,
             xticks=None,
             yticks=None):

    """
    Creates a REU plot of a secondary instrument (e.g. a Low-Cost Sensor, y = LCS)
    and a Reference Instrument (x = Ref).

    Parameters
    ----------
    data: pandas.DataFrame
        The dataframe containing the Reference and LCS time series
    ref: string
        Name of the column containing the reference data (e.g. 'NO2').
    lcs: string
        Name of the column containing the LCS data (e.g. 'LCS1').
    u_xi: float
        Random uncertainty for the reference method. Defaults to 0.
    k: float
        Scaling parameter. Defaults to 2.
    DQO: int or float
        Data Quality Objective (%)
    figsize: A 2 element list
         Figure dimensions (width, height) in inches
    xlim: List of 2 elements
        x-axis limits
    ylim: List of 2 elements
        y-axis limits
    xticks: Iterable
        x-ticks values
    yticks: Iterable
        y-ticks values

    Returns
    -------
    Figure object

    Example
    --------
    import quantpy.plots as plots
    import pandas as pd
    import numpy as np
    import matplotlib.pyplot as plt

    # Creating a simple dataframe with random reference data
    times = pd.date_range('2021-10-01', periods = 1000, freq ='60min')
    df = pd.DataFrame(np.random.lognormal(mean = 3, sigma = 0.4, size = 1000),
                      columns = ['NO2'], index = times)
    # Simulate a LCS with noise and bias
    df['LCS1'] = (df['NO2'] + np.random.normal(0,3,len(df.index)).tolist())*1.2

    plots.reu_plot(df, "NO2", "LCS1", DQO = 25, ylim=[0, 200])
    plt.show()
    """
    #initialise the figure
    fig, ax = plt.subplots(1, 1,figsize = figsize, dpi= 200)

    #inputs
    reu_vals = reu(data[ref], data[lcs], u_xi=u_xi, k=k)
    x = data[ref]
    y = reu_vals

    #masking the NaN's
    mask = ~np.isnan(x) & ~np.isnan(y)
    x = x[mask]
    y = y[mask]

    #data points density
    xy = np.vstack([x,y])
    z = scipy.stats.gaussian_kde(xy)(xy)
        
    #scatter plot REU vs Ref
    ax.scatter(x, y, c=z, s=14, alpha=1, linewidth=1)

    #add DQO line
    if DQO is not None:
        ax.axline((0, DQO), slope=0, color='darkgreen', linewidth=2, alpha=0.8, linestyle = '-')

    ##'x' and 'y' axis title
    ax.set_ylabel('REU %', labelpad = 5, fontsize = 16)
    ax.set_xlabel(ref + ' $[units]}$', labelpad = 10, fontsize = 16)

    #'x' and 'y' ticks
    if xticks is not None:
        ax.set_xticks(xticks)
    if yticks is not None:
        ax.set_yticks(yticks)

    #'x' and 'y' axis limits
    if xlim is not None:
        ax.set_xlim(xlim)
    if ylim is not None:
        ax.set_ylim(ylim)

    #Anotacion Data Quality Objective (DQO)
    annotation_string = r"DQO = %.f" % DQO
    annotation_string += r"%"
    ax.annotate(annotation_string, xy = (0.67 * np.max(x), DQO + 3), xycoords = 'data',fontsize = 12)


def time_series(data,
                ref,
                lcs,
                color="red",
                figsize=None,
                xlim=None,
                ylim=None
               ):

    """
    Creates a time series plot of a secondary instrument (e.g. a Low-Cost Sensor, y = LCS)
    and a Reference Instrument (x = Ref).

    Parameters
    ----------
    data: pandas.DataFrame
        The dataframe containing the Reference and LCS time series
    ref: string
        Name of the column containing the reference data (e.g. 'NO2').
    lcs: string
        Name of the column containing the LCS data (e.g. 'LCS1').
    color: string
        Colour of the line for the secondary measurement.
    figsize: A 2 element list
         Figure dimensions (width, height) in inches
    xlim: List of 2 elements
        x-axis limits
    ylim: List of 2 elements
        y-axis limits

    Returns
    -------
    Figure object

    Example
    --------
    import quantpy.plots as plots
    import pandas as pd
    import numpy as np
    import matplotlib.pyplot as plt

    # Creating a simple dataframe with random reference data
    times = pd.date_range('2021-10-01', periods = 1000, freq ='60min')
    df = pd.DataFrame(np.random.lognormal(mean = 3, sigma = 0.4, size = 1000),
                      columns = ['NO2'], index = times)
    # Simulate a LCS with noise and bias
    df['LCS1'] = (df['NO2'] + np.random.normal(0,3,len(df.index)).tolist())*1.2

    plots.time_series(df, 'NO2', 'LCS1')
    plt.show()
    """
    #initialise the figure
    fig, ax = plt.subplots(1, 1,figsize = figsize, dpi = 200)

    #Inputs
    x = data.index
    y1 = data[ref]
    y2 = data[lcs]

    #Reference line plot
    ax.plot(x, y1, lw = 1, alpha = 1,  color = 'black')

    #LCS line plot
    ax.plot(x, y2, lw = 1, alpha = 0.5,  color = color)

    #'y' axis limits
    if xlim is not None:
        ax.set_xlim(xlim)
    if ylim is not None:
        ax.set_ylim(ylim)

    #'x' and 'y' axis title
    ax.set_ylabel(ref + ' $[units]}$', labelpad = 5, fontsize = 16)

    #Legends
    legend = [ref, lcs]
    ax.legend(legend, frameon = False, markerfirst = False, fontsize = 14)

    #date format 'x' axis
    x_axis_format = mdates.DateFormatter('%m-%y')
    ax.xaxis.set_major_formatter(x_axis_format)
    ax.xaxis.set_major_locator(ticker.AutoLocator())
    ax.xaxis.set_minor_locator(ticker.AutoMinorLocator())
