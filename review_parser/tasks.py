from clutch_parser.celery import app
from review_parser.core.review_parser import review_parser


@app.task
def parse_review_task(countries, review_id):
    """Main task. """
    review_parser(countries, review_id)
