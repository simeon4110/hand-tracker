"""
Static helper functions. An emailer for sending reports.
"""
import smtplib
import datetime

import hand_tracker.settings

SMTP_SERVER = 'smtp.gmail.com'
SMTP_PORT = 587
SMTP_USER = 'joshuajharkema@gmail.com'


def send_email_report(email, report, class_number):
    """
    Simple SMTP mailer for sending reports. Uses GMAil SMTP servers.

    :param email: The email address to send to.
    :param report: The report list (student name, acknowledgements.)
    :param class_number: The class number.
    :return: Nothing.
    """
    s = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
    s.ehlo()
    s.starttls()
    s.ehlo()
    s.login(SMTP_USER, hand_tracker.settings.GMAIL_PASSWORD)
    s.ehlo()

    # :TODO: When this goes into full production, change the SMTP mailer.
    from_addr = 'Josh Harkema <joshuajharkema@gmail.com>'
    to_addr = str(email)

    subj = "Report for Class Number: %s" % class_number
    date = datetime.datetime.now().strftime("%d/%m/%Y %H:%M")

    # Append date and time to top line in email.
    message_text = date + "\n" + "Student name, acknowledgements \n"

    # Strip report items into a csv format.
    for item in report:
        message_text = message_text + "\n" + item[0] + ", " + item[1]

    # Format the message.
    msg = "From: %s\nTo: %s\nSubject: %s\nDate: %s\n\n%s" % (
        from_addr, to_addr, subj, date, message_text)

    s.sendmail(from_addr, to_addr, msg)
    s.quit()
