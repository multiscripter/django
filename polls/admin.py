from django.contrib import admin

# Register your models here.
from .models import Question
from .models import Choice

# Получить путь к установленному Django.
# python -c "import django; print(django.__path__)"

# Создаст для Choice отдельную страницу в админке.
# admin.site.register(Choice)

# class ChoiceInline(admin.TabularInline):  # Компактный вид формы.
class ChoiceInline(admin.StackedInline):  # Обычный вид формы.
    model = Choice
    # По умолчанию показывать формы для трех ответов.
    extra = 3


class QuestionAdmin(admin.ModelAdmin):
    # Порядок полей в админке.
    # fields = ['pub_date', 'question_text']

    # Перечень значений вопроса отображаемого в списке вопросов.
    list_display = ('question_text', 'pub_date', 'was_published_recently')

    # Добавить фильтр по дате публикации.
    list_filter = ['pub_date']

    # Добавить возможность поиска по записям.
    search_fields = ['question_text']

    # Удобно разбить большую форму на несколько наборов полей:
    fieldsets = [
        (None, {'fields': ['question_text']}),
        ('Date information', {'fields': ['pub_date'], 'classes': ['collapse']}),
    ]
    # Объекты Choice редактируются на странице Question.
    inlines = [ChoiceInline]


admin.site.register(Question, QuestionAdmin)
