import logging
import time

from aiogram.types import User
from amplitude import BaseEvent

from loader import client_amplitude, thread_executor

logger = logging.getLogger(__name__)


def send_event(event_type, user: User):
    try:
        user_id = str(user.id)
        language = user.language_code
        current_time = time.time_ns()
        event = BaseEvent(event_type=event_type, user_id=user_id, time=current_time, language=language)
        client_amplitude.track(event)
    except Exception as e:
        logger.error(f"Failed to send {event_type=}:{user.id=} to amplitude: {e}")


def send_event_in_thread(event_type, user: User):
    thread_executor.submit(lambda: send_event(event_type, user))
