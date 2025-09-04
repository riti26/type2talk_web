import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import config

def send_email(recipient: str, subject: str, body: str, html_body: str = None) -> bool:
    """
    Sends an email to the given recipient.
    
    Args:
        recipient (str): Email address of the recipient.
        subject (str): Subject of the email.
        body (str): Plain text body of the email.
        html_body (str): Optional HTML version of the email body.

    Returns:
        bool: True if email sent successfully, False otherwise.
    """
    try:
        message = MIMEMultipart("alternative")
        message["Subject"] = subject
        message["From"] = config.EMAIL_SENDER
        message["To"] = recipient

        # Plain text
        part1 = MIMEText(body, "plain")
        message.attach(part1)

        # Optional HTML
        if html_body:
            part2 = MIMEText(html_body, "html")
            message.attach(part2)

        context = ssl.create_default_context()
        with smtplib.SMTP_SSL(config.SMTP_SERVER, config.SMTP_PORT, context=context) as server:
            server.login(config.EMAIL_SENDER, config.EMAIL_PASSWORD)
            server.send_message(message)

        return True

    except Exception as e:
        print(f"Email send error: {e}")
        return False
