import smtplib
import datetime

import hand_tracker.settings


def send_email_report(email, report, class_number):
    """
    Simple SMTP mailer for sending reports.

    :param email:
    :param report:
    :param class_number:
    :return:
    """

    s = smtplib.SMTP('smtp.gmail.com', 587)
    s.ehlo()
    s.starttls()
    s.ehlo()
    s.login('joshuajharkema@gmail.com', hand_tracker.settings.GMAIL_PASSWORD)
    s.ehlo()

    from_addr = 'Josh Harkema <joshuajharkema@gmail.com>'
    to_addr = str(email)

    subj = "Report for Class Number: %s" % class_number
    date = datetime.datetime.now().strftime("%d/%m/%Y %H:%M")

    message_text = ""

    for item in report:
        message_text = message_text + "\n" + item[0] + ", " + item[1]

    msg = "From: %s\nTo: %s\nSubject: %s\nDate: %s\n\n%s" % (
        from_addr, to_addr, subj, date, message_text)

    s.sendmail(from_addr, to_addr, msg)
    s.quit()
