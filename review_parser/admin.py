from django.contrib import admin
from review_parser.models import Review


@admin.register(Review)
class ReviewsAdmin(admin.ModelAdmin):

    exclude = ('task_id', 'status')
