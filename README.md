# Macroeconomic Determinants of US Housing Starts (1987–2024)
Academic project — École des Ponts ParisTech, SIA 2025-2026

## Research question
Which macroeconomic factors explain the monthly variation in US housing starts between 1987 and 2024?

This project examines the housing market model proposed by DiPasquale & Wheaton (1996), which explains housing activity through demand factors (household income, employment stability) and supply factors (construction costs, credit availability).

## Project structure
## Installation

1. Clone the repository
2. Create and activate the conda environment
3. Launch the notebook
## Run tests
## Methodology
- **Data collection** — 445 monthly observations from January 1987 to January 2024 via FRED
- **Variable construction** — Log-transformed variables (l_housing_starts, l_real_price, l_income, l_real_cost); level variables kept in percentage points (mortgage_rate, unemployment)
- **Exploratory analysis** — Time-series plots with GFC (2008–09) and COVID-19 (2020) shading; scatter matrices for bivariate relationships
- **Regression** — OLS with HC3 heteroscedasticity-robust standard errors; mixed log-level specification for elasticity interpretation

## Limitations
- **Endogeneity**: housing starts affect house prices (more supply lowers prices), so OLS estimates for real_price are likely biased. An instrumental-variables approach would be needed.
- **Serial autocorrelation**: monthly time-series data tends to be autocorrelated.
- **Structural breaks**: the 2008 financial crisis and the 2020 pandemic represent large regime changes.

## Citation
DiPasquale, D., & Wheaton, W. C. (1996). Urban Economics and Real Estate Markets. Prentice Hall.

Federal Reserve Bank of St. Louis. (2024). Federal Reserve Economic Data (FRED). Retrieved from https://fred.stlouisfed.org
