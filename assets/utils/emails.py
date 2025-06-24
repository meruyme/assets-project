from django.core.mail import EmailMessage


def send_emails(emails: list, email_subject: str, email_message: str):
    message = EmailMessage(
        email_subject,
        email_message,
        to=emails,
    )
    message.content_subtype = "html"
    message.send()
