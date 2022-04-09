from calendar_app.tasks import send_notification


def send_mail_notification_signal(sender, **kwargs):
    if kwargs['instance'].official_holiday is False:
        start_time = kwargs['instance'].start_time
        user_email = kwargs['instance'].user.email
        notify = kwargs['instance'].notification.notification
        notification_time = start_time - notify

        send_notification.apply_async((user_email,), eta=notification_time)
