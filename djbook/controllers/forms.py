from django.http import HttpResponseRedirect
from django.shortcuts import render
from djbook.forms import TestForm
from djbook.models import Item


def get(request):
    path = request.get_full_path().split('?')
    tpl = 'djbook/forms.html'
    data = {}
    if path[0] == '/forms-response/':
        tpl = 'djbook/forms-response.html'
        if request.GET:
            for k, v in request.GET.items():
                data[k] = v
    else:
        data['form'] = TestForm()
        data['items'] = Item.objects.all()
    data['request'] = request
    return render(request, tpl, data)


def post(request):
    tpl = 'djbook/forms.html'
    data = {}
    if 'form-id' in request.POST:
        # if request.POST['form-id'] == 'form-1':
        #    form = TestForm(request.POST)
        #     if form.is_valid():
        #         name = form.cleaned_data['name']
        #         email_field = form.cleaned_data['email_field']
        #         email_input = form.cleaned_data['email_input']
        #         message = form.cleaned_data['message']
        #         turing = form.cleaned_data['turing']
        #         return HttpResponseRedirect('/forms/success/')
        if request.POST['form-id'] == 'form-2':
            form = TestForm(request.POST)
            if form.is_valid():
                text = form.cleaned_data['text']
                Item.objects.create(text=text)
                uri = '/forms-response/?status=ok&message=' + text
                return HttpResponseRedirect(uri)
            else:
                data['form'] = form
                data['items'] = Item.objects.all()
                return render(request, tpl, data)
    else:
        uri = '/forms-response/?status=fail&error=no-form-id'
        return HttpResponseRedirect(uri)


def common(request):
    if request.method == 'GET':
        return get(request)
    elif request.method == 'POST':
        return post(request)
