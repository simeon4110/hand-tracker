import smtplib
import datetime


def send_email_report(email, report, class_number):
    """
    Simple SMTP mailer for sending reports.

    :param email:
    :param report:
    :param class_number:
    :return:
    """
    report = ''.join(report)

    s = smtplib.SMTP('mail.joshharkema.com', 587)
    s.connect('mail.joshharkema.com', 587)
    s.login('pythonmailer', 'ToyCar11')

    from_addr = 'Josh Harkema <josh@joshharkema.com>'
    to_addr = str(email)

    subj = "Report for Class Number: %s" % class_number
    date = datetime.datetime.now().strftime("%d/%m/%Y %H:%M")

    message_text = report

    msg = "From: %s\nTo: %s\nSubject: %s\nDate: %s\n\n%s" % (
        from_addr, to_addr, subj, date, message_text)

    s.sendmail(from_addr, to_addr, msg)
    s.quit()
