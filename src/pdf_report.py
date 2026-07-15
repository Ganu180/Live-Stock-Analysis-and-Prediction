"""
=========================================================
Live Stock Analysis & Prediction
PDF Report Generator
Version : 2.0
Python  : 3.12
=========================================================
"""

from __future__ import annotations

import os
import io
import logging
from pathlib import Path
from datetime import datetime
from typing import Any, Dict, List, Optional

import pandas as pd

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    Image,
    PageBreak,
    HRFlowable
)

# ==========================================================
# LOGGING
# ==========================================================

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)

logger = logging.getLogger(__name__)

# ==========================================================
# CONFIGURATION
# ==========================================================

VERSION = "2.0"

REPORT_FOLDER = Path("reports")

REPORT_FOLDER.mkdir(
    parents=True,
    exist_ok=True
)

PAGE_WIDTH, PAGE_HEIGHT = A4

DEFAULT_FONT = "Helvetica"

TITLE_FONT = "Helvetica-Bold"

# ==========================================================
# COLORS
# ==========================================================

PRIMARY = colors.HexColor("#2563EB")
SECONDARY = colors.HexColor("#0F172A")
SUCCESS = colors.HexColor("#16A34A")
WARNING = colors.HexColor("#D97706")
DANGER = colors.HexColor("#DC2626")
GRAY = colors.HexColor("#64748B")
LIGHT = colors.HexColor("#F8FAFC")
BORDER = colors.HexColor("#CBD5E1")

# ==========================================================
# STYLES
# ==========================================================

_styles = getSampleStyleSheet()

TITLE_STYLE = ParagraphStyle(
    "Title",
    parent=_styles["Heading1"],
    fontName=TITLE_FONT,
    fontSize=24,
    alignment=TA_CENTER,
    textColor=PRIMARY,
    spaceAfter=20,
)

HEADING_STYLE = ParagraphStyle(
    "Heading",
    parent=_styles["Heading2"],
    fontName=TITLE_FONT,
    fontSize=16,
    textColor=SECONDARY,
    spaceAfter=10,
)

SUBHEADING_STYLE = ParagraphStyle(
    "SubHeading",
    parent=_styles["Heading3"],
    fontName=TITLE_FONT,
    fontSize=13,
    textColor=PRIMARY,
    spaceAfter=8,
)

BODY_STYLE = ParagraphStyle(
    "Body",
    parent=_styles["BodyText"],
    fontName=DEFAULT_FONT,
    fontSize=10,
    leading=18,
    alignment=TA_LEFT,
)

CENTER_STYLE = ParagraphStyle(
    "Center",
    parent=BODY_STYLE,
    alignment=TA_CENTER,
)

RIGHT_STYLE = ParagraphStyle(
    "Right",
    parent=BODY_STYLE,
    alignment=TA_RIGHT,
)

SMALL_STYLE = ParagraphStyle(
    "Small",
    parent=BODY_STYLE,
    fontSize=8,
    textColor=GRAY,
)

# ==========================================================
# HELPER FUNCTIONS
# ==========================================================

def format_currency(value: Any) -> str:
    """
    Format currency safely.
    """
    try:
        return f"₹ {float(value):,.2f}"
    except Exception:
        return "N/A"


def format_percent(value: Any) -> str:
    """
    Format percentage safely.
    """
    try:
        return f"{float(value):.2f}%"
    except Exception:
        return "N/A"


def format_number(value: Any) -> str:
    """
    Format number safely.
    """
    try:
        return f"{float(value):,.2f}"
    except Exception:
        return "N/A"


def current_datetime() -> str:
    """
    Current timestamp.
    """
    return datetime.now().strftime(
        "%d-%m-%Y %H:%M:%S"
    )


# ==========================================================
# PDF REPORT GENERATOR
# ==========================================================

class PDFReportGenerator:
    """
    Professional PDF Report Generator
    Version 2.0
    """

    def __init__(
        self,
        output_file: str | Path,
        title: str = "Live Stock Analysis Report"
    ) -> None:

        self.output_file = Path(output_file)

        self.title = title

        self.story: List[Any] = []

        self.document = SimpleDocTemplate(
            str(self.output_file),
            pagesize=A4,
            rightMargin=0.5 * inch,
            leftMargin=0.5 * inch,
            topMargin=0.7 * inch,
            bottomMargin=0.7 * inch,
            title=title,
            author="Live Stock Analysis & Prediction",
        )

        logger.info(
            "PDF Report Generator initialized."
        )

    # ------------------------------------------------------

    def add_space(
        self,
        height: float = 0.2
    ) -> None:
        """
        Add vertical spacing.
        """

        self.story.append(
            Spacer(1, height * inch)
        )

    # ------------------------------------------------------

    def add_line(self) -> None:
        """
        Add horizontal separator.
        """

        self.story.append(
            HRFlowable(
                width="100%",
                color=BORDER,
                thickness=1
            )
        )

        self.add_space(0.15)

    # ------------------------------------------------------

    def add_title(
        self,
        text: str
    ) -> None:
        """
        Add report title.
        """

        self.story.append(
            Paragraph(
                text,
                TITLE_STYLE
            )
        )

    # ------------------------------------------------------

    def add_heading(
        self,
        text: str
    ) -> None:
        """
        Add heading.
        """

        self.story.append(
            Paragraph(
                text,
                HEADING_STYLE
            )
        )

    # ------------------------------------------------------

    def add_subheading(
        self,
        text: str
    ) -> None:
        """
        Add subheading.
        """

        self.story.append(
            Paragraph(
                text,
                SUBHEADING_STYLE
            )
        )

    # ------------------------------------------------------

    def add_paragraph(
        self,
        text: str
    ) -> None:
        """
        Add body paragraph.
        """

        self.story.append(
            Paragraph(
                text,
                BODY_STYLE
            )
        )

# ==========================================================
# END OF PART 1
# ==========================================================

    # ------------------------------------------------------
    # COVER PAGE
    # ------------------------------------------------------

    def add_cover_page(
        self,
        company_name: str,
        stock_symbol: str,
        generated_by: str = "Live Stock Analysis & Prediction"
    ) -> None:
        """
        Add report cover page.
        """

        self.add_space(0.8)

        self.story.append(
            Paragraph(
                self.title,
                TITLE_STYLE
            )
        )

        self.add_space(0.30)

        self.story.append(
            Paragraph(
                f"<b>Company</b><br/>{company_name}",
                CENTER_STYLE
            )
        )

        self.add_space(0.20)

        self.story.append(
            Paragraph(
                f"<b>Stock Symbol</b><br/>{stock_symbol}",
                CENTER_STYLE
            )
        )

        self.add_space(0.20)

        self.story.append(
            Paragraph(
                f"<b>Generated On</b><br/>{current_datetime()}",
                CENTER_STYLE
            )
        )

        self.add_space(0.20)

        self.story.append(
            Paragraph(
                f"<b>Generated By</b><br/>{generated_by}",
                CENTER_STYLE
            )
        )

        self.add_space(0.50)

        self.story.append(
            Paragraph(
                "Professional Stock Analysis Report",
                SUBHEADING_STYLE
            )
        )

        self.story.append(PageBreak())

    # ------------------------------------------------------
    # REPORT INFORMATION
    # ------------------------------------------------------

    def add_report_information(
        self,
        report_info: Dict[str, Any]
    ) -> None:
        """
        Add report information table.
        """

        self.add_heading("Report Information")

        data = [
            ["Field", "Value"]
        ]

        for key, value in report_info.items():
            data.append(
                [
                    str(key),
                    str(value)
                ]
            )

        table = Table(
            data,
            colWidths=[2.5 * inch, 3.5 * inch]
        )

        table.setStyle(
            TableStyle(
                [

                    (
                        "BACKGROUND",
                        (0, 0),
                        (-1, 0),
                        PRIMARY
                    ),

                    (
                        "TEXTCOLOR",
                        (0, 0),
                        (-1, 0),
                        colors.white
                    ),

                    (
                        "GRID",
                        (0, 0),
                        (-1, -1),
                        0.5,
                        BORDER
                    ),

                    (
                        "BACKGROUND",
                        (0, 1),
                        (-1, -1),
                        LIGHT
                    ),

                    (
                        "FONTNAME",
                        (0, 0),
                        (-1, 0),
                        TITLE_FONT
                    ),

                    (
                        "BOTTOMPADDING",
                        (0, 0),
                        (-1, 0),
                        10
                    ),

                    (
                        "TOPPADDING",
                        (0, 1),
                        (-1, -1),
                        8
                    ),

                    (
                        "BOTTOMPADDING",
                        (0, 1),
                        (-1, -1),
                        8
                    ),

                ]
            )
        )

        self.story.append(table)

        self.add_space()

    # ------------------------------------------------------
    # COMPANY INFORMATION
    # ------------------------------------------------------

    def add_company_information(
        self,
        company_data: Dict[str, Any]
    ) -> None:
        """
        Add company information.
        """

        self.add_heading(
            "Company Information"
        )

        for key, value in company_data.items():

            self.story.append(

                Paragraph(
                    f"<b>{key}</b>: {value}",
                    BODY_STYLE
                )

            )

        self.add_space()

    # ------------------------------------------------------
    # EXECUTIVE SUMMARY
    # ------------------------------------------------------

    def add_executive_summary(
        self,
        summary: str
    ) -> None:
        """
        Add executive summary.
        """

        self.add_heading(
            "Executive Summary"
        )

        self.add_paragraph(
            summary
        )

        self.add_space()

    # ------------------------------------------------------
    # SECTION TITLE
    # ------------------------------------------------------

    def add_section(
        self,
        title: str
    ) -> None:
        """
        Add section title.
        """

        self.story.append(
            Paragraph(
                title,
                HEADING_STYLE
            )
        )

        self.add_line()

    # ------------------------------------------------------
    # SIMPLE KEY VALUE TABLE
    # ------------------------------------------------------

    def add_key_value_table(
        self,
        data: Dict[str, Any]
    ) -> None:
        """
        Add key-value table.
        """

        rows = [
            [
                "Parameter",
                "Value"
            ]
        ]

        for key, value in data.items():

            rows.append(
                [
                    str(key),
                    str(value)
                ]
            )

        table = Table(
            rows,
            colWidths=[
                3 * inch,
                3 * inch
            ]
        )

        table.setStyle(
            TableStyle(
                [

                    (
                        "BACKGROUND",
                        (0, 0),
                        (-1, 0),
                        SECONDARY
                    ),

                    (
                        "TEXTCOLOR",
                        (0, 0),
                        (-1, 0),
                        colors.white
                    ),

                    (
                        "GRID",
                        (0, 0),
                        (-1, -1),
                        0.5,
                        BORDER
                    ),

                    (
                        "BACKGROUND",
                        (0, 1),
                        (-1, -1),
                        colors.white
                    ),

                    (
                        "BOTTOMPADDING",
                        (0, 0),
                        (-1, 0),
                        8
                    ),

                    (
                        "TOPPADDING",
                        (0, 1),
                        (-1, -1),
                        7
                    ),

                ]
            )
        )

        self.story.append(table)

        self.add_space()

# ==========================================================
# END OF PART 2
# ==========================================================

    # ------------------------------------------------------
    # STOCK PRICE SUMMARY
    # ------------------------------------------------------

    def add_stock_summary(
        self,
        stock_data: Dict[str, Any]
    ) -> None:
        """
        Add stock price summary.
        """

        self.add_section("Stock Price Summary")

        rows = [
            ["Metric", "Value"]
        ]

        fields = [
            ("Current Price", format_currency(stock_data.get("current_price", 0))),
            ("Open", format_currency(stock_data.get("open", 0))),
            ("High", format_currency(stock_data.get("high", 0))),
            ("Low", format_currency(stock_data.get("low", 0))),
            ("Previous Close", format_currency(stock_data.get("previous_close", 0))),
            ("Volume", format_number(stock_data.get("volume", 0))),
            ("Market Cap", format_currency(stock_data.get("market_cap", 0))),
        ]

        rows.extend(fields)

        table = Table(
            rows,
            colWidths=[3 * inch, 3 * inch]
        )

        table.setStyle(
            TableStyle(
                [
                    ("BACKGROUND", (0, 0), (-1, 0), PRIMARY),
                    ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                    ("FONTNAME", (0, 0), (-1, 0), TITLE_FONT),
                    ("BACKGROUND", (0, 1), (-1, -1), LIGHT),
                    ("GRID", (0, 0), (-1, -1), 0.4, BORDER),
                    ("ALIGN", (1, 1), (-1, -1), "RIGHT"),
                    ("BOTTOMPADDING", (0, 0), (-1, 0), 8),
                ]
            )
        )

        self.story.append(table)

        self.add_space()

    # ------------------------------------------------------
    # PERFORMANCE METRICS
    # ------------------------------------------------------

    def add_performance_metrics(
        self,
        metrics: Dict[str, Any]
    ) -> None:
        """
        Add performance metrics.
        """

        self.add_section(
            "Performance Metrics"
        )

        rows = [
            ["Metric", "Value"]
        ]

        for key, value in metrics.items():

            if isinstance(value, (int, float)):
                value = format_number(value)

            rows.append(
                [key, value]
            )

        table = Table(
            rows,
            colWidths=[3.2 * inch, 2.8 * inch]
        )

        table.setStyle(
            TableStyle(
                [
                    ("BACKGROUND", (0, 0), (-1, 0), SUCCESS),
                    ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                    ("FONTNAME", (0, 0), (-1, 0), TITLE_FONT),
                    ("GRID", (0, 0), (-1, -1), 0.5, BORDER),
                    ("BACKGROUND", (0, 1), (-1, -1), colors.white),
                    ("BOTTOMPADDING", (0, 0), (-1, 0), 8),
                ]
            )
        )

        self.story.append(table)

        self.add_space()

    # ------------------------------------------------------
    # TECHNICAL INDICATORS
    # ------------------------------------------------------

    def add_technical_indicators(
        self,
        indicators: Dict[str, Any]
    ) -> None:
        """
        Add technical indicator table.
        """

        self.add_section(
            "Technical Indicators"
        )

        rows = [
            ["Indicator", "Value"]
        ]

        for indicator, value in indicators.items():

            if isinstance(value, float):
                value = f"{value:.2f}"

            rows.append(
                [indicator, str(value)]
            )

        table = Table(
            rows,
            colWidths=[
                3 * inch,
                3 * inch
            ]
        )

        table.setStyle(
            TableStyle(
                [
                    ("BACKGROUND", (0, 0), (-1, 0), WARNING),
                    ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                    ("FONTNAME", (0, 0), (-1, 0), TITLE_FONT),
                    ("GRID", (0, 0), (-1, -1), 0.5, BORDER),
                    ("BACKGROUND", (0, 1), (-1, -1), LIGHT),
                    ("ALIGN", (1, 1), (-1, -1), "CENTER"),
                ]
            )
        )

        self.story.append(table)

        self.add_space()

    # ------------------------------------------------------
    # HISTORICAL PRICE SUMMARY
    # ------------------------------------------------------

    def add_price_statistics(
        self,
        dataframe: pd.DataFrame
    ) -> None:
        """
        Add historical statistics.
        """

        self.add_section(
            "Historical Price Statistics"
        )

        if dataframe.empty:
            self.add_paragraph(
                "No historical data available."
            )
            return

        summary = {
            "Highest Price": dataframe["High"].max(),
            "Lowest Price": dataframe["Low"].min(),
            "Average Close": dataframe["Close"].mean(),
            "Average Volume": dataframe["Volume"].mean(),
            "Trading Days": len(dataframe),
        }

        rows = [
            ["Statistic", "Value"]
        ]

        for key, value in summary.items():

            if isinstance(value, (int, float)):

                if "Volume" in key:

                    value = format_number(value)

                else:

                    value = format_currency(value)

            rows.append(
                [key, value]
            )

        table = Table(
            rows,
            colWidths=[
                3 * inch,
                3 * inch
            ]
        )

        table.setStyle(
            TableStyle(
                [
                    ("BACKGROUND", (0, 0), (-1, 0), SECONDARY),
                    ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                    ("GRID", (0, 0), (-1, -1), 0.5, BORDER),
                    ("BACKGROUND", (0, 1), (-1, -1), colors.white),
                ]
            )
        )

        self.story.append(table)

        self.add_space()

# ==========================================================
# END OF PART 3
# ==========================================================

    # ------------------------------------------------------
    # AI RECOMMENDATION
    # ------------------------------------------------------

    def add_ai_recommendation(
        self,
        recommendation: Dict[str, Any]
    ) -> None:
        """
        Add AI recommendation section.
        """

        self.add_section(
            "AI Recommendation"
        )

        score = recommendation.get("score", 0)

        if score >= 80:
            color = SUCCESS
        elif score >= 60:
            color = colors.darkgreen
        elif score >= 40:
            color = WARNING
        else:
            color = DANGER

        rows = [
            ["Parameter", "Value"],
            ["Recommendation", recommendation.get("recommendation", "N/A")],
            ["Confidence", format_percent(recommendation.get("confidence", 0))],
            ["Score", f"{score:.2f}/100"],
            ["Risk Level", recommendation.get("risk", "Unknown")],
            ["Trend", recommendation.get("trend", "Unknown")],
        ]

        table = Table(
            rows,
            colWidths=[3 * inch, 3 * inch]
        )

        table.setStyle(
            TableStyle(
                [
                    ("BACKGROUND", (0, 0), (-1, 0), color),
                    ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                    ("FONTNAME", (0, 0), (-1, 0), TITLE_FONT),
                    ("GRID", (0, 0), (-1, -1), 0.5, BORDER),
                    ("BACKGROUND", (0, 1), (-1, -1), LIGHT),
                    ("BOTTOMPADDING", (0, 0), (-1, 0), 8),
                ]
            )
        )

        self.story.append(table)

        self.add_space()

    # ------------------------------------------------------
    # PREDICTION SUMMARY
    # ------------------------------------------------------

    def add_prediction_summary(
        self,
        prediction: Dict[str, Any]
    ) -> None:
        """
        Add stock prediction summary.
        """

        self.add_section(
            "Prediction Summary"
        )

        rows = [
            ["Metric", "Value"]
        ]

        fields = [

            (
                "Predicted Price",
                format_currency(
                    prediction.get(
                        "predicted_price",
                        0
                    )
                )
            ),

            (
                "Expected Change",
                format_percent(
                    prediction.get(
                        "expected_change",
                        0
                    )
                )
            ),

            (
                "Prediction Date",
                prediction.get(
                    "prediction_date",
                    current_datetime()
                )
            ),

            (
                "Prediction Model",
                prediction.get(
                    "model",
                    "Machine Learning"
                )
            ),

            (
                "Accuracy",
                format_percent(
                    prediction.get(
                        "accuracy",
                        0
                    )
                )
            )

        ]

        rows.extend(fields)

        table = Table(
            rows,
            colWidths=[3 * inch, 3 * inch]
        )

        table.setStyle(
            TableStyle(
                [

                    ("BACKGROUND", (0, 0), (-1, 0), PRIMARY),

                    ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),

                    ("FONTNAME", (0, 0), (-1, 0), TITLE_FONT),

                    ("GRID", (0, 0), (-1, -1), 0.5, BORDER),

                    ("BACKGROUND", (0, 1), (-1, -1), colors.white),

                ]
            )
        )

        self.story.append(table)

        self.add_space()

    # ------------------------------------------------------
    # RISK ANALYSIS
    # ------------------------------------------------------

    def add_risk_analysis(
        self,
        risk_data: Dict[str, Any]
    ) -> None:
        """
        Add risk analysis section.
        """

        self.add_section(
            "Risk Analysis"
        )

        rows = [
            ["Risk Factor", "Assessment"]
        ]

        for key, value in risk_data.items():

            rows.append(
                [
                    str(key),
                    str(value)
                ]
            )

        table = Table(
            rows,
            colWidths=[3 * inch, 3 * inch]
        )

        table.setStyle(
            TableStyle(
                [

                    ("BACKGROUND", (0, 0), (-1, 0), DANGER),

                    ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),

                    ("GRID", (0, 0), (-1, -1), 0.5, BORDER),

                    ("BACKGROUND", (0, 1), (-1, -1), LIGHT),

                    ("FONTNAME", (0, 0), (-1, 0), TITLE_FONT),

                ]
            )
        )

        self.story.append(table)

        self.add_space()

    # ------------------------------------------------------
    # AI NOTES
    # ------------------------------------------------------

    def add_ai_notes(
        self,
        notes: List[str]
    ) -> None:
        """
        Add AI generated notes.
        """

        self.add_section(
            "AI Analysis Notes"
        )

        if not notes:

            self.add_paragraph(
                "No analysis notes available."
            )

            self.add_space()

            return

        for note in notes:

            self.story.append(
                Paragraph(
                    f"• {note}",
                    BODY_STYLE
                )
            )

        self.add_space()

    # ------------------------------------------------------
    # MARKET SENTIMENT
    # ------------------------------------------------------

    def add_market_sentiment(
        self,
        sentiment: str,
        score: float
    ) -> None:
        """
        Add market sentiment.
        """

        self.add_section(
            "Market Sentiment"
        )

        self.story.append(
            Paragraph(
                f"<b>Sentiment:</b> {sentiment}",
                BODY_STYLE
            )
        )

        self.story.append(
            Paragraph(
                f"<b>Sentiment Score:</b> {score:.2f}/100",
                BODY_STYLE
            )
        )

        self.add_space()

# ==========================================================
# END OF PART 4
# ==========================================================

    # ------------------------------------------------------
    # PORTFOLIO SUMMARY
    # ------------------------------------------------------

    def add_portfolio_summary(
        self,
        portfolio: Dict[str, Any]
    ) -> None:
        """
        Add portfolio summary.
        """

        self.add_section("Portfolio Summary")

        rows = [
            ["Metric", "Value"],
            ["Total Investment", format_currency(portfolio.get("investment", 0))],
            ["Current Value", format_currency(portfolio.get("current_value", 0))],
            ["Profit / Loss", format_currency(portfolio.get("profit_loss", 0))],
            ["Return (%)", format_percent(portfolio.get("return_percentage", 0))],
            ["Number of Holdings", str(portfolio.get("holdings", 0))]
        ]

        table = Table(rows, colWidths=[3 * inch, 3 * inch])

        table.setStyle(
            TableStyle(
                [
                    ("BACKGROUND", (0, 0), (-1, 0), PRIMARY),
                    ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                    ("FONTNAME", (0, 0), (-1, 0), TITLE_FONT),
                    ("GRID", (0, 0), (-1, -1), 0.5, BORDER),
                    ("BACKGROUND", (0, 1), (-1, -1), LIGHT),
                    ("BOTTOMPADDING", (0, 0), (-1, 0), 8),
                ]
            )
        )

        self.story.append(table)
        self.add_space()

    # ------------------------------------------------------
    # HOLDINGS TABLE
    # ------------------------------------------------------

    def add_holdings_table(
        self,
        holdings: pd.DataFrame
    ) -> None:
        """
        Add portfolio holdings.
        """

        self.add_section("Portfolio Holdings")

        if holdings.empty:

            self.add_paragraph(
                "No holdings available."
            )

            self.add_space()

            return

        rows = [[
            "Symbol",
            "Qty",
            "Buy Price",
            "Current",
            "P/L"
        ]]

        for _, row in holdings.iterrows():

            rows.append([
                str(row.get("Symbol", "")),
                str(row.get("Quantity", "")),
                format_currency(row.get("Buy Price", 0)),
                format_currency(row.get("Current Price", 0)),
                format_currency(row.get("Profit/Loss", 0)),
            ])

        table = Table(
            rows,
            repeatRows=1
        )

        table.setStyle(
            TableStyle(
                [
                    ("BACKGROUND", (0, 0), (-1, 0), SECONDARY),
                    ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                    ("FONTNAME", (0, 0), (-1, 0), TITLE_FONT),
                    ("GRID", (0, 0), (-1, -1), 0.4, BORDER),
                    ("BACKGROUND", (0, 1), (-1, -1), colors.white),
                    ("ALIGN", (1, 1), (-1, -1), "CENTER"),
                    ("BOTTOMPADDING", (0, 0), (-1, 0), 8),
                ]
            )
        )

        self.story.append(table)

        self.add_space()

    # ------------------------------------------------------
    # TOP GAINERS / LOSERS
    # ------------------------------------------------------

    def add_top_movers(
        self,
        gainers: pd.DataFrame,
        losers: pd.DataFrame
    ) -> None:
        """
        Add top gainers and losers.
        """

        self.add_section("Top Movers")

        self.add_subheading("Top Gainers")

        if gainers.empty:

            self.add_paragraph("No gainers available.")

        else:

            gainers_table = Table(
                [["Symbol", "Return %"]] +
                gainers.values.tolist()
            )

            gainers_table.setStyle(
                TableStyle([
                    ("BACKGROUND", (0, 0), (-1, 0), SUCCESS),
                    ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                    ("GRID", (0, 0), (-1, -1), 0.4, BORDER),
                ])
            )

            self.story.append(gainers_table)

        self.add_space(0.20)

        self.add_subheading("Top Losers")

        if losers.empty:

            self.add_paragraph("No losers available.")

        else:

            losers_table = Table(
                [["Symbol", "Return %"]] +
                losers.values.tolist()
            )

            losers_table.setStyle(
                TableStyle([
                    ("BACKGROUND", (0, 0), (-1, 0), DANGER),
                    ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                    ("GRID", (0, 0), (-1, -1), 0.4, BORDER),
                ])
            )

            self.story.append(losers_table)

        self.add_space()

    # ------------------------------------------------------
    # PORTFOLIO NOTES
    # ------------------------------------------------------

    def add_portfolio_notes(
        self,
        notes: List[str]
    ) -> None:
        """
        Add portfolio notes.
        """

        self.add_section("Portfolio Notes")

        if not notes:

            self.add_paragraph(
                "No portfolio notes available."
            )

            self.add_space()

            return

        for note in notes:

            self.story.append(
                Paragraph(
                    f"• {note}",
                    BODY_STYLE
                )
            )

        self.add_space()

# ==========================================================
# END OF PART 5
# ==========================================================

    # ------------------------------------------------------
    # ADD IMAGE
    # ------------------------------------------------------

    def add_image(
        self,
        image_path: str | Path,
        width: float = 6.0,
        height: float = 3.5
    ) -> None:
        """
        Add an image to the report.
        """

        try:

            image_path = Path(image_path)

            if not image_path.exists():

                logger.warning(
                    "Image not found: %s",
                    image_path
                )

                return

            image = Image(
                str(image_path),
                width=width * inch,
                height=height * inch
            )

            self.story.append(image)

            self.add_space()

        except Exception as error:

            logger.exception(error)

    # ------------------------------------------------------
    # ADD CHART
    # ------------------------------------------------------

    def add_chart(
        self,
        chart_path: str | Path,
        title: str
    ) -> None:
        """
        Add chart section.
        """

        self.add_section(title)

        self.add_image(chart_path)

    # ------------------------------------------------------
    # ADD MULTIPLE CHARTS
    # ------------------------------------------------------

    def add_chart_gallery(
        self,
        charts: List[str | Path]
    ) -> None:
        """
        Add multiple charts.
        """

        self.add_section(
            "Charts & Visualizations"
        )

        if not charts:

            self.add_paragraph(
                "No charts available."
            )

            self.add_space()

            return

        for chart in charts:

            self.add_image(chart)

    # ------------------------------------------------------
    # ADD DATAFRAME
    # ------------------------------------------------------

    def add_dataframe(
        self,
        dataframe: pd.DataFrame,
        title: str
    ) -> None:
        """
        Convert dataframe into PDF table.
        """

        self.add_section(title)

        if dataframe.empty:

            self.add_paragraph(
                "No data available."
            )

            self.add_space()

            return

        rows = [
            dataframe.columns.tolist()
        ]

        for _, row in dataframe.iterrows():

            rows.append(
                [
                    str(value)
                    for value in row.tolist()
                ]
            )

        table = Table(
            rows,
            repeatRows=1
        )

        table.setStyle(
            TableStyle(
                [

                    (
                        "BACKGROUND",
                        (0, 0),
                        (-1, 0),
                        PRIMARY
                    ),

                    (
                        "TEXTCOLOR",
                        (0, 0),
                        (-1, 0),
                        colors.white
                    ),

                    (
                        "FONTNAME",
                        (0, 0),
                        (-1, 0),
                        TITLE_FONT
                    ),

                    (
                        "GRID",
                        (0, 0),
                        (-1, -1),
                        0.35,
                        BORDER
                    ),

                    (
                        "BACKGROUND",
                        (0, 1),
                        (-1, -1),
                        colors.white
                    ),

                    (
                        "BOTTOMPADDING",
                        (0, 0),
                        (-1, 0),
                        8
                    ),

                ]
            )
        )

        self.story.append(table)

        self.add_space()

    # ------------------------------------------------------
    # ADD PAGE BREAK
    # ------------------------------------------------------

    def add_page_break(
        self
    ) -> None:
        """
        Insert a new page.
        """

        self.story.append(
            PageBreak()
        )

    # ------------------------------------------------------
    # DISCLAIMER
    # ------------------------------------------------------

    def add_disclaimer(
        self
    ) -> None:
        """
        Add investment disclaimer.
        """

        self.add_section(
            "Disclaimer"
        )

        disclaimer = (
            "This report is generated automatically for "
            "educational and informational purposes only. "
            "It should not be considered financial or "
            "investment advice. Always perform your own "
            "research and consult a qualified financial "
            "advisor before making investment decisions."
        )

        self.story.append(
            Paragraph(
                disclaimer,
                SMALL_STYLE
            )
        )

        self.add_space()

# ==========================================================
# END OF PART 6
# ==========================================================

    # ------------------------------------------------------
    # HEADER
    # ------------------------------------------------------

    def _header(
        self,
        canvas,
        document
    ) -> None:
        """
        Draw page header.
        """

        canvas.saveState()

        canvas.setFont(
            TITLE_FONT,
            12
        )

        canvas.setFillColor(
            PRIMARY
        )

        canvas.drawString(
            document.leftMargin,
            PAGE_HEIGHT - 40,
            self.title
        )

        canvas.setFont(
            DEFAULT_FONT,
            8
        )

        canvas.setFillColor(
            GRAY
        )

        canvas.drawRightString(
            PAGE_WIDTH - document.rightMargin,
            PAGE_HEIGHT - 40,
            current_datetime()
        )

        canvas.restoreState()

    # ------------------------------------------------------
    # FOOTER
    # ------------------------------------------------------

    def _footer(
        self,
        canvas,
        document
    ) -> None:
        """
        Draw page footer.
        """

        canvas.saveState()

        canvas.setStrokeColor(
            BORDER
        )

        canvas.line(
            document.leftMargin,
            30,
            PAGE_WIDTH - document.rightMargin,
            30
        )

        canvas.setFont(
            DEFAULT_FONT,
            8
        )

        canvas.setFillColor(
            GRAY
        )

        canvas.drawString(
            document.leftMargin,
            18,
            "Live Stock Analysis & Prediction | PDF Report Version 2.0"
        )

        canvas.drawRightString(
            PAGE_WIDTH - document.rightMargin,
            18,
            f"Page {canvas.getPageNumber()}"
        )

        canvas.restoreState()

    # ------------------------------------------------------
    # BUILD PDF
    # ------------------------------------------------------

    def build(
        self
    ) -> Path:
        """
        Generate the PDF report.
        """

        try:

            self.document.build(
                self.story,
                onFirstPage=self._header_footer,
                onLaterPages=self._header_footer
            )

            logger.info(
                "PDF report generated successfully: %s",
                self.output_file
            )

            return self.output_file

        except Exception as error:

            logger.exception(error)

            raise

    # ------------------------------------------------------

    def _header_footer(
        self,
        canvas,
        document
    ) -> None:
        """
        Draw header and footer.
        """

        self._header(
            canvas,
            document
        )

        self._footer(
            canvas,
            document
        )

    # ------------------------------------------------------

    def clear(
        self
    ) -> None:
        """
        Clear report content.
        """

        self.story.clear()

    # ------------------------------------------------------

    @property
    def page_count(
        self
    ) -> int:
        """
        Current number of report elements.
        """

        return len(
            self.story
        )


# ==========================================================
# FACTORY FUNCTION
# ==========================================================

def create_pdf_report(
    output_file: str | Path,
    title: str = "Live Stock Analysis Report"
) -> PDFReportGenerator:
    """
    Create a PDFReportGenerator instance.
    """

    return PDFReportGenerator(
        output_file=output_file,
        title=title
    )


# ==========================================================
# MODULE EXPORTS
# ==========================================================

__all__ = [
    "PDFReportGenerator",
    "create_pdf_report",
    "VERSION",
]

# ==========================================================
# END OF pdf_report.py VERSION 2.0
# ==========================================================

