## Visually evaluating air quality low-cost-sensors

This repository contains Python and R code for reproducing the diagnostic plots shown in <PAPER REFERENCE>.

## Python package

TODO

## R package

To install the R code, run `devtools::install_github("wacl-york/quant-measurement-errors-tools/quantr")` to install the `quantr` package.
This package contains functions to reproduce all 4 of the main plots in the functions: `plot_time_series`, `plot_scatter`, `plot_bland_altman`, `plot_reu`.

These can be used as follows:

```r
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

plot_bland_altman(df, lcs_column="lowcost", reference_column="ref")
```

See the accompanying help pages (e.g. `?plot_reu`) for further details.
