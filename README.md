[![DOI](https://zenodo.org/badge/485404967.svg)](https://zenodo.org/badge/latestdoi/485404967)

# Air pollution measurement errors: Is your data fit for purpose?

This repository contains Python and R code for reproducing the diagnostic plots shown in _Air pollution measurement errors: Is your data fit for purpose?_ (Diez et al, 2022) published in Atmospheric Measurement Techniques ([https://doi.org/10.5194/amt-15-4091-2022](https://doi.org/10.5194/amt-15-4091-2022)).

## Python package

To install the Python package, run `pip install git+https://github.com/wacl-york/quant-measurement-errors-tools#subdirectory=quantpy`.

The `quantpy.plots` module contains functions to reproduce all 4 of the main plots in the functions: `time_series`, `scatter`, `bland_altman`, `reu_plot`.
These can be used as follows:

```python
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

plots.scatter(df, 'NO2', 'LCS1')

plots.reu_plot(df, "NO2", "LCS1", DQO = 25, ylim=[0, 200])

plots.time_series(df, 'NO2', 'LCS1')
```

See the accompanying documentation for further support (i.e. `help(plots.bland_altman)`).
Furthermore, the `quantpy.reu` module contains the function `reu` to calculate the REU.

## R package

To install the R code, run `devtools::install_github("wacl-york/quant-measurement-errors-tools/quantr")` to install the `quantr` package.
This package contains functions to reproduce all 4 of the main plots in the functions: `plot_time_series`, `plot_scatter`, `plot_bland_altman`, `plot_reu`.

These can be used as follows:

```r
library(quantr)

# Create dummy data frame
n_vals <- 100
df <- data.frame(timestamp=seq.POSIXt(from=as.POSIXct("2020-09-24 09:00:00"),
                                      to=as.POSIXct("2020-09-30 09:00:00"),
                                      length.out=n_vals),
                 ref=rnorm(n_vals, 30, 5),
                 lowcost=rnorm(n_vals, 32, 8))

plot_reu(df, lcs_column="lowcost", reference_column="ref", y_limits=NULL)

plot_scatter(df, lcs_column="lowcost", reference_column="ref")

plot_bland_altman(df, lcs_column="lowcost", reference_column="ref")

plot_time_series(df, lcs_column="lowcost", reference_column="ref")
```

See the accompanying help pages (e.g. `?plot_reu`) for further details.

## Real world data

The real world air quality measurements that were used to generate some of the figures in the paper are available in the `data` sub-folder.
See the README in that directory for details on the data structure.
