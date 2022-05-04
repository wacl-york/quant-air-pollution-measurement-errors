## Real world data plotted in the paper

This folder contains the data used to generate the figures based on real-world observations from low cost sensors (LCS).
It is organised with one folder per Figure, each containing relevant CSV files, with this document providing documentation for the fields available in the files.
All units are in ppb unless stated otherwise.

## Figure 5 

  - Columns:
    - `Timestamp` Date-time of measurement in YYYY-mm-ddTHH:MM:SS format in UTC
    - `NO2` Reference data as measured by a Teledyne T500U
    - `O3` Reference data as measured by a Thermo 49i
    - `LCS1` NO2 as recorded by a LCS
    - `LCS2` O3 as recorded by a LCS
  - These measurements were recorded in the same period (2021-07-17 to 2022-02-17) and in the same site (Manchester)

## Figure 6 

### Panels a & c 

  - Columns:
    - `Timestamp` Date-time of measurement in YYYY-mm-ddTHH:MM:SS format in UTC
    - `PM2.5_Fidas200` Reference PM2.5 in Manchester as measured by a Fidas200
    - `LCS3` PM2.5 in Manchester as measured by a LCS
    - `PM2.5_BAM1020` Reference PM2.5 in Manchster as measured by a BAM1020
    - `LCS4` PM2.5 in York as measured by a LCS
  - These measurements were recorded in the same period (2020-04-01 to 2020-05-31) in two different sites (Manchester & York)
  - All measurements are in ug/m3

### Panel b 

  - Columns:
    - `Timestamp` Date-time of measurement in YYYY-mm-ddTHH:MM:SS format in UTC
    - `PM2.5_Fidas200` Reference PM2.5 in Manchester as measured by a Fidas200
    - `LCS3` PM2.5 in Manchester as measured by a LCS, the same LCS used in panels a and c
  - These measurements were recorded in the period 2020-10-01 to 2020-11-29
  - All measurements are in ug/m3

## Figure 7 

### Panel a

  - Columns:
    - `Timestamp` Date-time of measurement in YYYY-mm-ddTHH:MM:SS format in UTC
    - `NO2_T500U` Reference data as measured by a Teledyne T500U
    - `NO2_T200U(a)` Reference data as measured by a Teledyne T200U
  - These measurements were recorded in Manchester in the period 2020-10-14 to 2020-12-14

### Panel b

  - Columns:
    - `Timestamp` Date-time of measurement in YYYY-mm-ddTHH:MM:SS format in UTC
    - `NO2_T500U` Reference data as measured by a Teledyne T500U
    - `NO2_T200U(b)` Reference data as measured by a Teledyne T200U
  - These measurements were recorded in Manchester in the period 2021-07-01 to 2021-08-31

## Figure S2

### Panels a & c 

  - Columns:
    - `Timestamp` Date-time of measurement in YYYY-mm-ddTHH:MM:SS format in UTC
    - `PM2.5_Fidas200` Reference PM2.5 in Manchester as measured by a Fidas200
    - `LCS3*` PM2.5 in Manchester as measured by a LCS and corrected for bias
    - `PM2.5_BAM1020` Reference PM2.5 in Manchster as measured by a BAM1020
    - `LCS4*` PM2.5 in York as measured by a LCS and corrected for bias
  - These measurements were recorded in the same period (2020-04-01 to 2020-05-31) in two different sites (Manchester & York)
  - All measurements are in ug/m3
  - This plot is identical to Figure 6 (a & c), but with the sensors having a linear bias-correction applied

### Panel b 

  - Columns:
    - `Timestamp` Date-time of measurement in YYYY-mm-ddTHH:MM:SS format in UTC
    - `PM2.5_Fidas200` Reference PM2.5 in Manchester as measured by a Fidas200
    - `LCS3*` PM2.5 in Manchester as measured by a LCS and corrected for bias, the same LCS used in panels a and c
  - These measurements were recorded in the period 2020-10-01 to 2020-11-29
  - All measurements are in ug/m3
  - This plot is identical to Figure 6b, but with the sensor having a linear bias-correction applied

## Figure S3 

### Panel a

  - Columns:
    - `Timestamp` Date-time of measurement in YYYY-mm-ddTHH:MM:SS format in UTC
    - `O3_49i` Reference O3 as measured by a Thermo 49i
    - `49i` Reference O3 as measured by a secondary Thermo 49i
  - These measurements were recorded in Manchester in the period from 2021-07-01 to 2021-08-31

### Panel b

  - Columns:
    - `Timestamp` Date-time of measurement in YYYY-mm-ddTHH:MM:SS format in UTC
    - `O3_49i` Reference O3 as measured by a Thermo 49i
    - `2B` Reference O3 as measured by a 2B
  - These measurements were recorded in Manchester in the period from 2021-06-15 to 2021-09-07

