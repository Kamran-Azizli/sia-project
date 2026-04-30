
from pathlib import Path
import pandas as pd
import statsmodels.api as sm
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import seaborn as sns

sns.set_theme(style="whitegrid", palette="muted")

_REQUIRED_COLUMNS = [
    "date", "housing_starts", "real_price", "mortgage_rate",
    "unemployment", "income", "real_cost",
    "l_housing_starts", "l_real_price", "l_income", "l_real_cost",
]

DEFAULT_PREDICTORS = [
    "l_real_price", "mortgage_rate", "unemployment", "l_income", "l_real_cost",
]

def load_and_prepare(csv_path):
    """Load the housing-market CSV and return a clean, typed DataFrame.
    Parameters
    ----------
    csv_path : str or Path
    Returns
    -------
    pd.DataFrame indexed by date, all columns as float64
    """
    csv_path = Path(csv_path)
    if not csv_path.exists():
        raise FileNotFoundError(f"Data file not found: {csv_path}")
    df = pd.read_csv(csv_path, parse_dates=["date"])
    missing = [c for c in _REQUIRED_COLUMNS if c not in df.columns]
    if missing:
        raise ValueError(f"Missing columns: {missing}")
    df = df.set_index("date").sort_index()
    return df.astype(float)

def run_ols(df, outcome="l_housing_starts", predictors=None):
    """Fit OLS regression with HC3 robust standard errors.
    Parameters
    ----------
    df : pd.DataFrame
    outcome : str
    predictors : list[str] or None
    Returns
    -------
    RegressionResultsWrapper
    """
    if predictors is None:
        predictors = DEFAULT_PREDICTORS
    missing = [c for c in [outcome] + predictors if c not in df.columns]
    if missing:
        raise ValueError(f"Missing columns: {missing}")
    X = sm.add_constant(df[predictors])
    y = df[outcome]
    # HC3 robust SEs preferred over homoscedastic default for macro time series
    return sm.OLS(y, X).fit(cov_type="HC3")

def plot_time_series(df, columns, title="Housing Market Variables Over Time", figsize=(14, 8)):
    """Plot time-series columns as stacked subplots with recession shading.
    Parameters
    ----------
    df : pd.DataFrame (DatetimeIndex)
    columns : list[str]
    title : str
    figsize : tuple[int, int]
    Returns
    -------
    plt.Figure
    """
    n = len(columns)
    fig, axes = plt.subplots(n, 1, figsize=figsize, sharex=True)
    if n == 1:
        axes = [axes]
    labels = {
        "housing_starts":   "Housing Starts (thousands)",
        "mortgage_rate":    "Mortgage Rate (%)",
        "unemployment":     "Unemployment Rate (%)",
        "l_housing_starts": "Log Housing Starts",
        "l_real_price":     "Log Real House Price",
        "l_income":         "Log Real Income",
        "l_real_cost":      "Log Real Construction Cost",
    }
    for ax, col in zip(axes, columns):
        ax.plot(df.index, df[col], linewidth=1.2)
        ax.set_ylabel(labels.get(col, col), fontsize=10)
        ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y"))
        ax.xaxis.set_major_locator(mdates.YearLocator(5))
        ax.axvspan(pd.Timestamp("2007-12-01"), pd.Timestamp("2009-06-01"),
                   alpha=0.15, color="red", label="GFC (2008-09)")
        ax.axvspan(pd.Timestamp("2020-02-01"), pd.Timestamp("2020-06-01"),
                   alpha=0.15, color="orange", label="COVID (2020)")
    axes[0].legend(fontsize=8, loc="upper right")
    axes[-1].set_xlabel("Date", fontsize=11)
    fig.suptitle(title, fontsize=14, fontweight="bold", y=1.01)
    fig.tight_layout()
    return fig

def plot_scatter_matrix(df, predictors, outcome="l_housing_starts", figsize=(14, 4)):
    """Plot each predictor against the outcome variable side by side.
    Parameters
    ----------
    df : pd.DataFrame
    predictors : list[str]
    outcome : str
    figsize : tuple[int, int]
    Returns
    -------
    plt.Figure
    """
    n = len(predictors)
    fig, axes = plt.subplots(1, n, figsize=figsize, sharey=True)
    pretty = {
        "l_real_price":  "Log Real Price",
        "mortgage_rate": "Mortgage Rate (%)",
        "unemployment":  "Unemployment (%)",
        "l_income":      "Log Real Income",
        "l_real_cost":   "Log Real Cost",
    }
    for ax, pred in zip(axes, predictors):
        ax.scatter(df[pred], df[outcome], alpha=0.3, s=10, color="steelblue")
        ax.set_xlabel(pretty.get(pred, pred), fontsize=10)
    axes[0].set_ylabel("Log Housing Starts", fontsize=10)
    fig.suptitle("Log Housing Starts vs. Key Predictors (1987-2024)",
                 fontsize=13, fontweight="bold")
    fig.tight_layout()
    return fig

def plot_residuals(fitted_values, residuals, figsize=(12, 4)):
    """Plot residuals vs fitted values and a residual histogram.
    Parameters
    ----------
    fitted_values : pd.Series
    residuals : pd.Series
    figsize : tuple[int, int]
    Returns
    -------
    plt.Figure
    """
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=figsize)
    ax1.scatter(fitted_values, residuals, alpha=0.3, s=10, color="steelblue")
    ax1.axhline(0, color="red", linewidth=1, linestyle="--")
    ax1.set_xlabel("Fitted Values", fontsize=10)
    ax1.set_ylabel("Residuals", fontsize=10)
    ax1.set_title("Residuals vs. Fitted", fontsize=11)
    ax2.hist(residuals, bins=40, color="steelblue", edgecolor="white", alpha=0.8)
    ax2.set_xlabel("Residual", fontsize=10)
    ax2.set_ylabel("Frequency", fontsize=10)
    ax2.set_title("Residual Distribution", fontsize=11)
    fig.suptitle("OLS Regression Diagnostics", fontsize=13, fontweight="bold")
    fig.tight_layout()
    return fig
