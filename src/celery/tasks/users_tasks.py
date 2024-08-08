from jinja2 import Template

from src.celery.celery_app import celery
from src.celery.utils import send_email, get_email_template, create_message_object
from src.celery.config import PathsConfig, EmailSubjectsConfig


@celery.task
def send_vote_notification_message(
        voted_for_user_email: str,
        voted_for_user_username: str,
        voting_user_username: str,
        voting_user_email: str,
        liked: bool,
        disliked: bool
) -> None:

    template: Template = get_email_template(path=PathsConfig.VOTE_FOR_USER_EMAIL_TEMPLATE)
    text: str = template.render(
        data={
            'voted_for_user_email': voted_for_user_email,
            'voted_for_user_username': voted_for_user_username,
            'voting_user_username': voting_user_username,
            'voting_user_email': voting_user_email,
            'vote_info': 'liked' if liked else 'disliked'
        }
    )

    message: str = create_message_object(
        text=text,
        subject=EmailSubjectsConfig.VOTED_FOR_USER,
        email_to=voted_for_user_email
    )

    send_email(to_addrs=voted_for_user_email, message=message)
