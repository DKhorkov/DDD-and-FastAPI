from celery import Celery

# from src.celery.tasks.users_tasks import send_vote_notification_message


def test_send_vote_notification_message(celery_app: Celery) -> None:
    """
    Include in your tests after changing SMTP host and port to valid in .env.test file.
    """
    pass

    # assert send_vote_notification_message.apply(
    #     kwargs={
    #         'voted_for_user_email': 'tested@yandex.ru',
    #         'voted_for_user_username': 'tested',
    #         'voting_user_username': 'test',
    #         'voting_user_email': 'test@yandex.ru',
    #         'liked': False,
    #         'disliked': True
    #     }
    # ).get() is None
