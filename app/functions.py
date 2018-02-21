import smtplib
from email.header import Header
from email.mime.text import MIMEText


def send_email_report(email, report, class_number):
    """
    Simple SMTP mailer for sending reports.

    :param email:
    :param report:
    :param class_number:
    :return:
    """
    msg = MIMEText(report, "html", "utf-8")

    msg['Subject'] = Header("Hand Tracker Report" + class_number, "utf-8")
    msg['From'] = "noreply@hand-tracker.com"
    msg["To"] = email

    s = smtplib.SMTP('127.0.0.1')
    s.send_message(msg)
    s.quit()
