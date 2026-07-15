"""
=========================================================
Live Stock Analysis & Prediction
src/data_loader.py
Version : 2.0
Part 1
Python  : 3.12
=========================================================
"""

from __future__ import annotations

import logging
from pathlib import Path
from datetime import datetime
from typing import Any

import pandas as pd
import streamlit as st
import yfinance as yf

# ==========================================================
# LOGGING
# ==========================================================

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
)

logger = logging.getLogger(__name__)

# ==========================================================
# CONSTANTS
# ==========================================================

VERSION = "2.0"

DEFAULT_PERIOD = "1y"
DEFAULT_INTERVAL = "1d"

VALID_PERIODS = (
    "1d",
    "5d",
    "1mo",
    "3mo",
    "6mo",
    "1y",
    "2y",
    "5y",
    "10y",
    "max",
)

VALID_INTERVALS = (
    "1m",
    "2m",
    "5m",
    "15m",
    "30m",
    "60m",
    "90m",
    "1h",
    "1d",
    "5d",
    "1wk",
    "1mo",
    "3mo",
)

REQUIRED_COLUMNS = [
    "Open",
    "High",
    "Low",
    "Close",
    "Volume",
]

# ==========================================================
# EXCEPTIONS
# ==========================================================

class DataLoaderError(Exception):
    """Base exception."""


class InvalidTickerError(DataLoaderError):
    """Invalid ticker."""


class DownloadError(DataLoaderError):
    """Download failed."""


# ==========================================================
# VALIDATION
# ==========================================================

def validate_ticker(
    ticker: str,
) -> str:
    """
    Validate stock ticker.
    """

    if not isinstance(ticker, str):
        raise InvalidTickerError(
            "Ticker must be string."
        )

    ticker = ticker.strip().upper()

    if ticker == "":
        raise InvalidTickerError(
            "Ticker cannot be empty."
        )

    return ticker


def validate_period(
    period: str,
) -> str:
    """
    Validate period.
    """

    if period not in VALID_PERIODS:
        return DEFAULT_PERIOD

    return period


def validate_interval(
    interval: str,
) -> str:
    """
    Validate interval.
    """

    if interval not in VALID_INTERVALS:
        return DEFAULT_INTERVAL

    return interval


# ==========================================================
# DATAFRAME UTILITIES
# ==========================================================

def validate_dataframe(
    df: pd.DataFrame,
) -> bool:
    """
    Validate downloaded dataframe.
    """

    if df is None:
        return False

    if df.empty:
        return False

    for column in REQUIRED_COLUMNS:

        if column not in df.columns:
            return False

    return True


def clean_dataframe(
    df: pd.DataFrame,
) -> pd.DataFrame:
    """
    Clean stock dataframe.
    """

    if df.empty:
        return df

    df = df.copy()

    df.drop_duplicates(inplace=True)

    df.sort_index(inplace=True)

    df.ffill(inplace=True)

    df.bfill(inplace=True)

    return df


# ==========================================================
# MAIN DATA LOADER
# ==========================================================

@st.cache_data(show_spinner=False)
def load_stock_data(
    ticker: str,
    period: str = DEFAULT_PERIOD,
    interval: str = DEFAULT_INTERVAL,
    auto_adjust: bool = True,
) -> pd.DataFrame:
    """
    Download stock data.
    """

    ticker = validate_ticker(ticker)

    period = validate_period(period)

    interval = validate_interval(interval)

    try:

        logger.info(
            "Downloading %s",
            ticker,
        )

        df = yf.download(
            ticker,
            period=period,
            interval=interval,
            auto_adjust=auto_adjust,
            progress=False,
            threads=True,
        )

        if not validate_dataframe(df):

            raise DownloadError(
                f"No data found for {ticker}"
            )

        df = clean_dataframe(df)

        logger.info(
            "%s rows downloaded.",
            len(df),
        )

        return df

    except Exception as error:

        logger.exception(error)

        raise DownloadError(
            str(error)
        ) from error

# ==========================================================
# END OF PART 1
# ==========================================================

# ==========================================================
# COMPANY INFORMATION
# ==========================================================

@st.cache_data(show_spinner=False)
def get_company_info(
    ticker: str,
) -> dict[str, Any]:
    """
    Get company information.
    """

    ticker = validate_ticker(ticker)

    try:

        stock = yf.Ticker(ticker)

        info = stock.info

        if not info:
            return {}

        return info

    except Exception as error:

        logger.exception(error)

        return {}


# ==========================================================
# HISTORICAL DATA
# ==========================================================

@st.cache_data(show_spinner=False)
def load_historical_data(
    ticker: str,
    start: str | datetime,
    end: str | datetime,
    interval: str = "1d",
) -> pd.DataFrame:
    """
    Download historical stock data.
    """

    ticker = validate_ticker(ticker)

    interval = validate_interval(interval)

    try:

        df = yf.download(
            ticker,
            start=start,
            end=end,
            interval=interval,
            auto_adjust=True,
            progress=False,
        )

        if validate_dataframe(df):

            return clean_dataframe(df)

        return pd.DataFrame()

    except Exception as error:

        logger.exception(error)

        return pd.DataFrame()


# ==========================================================
# MULTIPLE STOCKS
# ==========================================================

@st.cache_data(show_spinner=False)
def load_multiple_stocks(
    tickers: list[str],
    period: str = DEFAULT_PERIOD,
    interval: str = DEFAULT_INTERVAL,
) -> dict[str, pd.DataFrame]:
    """
    Download multiple stocks.
    """

    datasets: dict[str, pd.DataFrame] = {}

    for ticker in tickers:

        try:

            datasets[ticker] = load_stock_data(
                ticker=ticker,
                period=period,
                interval=interval,
            )

        except Exception:

            datasets[ticker] = pd.DataFrame()

    return datasets


# ==========================================================
# SAVE DATA
# ==========================================================

def save_to_csv(
    dataframe: pd.DataFrame,
    file_path: str | Path,
) -> bool:
    """
    Save dataframe to CSV.
    """

    try:

        file_path = Path(file_path)

        file_path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        dataframe.to_csv(file_path)

        return True

    except Exception as error:

        logger.exception(error)

        return False


# ==========================================================
# LOAD CSV
# ==========================================================

def load_from_csv(
    file_path: str | Path,
) -> pd.DataFrame:
    """
    Load dataframe from CSV.
    """

    try:

        dataframe = pd.read_csv(
            file_path,
            parse_dates=True,
            index_col=0,
        )

        return clean_dataframe(dataframe)

    except Exception as error:

        logger.exception(error)

        return pd.DataFrame()


# ==========================================================
# DATE FILTER
# ==========================================================

def filter_by_date(
    dataframe: pd.DataFrame,
    start_date: str | datetime,
    end_date: str | datetime,
) -> pd.DataFrame:
    """
    Filter dataframe by date.
    """

    try:

        return dataframe.loc[
            str(start_date):str(end_date)
        ].copy()

    except Exception as error:

        logger.exception(error)

        return pd.DataFrame()


# ==========================================================
# DATA SUMMARY
# ==========================================================

def data_summary(
    dataframe: pd.DataFrame,
) -> dict[str, Any]:
    """
    Return dataset summary.
    """

    if dataframe.empty:

        return {}

    return {

        "rows": len(dataframe),

        "columns": len(dataframe.columns),

        "start_date": str(dataframe.index.min()),

        "end_date": str(dataframe.index.max()),

        "missing_values": int(
            dataframe.isna().sum().sum()
        ),

        "duplicate_rows": int(
            dataframe.duplicated().sum()
        ),

    }

# ==========================================================
# END OF PART 2
# ==========================================================

# ==========================================================
# MARKET INDEX DATA
# ==========================================================

@st.cache_data(show_spinner=False)
def load_market_index(
    symbol: str = "^NSEI",
    period: str = DEFAULT_PERIOD,
) -> pd.DataFrame:
    """
    Download market index data.
    """

    try:

        dataframe = yf.download(
            symbol,
            period=period,
            auto_adjust=True,
            progress=False,
        )

        if validate_dataframe(dataframe):
            return clean_dataframe(dataframe)

        return pd.DataFrame()

    except Exception as error:

        logger.exception(error)

        return pd.DataFrame()


# ==========================================================
# LATEST STOCK PRICE
# ==========================================================

@st.cache_data(show_spinner=False)
def get_latest_price(
    ticker: str,
) -> float:
    """
    Return latest closing price.
    """

    try:

        dataframe = load_stock_data(
            ticker=ticker,
            period="5d",
        )

        if dataframe.empty:
            return 0.0

        return float(
            dataframe["Close"].iloc[-1]
        )

    except Exception as error:

        logger.exception(error)

        return 0.0


# ==========================================================
# DOWNLOAD METADATA
# ==========================================================

def download_metadata(
    dataframe: pd.DataFrame,
) -> dict[str, Any]:
    """
    Generate metadata for downloaded data.
    """

    try:

        return {

            "rows": len(dataframe),

            "columns": list(dataframe.columns),

            "start_date": dataframe.index.min(),

            "end_date": dataframe.index.max(),

            "created_at": datetime.now(),

        }

    except Exception:

        return {}


# ==========================================================
# PRICE STATISTICS
# ==========================================================

def price_statistics(
    dataframe: pd.DataFrame,
) -> dict[str, float]:
    """
    Calculate basic price statistics.
    """

    try:

        return {

            "open": float(dataframe["Open"].iloc[-1]),

            "high": float(dataframe["High"].max()),

            "low": float(dataframe["Low"].min()),

            "close": float(dataframe["Close"].iloc[-1]),

            "average_close": float(
                dataframe["Close"].mean()
            ),

            "average_volume": float(
                dataframe["Volume"].mean()
            ),

            "highest_volume": float(
                dataframe["Volume"].max()
            ),

        }

    except Exception as error:

        logger.exception(error)

        return {}


# ==========================================================
# DATA SPLIT
# ==========================================================

def split_train_test(
    dataframe: pd.DataFrame,
    train_size: float = 0.8,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """
    Split dataframe into train and test datasets.
    """

    try:

        split_index = int(
            len(dataframe) * train_size
        )

        train = dataframe.iloc[:split_index].copy()

        test = dataframe.iloc[split_index:].copy()

        return train, test

    except Exception as error:

        logger.exception(error)

        return (
            pd.DataFrame(),
            pd.DataFrame(),
        )


# ==========================================================
# NUMERIC COLUMNS
# ==========================================================

def numeric_columns(
    dataframe: pd.DataFrame,
) -> list[str]:
    """
    Return numeric columns.
    """

    try:

        return list(

            dataframe.select_dtypes(
                include="number"
            ).columns

        )

    except Exception:

        return []


# ==========================================================
# REMOVE MISSING VALUES
# ==========================================================

def remove_missing_values(
    dataframe: pd.DataFrame,
) -> pd.DataFrame:
    """
    Remove rows containing missing values.
    """

    try:

        return dataframe.dropna().copy()

    except Exception as error:

        logger.exception(error)

        return dataframe


# ==========================================================
# RESET INDEX
# ==========================================================

def reset_dataframe_index(
    dataframe: pd.DataFrame,
) -> pd.DataFrame:
    """
    Reset dataframe index.
    """

    try:

        return dataframe.reset_index(
            drop=False
        )

    except Exception as error:

        logger.exception(error)

        return dataframe

# ==========================================================
# END OF PART 3
# ==========================================================

# ==========================================================
# DATA CLEANING UTILITIES
# ==========================================================

def remove_duplicate_rows(
    dataframe: pd.DataFrame,
) -> pd.DataFrame:
    """
    Remove duplicate rows.
    """

    try:

        return dataframe.drop_duplicates().copy()

    except Exception as error:

        logger.exception(error)

        return dataframe


def fill_missing_values(
    dataframe: pd.DataFrame,
    method: str = "ffill",
) -> pd.DataFrame:
    """
    Fill missing values.
    """

    try:

        df = dataframe.copy()

        if method == "ffill":
            df.ffill(inplace=True)

        elif method == "bfill":
            df.bfill(inplace=True)

        else:
            df.fillna(0, inplace=True)

        return df

    except Exception as error:

        logger.exception(error)

        return dataframe


def sort_by_date(
    dataframe: pd.DataFrame,
    ascending: bool = True,
) -> pd.DataFrame:
    """
    Sort dataframe by index.
    """

    try:

        return dataframe.sort_index(
            ascending=ascending
        )

    except Exception as error:

        logger.exception(error)

        return dataframe


# ==========================================================
# STOCK PRICE UTILITIES
# ==========================================================

def latest_row(
    dataframe: pd.DataFrame,
) -> pd.Series:
    """
    Return latest row.
    """

    try:

        return dataframe.iloc[-1]

    except Exception:

        return pd.Series(dtype="object")


def latest_close(
    dataframe: pd.DataFrame,
) -> float:
    """
    Latest closing price.
    """

    try:

        return float(
            dataframe["Close"].iloc[-1]
        )

    except Exception:

        return 0.0


def latest_open(
    dataframe: pd.DataFrame,
) -> float:
    """
    Latest opening price.
    """

    try:

        return float(
            dataframe["Open"].iloc[-1]
        )

    except Exception:

        return 0.0


def latest_high(
    dataframe: pd.DataFrame,
) -> float:
    """
    Latest high price.
    """

    try:

        return float(
            dataframe["High"].iloc[-1]
        )

    except Exception:

        return 0.0


def latest_low(
    dataframe: pd.DataFrame,
) -> float:
    """
    Latest low price.
    """

    try:

        return float(
            dataframe["Low"].iloc[-1]
        )

    except Exception:

        return 0.0


def latest_volume(
    dataframe: pd.DataFrame,
) -> int:
    """
    Latest trading volume.
    """

    try:

        return int(
            dataframe["Volume"].iloc[-1]
        )

    except Exception:

        return 0


# ==========================================================
# DATE UTILITIES
# ==========================================================

def available_date_range(
    dataframe: pd.DataFrame,
) -> tuple[Any, Any]:
    """
    Return available date range.
    """

    try:

        return (
            dataframe.index.min(),
            dataframe.index.max(),
        )

    except Exception:

        return None, None


def trading_days(
    dataframe: pd.DataFrame,
) -> int:
    """
    Number of trading days.
    """

    try:

        return len(dataframe)

    except Exception:

        return 0


# ==========================================================
# CACHE UTILITIES
# ==========================================================

def clear_streamlit_cache() -> bool:
    """
    Clear Streamlit cache.
    """

    try:

        st.cache_data.clear()

        return True

    except Exception as error:

        logger.exception(error)

        return False


# ==========================================================
# FILE UTILITIES
# ==========================================================

def file_exists(
    file_path: str | Path,
) -> bool:
    """
    Check whether a file exists.
    """

    try:

        return Path(file_path).exists()

    except Exception:

        return False


# ==========================================================
# END OF PART 4
# ==========================================================

# ==========================================================
# DATA TRANSFORMATION UTILITIES
# ==========================================================

def rename_columns(
    dataframe: pd.DataFrame,
    columns: dict[str, str],
) -> pd.DataFrame:
    """
    Rename dataframe columns.
    """

    try:

        return dataframe.rename(
            columns=columns
        )

    except Exception as error:

        logger.exception(error)

        return dataframe


def select_columns(
    dataframe: pd.DataFrame,
    columns: list[str],
) -> pd.DataFrame:
    """
    Select dataframe columns.
    """

    try:

        available = [
            column
            for column in columns
            if column in dataframe.columns
        ]

        return dataframe[available].copy()

    except Exception as error:

        logger.exception(error)

        return pd.DataFrame()


def remove_columns(
    dataframe: pd.DataFrame,
    columns: list[str],
) -> pd.DataFrame:
    """
    Remove dataframe columns.
    """

    try:

        return dataframe.drop(
            columns=columns,
            errors="ignore",
        )

    except Exception as error:

        logger.exception(error)

        return dataframe


def dataframe_memory_usage(
    dataframe: pd.DataFrame,
) -> float:
    """
    Return dataframe memory usage in MB.
    """

    try:

        memory = dataframe.memory_usage(
            deep=True
        ).sum()

        return round(
            memory / (1024 ** 2),
            2,
        )

    except Exception:

        return 0.0


# ==========================================================
# RETURN CALCULATIONS
# ==========================================================

def daily_returns(
    dataframe: pd.DataFrame,
) -> pd.Series:
    """
    Calculate daily returns.
    """

    try:

        return (
            dataframe["Close"]
            .pct_change()
            .fillna(0)
        )

    except Exception as error:

        logger.exception(error)

        return pd.Series(dtype=float)


def cumulative_returns(
    dataframe: pd.DataFrame,
) -> pd.Series:
    """
    Calculate cumulative returns.
    """

    try:

        returns = daily_returns(dataframe)

        return (
            (1 + returns)
            .cumprod()
            - 1
        )

    except Exception as error:

        logger.exception(error)

        return pd.Series(dtype=float)


def volatility(
    dataframe: pd.DataFrame,
    window: int = 20,
) -> pd.Series:
    """
    Rolling volatility.
    """

    try:

        returns = daily_returns(dataframe)

        return (
            returns
            .rolling(window)
            .std()
        )

    except Exception as error:

        logger.exception(error)

        return pd.Series(dtype=float)


# ==========================================================
# MERGE UTILITIES
# ==========================================================

def merge_dataframes(
    left: pd.DataFrame,
    right: pd.DataFrame,
    how: str = "inner",
) -> pd.DataFrame:
    """
    Merge two dataframes by index.
    """

    try:

        return left.merge(
            right,
            left_index=True,
            right_index=True,
            how=how,
        )

    except Exception as error:

        logger.exception(error)

        return pd.DataFrame()


# ==========================================================
# EXPORT UTILITIES
# ==========================================================

def export_excel(
    dataframe: pd.DataFrame,
    file_path: str | Path,
) -> bool:
    """
    Export dataframe to Excel.
    """

    try:

        dataframe.to_excel(
            file_path,
            index=True,
        )

        return True

    except Exception as error:

        logger.exception(error)

        return False


def export_json(
    dataframe: pd.DataFrame,
    file_path: str | Path,
) -> bool:
    """
    Export dataframe to JSON.
    """

    try:

        dataframe.to_json(
            file_path,
            orient="records",
            indent=4,
        )

        return True

    except Exception as error:

        logger.exception(error)

        return False

# ==========================================================
# END OF PART 5
# ==========================================================

# ==========================================================
# RESAMPLING UTILITIES
# ==========================================================

def resample_data(
    dataframe: pd.DataFrame,
    frequency: str = "W",
) -> pd.DataFrame:
    """
    Resample OHLCV data.
    """

    try:

        if dataframe.empty:
            return dataframe.copy()

        result = dataframe.resample(frequency).agg(
            {
                "Open": "first",
                "High": "max",
                "Low": "min",
                "Close": "last",
                "Volume": "sum",
            }
        )

        return result.dropna()

    except Exception as error:

        logger.exception(error)

        return pd.DataFrame()


# ==========================================================
# COLUMN UTILITIES
# ==========================================================

def add_column(
    dataframe: pd.DataFrame,
    column_name: str,
    values: Any,
) -> pd.DataFrame:
    """
    Add a new column.
    """

    try:

        df = dataframe.copy()

        df[column_name] = values

        return df

    except Exception as error:

        logger.exception(error)

        return dataframe


def remove_constant_columns(
    dataframe: pd.DataFrame,
) -> pd.DataFrame:
    """
    Remove constant columns.
    """

    try:

        return dataframe.loc[
            :,
            dataframe.nunique(dropna=False) > 1
        ]

    except Exception as error:

        logger.exception(error)

        return dataframe


# ==========================================================
# DATA INFORMATION
# ==========================================================

def dataframe_info(
    dataframe: pd.DataFrame,
) -> dict[str, Any]:
    """
    Return dataframe information.
    """

    try:

        return {

            "shape": dataframe.shape,

            "rows": len(dataframe),

            "columns": list(dataframe.columns),

            "memory_mb": dataframe_memory_usage(dataframe),

            "missing_values": int(
                dataframe.isna().sum().sum()
            ),

            "duplicates": int(
                dataframe.duplicated().sum()
            ),

        }

    except Exception as error:

        logger.exception(error)

        return {}


# ==========================================================
# PRICE RANGE
# ==========================================================

def price_range(
    dataframe: pd.DataFrame,
) -> float:
    """
    High - Low.
    """

    try:

        return float(

            dataframe["High"].max()

            -

            dataframe["Low"].min()

        )

    except Exception:

        return 0.0


def average_volume(
    dataframe: pd.DataFrame,
) -> float:
    """
    Average trading volume.
    """

    try:

        return float(
            dataframe["Volume"].mean()
        )

    except Exception:

        return 0.0


# ==========================================================
# NORMALIZATION
# ==========================================================

def normalize_column(
    dataframe: pd.DataFrame,
    column: str,
) -> pd.Series:
    """
    Min-Max normalization.
    """

    try:

        values = dataframe[column]

        minimum = values.min()

        maximum = values.max()

        if maximum == minimum:

            return pd.Series(
                0,
                index=values.index,
            )

        return (

            values - minimum

        ) / (

            maximum - minimum

        )

    except Exception as error:

        logger.exception(error)

        return pd.Series(dtype=float)


# ==========================================================
# STOCK AVAILABILITY
# ==========================================================

def stock_exists(
    ticker: str,
) -> bool:
    """
    Check whether a ticker has data.
    """

    try:

        dataframe = load_stock_data(
            ticker=ticker,
            period="5d",
        )

        return not dataframe.empty

    except Exception:

        return False


# ==========================================================
# MODULE VERSION
# ==========================================================

def version() -> str:
    """
    Return module version.
    """

    return VERSION


# ==========================================================
# END OF PART 6
# ==========================================================

# ==========================================================
# FEATURE ENGINEERING UTILITIES
# ==========================================================

def add_price_change(
    dataframe: pd.DataFrame,
) -> pd.DataFrame:
    """
    Add daily price change.
    """

    try:

        df = dataframe.copy()

        df["Price Change"] = (

            df["Close"]

            -

            df["Open"]

        )

        return df

    except Exception as error:

        logger.exception(error)

        return dataframe


def add_price_change_percent(
    dataframe: pd.DataFrame,
) -> pd.DataFrame:
    """
    Add daily percentage change.
    """

    try:

        df = dataframe.copy()

        df["Price Change %"] = (

            (df["Close"] - df["Open"])

            /

            df["Open"]

        ) * 100

        return df

    except Exception as error:

        logger.exception(error)

        return dataframe


def add_daily_return(
    dataframe: pd.DataFrame,
) -> pd.DataFrame:
    """
    Add daily return column.
    """

    try:

        df = dataframe.copy()

        df["Daily Return"] = (

            df["Close"]

            .pct_change()

            .fillna(0)

        )

        return df

    except Exception as error:

        logger.exception(error)

        return dataframe


def add_log_return(
    dataframe: pd.DataFrame,
) -> pd.DataFrame:
    """
    Add logarithmic return.
    """

    try:

        import numpy as np

        df = dataframe.copy()

        df["Log Return"] = np.log(

            df["Close"]

            /

            df["Close"].shift(1)

        )

        df.fillna(0, inplace=True)

        return df

    except Exception as error:

        logger.exception(error)

        return dataframe


# ==========================================================
# DATE UTILITIES
# ==========================================================

def add_date_columns(
    dataframe: pd.DataFrame,
) -> pd.DataFrame:
    """
    Add useful date columns.
    """

    try:

        df = dataframe.copy()

        index = pd.to_datetime(df.index)

        df["Year"] = index.year

        df["Month"] = index.month

        df["Day"] = index.day

        df["Weekday"] = index.day_name()

        df["Quarter"] = index.quarter

        return df

    except Exception as error:

        logger.exception(error)

        return dataframe


# ==========================================================
# STOCK FILTERS
# ==========================================================

def filter_volume(
    dataframe: pd.DataFrame,
    minimum_volume: int,
) -> pd.DataFrame:
    """
    Filter by trading volume.
    """

    try:

        return dataframe.loc[
            dataframe["Volume"] >= minimum_volume
        ].copy()

    except Exception as error:

        logger.exception(error)

        return dataframe


def filter_close_price(
    dataframe: pd.DataFrame,
    minimum_price: float,
) -> pd.DataFrame:
    """
    Filter by closing price.
    """

    try:

        return dataframe.loc[
            dataframe["Close"] >= minimum_price
        ].copy()

    except Exception as error:

        logger.exception(error)

        return dataframe


# ==========================================================
# EXPORT SUMMARY
# ==========================================================

def dataset_summary(
    dataframe: pd.DataFrame,
) -> dict[str, Any]:
    """
    Generate dataset summary.
    """

    try:

        return {

            "shape": dataframe.shape,

            "columns": dataframe.columns.tolist(),

            "start": dataframe.index.min(),

            "end": dataframe.index.max(),

            "highest_close": float(
                dataframe["Close"].max()
            ),

            "lowest_close": float(
                dataframe["Close"].min()
            ),

            "average_close": float(
                dataframe["Close"].mean()
            ),

            "average_volume": float(
                dataframe["Volume"].mean()
            ),

        }

    except Exception as error:

        logger.exception(error)

        return {}

# ==========================================================
# END OF PART 7
# ==========================================================

# ==========================================================
# BATCH DATA LOADING
# ==========================================================

def load_stock_batch(
    tickers: list[str],
    period: str = DEFAULT_PERIOD,
    interval: str = DEFAULT_INTERVAL,
) -> dict[str, pd.DataFrame]:
    """
    Download data for multiple tickers.
    """

    results: dict[str, pd.DataFrame] = {}

    for ticker in tickers:

        try:

            results[ticker] = load_stock_data(
                ticker=ticker,
                period=period,
                interval=interval,
            )

        except Exception as error:

            logger.exception(error)

            results[ticker] = pd.DataFrame()

    return results


# ==========================================================
# COMPANY INFORMATION
# ==========================================================

@st.cache_data(show_spinner=False)
def company_information(
    ticker: str,
) -> dict[str, Any]:
    """
    Return company information.
    """

    try:

        ticker = validate_ticker(ticker)

        info = yf.Ticker(ticker).info

        if not info:

            return {}

        return {

            "symbol": ticker,

            "company_name": info.get("longName"),

            "sector": info.get("sector"),

            "industry": info.get("industry"),

            "country": info.get("country"),

            "currency": info.get("currency"),

            "exchange": info.get("exchange"),

            "website": info.get("website"),

            "employees": info.get("fullTimeEmployees"),

            "market_cap": info.get("marketCap"),

        }

    except Exception as error:

        logger.exception(error)

        return {}


# ==========================================================
# MARKET STATUS
# ==========================================================

def market_is_open() -> bool:
    """
    Basic weekday market status.
    """

    try:

        weekday = datetime.now().weekday()

        return weekday < 5

    except Exception:

        return False


# ==========================================================
# DATASET COMPARISON
# ==========================================================

def compare_datasets(
    first: pd.DataFrame,
    second: pd.DataFrame,
) -> dict[str, Any]:
    """
    Compare two datasets.
    """

    try:

        return {

            "first_rows": len(first),

            "second_rows": len(second),

            "first_start": first.index.min(),

            "first_end": first.index.max(),

            "second_start": second.index.min(),

            "second_end": second.index.max(),

            "same_columns": list(first.columns) == list(second.columns),

        }

    except Exception as error:

        logger.exception(error)

        return {}


# ==========================================================
# MODULE HEALTH CHECK
# ==========================================================

def self_test() -> bool:
    """
    Verify module configuration.
    """

    try:

        assert VERSION == "2.0"

        assert DEFAULT_PERIOD in VALID_PERIODS

        assert DEFAULT_INTERVAL in VALID_INTERVALS

        return True

    except Exception as error:

        logger.exception(error)

        return False


# ==========================================================
# MODULE EXPORTS
# ==========================================================

__all__ = [

    "VERSION",

    "DataLoaderError",
    "InvalidTickerError",
    "DownloadError",

    "load_stock_data",
    "load_historical_data",
    "load_multiple_stocks",
    "load_stock_batch",
    "load_market_index",

    "get_company_info",
    "company_information",

    "validate_ticker",
    "validate_period",
    "validate_interval",
    "validate_dataframe",
    "clean_dataframe",

    "save_to_csv",
    "load_from_csv",
    "export_excel",
    "export_json",

    "daily_returns",
    "cumulative_returns",
    "volatility",

    "price_statistics",
    "latest_price",
    "latest_close",
    "latest_open",
    "latest_high",
    "latest_low",
    "latest_volume",

    "market_is_open",
    "dataset_summary",
    "data_summary",
    "dataframe_info",
    "download_metadata",

    "clear_streamlit_cache",
    "version",
]

# ==========================================================
# END OF data_loader.py
# VERSION 2.0
# ==========================================================