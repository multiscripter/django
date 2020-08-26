# Create your views here.
from django.db.models import F
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.shortcuts import render
from django.urls import reverse
from django.utils import timezone
from .models import Choice
from .models import Question

# Использование пользовательских представлений.
# def index(request):
#     qlist = Question.objects.order_by('-pub_date')[:5]
#     data = {'latest_question_list': qlist}
#     return render(request, 'polls/index.html', data)
#
#
# def detail(request, question_id):
#     question = get_object_or_404(Question, pk=question_id)
#     data = {'question': question}
#     return render(request, 'polls/detail.html', data)
#
#
# def results(request, question_id):
#     question = get_object_or_404(Question, pk=question_id)
#     data = {'question': question}
#     return render(request, 'polls/results.html', data)

# ----------------------------------------------------------------------------
# Использование общих представлений, встроенных в Django (generic views).
from django.views import generic


# generic.ListView - отображает список объектов.
# По умолчанию представление ListView использует
# шаблон <app name>/<model name>_list.html.
# Если требуется использовать другой, то это нужно указать явно.
class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    # По умолчанию ListView генерирует перемнную контекста 'question_list',
    # которую неявно передаёт в шаблон. Чтобы использовать переменную
    # с другим именем нужно указать это явно:
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """
        Возвращает последние 5 опубликованных вопросов,
        исключая те, что опубликованы в будущем.
        """
        return Question.objects.filter(
            pub_date__lte=timezone.now()
        ).order_by('-pub_date')[:5]


# generic.DetailView - отображает объект детально.
# По умолчанию представление DetailView использует
# шаблон <app name>/<model name>_detail.html.
# Если требуется использовать другой, то это нужно указать явно.
class DetailView(generic.DetailView):
    # Указать Django с какой моделью работать.
    # В шаблон будет неяно передаваться переменная с именем 'question'.
    model = Question
    template_name = 'polls/detail.html'

    def get_queryset(self):
        """
        Исключает любые вопросы, которые еще не опубликованы.
        """
        return Question.objects.filter(pub_date__lte=timezone.now())


class ResultsView(generic.DetailView):
    # Указать Django с какой моделью работать.
    # В шаблон будет неяно передаваться переменная с именем 'question'.
    model = Question
    template_name = 'polls/results.html'


# ----------------------------------------------------------------------------
def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })

    # Конструкция F('votes') + 1 позволяет избежать "race conditions" для БД.
    # https://djbook.ru/rel3.0/ref/models/expressions.html#avoiding-race-conditions-using-f
    selected_choice.votes = F('votes') + 1
    selected_choice.save()
    return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))
