from django.contrib import admin

# Register your models here.
from results.models import Result


class ResultAdmin(admin.ModelAdmin):
    list_display = ('student', 'score')


admin.site.register(Result, ResultAdmin)