from flask_mail import Mail

mail = Mail()


def send_mail(subject, sender, recipients, html):
    mail.send_message(
        subject,
        sender=sender,
        recipients=recipients,
        html=html
    )
