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
        kids = Taxonomy.objects.filter(parent_id=self.id).order_by('rus_word')
        return ', '.join(kid.rus_word for kid in kids)
    get_kids_rus.short_description = 'Потомки'

    def get_parent_rus(self):
        return Taxonomy.objects.get(id=self.parent_id).rus_word
        #return self.ancestor.rus_word
    # Имя столбца в списке объектов в админке.
    get_parent_rus.short_description = 'Предок'

    # Возвращает строковое представление объекта.
    def __str__(self):
        return 'Taxonomy{{id:{0}, eng:{1}, rus:{2}, parent_id:{3}}}'.format(
            self.id, self.eng_word, self.rus_word, self.parent_id
        )

    class Meta:
        db_table = 'engvoc_tax'
        verbose_name = 'Таксономия'
        verbose_name_plural = 'Таксономии'
