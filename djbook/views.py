from django.shortcuts import render
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
            elem = '<div><b>' + kid.obj.eng_word + '</b> &ndash;&nbsp;'
            elem += kid.obj.rus_word + '</div>\n'
            if kid.kids:
                elem += build_html_by_tree(kid)
            html += elem
            html += '</li>\n'
        html += '</ul>\n'
    return html


def home(request):
    # Получить все записи с полем parent = null
    # tax_list = Taxonomy.objects.filter(parent__isnull=True)

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
        'tax_most_tree_html': tax_most_tree_html,
        'tax_theme_tree_html': tax_theme_tree_html
    }
    return render(request, 'djbook/home.html', data)
