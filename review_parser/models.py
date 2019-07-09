from django.db import models


STATUSES = (
    ('0', 'pending'),
    ('1', 'in progress'),
    ('2', 'done'),
    ('3', 'failed')
)


class Reviews(models.Model):
    """Class implementing the Upwork request model. """

    status = models.CharField(
        max_length=3,
        choices=STATUSES,
        default='0'
    )
    task_id = models.CharField(max_length=100, blank=True, null=True)
    file_name = models.CharField(max_length=100)
    file = models.FileField()
