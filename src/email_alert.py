import os
import ssl
import smtplib
import pandas as pd

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from app import EMAIL, PASSWORD

# ==========================================================
# PROJECT PATHS
# ==========================================================

DATA_FOLDER = "data"

ALERT_FILE = os.path.join(
    DATA_FOLDER,
    "email_alerts.csv"
)

# ==========================================================
# CREATE DATA FOLDER
# ==========================================================

if not os.path.exists(DATA_FOLDER):

    os.makedirs(DATA_FOLDER)

# ==========================================================
# CREATE ALERT FILE
# ==========================================================

def initialize_alert_file():

    """
    Create CSV if it does not exist.
    """

    if not os.path.exists(ALERT_FILE):

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

    return pd.read_csv(ALERT_FILE)

# ==========================================================
# SAVE ALERT
# ==========================================================

def save_alert(

        email,

        ticker,

        alert_type,

        target_price

):

    initialize_alert_file()

    df = load_alerts()

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

    df.to_csv(

        ALERT_FILE,

        index=False

    )

# ==========================================================
# DELETE ALERT
# ==========================================================

def delete_alert(index):

    df = load_alerts()

    df = df.drop(index)

    df.reset_index(

        drop=True,

        inplace=True

    )

    df.to_csv(

        ALERT_FILE,

        index=False

    )

# ==========================================================
# EMAIL VALIDATION
# ==========================================================

def validate_email(email):

    if (

        "@" in email

        and "." in email

        and len(email) > 5

    ):

        return True

    return False

# ==========================================================
# ALERT TYPES
# ==========================================================

def get_alert_types():

    return [

        "Price Above",

        "Price Below",

        "BUY",

        "SELL"

    ]
# ==========================================================
# GMAIL CONFIGURATION
# ==========================================================

SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 465


# ==========================================================
# CREATE HTML EMAIL
# ==========================================================

def create_email_body(
    ticker,
    current_price,
    alert_type
):

    body = f"""
    <html>

    <body style="font-family:Arial;">

        <h2 style="color:green;">
            📈 Live Stock Analysis Alert
        </h2>

        <hr>

        <p>
        <b>Stock :</b> {ticker}
        </p>

        <p>
        <b>Alert :</b> {alert_type}
        </p>

        <p>
        <b>Current Price :</b>
        ₹ {current_price:.2f}
        </p>

        <hr>

        <p>
        This email was generated automatically by your
        <b>Live Stock Analysis & Prediction</b> project.
        </p>

    </body>

    </html>
    """

    return body


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

    try:

        message = MIMEMultipart()

        message["From"] = sender_email

        message["To"] = receiver_email

        message["Subject"] = subject

        html = MIMEText(

            body,

            "html"

        )

        message.attach(html)

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

        print("Email Sent Successfully!")

        return True

    except Exception as e:

        print("Email Error")

        print(e)

        return False
# ==========================================================
# CHECK ALL ALERTS
# ==========================================================

def check_alerts(
    ticker,
    current_price,
    signal,
    sender_email,
    app_password
):
    """
    Check all saved alerts for the given ticker.
    Send email if condition is satisfied.
    """

    alerts = load_alerts()

    if alerts.empty:
        return

    for index, row in alerts.iterrows():

        # Only check alerts for this stock
        if row["Ticker"].upper() != ticker.upper():
            continue

        receiver_email = row["Email"]
        alert_type = row["Alert Type"]
        target_price = float(row["Target Price"])

        send = False

        # --------------------------------------
        # PRICE ABOVE
        # --------------------------------------

        if alert_type == "Price Above":

            if current_price >= target_price:
                send = True

        # --------------------------------------
        # PRICE BELOW
        # --------------------------------------

        elif alert_type == "Price Below":

            if current_price <= target_price:
                send = True

        # --------------------------------------
        # BUY SIGNAL
        # --------------------------------------

        elif alert_type == "BUY":

            if signal.upper() == "BUY":
                send = True

        # --------------------------------------
        # SELL SIGNAL
        # --------------------------------------

        elif alert_type == "SELL":

            if signal.upper() == "SELL":
                send = True

        # --------------------------------------
        # SEND EMAIL
        # --------------------------------------

        if send:

            body = create_email_body(
                ticker=ticker,
                current_price=current_price,
                alert_type=alert_type
            )

            success = send_email(
                sender_email=sender_email,
                app_password=app_password,
                receiver_email=receiver_email,
                subject=f"{ticker} Stock Alert",
                body=body
            )

            if success:
                print(
                    f"Alert sent to {receiver_email}"
                )

                # Remove alert after sending
                delete_alert(index)


# ==========================================================
# TEST FUNCTION
# ==========================================================

def test_alert_system():

    sender_email = EMAIL

    app_password = PASSWORD

    save_alert(
        email="gokhaleganesh67@gmail.com",
        ticker="HDFCBANK.NS",
        alert_type="Price Above",
        target_price=1900
    )

    check_alerts(
        ticker="HDFCBANK.NS",
        current_price=1950,
        signal="BUY",
        sender_email=sender_email,
        app_password=app_password
    )

    print("Alert system test completed.")    