from django.contrib import admin
from .models import Question, Choice


class QuestionAdmin(admin.ModelAdmin):
    list_display = ["id", "question_text", "pub_date"]
    list_filter = ["pub_date"]
    ordering = ["pub_date"]
    search_fields = ["question_text"]


class ChoiceAdmin(admin.ModelAdmin):
    list_display = ["id", "question", "choice_text", "votes"]
    list_filter = ["question", "votes"]
    ordering = ["question", "choice_text"]
    search_fields = ["choice_text", "question__question_text"]


admin.site.register(Question, QuestionAdmin)
admin.site.register(Choice, ChoiceAdmin)