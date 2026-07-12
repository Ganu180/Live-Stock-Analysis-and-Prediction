from src.email_alert import *

sender_email = "iamganeshgokhale180@gmail.com"
app_password = "cbxl cefy pmtc ybjr"

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