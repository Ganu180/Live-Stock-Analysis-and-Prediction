"""
=========================================================
Live Stock Analysis & Prediction
File    : prediction.py
Version : 3.0
Part    : 1
Python  : 3.12
=========================================================
"""

from __future__ import annotations

import logging
import warnings
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import joblib
import numpy as np
import pandas as pd

from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import (
    mean_absolute_error,
    mean_squared_error,
    r2_score,
)
from sklearn.model_selection import train_test_split

warnings.filterwarnings("ignore")

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

VERSION = "3.0"

MODEL_VERSION = "3.0"

MODEL_NAME = "Random Forest Regressor"

DEFAULT_RANDOM_STATE = 42

DEFAULT_TEST_SIZE = 0.20

DEFAULT_ESTIMATORS = 300

DEFAULT_MAX_DEPTH = 12

DEFAULT_MIN_SAMPLES_SPLIT = 5

DEFAULT_MIN_SAMPLES_LEAF = 2

TARGET_COLUMN = "Close"

# ==========================================================
# PROJECT PATHS
# ==========================================================

BASE_DIR = Path(__file__).resolve().parent.parent

MODEL_DIR = BASE_DIR / "models"

MODEL_DIR.mkdir(
    parents=True,
    exist_ok=True,
)

MODEL_FILE = MODEL_DIR / "random_forest_model.pkl"

# ==========================================================
# SINGLE FEATURE SCHEMA
# ==========================================================
# Every module in the project MUST use this list.

FEATURE_COLUMNS = [

    "Open",

    "High",

    "Low",

    "Volume",

    "SMA20",

    "SMA50",

    "EMA20",

    "EMA50",

    "RSI",

    "MACD",

    "MACD_SIGNAL",

    "MACD_DIFF",

    "ADX",

    "ATR",

    "OBV",

]

# ==========================================================
# EXCEPTIONS
# ==========================================================

class PredictionError(Exception):
    """Base prediction exception."""


class ModelNotFoundError(PredictionError):
    """Model file not found."""


class FeatureMismatchError(PredictionError):
    """Input features do not match training."""


class TrainingError(PredictionError):
    """Training failed."""


class PredictionValidationError(PredictionError):
    """Invalid prediction input."""


# ==========================================================
# CONFIGURATION
# ==========================================================

@dataclass(slots=True)
class PredictionConfig:

    random_state: int = DEFAULT_RANDOM_STATE

    test_size: float = DEFAULT_TEST_SIZE

    n_estimators: int = DEFAULT_ESTIMATORS

    max_depth: int = DEFAULT_MAX_DEPTH

    min_samples_split: int = DEFAULT_MIN_SAMPLES_SPLIT

    min_samples_leaf: int = DEFAULT_MIN_SAMPLES_LEAF

    target_column: str = TARGET_COLUMN

    auto_save: bool = True

    auto_train: bool = True


# ==========================================================
# HELPER FUNCTIONS
# ==========================================================

def model_exists() -> bool:
    """
    Check whether the Random Forest model exists.
    """

    return MODEL_FILE.exists()


def model_path() -> Path:
    """
    Return model path.
    """

    return MODEL_FILE


def get_feature_columns() -> list[str]:
    """
    Return feature schema.
    """

    return FEATURE_COLUMNS.copy()


def validate_dataframe(
    dataframe: pd.DataFrame,
) -> bool:
    """
    Basic dataframe validation.
    """

    if dataframe is None:
        return False

    if dataframe.empty:
        return False

    return True


def validate_target(
    dataframe: pd.DataFrame,
    target: str = TARGET_COLUMN,
) -> bool:
    """
    Validate target column.
    """

    return target in dataframe.columns


# ==========================================================
# END OF PART 1
# ==========================================================

# ==========================================================
# DATA VALIDATION
# ==========================================================

def validate_feature_columns(
    dataframe: pd.DataFrame,
    required_columns: list[str] | None = None,
) -> bool:
    """
    Validate feature columns.
    """

    if required_columns is None:

        required_columns = FEATURE_COLUMNS

    if not validate_dataframe(dataframe):

        return False

    missing = [

        column

        for column in required_columns

        if column not in dataframe.columns

    ]

    if missing:

        logger.error(
            "Missing feature columns: %s",
            ", ".join(missing),
        )

        return False

    return True


def validate_training_dataframe(
    dataframe: pd.DataFrame,
) -> bool:
    """
    Validate dataframe for training.
    """

    if not validate_dataframe(dataframe):

        return False

    if not validate_feature_columns(dataframe):

        return False

    if not validate_target(dataframe):

        logger.error(
            "Target column '%s' missing.",
            TARGET_COLUMN,
        )

        return False

    return True


# ==========================================================
# FEATURE ALIGNMENT
# ==========================================================

def align_features(
    dataframe: pd.DataFrame,
    feature_columns: list[str],
) -> pd.DataFrame:
    """
    Align dataframe with training features.

    Missing columns are added.
    Extra columns are removed.
    """

    try:

        df = dataframe.copy()

        for column in feature_columns:

            if column not in df.columns:

                logger.warning(
                    "Adding missing feature: %s",
                    column,
                )

                df[column] = 0.0

        df = df.reindex(
            columns=feature_columns,
            fill_value=0.0,
        )

        return df

    except Exception as error:

        logger.exception(error)

        raise FeatureMismatchError(
            "Unable to align feature columns."
        ) from error


# ==========================================================
# DATA CLEANING
# ==========================================================

def clean_dataframe(
    dataframe: pd.DataFrame,
) -> pd.DataFrame:
    """
    Clean prediction dataframe.
    """

    try:

        df = dataframe.copy()

        df.replace(
            [np.inf, -np.inf],
            np.nan,
            inplace=True,
        )

        numeric = df.select_dtypes(
            include=np.number,
        ).columns

        df[numeric] = df[numeric].fillna(
            df[numeric].median()
        )

        df.ffill(inplace=True)

        df.bfill(inplace=True)

        df.drop_duplicates(
            inplace=True,
        )

        return df

    except Exception as error:

        logger.exception(error)

        raise PredictionValidationError(
            "Failed to clean dataframe."
        ) from error


# ==========================================================
# FEATURE PREPARATION
# ==========================================================

def prepare_training_data(
    dataframe: pd.DataFrame,
) -> tuple[pd.DataFrame, pd.Series]:
    """
    Prepare X and y for training.
    """

    if not validate_training_dataframe(
        dataframe,
    ):

        raise PredictionValidationError(
            "Training dataframe is invalid."
        )

    df = clean_dataframe(
        dataframe,
    )

    X = df.loc[
        :,
        FEATURE_COLUMNS,
    ].copy()

    y = df.loc[
        :,
        TARGET_COLUMN,
    ].copy()

    return X, y


def prepare_prediction_data(
    dataframe: pd.DataFrame,
    trained_features: list[str],
) -> pd.DataFrame:
    """
    Prepare dataframe for prediction.
    """

    if not validate_dataframe(
        dataframe,
    ):

        raise PredictionValidationError(
            "Prediction dataframe is empty."
        )

    df = clean_dataframe(
        dataframe,
    )

    df = align_features(
        df,
        trained_features,
    )

    return df


# ==========================================================
# MODEL PACKAGE
# ==========================================================

def create_model_package(
    model: RandomForestRegressor,
    features: list[str],
    metrics: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """
    Create model package.
    """

    return {

        "version": MODEL_VERSION,

        "model_type": MODEL_NAME,

        "model": model,

        "features": features,

        "metrics": metrics or {},

    }


# ==========================================================
# END OF PART 2
# ==========================================================

# ==========================================================
# STOCK PREDICTION MODEL
# ==========================================================

class StockPredictionModel:
    """
    Random Forest prediction model.
    """

    def __init__(
        self,
        config: PredictionConfig | None = None,
    ) -> None:

        self.config = config or PredictionConfig()

        self.model: RandomForestRegressor | None = None

        self.feature_columns: list[str] = FEATURE_COLUMNS.copy()

        self.metrics: dict[str, Any] = {}

        self.is_trained: bool = False

        logger.info(
            "%s Version %s initialized.",
            MODEL_NAME,
            VERSION,
        )

    # ------------------------------------------------------

    def create_model(
        self,
    ) -> RandomForestRegressor:
        """
        Create Random Forest model.
        """

        return RandomForestRegressor(

            n_estimators=self.config.n_estimators,

            max_depth=self.config.max_depth,

            min_samples_split=self.config.min_samples_split,

            min_samples_leaf=self.config.min_samples_leaf,

            random_state=self.config.random_state,

            n_jobs=-1,

        )

    # ------------------------------------------------------

    def save(
        self,
    ) -> None:
        """
        Save model package.
        """

        if self.model is None:

            raise ModelNotFoundError(
                "No model available to save."
            )

        package = create_model_package(

            model=self.model,

            features=self.feature_columns,

            metrics=self.metrics,

        )

        joblib.dump(

            package,

            MODEL_FILE,

        )

        logger.info(

            "Model saved: %s",

            MODEL_FILE,

        )

    # ------------------------------------------------------

    def load(
        self,
    ) -> bool:
        """
        Load saved model.
        """

        if not MODEL_FILE.exists():

            logger.warning(

                "Model file not found."

            )

            return False

        package = joblib.load(

            MODEL_FILE

        )

        self.model = package["model"]

        self.feature_columns = package.get(

            "features",

            FEATURE_COLUMNS,

        )

        self.metrics = package.get(

            "metrics",

            {},

        )

        self.is_trained = True

        logger.info(

            "Model loaded successfully."

        )

        return True

    # ------------------------------------------------------

    def fit(
        self,
        dataframe: pd.DataFrame,
    ) -> dict[str, float]:
        """
        Train Random Forest.
        """

        try:

            X, y = prepare_training_data(

                dataframe

            )

            self.feature_columns = list(

                X.columns

            )

            X_train, X_test, y_train, y_test = train_test_split(

                X,

                y,

                test_size=self.config.test_size,

                random_state=self.config.random_state,

            )

            self.model = self.create_model()

            self.model.fit(

                X_train,

                y_train,

            )

            predictions = self.model.predict(

                X_test

            )

            self.metrics = {

                "mae": float(

                    mean_absolute_error(

                        y_test,

                        predictions,

                    )

                ),

                "mse": float(

                    mean_squared_error(

                        y_test,

                        predictions,

                    )

                ),

                "rmse": float(

                    np.sqrt(

                        mean_squared_error(

                            y_test,

                            predictions,

                        )

                    )

                ),

                "r2": float(

                    r2_score(

                        y_test,

                        predictions,

                    )

                ),

            }

            self.is_trained = True

            if self.config.auto_save:

                self.save()

            logger.info(

                "Training completed successfully."

            )

            return self.metrics

        except Exception as error:

            logger.exception(error)

            raise TrainingError(

                "Random Forest training failed."

            ) from error


# ==========================================================
# END OF PART 3
# ==========================================================

# ==========================================================
# PREDICTION METHODS
# ==========================================================

    def predict(
        self,
        dataframe: pd.DataFrame,
    ) -> np.ndarray:
        """
        Predict stock prices.
        """

        try:

            if self.model is None:

                if not self.load():

                    if self.config.auto_train:

                        logger.info(
                            "No trained model found. Training model..."
                        )

                        self.fit(dataframe)

                    else:

                        raise ModelNotFoundError(
                            "Random Forest model not found."
                        )

            X = prepare_prediction_data(

                dataframe,

                self.feature_columns,

            )

            predictions = self.model.predict(X)

            return predictions

        except Exception as error:

            logger.exception(error)

            raise PredictionError(
                "Prediction failed."
            ) from error

    # ------------------------------------------------------

    def predict_latest(
        self,
        dataframe: pd.DataFrame,
    ) -> float:
        """
        Predict latest stock price.
        """

        prediction = self.predict(dataframe)

        return float(prediction[-1])

    # ------------------------------------------------------

    def predict_batch(
        self,
        datasets: dict[str, pd.DataFrame],
    ) -> dict[str, float]:
        """
        Predict multiple stocks.
        """

        results: dict[str, float] = {}

        for ticker, df in datasets.items():

            try:

                results[ticker] = self.predict_latest(df)

            except Exception as error:

                logger.exception(error)

                results[ticker] = np.nan

        return results

# ==========================================================
# FEATURE IMPORTANCE
# ==========================================================

    def feature_importance(
        self,
    ) -> pd.DataFrame:
        """
        Return feature importance.
        """

        if self.model is None:

            raise ModelNotFoundError(
                "Model not loaded."
            )

        importance = pd.DataFrame({

            "Feature": self.feature_columns,

            "Importance": self.model.feature_importances_,

        })

        importance.sort_values(

            by="Importance",

            ascending=False,

            inplace=True,

        )

        importance.reset_index(

            drop=True,

            inplace=True,

        )

        return importance

# ==========================================================
# MODEL INFORMATION
# ==========================================================

    def model_information(
        self,
    ) -> dict[str, Any]:
        """
        Return model information.
        """

        return {

            "version": MODEL_VERSION,

            "model_name": MODEL_NAME,

            "trained": self.is_trained,

            "model_file": str(MODEL_FILE),

            "features": self.feature_columns,

            "feature_count": len(

                self.feature_columns

            ),

            "metrics": self.metrics,

        }

# ==========================================================
# MODEL UTILITIES
# ==========================================================

    def delete_model(
        self,
    ) -> bool:
        """
        Delete saved model.
        """

        try:

            if MODEL_FILE.exists():

                MODEL_FILE.unlink()

                logger.info(
                    "Model deleted."
                )

            self.model = None

            self.is_trained = False

            self.metrics.clear()

            return True

        except Exception as error:

            logger.exception(error)

            return False


# ==========================================================
# END OF PART 4
# ==========================================================

# ==========================================================
# AUTO TRAINING & FORECASTING
# ==========================================================

    def ensure_model(
        self,
        dataframe: pd.DataFrame | None = None,
    ) -> bool:
        """
        Ensure a trained model is available.
        """

        try:

            if self.model is not None:

                return True

            if self.load():

                return True

            if dataframe is None:

                raise ModelNotFoundError(
                    "No model found and no training data supplied."
                )

            if not self.config.auto_train:

                raise ModelNotFoundError(
                    "Automatic training is disabled."
                )

            logger.info(
                "Training a new Random Forest model..."
            )

            self.fit(dataframe)

            return True

        except Exception as error:

            logger.exception(error)

            raise

    # ------------------------------------------------------

    def forecast(
        self,
        dataframe: pd.DataFrame,
        periods: int = 5,
    ) -> list[float]:
        """
        Forecast future prices.

        Uses recursive prediction.
        """

        try:

            if periods <= 0:

                return []

            self.ensure_model(dataframe)

            df = dataframe.copy()

            forecasts: list[float] = []

            for _ in range(periods):

                prediction = float(

                    self.predict_latest(df)

                )

                forecasts.append(prediction)

                next_row = df.iloc[-1].copy()

                if TARGET_COLUMN in next_row.index:

                    next_row[TARGET_COLUMN] = prediction

                df = pd.concat(

                    [

                        df,

                        pd.DataFrame(

                            [next_row],

                            columns=df.columns,

                        ),

                    ],

                    ignore_index=True,

                )

            return forecasts

        except Exception as error:

            logger.exception(error)

            raise PredictionError(
                "Forecast failed."
            ) from error


# ==========================================================
# MODULE HELPERS
# ==========================================================

def load_prediction_model() -> StockPredictionModel:
    """
    Create prediction model and
    automatically load the saved model.
    """

    model = StockPredictionModel()

    model.load()

    return model


def train_prediction_model(
    dataframe: pd.DataFrame,
) -> StockPredictionModel:
    """
    Train and return a prediction model.
    """

    model = StockPredictionModel()

    model.fit(dataframe)

    return model


def predict_dataframe(
    dataframe: pd.DataFrame,
) -> np.ndarray:
    """
    Quick prediction helper.
    """

    model = load_prediction_model()

    model.ensure_model(dataframe)

    return model.predict(dataframe)


def predict_latest_price(
    dataframe: pd.DataFrame,
) -> float:
    """
    Predict latest price.
    """

    model = load_prediction_model()

    model.ensure_model(dataframe)

    return model.predict_latest(dataframe)


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

    "MODEL_VERSION",

    "MODEL_NAME",

    "FEATURE_COLUMNS",

    "PredictionConfig",

    "PredictionError",

    "ModelNotFoundError",

    "FeatureMismatchError",

    "TrainingError",

    "PredictionValidationError",

    "StockPredictionModel",

    "load_prediction_model",

    "train_prediction_model",

    "predict_dataframe",

    "predict_latest_price",

    "model_exists",

    "model_path",

    "version",

]

# ==========================================================
# END OF prediction.py
# Version 3.0
# ==========================================================