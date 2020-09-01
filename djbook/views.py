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
    kids = Taxonomy.objects.filter(parent_id=node.id)
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
        html += '<div>' + tree.obj.rus_word + '</div>\n'
        html += '<ul>\n'
        # TODO: добавить вывод дочерних таксономий итеративно.
        for kid in tree.kids:
            html += '   <li>'
            html += kid.obj.rus_word
            html += '</li>\n'
        html += '</ul>\n'
    return html


def home(request):
    # Получить все записи с полем parent = null
    # tax_list = Taxonomy.objects.filter(parent__isnull=True)
    tree = build_tree(17)
    tree_html = ''
    if tree:
        tree_html = build_html_by_tree(tree)
    tax_most_list = Taxonomy.objects.filter(parent_id=15)
    tax_theme_list = Taxonomy.objects.filter(parent_id=17).order_by('eng_word')
    data = {
        'tax_most_list': tax_most_list,
        'tax_theme_list': tax_theme_list,
        'tree_html': tree_html
    }
    return render(request, 'djbook/home.html', data)
