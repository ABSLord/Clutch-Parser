from django.db import models
from review_parser.tasks import parse_review_task


STATUSES = (
    ('0', 'pending'),
    ('1', 'in progress'),
    ('2', 'done'),
    ('3', 'failed')
)


class Review(models.Model):
    """Class implementing the Upwork request model. """

    status = models.CharField(
        max_length=3,
        choices=STATUSES,
        default='0'
    )
    task_id = models.CharField(max_length=100, blank=True, null=True)
    file_name = models.CharField(max_length=100)
    file = models.FileField(blank=True, null=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if not self.file:
            parse_review_task.delay(("ru", "ua", "by"), self.pk)


