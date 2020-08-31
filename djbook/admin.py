from django.contrib import admin

# Register your models here.
from .models import Taxonomy
from .models import Part
from .models import Rus
from .models import Eng


class TaxList(admin.ModelAdmin):
    list_display = ('id', 'rus_word', 'get_parent')


class PartList(admin.ModelAdmin):
    list_display = ('id', 'rus_word')


class RusList(admin.ModelAdmin):
    list_display = ('id', 'word')


class EngList(admin.ModelAdmin):
    list_display = ('id', 'word')


admin.site.register(Taxonomy, TaxList)
admin.site.register(Part, PartList)
admin.site.register(Rus, RusList)
admin.site.register(Eng, EngList)
