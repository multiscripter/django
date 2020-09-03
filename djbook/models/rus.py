from django.db import models


class Rus(models.Model):
    """Слово по-русски."""

    # Идентификатор.
    id = models.SmallAutoField(primary_key=True, verbose_name='ИД')
    # Слово.
    word = models.CharField(
        max_length=32,
        unique=True,
        verbose_name='Слово'
    )

    # Возвращает строковое представление объекта.
    def __str__(self):
        return 'Rus{{id:{0}, word:{1}}}'.format(self.id, self.word)

    class Meta:
        db_table = 'engvoc_rus'
        verbose_name = 'Слово по-русски'
        verbose_name_plural = 'Слова по-русски'
