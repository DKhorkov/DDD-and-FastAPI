from celery import Celery

from src.celery.tasks.users_tasks import send_verify_email_message
from tests.config import FakeUserConfig


def test_send_verify_email_message_success(celery_app: Celery) -> None:
    assert send_verify_email_message.apply(
        kwargs={
            'user_id': 1,
            'username': FakeUserConfig.USERNAME,
            'email': FakeUserConfig.EMAIL
        }
    ).get() is None
