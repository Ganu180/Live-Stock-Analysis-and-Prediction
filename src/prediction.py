"""
==========================================================
Live Stock Analysis & Prediction
Prediction Module
Version : 2.0
==========================================================
"""

import os
import joblib
import warnings
import numpy as np
import pandas as pd

from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import (
    mean_absolute_error,
    mean_squared_error,
    r2_score,
)

warnings.filterwarnings("ignore")

# ==========================================================
# MODEL DIRECTORY
# ==========================================================

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

MODEL_DIR = os.path.join(BASE_DIR, "models")

os.makedirs(MODEL_DIR, exist_ok=True)

RF_MODEL_PATH = os.path.join(
    MODEL_DIR,
    "random_forest_model.pkl"
)

SCALER_PATH = os.path.join(
    MODEL_DIR,
    "scaler.pkl"
)

LSTM_MODEL_PATH = os.path.join(
    MODEL_DIR,
    "lstm_model.keras"
)

# ==========================================================
# REQUIRED FEATURES
# ==========================================================

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

    "OBV"

]

TARGET_COLUMN = "Close"

# ==========================================================
# VALIDATE DATA
# ==========================================================

def validate_dataframe(df: pd.DataFrame) -> bool:
    """
    Validate dataframe before prediction.
    """

    if df is None:
        return False

    if df.empty:
        return False

    for column in FEATURE_COLUMNS:

        if column not in df.columns:
            return False

    if TARGET_COLUMN not in df.columns:
        return False

    return True

# ==========================================================
# PREPARE FEATURES
# ==========================================================

def prepare_features(df: pd.DataFrame):
    """
    Returns X and y for training.
    """

    if not validate_dataframe(df):

        raise ValueError(
            "Dataframe does not contain required columns."
        )

    data = df.copy()

    data = data.dropna()

    X = data[FEATURE_COLUMNS]

    y = data[TARGET_COLUMN]

    return X, y

# ==========================================================
# LOAD RANDOM FOREST MODEL
# ==========================================================

def load_random_forest():

    if not os.path.exists(RF_MODEL_PATH):

        return None

    try:

        model = joblib.load(RF_MODEL_PATH)

        return model

    except Exception:

        return None

# ==========================================================
# SAVE RANDOM FOREST MODEL
# ==========================================================

def save_random_forest(model):

    joblib.dump(

        model,

        RF_MODEL_PATH

    )

# ==========================================================
# LOAD LSTM MODEL
# ==========================================================

def load_lstm():

    if not os.path.exists(LSTM_MODEL_PATH):

        return None

    try:

        try:
            import importlib

            tensorflow = importlib.import_module("tensorflow")
            load_model = tensorflow.keras.models.load_model
        except Exception:
            from keras.models import load_model

        model = load_model(

            LSTM_MODEL_PATH,

            compile=False

        )

        return model

    except Exception:

        return None
# ==========================================================
# PART 2 : RANDOM FOREST TRAINING, EVALUATION & MODEL SAVING
# ==========================================================

from pathlib import Path
import joblib

from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import (
    mean_absolute_error,
    mean_squared_error,
    r2_score,
)


class StockPredictionModel:
    """
    Random Forest based prediction model.
    """

    def __init__(
        self,
        model_dir: str = "models",
        model_name: str = "random_forest_model.pkl",
        random_state: int = 42,
    ):
        self.random_state = random_state

        self.model_dir = Path(model_dir)
        self.model_dir.mkdir(parents=True, exist_ok=True)

        self.model_path = self.model_dir / model_name

        self.model = RandomForestRegressor(
            n_estimators=300,
            max_depth=12,
            min_samples_split=5,
            min_samples_leaf=2,
            random_state=self.random_state,
            n_jobs=-1,
        )

        self.metrics = {}
        self.feature_columns = []

    # ------------------------------------------------------
    # Train/Test Split
    # ------------------------------------------------------
    def split_data(
        self,
        X,
        y,
        test_size: float = 0.2,
    ):
        try:
            return train_test_split(
                X,
                y,
                test_size=test_size,
                random_state=self.random_state,
                shuffle=False,
            )

        except Exception as e:
            raise RuntimeError(
                f"Failed to split dataset: {e}"
            ) from e

    # ------------------------------------------------------
    # Train Model
    # ------------------------------------------------------
    def train(
        self,
        X_train,
        y_train,
    ):
        try:
            self.feature_columns = list(X_train.columns)

            self.model.fit(X_train, y_train)

            self.save_model()

            return self.model

        except Exception as e:
            raise RuntimeError(
                f"Model training failed: {e}"
            ) from e

    # ------------------------------------------------------
    # Evaluate Model
    # ------------------------------------------------------
    def evaluate(
        self,
        X_test,
        y_test,
    ):
        try:
            predictions = self.model.predict(X_test)

            mae = mean_absolute_error(y_test, predictions)

            rmse = mean_squared_error(
                y_test,
                predictions,
                squared=False,
            )

            r2 = r2_score(
                y_test,
                predictions,
            )

            self.metrics = {
                "MAE": float(mae),
                "RMSE": float(rmse),
                "R2": float(r2),
            }

            return {
                "predictions": predictions,
                "metrics": self.metrics,
            }

        except Exception as e:
            raise RuntimeError(
                f"Evaluation failed: {e}"
            ) from e

    # ------------------------------------------------------
    # Save Model
    # ------------------------------------------------------
    def save_model(self):
        try:
            model_package = {
                "model": self.model,
                "features": self.feature_columns,
                "metrics": self.metrics,
            }

            joblib.dump(
                model_package,
                self.model_path,
            )

            return self.model_path

        except Exception as e:
            raise RuntimeError(
                f"Unable to save model: {e}"
            ) from e

    # ------------------------------------------------------
    # Load Existing Model
    # ------------------------------------------------------
    def load_model(self):
        try:
            if not self.model_path.exists():
                raise FileNotFoundError(
                    f"Model not found: {self.model_path}"
                )

            package = joblib.load(self.model_path)

            self.model = package["model"]
            self.feature_columns = package.get(
                "features",
                [],
            )
            self.metrics = package.get(
                "metrics",
                {},
            )

            return self.model

        except Exception as e:
            raise RuntimeError(
                f"Unable to load model: {e}"
            ) from e    
# ==========================================================
# PART 3 : PREDICTION, FORECASTING & FEATURE IMPORTANCE
# ==========================================================

import numpy as np
import pandas as pd


    # ------------------------------------------------------
    # Predict
    # ------------------------------------------------------
    def predict(self, X):
        """
        Predict values using the trained model.
        """
        try:
            if self.model is None:
                self.load_model()

            X = X.copy()

            # Ensure feature order matches training
            if self.feature_columns:
                X = X[self.feature_columns]

            predictions = self.model.predict(X)

            return np.asarray(predictions)

        except Exception as e:
            raise RuntimeError(
                f"Prediction failed: {e}"
            ) from e

    # ------------------------------------------------------
    # Predict Single Record
    # ------------------------------------------------------
    def predict_single(self, features):
        """
        Predict a single sample.
        """
        try:
            if isinstance(features, dict):
                df = pd.DataFrame([features])

            elif isinstance(features, pd.Series):
                df = features.to_frame().T

            elif isinstance(features, pd.DataFrame):
                df = features.copy()

            else:
                raise ValueError(
                    "Input must be dict, Series or DataFrame."
                )

            prediction = self.predict(df)

            return float(prediction[0])

        except Exception as e:
            raise RuntimeError(
                f"Single prediction failed: {e}"
            ) from e

    # ------------------------------------------------------
    # Multi-day Forecast
    # ------------------------------------------------------
    def forecast(self, latest_features, days=7):
        """
        Recursive forecasting using the latest feature row.
        """
        try:
            if self.model is None:
                self.load_model()

            current = latest_features.copy()

            if isinstance(current, pd.Series):
                current = current.to_frame().T

            forecasts = []

            for _ in range(days):

                value = float(self.predict(current)[0])

                forecasts.append(value)

                # Update Close column if present
                if "Close" in current.columns:
                    current.loc[current.index[0], "Close"] = value

                # Update lag features if available
                lag_columns = sorted(
                    [c for c in current.columns if c.startswith("Lag_")],
                    reverse=True
                )

                if lag_columns:
                    previous = value

                    for lag in lag_columns:
                        temp = current.loc[current.index[0], lag]
                        current.loc[current.index[0], lag] = previous
                        previous = temp

            return forecasts

        except Exception as e:
            raise RuntimeError(
                f"Forecast failed: {e}"
            ) from e

    # ------------------------------------------------------
    # Feature Importance
    # ------------------------------------------------------
    def feature_importance(self):
        """
        Return feature importance values.
        """
        try:
            if self.model is None:
                self.load_model()

            importance = pd.DataFrame(
                {
                    "Feature": self.feature_columns,
                    "Importance": self.model.feature_importances_,
                }
            )

            importance = importance.sort_values(
                by="Importance",
                ascending=False,
            ).reset_index(drop=True)

            return importance

        except Exception as e:
            raise RuntimeError(
                f"Unable to compute feature importance: {e}"
            ) from e

    # ------------------------------------------------------
    # Model Information
    # ------------------------------------------------------
    def get_model_info(self):
        """
        Return model metadata.
        """
        try:
            return {
                "model_type": "Random Forest Regressor",
                "n_estimators": self.model.n_estimators,
                "max_depth": self.model.max_depth,
                "features": self.feature_columns,
                "metrics": self.metrics,
                "model_path": str(self.model_path),
            }

        except Exception as e:
            raise RuntimeError(
                f"Unable to fetch model information: {e}"
            ) from e
# ==========================================================
# PART 4 : UTILITIES, COMPLETE TRAINING PIPELINE & EXPORTS
# ==========================================================

    # ------------------------------------------------------
    # Complete Training Pipeline
    # ------------------------------------------------------
    def fit(
        self,
        X,
        y,
        test_size: float = 0.20,
    ):
        """
        Complete training pipeline.
        """
        try:
            (
                X_train,
                X_test,
                y_train,
                y_test,
            ) = self.split_data(
                X,
                y,
                test_size=test_size,
            )

            self.train(
                X_train,
                y_train,
            )

            evaluation = self.evaluate(
                X_test,
                y_test,
            )

            return {
                "model": self.model,
                "metrics": evaluation["metrics"],
                "predictions": evaluation["predictions"],
                "X_train": X_train,
                "X_test": X_test,
                "y_train": y_train,
                "y_test": y_test,
            }

        except Exception as e:
            raise RuntimeError(
                f"Training pipeline failed: {e}"
            ) from e

    # ------------------------------------------------------
    # Batch Prediction
    # ------------------------------------------------------
    def predict_dataframe(
        self,
        dataframe,
    ):
        """
        Predict an entire DataFrame and append predictions.
        """
        try:
            df = dataframe.copy()

            predictions = self.predict(df)

            df["Prediction"] = predictions

            return df

        except Exception as e:
            raise RuntimeError(
                f"Batch prediction failed: {e}"
            ) from e

    # ------------------------------------------------------
    # Export Predictions
    # ------------------------------------------------------
    def export_predictions(
        self,
        dataframe,
        output_file="predictions.csv",
    ):
        """
        Export prediction results to CSV.
        """
        try:
            df = self.predict_dataframe(dataframe)

            df.to_csv(
                output_file,
                index=False,
            )

            return output_file

        except Exception as e:
            raise RuntimeError(
                f"Export failed: {e}"
            ) from e

    # ------------------------------------------------------
    # Reset Model
    # ------------------------------------------------------
    def reset(self):
        """
        Reset model state.
        """
        try:
            self.model = RandomForestRegressor(
                n_estimators=300,
                max_depth=12,
                min_samples_split=5,
                min_samples_leaf=2,
                random_state=self.random_state,
                n_jobs=-1,
            )

            self.metrics = {}
            self.feature_columns = []

        except Exception as e:
            raise RuntimeError(
                f"Reset failed: {e}"
            ) from e

    # ------------------------------------------------------
    # Model Exists
    # ------------------------------------------------------
    def model_exists(self):
        """
        Check whether a saved model exists.
        """
        return self.model_path.exists()


# ==========================================================
# Convenience Function
# ==========================================================

def train_random_forest(
    X,
    y,
    test_size: float = 0.20,
):
    """
    Train a Random Forest model in one call.
    """
    try:
        predictor = StockPredictionModel()

        results = predictor.fit(
            X,
            y,
            test_size=test_size,
        )

        return predictor, results

    except Exception as e:
        raise RuntimeError(
            f"Random Forest training failed: {e}"
        ) from e


# ==========================================================
# Module Exports
# ==========================================================

__all__ = [
    "StockPredictionModel",
    "train_random_forest",
]                