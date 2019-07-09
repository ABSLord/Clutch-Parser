from clutch_parser.celery import app
from review_parser.models import Reviews


@app.task
def parse_review_task(self, review_id):
    """Main task. """

    review = Reviews.objects.get(pk=review_id)
    review.task_id = self.request.id
    review.save()
    # TODO do parse here
