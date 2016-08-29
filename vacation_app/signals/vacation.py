from vacation_app.tasks import notification_create_vacations, \
    notification_update_vacations


def vacation_post_save(instance, **kwargs):
    if kwargs['created'] or \
            instance.state == instance.VACATION_NEW:
        notification_create_vacations.delay(instance.pk)
    else:
        notification_update_vacations.delay(instance.pk)
