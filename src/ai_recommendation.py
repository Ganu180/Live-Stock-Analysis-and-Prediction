"""
=========================================================
Live Stock Analysis & Prediction
AI Recommendation Engine
Version : 2.0
Python : 3.12
=========================================================
"""

from __future__ import annotations

import logging
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional

import numpy as np
import pandas as pd

# =========================================================
# LOGGING
# =========================================================

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)

logger = logging.getLogger(__name__)

# =========================================================
# CONSTANTS
# =========================================================

VERSION = "2.0"

BUY_THRESHOLD = 70
SELL_THRESHOLD = 35

MIN_CONFIDENCE = 0.0
MAX_CONFIDENCE = 100.0

# =========================================================
# ENUMS
# =========================================================

class RecommendationType(str, Enum):
    BUY = "BUY"
    STRONG_BUY = "STRONG BUY"
    HOLD = "HOLD"
    SELL = "SELL"
    STRONG_SELL = "STRONG SELL"


class TrendType(str, Enum):
    BULLISH = "Bullish"
    BEARISH = "Bearish"
    SIDEWAYS = "Sideways"
    UNKNOWN = "Unknown"


class RiskLevel(str, Enum):
    LOW = "Low"
    MEDIUM = "Medium"
    HIGH = "High"


# =========================================================
# DATA CLASSES
# =========================================================

@dataclass(slots=True)
class IndicatorResult:
    name: str
    score: float
    signal: str
    message: str


@dataclass(slots=True)
class RecommendationResult:
    recommendation: RecommendationType
    score: float
    confidence: float
    trend: TrendType
    risk: RiskLevel
    reasons: List[str] = field(default_factory=list)
    indicators: Dict[str, IndicatorResult] = field(default_factory=dict)


# =========================================================
# VALIDATION UTILITIES
# =========================================================

def validate_dataframe(
    dataframe: pd.DataFrame
) -> bool:
    """
    Validate stock dataframe.
    """
    if dataframe is None:
        return False

    if not isinstance(dataframe, pd.DataFrame):
        return False

    if dataframe.empty:
        return False

    required = {
        "Open",
        "High",
        "Low",
        "Close",
        "Volume"
    }

    return required.issubset(dataframe.columns)


def latest_close(
    dataframe: pd.DataFrame
) -> float:
    """
    Return latest closing price.
    """
    try:
        return float(dataframe["Close"].iloc[-1])
    except Exception:
        return 0.0


# =========================================================
# AI RECOMMENDATION ENGINE
# =========================================================

class AIRecommendationEngine:
    """
    AI Recommendation Engine Version 2.0
    """

    def __init__(
        self,
        dataframe: pd.DataFrame
    ) -> None:

        if not validate_dataframe(dataframe):
            raise ValueError(
                "Invalid stock dataframe."
            )

        self.df = dataframe.copy()

        self.score = 50.0

        self.confidence = 50.0

        self.reasons: List[str] = []

        self.indicators: Dict[
            str,
            IndicatorResult
        ] = {}

        logger.info(
            "AI Recommendation Engine initialized."
        )

    # -----------------------------------------------------

    def reset(self) -> None:
        """
        Reset recommendation values.
        """

        self.score = 50.0

        self.confidence = 50.0

        self.reasons.clear()

        self.indicators.clear()

    # -----------------------------------------------------

    def add_score(
        self,
        points: float,
        reason: str
    ) -> None:
        """
        Update recommendation score.
        """

        self.score += points

        self.score = max(
            0.0,
            min(
                100.0,
                self.score
            )
        )

        self.reasons.append(reason)

    # -----------------------------------------------------

    def add_indicator(
        self,
        name: str,
        score: float,
        signal: str,
        message: str
    ) -> None:
        """
        Store indicator result.
        """

        self.indicators[name] = IndicatorResult(
            name=name,
            score=score,
            signal=signal,
            message=message
        )

    # -----------------------------------------------------

    @property
    def close(self) -> pd.Series:
        return self.df["Close"]

    @property
    def high(self) -> pd.Series:
        return self.df["High"]

    @property
    def low(self) -> pd.Series:
        return self.df["Low"]

    @property
    def volume(self) -> pd.Series:
        return self.df["Volume"]

# =========================================================
# END OF PART 1
# =========================================================
# =========================================================
# TECHNICAL INDICATOR ANALYSIS
# =========================================================

    def analyze_rsi(
        self,
        rsi: float
    ) -> None:
        """
        Analyze Relative Strength Index.
        """

        try:
            rsi = float(rsi)

            if rsi <= 30:
                self.add_score(
                    18,
                    f"RSI ({rsi:.2f}) indicates oversold conditions."
                )

                self.add_indicator(
                    "RSI",
                    18,
                    "BUY",
                    "Stock appears oversold."
                )

            elif rsi >= 70:
                self.add_score(
                    -18,
                    f"RSI ({rsi:.2f}) indicates overbought conditions."
                )

                self.add_indicator(
                    "RSI",
                    -18,
                    "SELL",
                    "Stock appears overbought."
                )

            else:
                self.add_indicator(
                    "RSI",
                    0,
                    "NEUTRAL",
                    "RSI is in a healthy range."
                )

        except Exception as error:
            logger.exception(error)

    # -----------------------------------------------------

    def analyze_macd(
        self,
        macd: float,
        signal: float
    ) -> None:
        """
        Analyze MACD.
        """

        try:

            if macd > signal:

                self.add_score(
                    15,
                    "MACD bullish crossover."
                )

                self.add_indicator(
                    "MACD",
                    15,
                    "BUY",
                    "Bullish momentum detected."
                )

            elif macd < signal:

                self.add_score(
                    -15,
                    "MACD bearish crossover."
                )

                self.add_indicator(
                    "MACD",
                    -15,
                    "SELL",
                    "Bearish momentum detected."
                )

            else:

                self.add_indicator(
                    "MACD",
                    0,
                    "NEUTRAL",
                    "MACD is neutral."
                )

        except Exception as error:
            logger.exception(error)

    # -----------------------------------------------------

    def analyze_sma(
        self,
        sma20: float,
        sma50: float
    ) -> None:
        """
        Analyze SMA crossover.
        """

        try:

            if sma20 > sma50:

                self.add_score(
                    10,
                    "20 SMA is above 50 SMA."
                )

                self.add_indicator(
                    "SMA",
                    10,
                    "BUY",
                    "Bullish SMA crossover."
                )

            elif sma20 < sma50:

                self.add_score(
                    -10,
                    "20 SMA is below 50 SMA."
                )

                self.add_indicator(
                    "SMA",
                    -10,
                    "SELL",
                    "Bearish SMA crossover."
                )

            else:

                self.add_indicator(
                    "SMA",
                    0,
                    "NEUTRAL",
                    "SMA trend is neutral."
                )

        except Exception as error:
            logger.exception(error)

    # -----------------------------------------------------

    def analyze_ema(
        self,
        ema20: float,
        ema50: float
    ) -> None:
        """
        Analyze EMA crossover.
        """

        try:

            if ema20 > ema50:

                self.add_score(
                    10,
                    "20 EMA is above 50 EMA."
                )

                self.add_indicator(
                    "EMA",
                    10,
                    "BUY",
                    "Bullish EMA crossover."
                )

            elif ema20 < ema50:

                self.add_score(
                    -10,
                    "20 EMA is below 50 EMA."
                )

                self.add_indicator(
                    "EMA",
                    -10,
                    "SELL",
                    "Bearish EMA crossover."
                )

            else:

                self.add_indicator(
                    "EMA",
                    0,
                    "NEUTRAL",
                    "EMA trend is neutral."
                )

        except Exception as error:
            logger.exception(error)

    # -----------------------------------------------------

    def analyze_bollinger(
        self,
        price: float,
        upper_band: float,
        lower_band: float
    ) -> None:
        """
        Analyze Bollinger Bands.
        """

        try:

            if price <= lower_band:

                self.add_score(
                    12,
                    "Price is near lower Bollinger Band."
                )

                self.add_indicator(
                    "Bollinger Bands",
                    12,
                    "BUY",
                    "Possible price reversal upward."
                )

            elif price >= upper_band:

                self.add_score(
                    -12,
                    "Price is near upper Bollinger Band."
                )

                self.add_indicator(
                    "Bollinger Bands",
                    -12,
                    "SELL",
                    "Possible price reversal downward."
                )

            else:

                self.add_indicator(
                    "Bollinger Bands",
                    0,
                    "NEUTRAL",
                    "Price is within Bollinger Bands."
                )

        except Exception as error:
            logger.exception(error)

    # -----------------------------------------------------

    def analyze_volume(
        self,
        current_volume: float,
        average_volume: float
    ) -> None:
        """
        Analyze trading volume.
        """

        try:

            if current_volume > average_volume * 1.5:

                self.add_score(
                    8,
                    "Trading volume is significantly above average."
                )

                self.add_indicator(
                    "Volume",
                    8,
                    "BUY",
                    "Strong market participation."
                )

            elif current_volume < average_volume * 0.5:

                self.add_score(
                    -5,
                    "Trading volume is weak."
                )

                self.add_indicator(
                    "Volume",
                    -5,
                    "SELL",
                    "Weak market participation."
                )

            else:

                self.add_indicator(
                    "Volume",
                    0,
                    "NEUTRAL",
                    "Normal trading volume."
                )

        except Exception as error:
            logger.exception(error)


# =========================================================
# END OF PART 2
# =========================================================

# =========================================================
# TREND & MOMENTUM ANALYSIS
# =========================================================

    def analyze_price_trend(self) -> None:
        """
        Analyze short-term and long-term price trend.
        """

        try:

            sma20 = self.close.rolling(20).mean().iloc[-1]
            sma50 = self.close.rolling(50).mean().iloc[-1]
            current_price = self.close.iloc[-1]

            if current_price > sma20 > sma50:

                self.add_score(
                    15,
                    "Strong bullish price trend."
                )

                self.add_indicator(
                    "Trend",
                    15,
                    "BUY",
                    "Price is above both moving averages."
                )

            elif current_price < sma20 < sma50:

                self.add_score(
                    -15,
                    "Strong bearish price trend."
                )

                self.add_indicator(
                    "Trend",
                    -15,
                    "SELL",
                    "Price is below both moving averages."
                )

            else:

                self.add_indicator(
                    "Trend",
                    0,
                    "NEUTRAL",
                    "Mixed market trend."
                )

        except Exception as error:
            logger.exception(error)

    # -----------------------------------------------------

    def analyze_price_momentum(
        self,
        periods: int = 10
    ) -> None:
        """
        Analyze price momentum.
        """

        try:

            if len(self.close) <= periods:
                return

            momentum = (
                self.close.iloc[-1]
                - self.close.iloc[-periods]
            )

            if momentum > 0:

                self.add_score(
                    8,
                    "Positive price momentum."
                )

                self.add_indicator(
                    "Momentum",
                    8,
                    "BUY",
                    "Price is gaining momentum."
                )

            elif momentum < 0:

                self.add_score(
                    -8,
                    "Negative price momentum."
                )

                self.add_indicator(
                    "Momentum",
                    -8,
                    "SELL",
                    "Price momentum is weakening."
                )

            else:

                self.add_indicator(
                    "Momentum",
                    0,
                    "NEUTRAL",
                    "No clear momentum."
                )

        except Exception as error:
            logger.exception(error)

    # -----------------------------------------------------

    def analyze_volatility(
        self,
        window: int = 20
    ) -> None:
        """
        Analyze market volatility.
        """

        try:

            returns = self.close.pct_change()

            volatility = (
                returns
                .rolling(window)
                .std()
                .iloc[-1]
            )

            if np.isnan(volatility):
                return

            if volatility < 0.015:

                self.add_score(
                    5,
                    "Low volatility market."
                )

                self.add_indicator(
                    "Volatility",
                    5,
                    "LOW RISK",
                    "Stable price movement."
                )

            elif volatility > 0.04:

                self.add_score(
                    -5,
                    "High volatility market."
                )

                self.add_indicator(
                    "Volatility",
                    -5,
                    "HIGH RISK",
                    "Large price swings detected."
                )

            else:

                self.add_indicator(
                    "Volatility",
                    0,
                    "NORMAL",
                    "Average market volatility."
                )

        except Exception as error:
            logger.exception(error)

    # -----------------------------------------------------

    def analyze_support_resistance(
        self,
        lookback: int = 30
    ) -> None:
        """
        Analyze support and resistance.
        """

        try:

            recent = self.df.tail(lookback)

            support = recent["Low"].min()

            resistance = recent["High"].max()

            current = recent["Close"].iloc[-1]

            if current <= support * 1.02:

                self.add_score(
                    8,
                    "Price is near support."
                )

                self.add_indicator(
                    "Support",
                    8,
                    "BUY",
                    "Potential upward reversal."
                )

            elif current >= resistance * 0.98:

                self.add_score(
                    -8,
                    "Price is near resistance."
                )

                self.add_indicator(
                    "Resistance",
                    -8,
                    "SELL",
                    "Potential downward reversal."
                )

            else:

                self.add_indicator(
                    "Support/Resistance",
                    0,
                    "NEUTRAL",
                    "Price is between support and resistance."
                )

        except Exception as error:
            logger.exception(error)

    # -----------------------------------------------------

    def analyze_gap(self) -> None:
        """
        Detect opening gap.
        """

        try:

            if len(self.df) < 2:
                return

            previous_close = self.close.iloc[-2]
            today_open = self.df["Open"].iloc[-1]

            gap = (
                (today_open - previous_close)
                / previous_close
            ) * 100

            if gap > 2:

                self.add_score(
                    4,
                    f"Bullish gap up ({gap:.2f}%)."
                )

                self.add_indicator(
                    "Gap",
                    4,
                    "BUY",
                    "Gap-up opening detected."
                )

            elif gap < -2:

                self.add_score(
                    -4,
                    f"Bearish gap down ({gap:.2f}%)."
                )

                self.add_indicator(
                    "Gap",
                    -4,
                    "SELL",
                    "Gap-down opening detected."
                )

            else:

                self.add_indicator(
                    "Gap",
                    0,
                    "NEUTRAL",
                    "No significant opening gap."
                )

        except Exception as error:
            logger.exception(error)

    # -----------------------------------------------------

    def analyze_volume_trend(
        self,
        window: int = 20
    ) -> None:
        """
        Analyze volume trend.
        """

        try:

            average_volume = (
                self.volume
                .rolling(window)
                .mean()
                .iloc[-1]
            )

            current_volume = self.volume.iloc[-1]

            if current_volume > average_volume * 2:

                self.add_score(
                    6,
                    "Exceptional trading volume."
                )

                self.add_indicator(
                    "Volume Trend",
                    6,
                    "BUY",
                    "Heavy buying interest."
                )

            elif current_volume < average_volume * 0.5:

                self.add_score(
                    -3,
                    "Very weak trading volume."
                )

                self.add_indicator(
                    "Volume Trend",
                    -3,
                    "SELL",
                    "Low market participation."
                )

            else:

                self.add_indicator(
                    "Volume Trend",
                    0,
                    "NORMAL",
                    "Volume trend is healthy."
                )

        except Exception as error:
            logger.exception(error)


# =========================================================
# END OF PART 3
# =========================================================

# =========================================================
# RECOMMENDATION SCORING ENGINE
# =========================================================

    def calculate_score(self) -> float:
        """
        Return normalized recommendation score.
        """

        try:

            self.score = max(
                0.0,
                min(100.0, self.score)
            )

            return round(self.score, 2)

        except Exception as error:
            logger.exception(error)
            return 50.0

    # -----------------------------------------------------

    def calculate_confidence(self) -> float:
        """
        Calculate confidence based on indicator agreement.
        """

        try:

            if not self.indicators:
                self.confidence = 0.0
                return self.confidence

            total = len(self.indicators)

            bullish = sum(
                1
                for indicator in self.indicators.values()
                if indicator.score > 0
            )

            bearish = sum(
                1
                for indicator in self.indicators.values()
                if indicator.score < 0
            )

            neutral = total - bullish - bearish

            dominant = max(
                bullish,
                bearish,
                neutral
            )

            self.confidence = round(
                (dominant / total) * 100,
                2
            )

            return self.confidence

        except Exception as error:
            logger.exception(error)
            return 0.0

    # -----------------------------------------------------

    def determine_trend(self) -> TrendType:
        """
        Determine overall market trend.
        """

        try:

            sma20 = self.close.rolling(20).mean().iloc[-1]
            sma50 = self.close.rolling(50).mean().iloc[-1]
            latest = self.close.iloc[-1]

            if latest > sma20 > sma50:
                return TrendType.BULLISH

            if latest < sma20 < sma50:
                return TrendType.BEARISH

            return TrendType.SIDEWAYS

        except Exception as error:
            logger.exception(error)
            return TrendType.UNKNOWN

    # -----------------------------------------------------

    def determine_risk(self) -> RiskLevel:
        """
        Determine market risk level.
        """

        try:

            volatility = (
                self.close
                .pct_change()
                .rolling(20)
                .std()
                .iloc[-1]
            )

            if np.isnan(volatility):
                return RiskLevel.MEDIUM

            if volatility < 0.015:
                return RiskLevel.LOW

            if volatility > 0.040:
                return RiskLevel.HIGH

            return RiskLevel.MEDIUM

        except Exception as error:
            logger.exception(error)
            return RiskLevel.MEDIUM

    # -----------------------------------------------------

    def determine_recommendation(
        self
    ) -> RecommendationType:
        """
        Convert score into recommendation.
        """

        score = self.calculate_score()

        if score >= 85:
            return RecommendationType.STRONG_BUY

        if score >= BUY_THRESHOLD:
            return RecommendationType.BUY

        if score >= SELL_THRESHOLD:
            return RecommendationType.HOLD

        if score >= 15:
            return RecommendationType.SELL

        return RecommendationType.STRONG_SELL

    # -----------------------------------------------------

    def build_result(
        self
    ) -> RecommendationResult:
        """
        Build recommendation result object.
        """

        return RecommendationResult(
            recommendation=self.determine_recommendation(),
            score=self.calculate_score(),
            confidence=self.calculate_confidence(),
            trend=self.determine_trend(),
            risk=self.determine_risk(),
            reasons=self.reasons.copy(),
            indicators=self.indicators.copy()
        )

    # -----------------------------------------------------

    def recommendation_summary(
        self
    ) -> Dict[str, Any]:
        """
        Return recommendation as dictionary.
        """

        result = self.build_result()

        return {
            "recommendation": result.recommendation.value,
            "score": result.score,
            "confidence": result.confidence,
            "trend": result.trend.value,
            "risk": result.risk.value,
            "reasons": result.reasons,
            "indicator_count": len(result.indicators)
        }

    # -----------------------------------------------------

    def reset_engine(self) -> None:
        """
        Reset engine state.
        """

        self.score = 50.0
        self.confidence = 50.0
        self.reasons.clear()
        self.indicators.clear()

        logger.info(
            "Recommendation engine reset."
        )


# =========================================================
# END OF PART 4
# =========================================================

# =========================================================
# EXPLANATION & RECOMMENDATION UTILITIES
# =========================================================

    def generate_explanation(self) -> str:
        """
        Generate a human-readable explanation for the recommendation.
        """

        try:

            recommendation = self.determine_recommendation()

            lines: list[str] = []

            lines.append(
                f"Recommendation : {recommendation.value}"
            )

            lines.append(
                f"Score : {self.calculate_score():.2f}/100"
            )

            lines.append(
                f"Confidence : {self.calculate_confidence():.2f}%"
            )

            lines.append(
                f"Trend : {self.determine_trend().value}"
            )

            lines.append(
                f"Risk : {self.determine_risk().value}"
            )

            if self.reasons:

                lines.append("")
                lines.append("Reasons:")

                for reason in self.reasons:
                    lines.append(f"• {reason}")

            return "\n".join(lines)

        except Exception as error:
            logger.exception(error)
            return "Unable to generate recommendation."

    # -----------------------------------------------------

    def indicator_summary(
        self
    ) -> pd.DataFrame:
        """
        Return indicator summary dataframe.
        """

        try:

            rows = []

            for indicator in self.indicators.values():

                rows.append(
                    {
                        "Indicator": indicator.name,
                        "Signal": indicator.signal,
                        "Score": indicator.score,
                        "Message": indicator.message
                    }
                )

            return pd.DataFrame(rows)

        except Exception as error:
            logger.exception(error)
            return pd.DataFrame()

    # -----------------------------------------------------

    def recommendation_color(
        self
    ) -> str:
        """
        Return UI color for recommendation.
        """

        recommendation = self.determine_recommendation()

        colors = {

            RecommendationType.STRONG_BUY: "#008000",
            RecommendationType.BUY: "#2E8B57",
            RecommendationType.HOLD: "#FFA500",
            RecommendationType.SELL: "#FF6347",
            RecommendationType.STRONG_SELL: "#DC143C"

        }

        return colors.get(
            recommendation,
            "#808080"
        )

    # -----------------------------------------------------

    def recommendation_icon(
        self
    ) -> str:
        """
        Return emoji/icon.
        """

        recommendation = self.determine_recommendation()

        icons = {

            RecommendationType.STRONG_BUY: "🟢🚀",
            RecommendationType.BUY: "🟢",
            RecommendationType.HOLD: "🟡",
            RecommendationType.SELL: "🔴",
            RecommendationType.STRONG_SELL: "🚨🔴"

        }

        return icons.get(
            recommendation,
            "⚪"
        )

    # -----------------------------------------------------

    def export_dict(
        self
    ) -> Dict[str, Any]:
        """
        Export recommendation.
        """

        result = self.build_result()

        return {

            "recommendation": result.recommendation.value,
            "score": result.score,
            "confidence": result.confidence,
            "trend": result.trend.value,
            "risk": result.risk.value,
            "reasons": result.reasons,
            "indicators": {

                name: {
                    "signal": indicator.signal,
                    "score": indicator.score,
                    "message": indicator.message
                }

                for name, indicator in result.indicators.items()

            }

        }

    # -----------------------------------------------------

    def export_dataframe(
        self
    ) -> pd.DataFrame:
        """
        Export indicators as dataframe.
        """

        try:

            return pd.DataFrame(
                [
                    {
                        "Indicator": indicator.name,
                        "Signal": indicator.signal,
                        "Score": indicator.score,
                        "Message": indicator.message
                    }

                    for indicator in self.indicators.values()

                ]
            )

        except Exception as error:
            logger.exception(error)
            return pd.DataFrame()

    # -----------------------------------------------------

    def print_summary(
        self
    ) -> None:
        """
        Print recommendation summary.
        """

        try:

            print(self.generate_explanation())

        except Exception as error:
            logger.exception(error)


# =========================================================
# MODULE HELPER FUNCTIONS
# =========================================================

def create_engine(
    dataframe: pd.DataFrame
) -> AIRecommendationEngine:
    """
    Factory function.
    """

    return AIRecommendationEngine(dataframe)


def version() -> str:
    """
    Module version.
    """

    return VERSION


__all__ = [

    "AIRecommendationEngine",
    "RecommendationResult",
    "IndicatorResult",
    "RecommendationType",
    "TrendType",
    "RiskLevel",
    "create_engine",
    "version"

]

# =========================================================
# END OF PART 5
# =========================================================

def generate_recommendation(
    ticker: str,
    current_price: float,
    predicted_price: float,
    rsi: float,
    macd: float,
    adx: float,
) -> str:
    """
    Simple recommendation wrapper used by app.py.
    """

    score = 0

    if predicted_price > current_price:
        score += 2
    else:
        score -= 2

    if rsi < 30:
        score += 1
    elif rsi > 70:
        score -= 1

    if macd > 0:
        score += 1
    else:
        score -= 1

    if adx > 25:
        score += 1

    if score >= 3:
        return f"✅ BUY {ticker} - Bullish signals detected."

    elif score <= -2:
        return f"🔴 SELL {ticker} - Bearish signals detected."

    return f"🟡 HOLD {ticker} - Wait for a stronger trend."