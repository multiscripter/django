from django import forms


class TestForm(forms.Form):
    # name = forms.CharField(label='имя', max_length=100)
    text = forms.CharField(
        label='Ваше имя',
        help_text='Введите своё имя тут',
        widget=forms.TextInput(attrs={
            'class': 'form-control text-field',
            'name': 'firstName',
            'size': 99,
            'title': 'title ваше имя'
        })
    )
    # email_field = forms.EmailField(label='field Е-почта')
    # email_input = forms.EmailInput()
    # message = forms.CharField(widget=forms.Textarea)
    # turing = forms.BooleanField()
