from django.db import models


class Item(models.Model):
    """Элемент."""

    # Идентификатор.
    id = models.SmallAutoField(primary_key=True, verbose_name='ИД')
    # Текст.
    text = models.TextField(default='', verbose_name='Текст')
