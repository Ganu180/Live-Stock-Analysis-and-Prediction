"""
==========================================================
Live Stock Analysis & Prediction
Email Alert Module
Version : 2.0
==========================================================
"""

import os
import ssl
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import pandas as pd
import streamlit as st

# ==========================================================
# EMAIL CONFIGURATION
# ==========================================================

EMAIL = st.secrets.get("EMAIL_ADDRESS", "")
PASSWORD = st.secrets.get("EMAIL_APP_PASSWORD", "")

SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 465

# ==========================================================
# DATA PATHS
# ==========================================================

DATA_FOLDER = "data"

ALERT_FILE = os.path.join(
    DATA_FOLDER,
    "email_alerts.csv"
)

os.makedirs(
    DATA_FOLDER,
    exist_ok=True
)

# ==========================================================
# CSV INITIALIZATION
# ==========================================================

def initialize_alert_file():
    """
    Create email alert CSV if it does not exist.
    """

    if os.path.exists(ALERT_FILE):
        return

    df = pd.DataFrame(
        columns=[
            "Email",
            "Ticker",
            "Alert Type",
            "Target Price"
        ]
    )

    df.to_csv(
        ALERT_FILE,
        index=False
    )

# ==========================================================
# LOAD ALERTS
# ==========================================================

def load_alerts():

    initialize_alert_file()

    try:

        df = pd.read_csv(ALERT_FILE)

    except Exception:

        df = pd.DataFrame(
            columns=[
                "Email",
                "Ticker",
                "Alert Type",
                "Target Price"
            ]
        )

    return df

# ==========================================================
# SAVE ALERTS
# ==========================================================

def save_alerts(df):

    df.to_csv(
        ALERT_FILE,
        index=False
    )

# ==========================================================
# EMAIL VALIDATION
# ==========================================================

def validate_email(email):

    if not isinstance(email, str):
        return False

    email = email.strip()

    if len(email) < 6:
        return False

    if "@" not in email:
        return False

    if "." not in email:
        return False

    return True

# ==========================================================
# AVAILABLE ALERT TYPES
# ==========================================================

def get_alert_types():

    return [

        "Price Above",

        "Price Below",

        "BUY",

        "SELL"

    ]
# ==========================================================
# SAVE ALERT
# ==========================================================

def save_alert(
    email,
    ticker,
    alert_type,
    target_price
):
    """
    Save a new email alert.
    """

    if not validate_email(email):
        raise ValueError("Invalid email address.")

    ticker = ticker.strip().upper()

    if ticker == "":
        raise ValueError("Invalid ticker.")

    try:
        target_price = float(target_price)
    except Exception:
        raise ValueError("Invalid target price.")

    initialize_alert_file()

    df = load_alerts()

    # Prevent duplicate alerts
    duplicate = (
        (df["Email"].astype(str).str.lower() == email.lower()) &
        (df["Ticker"].astype(str).str.upper() == ticker) &
        (df["Alert Type"] == alert_type) &
        (df["Target Price"].astype(float) == target_price)
    )

    if duplicate.any():
        return False

    new_row = pd.DataFrame([{
        "Email": email,
        "Ticker": ticker,
        "Alert Type": alert_type,
        "Target Price": target_price
    }])

    df = pd.concat(
        [df, new_row],
        ignore_index=True
    )

    save_alerts(df)

    return True


# ==========================================================
# DELETE ALERT
# ==========================================================

def delete_alert(index):
    """
    Delete alert by index.
    """

    df = load_alerts()

    if df.empty:
        return False

    if index not in df.index:
        return False

    df = df.drop(index)

    df.reset_index(
        drop=True,
        inplace=True
    )

    save_alerts(df)

    return True


# ==========================================================
# UPDATE ALERT
# ==========================================================

def update_alert(
    index,
    email=None,
    ticker=None,
    alert_type=None,
    target_price=None
):
    """
    Update an existing alert.
    """

    df = load_alerts()

    if df.empty:
        return False

    if index not in df.index:
        return False

    if email is not None:

        if not validate_email(email):
            raise ValueError("Invalid email.")

        df.loc[index, "Email"] = email

    if ticker is not None:

        df.loc[index, "Ticker"] = (
            ticker.strip().upper()
        )

    if alert_type is not None:

        df.loc[index, "Alert Type"] = alert_type

    if target_price is not None:

        df.loc[index, "Target Price"] = float(target_price)

    save_alerts(df)

    return True


# ==========================================================
# SEARCH ALERTS
# ==========================================================

def search_alerts(email=None, ticker=None):

    df = load_alerts()

    if df.empty:
        return df

    if email:

        df = df[
            df["Email"].astype(str).str.lower()
            == email.lower()
        ]

    if ticker:

        ticker = ticker.upper()

        df = df[
            df["Ticker"].astype(str).str.upper()
            == ticker
        ]

    return df


# ==========================================================
# CHECK ALERT EXISTS
# ==========================================================

def alert_exists(
    email,
    ticker,
    alert_type
):

    df = load_alerts()

    if df.empty:
        return False

    ticker = ticker.upper()

    return (
        (
            df["Email"].astype(str).str.lower()
            == email.lower()
        )
        &
        (
            df["Ticker"].astype(str).str.upper()
            == ticker
        )
        &
        (
            df["Alert Type"]
            == alert_type
        )
    ).any()
# ==========================================================
# CREATE HTML EMAIL
# ==========================================================

def create_email_body(
    ticker,
    current_price,
    alert_type
):
    """
    Creates HTML email body.
    """

    return f"""
    <html>

    <head>

    <style>

    body {{
        font-family: Arial, Helvetica, sans-serif;
        background-color: #f5f5f5;
        padding: 20px;
    }}

    .container {{
        background: white;
        padding: 20px;
        border-radius: 10px;
        border: 1px solid #dddddd;
    }}

    h2 {{
        color: #1f77b4;
    }}

    table {{
        width: 100%;
        border-collapse: collapse;
        margin-top: 15px;
    }}

    td {{
        padding: 10px;
        border-bottom: 1px solid #eeeeee;
    }}

    .footer {{
        margin-top: 25px;
        color: gray;
        font-size: 12px;
    }}

    </style>

    </head>

    <body>

    <div class="container">

    <h2>
    📈 Live Stock Analysis Alert
    </h2>

    <p>
    Your stock alert has been triggered.
    </p>

    <table>

    <tr>
        <td><b>Stock</b></td>
        <td>{ticker}</td>
    </tr>

    <tr>
        <td><b>Alert Type</b></td>
        <td>{alert_type}</td>
    </tr>

    <tr>
        <td><b>Current Price</b></td>
        <td>₹ {current_price:.2f}</td>
    </tr>

    </table>

    <div class="footer">

    Generated automatically by
    <b>Live Stock Analysis & Prediction</b>

    </div>

    </div>

    </body>

    </html>
    """


# ==========================================================
# SEND EMAIL
# ==========================================================

def send_email(
    sender_email,
    app_password,
    receiver_email,
    subject,
    body
):
    """
    Send email using Gmail SMTP.
    """

    if not validate_email(receiver_email):
        return False

    if sender_email == "":
        return False

    if app_password == "":
        return False

    try:

        message = MIMEMultipart()

        message["From"] = sender_email

        message["To"] = receiver_email

        message["Subject"] = subject

        message.attach(

            MIMEText(
                body,
                "html"
            )

        )

        context = ssl.create_default_context()

        with smtplib.SMTP_SSL(

            SMTP_SERVER,
            SMTP_PORT,
            context=context

        ) as server:

            server.login(

                sender_email,
                app_password

            )

            server.sendmail(

                sender_email,

                receiver_email,

                message.as_string()

            )

        return True

    except smtplib.SMTPAuthenticationError:

        print(
            "SMTP Authentication Failed"
        )

        return False

    except smtplib.SMTPException as e:

        print(
            f"SMTP Error: {e}"
        )

        return False

    except Exception as e:

        print(
            f"Unexpected Error: {e}"
        )

        return False


# ==========================================================
# SEND ALERT EMAIL
# ==========================================================

def send_alert_email(
    receiver_email,
    ticker,
    current_price,
    alert_type
):
    """
    Send formatted stock alert email.
    """

    subject = f"Stock Alert - {ticker}"

    body = create_email_body(
        ticker,
        current_price,
        alert_type
    )

    return send_email(

        EMAIL,

        PASSWORD,

        receiver_email,

        subject,

        body

    )
# ==========================================================
# CHECK ALERT CONDITIONS
# ==========================================================

def check_alerts(
    ticker,
    current_price,
    signal,
    sender_email=EMAIL,
    app_password=PASSWORD
):
    """
    Check all alerts for a ticker and send emails
    when conditions are satisfied.

    Returns:
        Number of emails sent.
    """

    df = load_alerts()

    if df.empty:
        return 0

    ticker = ticker.strip().upper()

    sent_count = 0

    alerts = df[
        df["Ticker"].astype(str).str.upper() == ticker
    ]

    if alerts.empty:
        return 0

    for _, row in alerts.iterrows():

        try:

            receiver_email = str(row["Email"]).strip()

            alert_type = str(row["Alert Type"]).strip()

            target_price = float(row["Target Price"])

            trigger = False

            # --------------------------------------
            # PRICE ABOVE
            # --------------------------------------

            if (
                alert_type == "Price Above"
                and current_price >= target_price
            ):
                trigger = True

            # --------------------------------------
            # PRICE BELOW
            # --------------------------------------

            elif (
                alert_type == "Price Below"
                and current_price <= target_price
            ):
                trigger = True

            # --------------------------------------
            # BUY SIGNAL
            # --------------------------------------

            elif (
                alert_type == "BUY"
                and str(signal).upper() == "BUY"
            ):
                trigger = True

            # --------------------------------------
            # SELL SIGNAL
            # --------------------------------------

            elif (
                alert_type == "SELL"
                and str(signal).upper() == "SELL"
            ):
                trigger = True

            # --------------------------------------
            # SEND EMAIL
            # --------------------------------------

            if trigger:

                success = send_alert_email(
                    receiver_email,
                    ticker,
                    current_price,
                    alert_type
                )

                if success:
                    sent_count += 1

        except Exception as e:

            print(
                f"Alert Error: {e}"
            )

            continue

    return sent_count


# ==========================================================
# REMOVE ALL ALERTS FOR STOCK
# ==========================================================

def remove_stock_alerts(
    ticker
):

    ticker = ticker.strip().upper()

    df = load_alerts()

    if df.empty:
        return False

    df = df[
        df["Ticker"].astype(str).str.upper()
        != ticker
    ]

    save_alerts(df)

    return True


# ==========================================================
# REMOVE ALL ALERTS FOR EMAIL
# ==========================================================

def remove_email_alerts(
    email
):

    df = load_alerts()

    if df.empty:
        return False

    df = df[
        df["Email"].astype(str).str.lower()
        != email.lower()
    ]

    save_alerts(df)

    return True


# ==========================================================
# COUNT ALERTS
# ==========================================================

def alert_count():

    return len(load_alerts())


# ==========================================================
# HAS ALERTS
# ==========================================================

def has_alerts():

    return alert_count() > 0
# ==========================================================
# ALERT STATISTICS
# ==========================================================

def alert_statistics():
    """
    Returns alert statistics.
    """

    df = load_alerts()

    if df.empty:

        return {
            "Total Alerts": 0,
            "Unique Emails": 0,
            "Unique Stocks": 0,
            "BUY Alerts": 0,
            "SELL Alerts": 0,
            "Price Above": 0,
            "Price Below": 0
        }

    return {

        "Total Alerts": len(df),

        "Unique Emails":
            df["Email"].nunique(),

        "Unique Stocks":
            df["Ticker"].nunique(),

        "BUY Alerts":
            (df["Alert Type"] == "BUY").sum(),

        "SELL Alerts":
            (df["Alert Type"] == "SELL").sum(),

        "Price Above":
            (df["Alert Type"] == "Price Above").sum(),

        "Price Below":
            (df["Alert Type"] == "Price Below").sum()

    }


# ==========================================================
# EXPORT ALERTS
# ==========================================================

def export_alerts(
    filename="email_alerts_export.csv"
):

    df = load_alerts()

    df.to_csv(
        filename,
        index=False
    )

    return filename


# ==========================================================
# IMPORT ALERTS
# ==========================================================

def import_alerts(filename):

    try:

        df = pd.read_csv(filename)

        required = [
            "Email",
            "Ticker",
            "Alert Type",
            "Target Price"
        ]

        for col in required:

            if col not in df.columns:
                raise ValueError(
                    f"Missing column: {col}"
                )

        save_alerts(df)

        return True

    except Exception as e:

        print(e)

        return False


# ==========================================================
# CLEAN ALERTS
# ==========================================================

def clean_alerts():

    df = load_alerts()

    if df.empty:
        return

    df.drop_duplicates(
        inplace=True
    )

    df.dropna(
        inplace=True
    )

    df["Email"] = (
        df["Email"]
        .astype(str)
        .str.strip()
    )

    df["Ticker"] = (
        df["Ticker"]
        .astype(str)
        .str.upper()
        .str.strip()
    )

    df["Target Price"] = pd.to_numeric(

        df["Target Price"],

        errors="coerce"

    )

    df.dropna(
        inplace=True
    )

    save_alerts(df)


# ==========================================================
# RESET ALERTS
# ==========================================================

def reset_alerts():

    df = pd.DataFrame(

        columns=[

            "Email",

            "Ticker",

            "Alert Type",

            "Target Price"

        ]

    )

    save_alerts(df)

    return True


# ==========================================================
# GET ALERT EMAILS
# ==========================================================

def get_registered_emails():

    df = load_alerts()

    if df.empty:
        return []

    return sorted(

        df["Email"]

        .dropna()

        .unique()

        .tolist()

    )


# ==========================================================
# GET REGISTERED STOCKS
# ==========================================================

def get_registered_stocks():

    df = load_alerts()

    if df.empty:
        return []

    return sorted(

        df["Ticker"]

        .dropna()

        .unique()

        .tolist()

    )


# ==========================================================
# TOTAL ALERTS
# ==========================================================

def total_alerts():

    return len(load_alerts())
# ==========================================================
# ALERT REPORT
# ==========================================================

def alert_report():
    """
    Returns a complete alert report.
    """

    df = load_alerts()

    return {
        "Alerts": df,
        "Statistics": alert_statistics(),
        "Total Alerts": total_alerts(),
        "Registered Emails": get_registered_emails(),
        "Registered Stocks": get_registered_stocks()
    }


# ==========================================================
# EMAIL CONFIGURATION CHECK
# ==========================================================

def email_configuration_ok():
    """
    Verify SMTP configuration.
    """

    if EMAIL == "":
        return False

    if PASSWORD == "":
        return False

    return True


# ==========================================================
# TEST EMAIL
# ==========================================================

def send_test_email(receiver_email):
    """
    Sends a test email.
    """

    body = """
    <h2>Live Stock Analysis & Prediction</h2>

    <p>
    Your email configuration is working correctly.
    </p>

    <p>
    You will now receive stock alerts automatically.
    </p>
    """

    return send_email(
        EMAIL,
        PASSWORD,
        receiver_email,
        "Test Email - Live Stock Analysis",
        body
    )


# ==========================================================
# RELOAD ALERTS
# ==========================================================

def reload_alerts():

    return load_alerts()


# ==========================================================
# MODULE EXPORTS
# ==========================================================

__all__ = [

    "initialize_alert_file",

    "load_alerts",

    "save_alerts",

    "save_alert",

    "delete_alert",

    "update_alert",

    "search_alerts",

    "alert_exists",

    "check_alerts",

    "remove_stock_alerts",

    "remove_email_alerts",

    "alert_statistics",

    "alert_report",

    "export_alerts",

    "import_alerts",

    "clean_alerts",

    "reset_alerts",

    "get_registered_emails",

    "get_registered_stocks",

    "total_alerts",

    "alert_count",

    "has_alerts",

    "email_configuration_ok",

    "send_email",

    "send_alert_email",

    "send_test_email",

    "reload_alerts"

]


# ==========================================================
# MAIN (Testing)
# ==========================================================

if __name__ == "__main__":

    initialize_alert_file()

    print("Email Alert Module Version 2.0 Loaded Successfully")