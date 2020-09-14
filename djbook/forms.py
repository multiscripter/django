from django import forms


class TestForm(forms.Form):

    def __init__(self, *args, **kwargs):
        super(TestForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.error_messages = {
                'required': f'Поле "{field.label}" обязательно.'
            }

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
