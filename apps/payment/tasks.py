from celery import shared_task
from django.utils import timezone
from datetime import timedelta

from .models import Payment, WebhookEvent


@shared_task
def cleanup_old_payments():
    '''Прибираємо старі платежні записи'''
    cutoff_data = timezone.now() - timedelta(days=90)

    # Видаляємо невдавшийся, відмінені платежи
    old_payment = Payment.objects.filter(
        created_at__lt=cutoff_data,
        status__in=['failed', 'cancelled']
    )

    deleted_payments, _ = old_payment.delete()

    return {'deleted_payments': deleted_payments}


@shared_task
def cleanup_old_webhook_events():
    '''Прибираємо старі webhook події'''
    cutoff_data = timezone.now() - timedelta(days=30)

    # Видаляємо старі оброблені події
    old_events = WebhookEvent.objects.filter(
        created_at__lt=cutoff_data,
        status__in=['processed', 'ignored']
    )

    deleted_events, _ = old_events.delete()

    return {'deleted_webhook_events': deleted_events}


@shared_task
def retry_failed_webhook_events():
    '''Повторна обробка webhook подій'''
    from .services import WebhookService

    retry_cutoff = timezone.now() - timedelta(hours=24)

    # Знаходимо події які невдалося обробити за останні 24 години
    failed_events = WebhookEvent.objects.filter(
        status='failed',
        created_at__lt=retry_cutoff,
    )[:50]

    processed_count = 0

    for event in failed_events:
        success = WebhookService.process_stripe_webhook(event.data)
        if success:
            event.mark_as_processed()
            processed_count += 1

    return {'reprocessed_count': processed_count}
