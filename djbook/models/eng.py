from django.db import models
from djbook.models import Part
from djbook.models import Rus
from djbook.models import Taxonomy


class Eng(models.Model):
    """Слово по-английски"""

    # Идентификатор.
    id = models.SmallAutoField(primary_key=True, verbose_name='ИД')
    # Слово.
    word = models.CharField(max_length=32, verbose_name='Слово')
    # Часть речи. Связь "Many-to-One".
    # Много слов могут пренадлежать одной части речи.
    part = models.ForeignKey(
        Part,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='part',
        verbose_name='Часть речи'
    )
    # Категории.
    taxonomies = models.ManyToManyField(Taxonomy, related_name='eng')
    # Переводы.
    translations = models.ManyToManyField(Rus, related_name='eng')

    # Возвращает строковое представление объекта.
    def __str__(self):
        return 'Eng{{id:{0}, word:{1}}}'.format(self.id, self.word)

    class Meta:
        db_table = 'engvoc_eng'
        verbose_name = 'Слово по-английски'
        verbose_name_plural = 'Слова по-английски'
