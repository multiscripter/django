from django import forms


class TestForm(forms.Form):
    # name = forms.CharField(label='имя', max_length=100)
    text = forms.CharField(
        label='Ваш текст',
        help_text='Введите свой текст тут',
        widget=forms.TextInput(attrs={
            'class': 'form-control text-field',
            'name': 'text',
            'size': 99,
            'title': 'title ваш текст'
        })
    )
    # email_field = forms.EmailField(label='field Е-почта')
    # email_input = forms.EmailInput()
    # message = forms.CharField(widget=forms.Textarea)
    # turing = forms.BooleanField()
