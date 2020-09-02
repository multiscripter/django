from django.shortcuts import render
from .models import Eng
from .models import Part
from .models import Taxonomy


class Node:
    def __init__(self, obj, parent):
        self.id = obj.id
        self.obj = obj
        self.parent = parent
        self.kids = []


def get_kids(node):
    nodes = []
    kids = Taxonomy.objects.filter(parent_id=node.id).order_by('eng_word')
    if kids:
        for kid in kids:
            child = Node(kid, node)
            node.kids.append(child)
            nodes.append(child)
    return nodes


def build_tree(tax_id):
    tree = None
    root = Taxonomy.objects.get(id=tax_id)
    if root:
        tree = Node(root, None)
        nodes = [tree]
        while nodes:
            node = nodes.pop(0)
            nodes.extend(get_kids(node))
    return tree


def build_html_by_tree(tree):
    html = ''
    if tree.kids:
        html += '<ul class="list-group list-group-compact">\n'
        for kid in tree.kids:
            html += '   <li class="list-group-item list-group-item-action">'
            elem = f'<a class="ref" href="theme/{kid.obj.slug}/">'
            elem += '<b>' + kid.obj.eng_word + '</b> &ndash;&nbsp;'
            elem += kid.obj.rus_word + '</a>\n'
            if kid.kids:
                elem += build_html_by_tree(kid)
            html += elem
            html += '</li>\n'
        html += '</ul>\n'
    return html


def home(request):
    # Получить все записи с полем parent = null
    # tax_list = Taxonomy.objects.filter(parent__isnull=True)

    # Получить все части речи.
    parts = Part.objects.all()
    if parts:
        for part in parts:
            part.count = Eng.objects.filter(part_id=part.id).count()
    # Получить все англ. существительные.
    # nouns = Eng.objects.filter(part=1).order_by('word')

    tree = build_tree(15)
    elem = '<h6 class="mt-3 list-group-head">'
    elem += '<b>' + tree.obj.eng_word + '</b> &ndash;&nbsp;'
    elem += tree.obj.rus_word + '</h6>\n'
    tax_most_tree_html = elem
    if tree:
        tax_most_tree_html += build_html_by_tree(tree)

    tree = build_tree(17)
    elem = '<h6 class="mt-3 list-group-head">'
    elem += '<b>' + tree.obj.eng_word + '</b> &ndash;&nbsp;'
    elem += tree.obj.rus_word + '</h6>\n'
    tax_theme_tree_html = elem
    if tree:
        tax_theme_tree_html += build_html_by_tree(tree)

    data = {
        'parts': parts,
        #'nouns': nouns,
        'tax_most_tree_html': tax_most_tree_html,
        'tax_theme_tree_html': tax_theme_tree_html
    }
    return render(request, 'djbook/home.html', data)


def theme(request, slug):
    tax = Taxonomy.objects.get(slug=slug)
    words = Eng.objects.filter(taxonomies=tax).order_by('word')
    if words:
        for word in words:
            word.trans = '<br>'.join(rus.word for rus in word.translations.all())

    data = {
        'count': len(words),
        'tax': tax,
        'words': words
    }
    return render(request, 'djbook/theme.html', data)
