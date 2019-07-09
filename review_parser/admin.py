from django.contrib import admin
from review_parser.models import Reviews


@admin.register(Reviews)
class RequestAdmin(admin.ModelAdmin):
    """Class setting the rendering of the change and list view for admin interface. """

    exclude = ('task_id', )
