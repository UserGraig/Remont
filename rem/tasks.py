from celery import shared_task
import logging

logger = logging.getLogger(__name__)

@shared_task
def send_reminder_email():
    logger.info("Отправка напоминания по электронной почте")
    # Добавьте вашу логику отправки почты

@shared_task
def cleanup_old_orders():
    logger.info("Очистка старых заказов")
    # Добавьте вашу логику для очистки старых заказов
