from django.db import models


class Part(models.Model):
    """Часть речи."""

    # Идентификатор.
    id = models.SmallAutoField(primary_key=True, verbose_name='ИД')
    # Название по-английски.
    eng_word = models.CharField(max_length=32, verbose_name='Англ')
    # Название по-русски.
    rus_word = models.CharField(max_length=32, verbose_name='Рус')

    # Возвращает строковое представление объекта.
    def __str__(self):
        return 'Part{{id:{0}, eng:{1}, rus:{2}}}'.format(
            self.id, self.eng_word, self.rus_word
        )

    class Meta:
        db_table = 'engvoc_part'
        verbose_name = 'Часть речи'
        verbose_name_plural = 'Части речи'
