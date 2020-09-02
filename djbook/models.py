from django.db import models
from django.utils.text import slugify


class Taxonomy(models.Model):
    """Таксономия."""

    # Идентификатор.
    id = models.SmallAutoField(primary_key=True, verbose_name='ИД')
    # Название по-английски.
    eng_word = models.CharField(max_length=32, verbose_name='Англ')
    # Название по-русски.
    rus_word = models.CharField(max_length=32, verbose_name='Рус')
    # Название для URI-ссылки.
    slug = models.SlugField(
        max_length=32,
        unique=True,
        verbose_name='Слаг'
    )

    # Родительская таксономия. Связь "Many-to-One".
    # Много подкатегорий могут пренадлежать одной родительской категории.
    parent = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='ancestor',
        verbose_name='Предок'
    )

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        self.slug = self.slug.strip()
        if not self.slug:
            self.slug = slugify(self.eng_word)
        super(Taxonomy, self).save(force_insert, force_update, using, update_fields)

    def get_kids_rus(self):
        kids = Taxonomy.objects.filter(parent_id=self.id)
        return ', '.join(kid.rus_word for kid in kids)
    get_kids_rus.short_description = 'Потомки'

    def get_parent_rus(self):
        return Taxonomy.objects.get(id=self.parent_id).rus_word
        #return self.ancestor.rus_word
    # Имя столбца в списке объектов в админке.
    get_parent_rus.short_description = 'Предок'

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
