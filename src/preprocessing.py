"""
=========================================================
Live Stock Analysis & Prediction
File    : preprocessing.py
Version : 2.0
Part    : 1
Python  : 3.12
=========================================================
"""

from __future__ import annotations

import logging
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd
import streamlit as st

# ==========================================================
# LOGGING
# ==========================================================

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
)

logger = logging.getLogger(__name__)

# ==========================================================
# MODULE INFORMATION
# ==========================================================

VERSION = "2.0"

DEFAULT_TARGET = "Close"

DEFAULT_TEST_SIZE = 0.20

DEFAULT_RANDOM_STATE = 42

DEFAULT_SEQUENCE_LENGTH = 60

# ==========================================================
# REQUIRED COLUMNS
# ==========================================================

OHLCV_COLUMNS = [
    "Open",
    "High",
    "Low",
    "Close",
    "Volume",
]

FEATURE_COLUMNS = [

    "Open",
    "High",
    "Low",
    "Close",
    "Volume",

    "SMA_20",
    "SMA_50",

    "EMA_20",
    "EMA_50",

    "RSI",

    "MACD",
    "MACD_Signal",

    "BB_High",
    "BB_Low",

    "ATR",

]

# ==========================================================
# EXCEPTIONS
# ==========================================================

class PreprocessingError(Exception):
    """Base preprocessing exception."""


class ValidationError(PreprocessingError):
    """Validation failed."""


class FeatureEngineeringError(PreprocessingError):
    """Feature engineering failed."""


# ==========================================================
# CONFIGURATION
# ==========================================================

@dataclass(slots=True)
class PreprocessingConfig:

    target_column: str = DEFAULT_TARGET

    sequence_length: int = DEFAULT_SEQUENCE_LENGTH

    test_size: float = DEFAULT_TEST_SIZE

    random_state: int = DEFAULT_RANDOM_STATE

    fill_method: str = "ffill"

    remove_duplicates: bool = True

    sort_index: bool = True

    drop_missing_target: bool = True


# ==========================================================
# VALIDATION
# ==========================================================

def validate_dataframe(
    dataframe: pd.DataFrame,
) -> bool:
    """
    Validate dataframe.
    """

    if dataframe is None:

        return False

    if dataframe.empty:

        return False

    return True


def validate_ohlcv(
    dataframe: pd.DataFrame,
) -> bool:
    """
    Validate OHLCV columns.
    """

    if not validate_dataframe(dataframe):

        return False

    for column in OHLCV_COLUMNS:

        if column not in dataframe.columns:

            logger.error(
                "%s column missing.",
                column,
            )

            return False

    return True


def validate_features(
    dataframe: pd.DataFrame,
    columns: list[str],
) -> bool:
    """
    Validate feature columns.
    """

    if not validate_dataframe(dataframe):

        return False

    missing = [

        column

        for column in columns

        if column not in dataframe.columns

    ]

    if missing:

        logger.warning(
            "Missing features: %s",
            ", ".join(missing),
        )

        return False

    return True


# ==========================================================
# PREPROCESSOR
# ==========================================================

class Preprocessor:
    """
    Main preprocessing class.
    """

    def __init__(
        self,
        config: PreprocessingConfig | None = None,
    ) -> None:

        self.config = (
            config
            if config
            else PreprocessingConfig()
        )

        logger.info(
            "Preprocessor Version %s initialized.",
            VERSION,
        )

    @property
    def target_column(
        self,
    ) -> str:

        return self.config.target_column

    @property
    def sequence_length(
        self,
    ) -> int:

        return self.config.sequence_length

    def copy(
        self,
        dataframe: pd.DataFrame,
    ) -> pd.DataFrame:
        """
        Safe dataframe copy.
        """

        return dataframe.copy(deep=True)


# ==========================================================
# STREAMLIT CACHE
# ==========================================================

@st.cache_data(show_spinner=False)
def cached_copy(
    dataframe: pd.DataFrame,
) -> pd.DataFrame:
    """
    Return cached dataframe copy.
    """

    return dataframe.copy(deep=True)


# ==========================================================
# END OF PART 1
# ==========================================================
# ==========================================================
# DATA CLEANING
# ==========================================================

    def remove_duplicate_rows(
        self,
        dataframe: pd.DataFrame,
    ) -> pd.DataFrame:
        """
        Remove duplicate rows.
        """

        try:

            if not self.config.remove_duplicates:
                return dataframe

            return dataframe.drop_duplicates()

        except Exception as error:

            logger.exception(error)

            raise PreprocessingError(
                "Failed to remove duplicate rows."
            ) from error

    # ------------------------------------------------------

    def sort_dataframe(
        self,
        dataframe: pd.DataFrame,
    ) -> pd.DataFrame:
        """
        Sort dataframe by index.
        """

        try:

            if not self.config.sort_index:
                return dataframe

            return dataframe.sort_index()

        except Exception as error:

            logger.exception(error)

            raise PreprocessingError(
                "Failed to sort dataframe."
            ) from error

    # ------------------------------------------------------

    def fill_missing_values(
        self,
        dataframe: pd.DataFrame,
    ) -> pd.DataFrame:
        """
        Fill missing values.
        """

        try:

            df = dataframe.copy()

            method = self.config.fill_method.lower()

            if method == "ffill":

                df.ffill(inplace=True)

            elif method == "bfill":

                df.bfill(inplace=True)

            elif method == "zero":

                df.fillna(0, inplace=True)

            elif method == "mean":

                numeric_columns = df.select_dtypes(
                    include="number"
                ).columns

                df[numeric_columns] = df[
                    numeric_columns
                ].fillna(
                    df[numeric_columns].mean()
                )

            else:

                df.ffill(inplace=True)

            return df

        except Exception as error:

            logger.exception(error)

            raise PreprocessingError(
                "Failed to fill missing values."
            ) from error

    # ------------------------------------------------------

    def remove_missing_target(
        self,
        dataframe: pd.DataFrame,
    ) -> pd.DataFrame:
        """
        Remove rows with missing target.
        """

        try:

            if not self.config.drop_missing_target:

                return dataframe

            return dataframe.dropna(
                subset=[self.target_column]
            )

        except Exception as error:

            logger.exception(error)

            raise PreprocessingError(
                "Failed to remove missing target."
            ) from error

    # ------------------------------------------------------

    def clean_dataframe(
        self,
        dataframe: pd.DataFrame,
    ) -> pd.DataFrame:
        """
        Complete cleaning pipeline.
        """

        try:

            if not validate_dataframe(dataframe):

                raise ValidationError(
                    "Invalid dataframe."
                )

            df = self.copy(dataframe)

            df = self.remove_duplicate_rows(df)

            df = self.sort_dataframe(df)

            df = self.fill_missing_values(df)

            df = self.remove_missing_target(df)

            return df

        except Exception as error:

            logger.exception(error)

            raise


# ==========================================================
# HELPER FUNCTIONS
# ==========================================================

def dataframe_shape(
    dataframe: pd.DataFrame,
) -> tuple[int, int]:
    """
    Return dataframe shape.
    """

    try:

        return dataframe.shape

    except Exception:

        return (0, 0)


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


def categorical_columns(
    dataframe: pd.DataFrame,
) -> list[str]:
    """
    Return categorical columns.
    """

    try:

        return list(
            dataframe.select_dtypes(
                exclude="number"
            ).columns
        )

    except Exception:

        return []


# ==========================================================
# END OF PART 2
# ==========================================================

# ==========================================================
# OUTLIER HANDLING
# ==========================================================

    def detect_outliers_iqr(
        self,
        dataframe: pd.DataFrame,
        columns: list[str] | None = None,
    ) -> dict[str, int]:
        """
        Detect outliers using IQR.
        """

        try:

            df = dataframe.copy()

            if columns is None:

                columns = numeric_columns(df)

            result: dict[str, int] = {}

            for column in columns:

                if column not in df.columns:

                    continue

                q1 = df[column].quantile(0.25)

                q3 = df[column].quantile(0.75)

                iqr = q3 - q1

                lower = q1 - (1.5 * iqr)

                upper = q3 + (1.5 * iqr)

                count = int(

                    (
                        (df[column] < lower)

                        |

                        (df[column] > upper)

                    ).sum()

                )

                result[column] = count

            return result

        except Exception as error:

            logger.exception(error)

            raise PreprocessingError(
                "Failed to detect outliers."
            ) from error

    # ------------------------------------------------------

    def clip_outliers(
        self,
        dataframe: pd.DataFrame,
        columns: list[str] | None = None,
    ) -> pd.DataFrame:
        """
        Clip outliers using IQR boundaries.
        """

        try:

            df = dataframe.copy()

            if columns is None:

                columns = numeric_columns(df)

            for column in columns:

                if column not in df.columns:

                    continue

                q1 = df[column].quantile(0.25)

                q3 = df[column].quantile(0.75)

                iqr = q3 - q1

                lower = q1 - (1.5 * iqr)

                upper = q3 + (1.5 * iqr)

                df[column] = df[column].clip(
                    lower=lower,
                    upper=upper,
                )

            return df

        except Exception as error:

            logger.exception(error)

            raise PreprocessingError(
                "Failed to clip outliers."
            ) from error


# ==========================================================
# FEATURE ENGINEERING
# ==========================================================

    def add_price_features(
        self,
        dataframe: pd.DataFrame,
    ) -> pd.DataFrame:
        """
        Create price-based features.
        """

        try:

            df = dataframe.copy()

            df["Price_Change"] = (

                df["Close"]

                -

                df["Open"]

            )

            df["Daily_Return"] = (

                df["Close"]

                .pct_change()

                .fillna(0)

            )

            df["High_Low_Spread"] = (

                df["High"]

                -

                df["Low"]

            )

            df["Open_Close_Spread"] = (

                df["Open"]

                -

                df["Close"]

            )

            df["Volume_Change"] = (

                df["Volume"]

                .pct_change()

                .fillna(0)

            )

            return df

        except Exception as error:

            logger.exception(error)

            raise FeatureEngineeringError(
                "Failed to create price features."
            ) from error

    # ------------------------------------------------------

    def add_date_features(
        self,
        dataframe: pd.DataFrame,
    ) -> pd.DataFrame:
        """
        Create calendar features.
        """

        try:

            df = dataframe.copy()

            index = pd.to_datetime(df.index)

            df["Year"] = index.year

            df["Month"] = index.month

            df["Day"] = index.day

            df["Week"] = index.isocalendar().week.astype(int)

            df["Quarter"] = index.quarter

            df["Weekday"] = index.dayofweek

            df["Is_Month_End"] = index.is_month_end.astype(int)

            df["Is_Month_Start"] = index.is_month_start.astype(int)

            return df

        except Exception as error:

            logger.exception(error)

            raise FeatureEngineeringError(
                "Failed to create date features."
            ) from error

# ==========================================================
# END OF PART 3
# ==========================================================

# ==========================================================
# FEATURE ENGINEERING
# ==========================================================

    def create_target(
        self,
        dataframe: pd.DataFrame,
        target_column: str | None = None,
    ) -> pd.DataFrame:
        """
        Create prediction target column.
        """

        try:

            df = dataframe.copy()

            column = (
                target_column
                or self.target_column
            )

            df["Target"] = df[column].shift(-1)

            df.dropna(
                subset=["Target"],
                inplace=True,
            )

            return df

        except Exception as error:

            logger.exception(error)

            raise FeatureEngineeringError(
                "Failed to create target."
            ) from error

    # ------------------------------------------------------

    def select_features(
        self,
        dataframe: pd.DataFrame,
        features: list[str],
    ) -> pd.DataFrame:
        """
        Select required features.
        """

        try:

            missing = [

                feature

                for feature in features

                if feature not in dataframe.columns

            ]

            if missing:

                raise ValidationError(

                    f"Missing features: {missing}"

                )

            return dataframe[features].copy()

        except Exception as error:

            logger.exception(error)

            raise

    # ------------------------------------------------------

    def prepare_features(
        self,
        dataframe: pd.DataFrame,
    ) -> pd.DataFrame:
        """
        Complete feature engineering pipeline.
        """

        try:

            df = self.clean_dataframe(
                dataframe
            )

            df = self.add_price_features(
                df
            )

            df = self.add_date_features(
                df
            )

            df = self.create_target(
                df
            )

            return df

        except Exception as error:

            logger.exception(error)

            raise FeatureEngineeringError(
                "Feature preparation failed."
            ) from error


# ==========================================================
# SCALING UTILITIES
# ==========================================================

class MinMaxScaler:
    """
    Simple Min-Max scaler.
    """

    def __init__(self):

        self.minimum: pd.Series | None = None

        self.maximum: pd.Series | None = None

    def fit(
        self,
        dataframe: pd.DataFrame,
    ) -> "MinMaxScaler":

        self.minimum = dataframe.min()

        self.maximum = dataframe.max()

        return self

    def transform(
        self,
        dataframe: pd.DataFrame,
    ) -> pd.DataFrame:

        if self.minimum is None:

            raise ValidationError(
                "Scaler is not fitted."
            )

        denominator = (

            self.maximum

            -

            self.minimum

        )

        denominator.replace(
            0,
            1,
            inplace=True,
        )

        return (

            dataframe

            -

            self.minimum

        ) / denominator

    def fit_transform(
        self,
        dataframe: pd.DataFrame,
    ) -> pd.DataFrame:

        return self.fit(
            dataframe
        ).transform(
            dataframe
        )


# ==========================================================
# END OF PART 4
# ==========================================================

# ==========================================================
# STANDARD SCALER
# ==========================================================

class StandardScaler:
    """
    Standard score scaler.
    """

    def __init__(self) -> None:

        self.mean: pd.Series | None = None

        self.std: pd.Series | None = None

    def fit(
        self,
        dataframe: pd.DataFrame,
    ) -> "StandardScaler":
        """
        Calculate mean and standard deviation.
        """

        self.mean = dataframe.mean()

        self.std = dataframe.std()

        self.std.replace(
            0,
            1,
            inplace=True,
        )

        return self

    def transform(
        self,
        dataframe: pd.DataFrame,
    ) -> pd.DataFrame:
        """
        Transform dataframe.
        """

        if self.mean is None or self.std is None:

            raise ValidationError(
                "Scaler has not been fitted."
            )

        return (

            dataframe

            -

            self.mean

        ) / self.std

    def fit_transform(
        self,
        dataframe: pd.DataFrame,
    ) -> pd.DataFrame:
        """
        Fit and transform.
        """

        return self.fit(
            dataframe
        ).transform(
            dataframe
        )

    def inverse_transform(
        self,
        dataframe: pd.DataFrame,
    ) -> pd.DataFrame:
        """
        Restore original values.
        """

        if self.mean is None or self.std is None:

            raise ValidationError(
                "Scaler has not been fitted."
            )

        return (

            dataframe

            *

            self.std

        ) + self.mean


# ==========================================================
# TRAIN / TEST SPLIT
# ==========================================================

def train_test_split(
    dataframe: pd.DataFrame,
    test_size: float = DEFAULT_TEST_SIZE,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """
    Split dataframe into train and test sets.
    """

    if not validate_dataframe(dataframe):

        raise ValidationError(
            "Invalid dataframe."
        )

    if not 0 < test_size < 1:

        raise ValidationError(
            "test_size must be between 0 and 1."
        )

    split_index = int(

        len(dataframe)

        *

        (1 - test_size)

    )

    train = dataframe.iloc[:split_index].copy()

    test = dataframe.iloc[split_index:].copy()

    return train, test


# ==========================================================
# FEATURE / TARGET SPLIT
# ==========================================================

def split_features_target(
    dataframe: pd.DataFrame,
    target: str = "Target",
) -> tuple[pd.DataFrame, pd.Series]:
    """
    Split X and y.
    """

    if target not in dataframe.columns:

        raise ValidationError(
            f"{target} column not found."
        )

    x = dataframe.drop(
        columns=[target]
    )

    y = dataframe[target]

    return x, y


# ==========================================================
# NUMERIC FEATURE SELECTION
# ==========================================================

def numeric_features(
    dataframe: pd.DataFrame,
) -> pd.DataFrame:
    """
    Return only numeric columns.
    """

    return dataframe.select_dtypes(
        include=[
            np.number,
        ]
    ).copy()


# ==========================================================
# END OF PART 5
# ==========================================================

# ==========================================================
# SEQUENCE GENERATION (LSTM)
# ==========================================================

def create_sequences(
    features: pd.DataFrame | np.ndarray,
    target: pd.Series | np.ndarray,
    sequence_length: int = DEFAULT_SEQUENCE_LENGTH,
) -> tuple[np.ndarray, np.ndarray]:
    """
    Create sequences for sequence-based models such as LSTM.
    """

    try:

        x = np.asarray(features)

        y = np.asarray(target)

        x_sequences: list[np.ndarray] = []

        y_sequences: list[Any] = []

        for i in range(

            sequence_length,

            len(x)

        ):

            x_sequences.append(

                x[
                    i-sequence_length:i
                ]

            )

            y_sequences.append(

                y[i]

            )

        return (

            np.asarray(x_sequences),

            np.asarray(y_sequences),

        )

    except Exception as error:

        logger.exception(error)

        raise PreprocessingError(
            "Failed to create sequences."
        ) from error


# ==========================================================
# TRAINING DATA PREPARATION
# ==========================================================

def prepare_training_data(
    dataframe: pd.DataFrame,
    target_column: str = "Target",
    sequence_length: int = DEFAULT_SEQUENCE_LENGTH,
    scale: bool = True,
) -> tuple[
    np.ndarray,
    np.ndarray,
    MinMaxScaler | None,
]:
    """
    Prepare training data for deep learning models.
    """

    try:

        if target_column not in dataframe.columns:

            raise ValidationError(
                f"{target_column} not found."
            )

        numeric_df = numeric_features(
            dataframe
        )

        scaler = None

        if scale:

            scaler = MinMaxScaler()

            numeric_df = scaler.fit_transform(
                numeric_df
            )

        x = numeric_df.drop(
            columns=[target_column]
        )

        y = numeric_df[target_column]

        x_sequences, y_sequences = create_sequences(
            x,
            y,
            sequence_length,
        )

        return (

            x_sequences,

            y_sequences,

            scaler,

        )

    except Exception as error:

        logger.exception(error)

        raise


# ==========================================================
# FEATURE SUMMARY
# ==========================================================

def feature_summary(
    dataframe: pd.DataFrame,
) -> pd.DataFrame:
    """
    Generate feature statistics.
    """

    try:

        numeric_df = numeric_features(
            dataframe
        )

        summary = pd.DataFrame({

            "dtype": numeric_df.dtypes,

            "missing": numeric_df.isna().sum(),

            "minimum": numeric_df.min(),

            "maximum": numeric_df.max(),

            "mean": numeric_df.mean(),

            "std": numeric_df.std(),

        })

        return summary

    except Exception as error:

        logger.exception(error)

        return pd.DataFrame()


# ==========================================================
# CORRELATION MATRIX
# ==========================================================

def correlation_matrix(
    dataframe: pd.DataFrame,
) -> pd.DataFrame:
    """
    Calculate feature correlation matrix.
    """

    try:

        return numeric_features(
            dataframe
        ).corr()

    except Exception as error:

        logger.exception(error)

        return pd.DataFrame()


# ==========================================================
# END OF PART 6
# ==========================================================

# ==========================================================
# PREPROCESSING PIPELINE
# ==========================================================

def preprocess_dataset(
    dataframe: pd.DataFrame,
    config: PreprocessingConfig | None = None,
) -> pd.DataFrame:
    """
    Complete preprocessing pipeline.
    """

    try:

        processor = Preprocessor(config)

        dataframe = processor.clean_dataframe(
            dataframe
        )

        dataframe = processor.add_price_features(
            dataframe
        )

        dataframe = processor.add_date_features(
            dataframe
        )

        dataframe = processor.create_target(
            dataframe
        )

        return dataframe

    except Exception as error:

        logger.exception(error)

        raise PreprocessingError(
            "Dataset preprocessing failed."
        ) from error


# ==========================================================
# DATASET INFORMATION
# ==========================================================

def dataset_information(
    dataframe: pd.DataFrame,
) -> dict[str, Any]:
    """
    Return dataset information.
    """

    try:

        return {

            "rows": len(dataframe),

            "columns": len(dataframe.columns),

            "column_names": dataframe.columns.tolist(),

            "memory_mb": round(

                dataframe.memory_usage(
                    deep=True
                ).sum()

                / (1024 ** 2),

                2,

            ),

            "missing_values": int(

                dataframe.isna()

                .sum()

                .sum()

            ),

            "duplicate_rows": int(

                dataframe.duplicated()

                .sum()

            ),

            "start_date": dataframe.index.min(),

            "end_date": dataframe.index.max(),

        }

    except Exception as error:

        logger.exception(error)

        return {}


# ==========================================================
# DATA VALIDATION REPORT
# ==========================================================

def validation_report(
    dataframe: pd.DataFrame,
) -> dict[str, Any]:
    """
    Generate validation report.
    """

    try:

        return {

            "valid_dataframe": validate_dataframe(
                dataframe
            ),

            "valid_ohlcv": validate_ohlcv(
                dataframe
            ),

            "total_rows": len(dataframe),

            "total_columns": len(dataframe.columns),

            "numeric_columns": len(

                dataframe.select_dtypes(
                    include=np.number
                ).columns

            ),

            "missing_cells": int(

                dataframe.isna()

                .sum()

                .sum()

            ),

        }

    except Exception as error:

        logger.exception(error)

        return {}


# ==========================================================
# CACHE UTILITIES
# ==========================================================

def clear_cache() -> None:
    """
    Clear Streamlit cache.
    """

    try:

        st.cache_data.clear()

    except Exception as error:

        logger.exception(error)


# ==========================================================
# VERSION
# ==========================================================

def version() -> str:
    """
    Return module version.
    """

    return VERSION


# ==========================================================
# MODULE EXPORTS
# ==========================================================

__all__ = [

    "VERSION",

    "OHLCV_COLUMNS",

    "FEATURE_COLUMNS",

    "PreprocessingConfig",

    "PreprocessingError",

    "ValidationError",

    "FeatureEngineeringError",

    "Preprocessor",

    "MinMaxScaler",

    "StandardScaler",

    "validate_dataframe",

    "validate_ohlcv",

    "validate_features",

    "train_test_split",

    "split_features_target",

    "numeric_features",

    "create_sequences",

    "prepare_training_data",

    "feature_summary",

    "correlation_matrix",

    "preprocess_dataset",

    "dataset_information",

    "validation_report",

    "clear_cache",

    "version",

]

# ==========================================================
# END OF preprocessing.py
# Version 2.0
# ==========================================================