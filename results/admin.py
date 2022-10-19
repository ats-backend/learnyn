from django.contrib import admin

# Register your models here.
from results.models import Result, Token


class ResultAdmin(admin.ModelAdmin):
    list_display = ('student', 'score')


admin.site.register(Result, ResultAdmin)
admin.site.register(Token)