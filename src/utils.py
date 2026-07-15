"""
=========================================================
Live Stock Analysis & Prediction
Utility Module
Version : 2.0
=========================================================
"""

import os
import json
import logging
from pathlib import Path
from datetime import datetime
from typing import Any, Dict, Tuple, Optional

import numpy as np
import pandas as pd


# =========================================================
# CONFIGURATION
# =========================================================

VERSION = "2.0"

DATA_FOLDER = Path("data")

PREDICTION_FILE = DATA_FOLDER / "prediction_history.csv"


# =========================================================
# LOGGING
# =========================================================

logging.basicConfig(

    level=logging.INFO,

    format="%(asctime)s - %(levelname)s - %(message)s"

)

logger = logging.getLogger(__name__)


# =========================================================
# VALIDATION HELPERS
# =========================================================

def is_number(value: Any) -> bool:
    """
    Check whether value is numeric.
    """

    try:

        float(value)

        return True

    except (TypeError, ValueError):

        return False



def safe_float(
    value: Any,
    default: float = 0.0
) -> float:
    """
    Convert value safely to float.
    """

    try:

        return float(value)

    except (TypeError, ValueError):

        return default



def validate_dataframe(
    df: pd.DataFrame
) -> bool:
    """
    Validate pandas dataframe.
    """

    if df is None:

        return False


    if not isinstance(df, pd.DataFrame):

        return False


    return True



# =========================================================
# CURRENCY FORMATTER
# =========================================================

def format_currency(
    value: Any
) -> str:
    """
    Format number as Indian currency.
    """

    try:

        value = float(value)

        return f"₹ {value:,.2f}"


    except (TypeError, ValueError):

        return "N/A"



# =========================================================
# PERCENTAGE FORMATTER
# =========================================================

def format_percentage(
    value: Any
) -> str:
    """
    Format percentage value.
    """

    try:

        value = float(value)

        return f"{value:.2f}%"


    except (TypeError, ValueError):

        return "N/A"



# =========================================================
# NUMBER FORMATTER
# =========================================================

def format_number(
    value: Any
) -> str:
    """
    Format number with commas.
    """

    try:

        return f"{float(value):,.0f}"


    except (TypeError, ValueError):

        return "N/A"



# =========================================================
# DATE & TIME HELPERS
# =========================================================

def current_date() -> str:
    """
    Return current date.
    """

    return datetime.now().strftime(
        "%d-%m-%Y"
    )



def current_time() -> str:
    """
    Return current time.
    """

    return datetime.now().strftime(
        "%H:%M:%S"
    )



def current_datetime() -> str:
    """
    Return current date and time.
    """

    return datetime.now().strftime(
        "%d-%m-%Y %H:%M:%S"
    )
# =========================================================
# ADVANCED HELPER UTILITIES
# =========================================================

def safe_int(
    value: Any,
    default: int = 0
) -> int:
    """
    Safely convert value to integer.
    """
    try:
        return int(float(value))
    except (TypeError, ValueError):
        return default


def safe_str(
    value: Any,
    default: str = ""
) -> str:
    """
    Safely convert value to string.
    """
    try:
        if value is None:
            return default
        return str(value)
    except Exception:
        return default


def safe_bool(
    value: Any,
    default: bool = False
) -> bool:
    """
    Safely convert value to boolean.
    """
    try:
        if isinstance(value, bool):
            return value

        if isinstance(value, (int, float)):
            return value != 0

        if isinstance(value, str):
            value = value.strip().lower()

            if value in (
                "true",
                "yes",
                "1",
                "y",
                "on"
            ):
                return True

            if value in (
                "false",
                "no",
                "0",
                "off",
                "n"
            ):
                return False

        return default

    except Exception:
        return default


def safe_datetime(
    value: Any,
    default: Optional[datetime] = None
) -> Optional[datetime]:
    """
    Safely convert value to datetime.
    """
    try:
        return pd.to_datetime(value)
    except Exception:
        return default


# =========================================================
# PERCENTAGE UTILITIES
# =========================================================

def calculate_percentage(
    value: float,
    total: float,
    decimals: int = 2
) -> float:
    """
    Calculate percentage safely.
    """
    try:
        value = float(value)
        total = float(total)

        if total == 0:
            return 0.0

        return round((value / total) * 100, decimals)

    except Exception:
        return 0.0


def percentage_change(
    old_value: float,
    new_value: float,
    decimals: int = 2
) -> float:
    """
    Calculate percentage change.
    """
    try:
        old_value = float(old_value)
        new_value = float(new_value)

        if old_value == 0:
            return 0.0

        return round(
            ((new_value - old_value) / old_value) * 100,
            decimals
        )

    except Exception:
        return 0.0


# =========================================================
# NUMBER UTILITIES
# =========================================================

def round_number(
    value: Any,
    decimals: int = 2
) -> float:
    """
    Round numeric value safely.
    """
    try:
        return round(float(value), decimals)
    except Exception:
        return 0.0


def clamp(
    value: float,
    minimum: float,
    maximum: float
) -> float:
    """
    Restrict value within a range.
    """
    try:
        return max(minimum, min(value, maximum))
    except Exception:
        return minimum


def abbreviate_number(
    value: Any
) -> str:
    """
    Convert large numbers into readable format.
    """
    try:
        value = float(value)

        if abs(value) >= 1_000_000_000:
            return f"{value/1_000_000_000:.2f}B"

        if abs(value) >= 1_000_000:
            return f"{value/1_000_000:.2f}M"

        if abs(value) >= 1_000:
            return f"{value/1_000:.2f}K"

        return f"{value:.2f}"

    except Exception:
        return "N/A"


# =========================================================
# ADVANCED DATE & TIME UTILITIES
# =========================================================

def format_date(
    value: Any,
    fmt: str = "%d-%m-%Y"
) -> str:
    """
    Format date safely.
    """
    try:
        return pd.to_datetime(value).strftime(fmt)
    except Exception:
        return "N/A"


def format_datetime(
    value: Any,
    fmt: str = "%d-%m-%Y %H:%M:%S"
) -> str:
    """
    Format datetime safely.
    """
    try:
        return pd.to_datetime(value).strftime(fmt)
    except Exception:
        return "N/A"


def days_between(
    start: Any,
    end: Any
) -> int:
    """
    Return difference in days.
    """
    try:
        start = pd.to_datetime(start)
        end = pd.to_datetime(end)

        return abs((end - start).days)

    except Exception:
        return 0


# =========================================================
# ADDITIONAL CURRENCY UTILITIES
# =========================================================

def currency_symbol(
    currency: str = "INR"
) -> str:
    """
    Return currency symbol.
    """
    symbols = {
        "INR": "₹",
        "USD": "$",
        "EUR": "€",
        "GBP": "£",
        "JPY": "¥"
    }

    return symbols.get(currency.upper(), "₹")


def format_currency_with_code(
    value: Any,
    currency: str = "INR"
) -> str:
    """
    Format currency with currency code.
    """
    try:
        value = float(value)
        return f"{currency.upper()} {value:,.2f}"
    except Exception:
        return "N/A"


# =========================================================
# DATAFRAME UTILITIES
# =========================================================

def dataframe_is_empty(
    df: pd.DataFrame
) -> bool:
    """
    Check whether dataframe is empty.
    """
    try:
        return (
            not isinstance(df, pd.DataFrame)
            or df.empty
        )
    except Exception:
        return True


def dataframe_has_columns(
    df: pd.DataFrame,
    columns: list[str]
) -> bool:
    """
    Check required columns.
    """
    try:
        if dataframe_is_empty(df):
            return False

        return all(
            column in df.columns
            for column in columns
        )

    except Exception:
        return False


def remove_duplicate_rows(
    df: pd.DataFrame
) -> pd.DataFrame:
    """
    Remove duplicate dataframe rows.
    """
    try:
        return df.drop_duplicates()
    except Exception:
        return pd.DataFrame()


def fill_missing_values(
    df: pd.DataFrame,
    value: Any = 0
) -> pd.DataFrame:
    """
    Fill missing values safely.
    """
    try:
        return df.fillna(value)
    except Exception:
        return pd.DataFrame()
# =========================================================
# DATAFRAME CLEANING UTILITIES
# =========================================================

def normalize_column_names(
    df: pd.DataFrame
) -> pd.DataFrame:
    """
    Normalize dataframe column names.
    """
    try:
        dataframe = df.copy()

        dataframe.columns = [
            str(column)
            .strip()
            .lower()
            .replace(" ", "_")
            for column in dataframe.columns
        ]

        return dataframe

    except Exception as error:
        logger.exception(error)
        return pd.DataFrame()


def drop_missing_rows(
    df: pd.DataFrame
) -> pd.DataFrame:
    """
    Remove rows containing missing values.
    """
    try:
        return df.dropna()

    except Exception as error:
        logger.exception(error)
        return pd.DataFrame()


def get_missing_value_count(
    df: pd.DataFrame
) -> Dict[str, int]:
    """
    Return missing values for each column.
    """
    try:
        return df.isnull().sum().to_dict()

    except Exception as error:
        logger.exception(error)
        return {}


def dataframe_memory_usage(
    df: pd.DataFrame
) -> float:
    """
    Return dataframe memory usage in MB.
    """
    try:
        memory = df.memory_usage(deep=True).sum()

        return round(
            memory / (1024 * 1024),
            2
        )

    except Exception as error:
        logger.exception(error)
        return 0.0


def dataframe_summary(
    df: pd.DataFrame
) -> Dict[str, Any]:
    """
    Return dataframe summary.
    """
    try:
        return {
            "rows": len(df),
            "columns": len(df.columns),
            "missing_values": int(df.isnull().sum().sum()),
            "duplicates": int(df.duplicated().sum()),
            "memory_mb": dataframe_memory_usage(df)
        }

    except Exception as error:
        logger.exception(error)
        return {}


# =========================================================
# FILE UTILITIES
# =========================================================

def file_exists(
    file_path: str | Path
) -> bool:
    """
    Check whether file exists.
    """
    try:
        return Path(file_path).exists()

    except Exception:
        return False


def create_directory(
    directory: str | Path
) -> bool:
    """
    Create directory safely.
    """
    try:
        Path(directory).mkdir(
            parents=True,
            exist_ok=True
        )
        return True

    except Exception as error:
        logger.exception(error)
        return False


def read_json_file(
    file_path: str | Path
) -> Dict[str, Any]:
    """
    Read JSON safely.
    """
    try:
        with open(
            file_path,
            "r",
            encoding="utf-8"
        ) as file:
            return json.load(file)

    except Exception as error:
        logger.exception(error)
        return {}


def write_json_file(
    data: Dict[str, Any],
    file_path: str | Path
) -> bool:
    """
    Write JSON safely.
    """
    try:
        with open(
            file_path,
            "w",
            encoding="utf-8"
        ) as file:
            json.dump(
                data,
                file,
                indent=4,
                ensure_ascii=False
            )

        return True

    except Exception as error:
        logger.exception(error)
        return False


# =========================================================
# STOCK DATA UTILITIES
# =========================================================

def validate_stock_dataframe(
    df: pd.DataFrame
) -> bool:
    """
    Validate stock dataframe structure.
    """
    required_columns = [
        "Open",
        "High",
        "Low",
        "Close",
        "Volume"
    ]

    try:
        if dataframe_is_empty(df):
            return False

        return all(
            column in df.columns
            for column in required_columns
        )

    except Exception:
        return False


def latest_close_price(
    df: pd.DataFrame
) -> float:
    """
    Return latest closing price.
    """
    try:
        return float(
            df["Close"].iloc[-1]
        )

    except Exception:
        return 0.0


def latest_volume(
    df: pd.DataFrame
) -> int:
    """
    Return latest trading volume.
    """
    try:
        return int(
            df["Volume"].iloc[-1]
        )

    except Exception:
        return 0


def price_range(
    df: pd.DataFrame
) -> Tuple[float, float]:
    """
    Return lowest and highest prices.
    """
    try:
        return (
            float(df["Low"].min()),
            float(df["High"].max())
        )

    except Exception:
        return (
            0.0,
            0.0
        )


# =========================================================
# LOGGING UTILITIES
# =========================================================

def log_info(
    message: str
) -> None:
    """
    Log info message.
    """
    try:
        logger.info(message)
    except Exception:
        pass


def log_warning(
    message: str
) -> None:
    """
    Log warning message.
    """
    try:
        logger.warning(message)
    except Exception:
        pass


def log_error(
    message: str
) -> None:
    """
    Log error message.
    """
    try:
        logger.error(message)
    except Exception:
        pass


def log_exception(
    exception: Exception
) -> None:
    """
    Log exception safely.
    """
    try:
        logger.exception(exception)
    except Exception:
        pass
# =========================================================
# DATAFRAME STATISTICS UTILITIES
# =========================================================

def dataframe_shape(
    df: pd.DataFrame
) -> Tuple[int, int]:
    """
    Return dataframe shape.
    """
    try:
        return df.shape
    except Exception:
        return (0, 0)


def numeric_columns(
    df: pd.DataFrame
) -> list[str]:
    """
    Return numeric columns.
    """
    try:
        return df.select_dtypes(
            include=np.number
        ).columns.tolist()

    except Exception:
        return []


def categorical_columns(
    df: pd.DataFrame
) -> list[str]:
    """
    Return categorical columns.
    """
    try:
        return df.select_dtypes(
            exclude=np.number
        ).columns.tolist()

    except Exception:
        return []


def dataframe_description(
    df: pd.DataFrame
) -> pd.DataFrame:
    """
    Return dataframe statistics.
    """
    try:
        return df.describe(include="all")

    except Exception:
        return pd.DataFrame()


# =========================================================
# MATHEMATICAL UTILITIES
# =========================================================

def safe_divide(
    numerator: float,
    denominator: float,
    default: float = 0.0
) -> float:
    """
    Safely divide two numbers.
    """
    try:
        denominator = float(denominator)

        if denominator == 0:
            return default

        return float(numerator) / denominator

    except Exception:
        return default


def average(
    values: list[float]
) -> float:
    """
    Return average value.
    """
    try:
        if not values:
            return 0.0

        return float(np.mean(values))

    except Exception:
        return 0.0


def median(
    values: list[float]
) -> float:
    """
    Return median value.
    """
    try:
        if not values:
            return 0.0

        return float(np.median(values))

    except Exception:
        return 0.0


def standard_deviation(
    values: list[float]
) -> float:
    """
    Return standard deviation.
    """
    try:
        if not values:
            return 0.0

        return float(np.std(values))

    except Exception:
        return 0.0


def variance(
    values: list[float]
) -> float:
    """
    Return variance.
    """
    try:
        if not values:
            return 0.0

        return float(np.var(values))

    except Exception:
        return 0.0


# =========================================================
# DATE DIFFERENCE UTILITIES
# =========================================================

def is_weekend(
    date_value: Any
) -> bool:
    """
    Check if date is weekend.
    """
    try:
        return pd.to_datetime(date_value).weekday() >= 5

    except Exception:
        return False


def current_timestamp() -> int:
    """
    Return Unix timestamp.
    """
    try:
        return int(datetime.now().timestamp())

    except Exception:
        return 0


def timestamp_to_datetime(
    timestamp: int
) -> str:
    """
    Convert timestamp to datetime string.
    """
    try:
        return datetime.fromtimestamp(
            int(timestamp)
        ).strftime("%d-%m-%Y %H:%M:%S")

    except Exception:
        return "N/A"


# =========================================================
# STRING UTILITIES
# =========================================================

def clean_string(
    value: Any
) -> str:
    """
    Clean string value.
    """
    try:
        return str(value).strip()

    except Exception:
        return ""


def title_case(
    value: Any
) -> str:
    """
    Convert string to title case.
    """
    try:
        return clean_string(value).title()

    except Exception:
        return ""


def snake_case(
    value: Any
) -> str:
    """
    Convert string to snake_case.
    """
    try:
        return (
            clean_string(value)
            .lower()
            .replace(" ", "_")
        )

    except Exception:
        return ""


# =========================================================
# LIST UTILITIES
# =========================================================

def unique_list(
    values: list[Any]
) -> list[Any]:
    """
    Return unique values.
    """
    try:
        return list(dict.fromkeys(values))

    except Exception:
        return []


def flatten_list(
    values: list[list[Any]]
) -> list[Any]:
    """
    Flatten nested list.
    """
    try:
        return [
            item
            for sublist in values
            for item in sublist
        ]

    except Exception:
        return []


# =========================================================
# PATH UTILITIES
# =========================================================

def join_path(
    *parts: str
) -> Path:
    """
    Join path components.
    """
    try:
        return Path(*parts)

    except Exception:
        return Path(".")


def ensure_data_directory() -> Path:
    """
    Ensure data directory exists.
    """
    try:
        DATA_FOLDER.mkdir(
            parents=True,
            exist_ok=True
        )
        return DATA_FOLDER

    except Exception:
        return Path(".")


# =========================================================
# SYSTEM UTILITIES
# =========================================================

def module_version() -> str:
    """
    Return utility module version.
    """
    return VERSION


def project_paths() -> Dict[str, Path]:
    """
    Return important project paths.
    """
    return {
        "data": DATA_FOLDER,
        "prediction_history": PREDICTION_FILE,
    }


def system_status() -> Dict[str, Any]:
    """
    Return utility module status.
    """
    return {
        "version": VERSION,
        "python": "3.12",
        "module": "utils",
        "status": "Ready",
        "data_directory_exists": DATA_FOLDER.exists(),
    }
# =========================================================
# CONFIGURATION UTILITIES
# =========================================================

def get_env(
    key: str,
    default: str = ""
) -> str:
    """
    Return environment variable.
    """
    try:
        return os.getenv(key, default)
    except Exception:
        return default


def env_exists(
    key: str
) -> bool:
    """
    Check if environment variable exists.
    """
    try:
        return key in os.environ
    except Exception:
        return False


def load_json_config(
    config_path: str | Path
) -> Dict[str, Any]:
    """
    Load JSON configuration safely.
    """
    try:
        config_path = Path(config_path)

        if not config_path.exists():
            return {}

        with open(config_path, "r", encoding="utf-8") as file:
            return json.load(file)

    except Exception as error:
        logger.exception(error)
        return {}


def save_json_config(
    config: Dict[str, Any],
    config_path: str | Path
) -> bool:
    """
    Save configuration to JSON.
    """
    try:
        config_path = Path(config_path)

        config_path.parent.mkdir(
            parents=True,
            exist_ok=True
        )

        with open(config_path, "w", encoding="utf-8") as file:
            json.dump(
                config,
                file,
                indent=4,
                ensure_ascii=False
            )

        return True

    except Exception as error:
        logger.exception(error)
        return False


# =========================================================
# CSV UTILITIES
# =========================================================

def load_csv(
    file_path: str | Path
) -> pd.DataFrame:
    """
    Load CSV safely.
    """
    try:
        return pd.read_csv(file_path)

    except Exception as error:
        logger.exception(error)
        return pd.DataFrame()


def save_csv(
    dataframe: pd.DataFrame,
    file_path: str | Path,
    index: bool = False
) -> bool:
    """
    Save dataframe to CSV.
    """
    try:
        dataframe.to_csv(
            file_path,
            index=index
        )
        return True

    except Exception as error:
        logger.exception(error)
        return False


# =========================================================
# DICTIONARY UTILITIES
# =========================================================

def safe_get(
    dictionary: Dict[str, Any],
    key: str,
    default: Any = None
) -> Any:
    """
    Safely get dictionary value.
    """
    try:
        return dictionary.get(key, default)
    except Exception:
        return default


def merge_dictionaries(
    *dictionaries: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Merge multiple dictionaries.
    """
    try:
        merged: Dict[str, Any] = {}

        for dictionary in dictionaries:
            merged.update(dictionary)

        return merged

    except Exception:
        return {}


# =========================================================
# STOCK PRICE UTILITIES
# =========================================================

def highest_price(
    df: pd.DataFrame
) -> float:
    """
    Return highest High price.
    """
    try:
        return float(df["High"].max())
    except Exception:
        return 0.0


def lowest_price(
    df: pd.DataFrame
) -> float:
    """
    Return lowest Low price.
    """
    try:
        return float(df["Low"].min())
    except Exception:
        return 0.0


def latest_open_price(
    df: pd.DataFrame
) -> float:
    """
    Return latest Open price.
    """
    try:
        return float(df["Open"].iloc[-1])
    except Exception:
        return 0.0


def latest_high_price(
    df: pd.DataFrame
) -> float:
    """
    Return latest High price.
    """
    try:
        return float(df["High"].iloc[-1])
    except Exception:
        return 0.0


def latest_low_price(
    df: pd.DataFrame
) -> float:
    """
    Return latest Low price.
    """
    try:
        return float(df["Low"].iloc[-1])
    except Exception:
        return 0.0


# =========================================================
# DATA VALIDATION UTILITIES
# =========================================================

def has_null_values(
    df: pd.DataFrame
) -> bool:
    """
    Check whether dataframe contains null values.
    """
    try:
        return bool(df.isnull().values.any())
    except Exception:
        return False


def has_duplicate_rows(
    df: pd.DataFrame
) -> bool:
    """
    Check whether dataframe contains duplicate rows.
    """
    try:
        return bool(df.duplicated().any())
    except Exception:
        return False


def validate_numeric_column(
    df: pd.DataFrame,
    column: str
) -> bool:
    """
    Validate numeric column.
    """
    try:
        return pd.api.types.is_numeric_dtype(df[column])
    except Exception:
        return False


# =========================================================
# RANDOM UTILITIES
# =========================================================

def generate_id(
    prefix: str = "ID"
) -> str:
    """
    Generate timestamp based ID.
    """
    try:
        return f"{prefix}_{datetime.now().strftime('%Y%m%d%H%M%S%f')}"
    except Exception:
        return prefix


def current_year() -> int:
    """
    Return current year.
    """
    try:
        return datetime.now().year
    except Exception:
        return 0


def current_month() -> int:
    """
    Return current month.
    """
    try:
        return datetime.now().month
    except Exception:
        return 0


def current_day() -> int:
    """
    Return current day.
    """
    try:
        return datetime.now().day
    except Exception:
        return 0


# =========================================================
# END OF utils.py VERSION 2.0
# =========================================================    
