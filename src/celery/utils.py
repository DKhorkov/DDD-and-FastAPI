import smtplib
import ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from typing import List, Union
from jinja2 import Environment, FileSystemLoader, Template

from src.celery.config import smtp_config, PathsConfig


def get_email_template(path: str) -> Template:
    return Environment(
        loader=FileSystemLoader(
            searchpath=PathsConfig.EMAIL_TEMPLATES
        )
    ).get_template(
        name=path
    )


def create_message_object(text: str, subject: str, email_to: str, email_from: str = smtp_config.SMTP_LOGIN) -> str:
    message = MIMEMultipart()
    message['Subject'] = subject
    message['From'] = email_from
    message['To'] = email_to

    message.attach(MIMEText(text, 'html'))
    return message.as_string()


def send_email(to_addrs: Union[str, List[str]], message: str) -> None:
    with smtplib.SMTP_SSL(
            host=smtp_config.SMTP_HOST,
            port=smtp_config.SMTP_PORT,
            context=ssl.create_default_context()
    ) as server:

        server.login(user=smtp_config.SMTP_LOGIN, password=smtp_config.SMTP_PASSWORD)
        server.sendmail(
            from_addr=smtp_config.SMTP_LOGIN,
            to_addrs=to_addrs,
            msg=message
        )
