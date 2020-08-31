from django.db import models


class Taxonomy(models.Model):
    """Таксономия."""

    # Идентификатор.
    id = models.SmallAutoField(primary_key=True, verbose_name='ИД')
    # Название по-английски.
    eng_word = models.CharField(max_length=32, verbose_name='Англ')
    # Название по-русски.
    rus_word = models.CharField(max_length=32, verbose_name='Рус')

    # Родительская таксономия.
    parent = models.OneToOneField(
        'Taxonomy',
        on_delete=models.SET_NULL,
        null=True,
        related_name='ancestor',
        verbose_name='Предок'
    )
    # Дочерние таксономии. One-To-Many.
    kids = models.ForeignKey(
        'Taxonomy',
        models.SET_NULL,
        blank=True,
        null=True,
        related_name='descendants',
        verbose_name='Потомки'
    )

    def get_parent(self):
        return self.ancestor.rus_word

    # Имя столбца в списке объектов в админке.
    get_parent.short_description = 'Предок'

    # Возвращает строковое представление объекта.
    def __str__(self):
        return 'Taxonomy{{id:{0}, eng:{1}, rus:{2}}}'.format(
            self.id, self.eng_word, self.rus_word
        )

    class Meta:
        db_table = 'engvoc_tax'
        verbose_name = 'Таксономия'
        verbose_name_plural = 'Таксономии'


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


class Rus(models.Model):
    """Слово по-русски."""

    # Идентификатор.
    id = models.SmallAutoField(primary_key=True, verbose_name='ИД')
    # Слово.
    word = models.CharField(max_length=32, verbose_name='Слово')

    # Возвращает строковое представление объекта.
    def __str__(self):
        return 'Rus{{id:{0}, word:{1}}}'.format(self.id, self.word)

    class Meta:
        db_table = 'engvoc_rus'
        verbose_name = 'Слово по-русски'
        verbose_name_plural = 'Слова по-русски'


class Eng(models.Model):
    """Слово по-английски"""

    # Идентификатор.
    id = models.SmallAutoField(primary_key=True, verbose_name='ИД')
    # Слово.
    word = models.CharField(max_length=32, verbose_name='Слово')

    parts = models.ManyToManyField(Part)
    taxonomies = models.ManyToManyField(Taxonomy)
    translations = models.ManyToManyField(Rus)

    # Возвращает строковое представление объекта.
    def __str__(self):
        return 'Eng{{id:{0}, word:{1}}}'.format(self.id, self.word)

    class Meta:
        db_table = 'engvoc_eng'
        verbose_name = 'Слово по-английски'
        verbose_name_plural = 'Слова по-английски'
