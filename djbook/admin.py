from django.contrib import admin

# Register your models here.
from .models import Taxonomy
from .models import Part
from .models import Rus
from .models import Eng


class TaxonomyAdmin(admin.ModelAdmin):
    list_display = ('id', 'rus_word', 'slug', 'get_parent_rus', 'get_kids_rus')
    prepopulated_fields = {"slug": ("eng_word",)}


class PartList(admin.ModelAdmin):
    list_display = ('id', 'rus_word')


class RusList(admin.ModelAdmin):
    list_display = ('id', 'word')


class EngList(admin.ModelAdmin):
    list_display = ('id', 'word')


admin.site.register(Taxonomy, TaxonomyAdmin)
admin.site.register(Part, PartList)
admin.site.register(Rus, RusList)
admin.site.register(Eng, EngList)
