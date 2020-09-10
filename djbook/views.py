from django.db import connection
from django.db.models import Avg, Count
from django.http import HttpResponseRedirect
from django.shortcuts import render
import logging
from .forms import TestForm
from .models import Eng
from .models import Taxonomy

logger = logging.getLogger(__name__)


def forms(request):
    path = request.get_full_path().split('?')
    tpl = 'djbook/forms.html'
    data = {}
    if request.method == 'POST':
        meth = request.POST
        if 'form-id' in request.POST:
            if request.POST['form-id'] == 'form-1':
                form = TestForm(request.POST)
        #     if form.is_valid():
        #         name = form.cleaned_data['name']
        #         email_field = form.cleaned_data['email_field']
        #         email_input = form.cleaned_data['email_input']
        #         message = form.cleaned_data['message']
        #         turing = form.cleaned_data['turing']
        #         return HttpResponseRedirect('/forms/success/')
            elif request.POST['form-id'] == 'form-2':
                form = TestForm(request.POST)
                if form.is_valid():
                    text = form.cleaned_data['text']
                    uri = '/forms-response/?status=ok&message=' + text
                    return HttpResponseRedirect(uri)
        else:
            uri = '/forms-response/?status=fail&error=no-form-id'
            return HttpResponseRedirect(uri)

    elif path[0] == '/forms-response/':
        tpl = 'djbook/forms-response.html'
        if request.GET:
            for k, v in request.GET.items():
                data[k] = v
    else:
        data['form'] = TestForm()
    data['request'] = request
    return render(request, tpl, data)


def aggregation(request):
    eng_count = Eng.objects.count()
    eng_f_count = Eng.objects.filter(taxonomies__eng_word='birds').count()
    eng_avg_id = Eng.objects.aggregate(foo= Avg('id'))
    tax_count = Taxonomy.objects.annotate(foo=Count('eng'))
    data = {
        'eng_count': {
            'call': 'Eng.objects.count()',
            'query': 'SELECT COUNT(*) AS "__count" FROM "engvoc_eng"',
            'result': eng_count
        },
        'eng_f_count': {
            'call': "Eng.objects.filter(taxonomies__eng_word='birds').count()",
            'query': '''SELECT COUNT(*) AS "__count"<br /> 
                        FROM "engvoc_eng"<br />
                        INNER JOIN "engvoc_eng_taxonomies"<br />
                        ON ("engvoc_eng"."id" = "engvoc_eng_taxonomies"."eng_id")<br /> 
                        INNER JOIN "engvoc_tax"<br />
                        ON ("engvoc_eng_taxonomies"."taxonomy_id" = "engvoc_tax"."id")<br /> 
                        WHERE "engvoc_tax"."eng_word" = 'birds';''',
            'result': eng_f_count
        },
        'eng_avg_id': {
            'call': '''Eng.objects.aggregate(Avg('id'))''',
            'query': '''SELECT AVG("engvoc_eng"."id") AS "id__avg" FROM "engvoc_eng";''',
            'result': eng_avg_id
        },
        'tax_count': {
            'call': '''Taxonomy.objects.annotate(foo=Count('eng'))''',
            'query': '''SELECT "engvoc_tax"."id", "engvoc_tax"."eng_word",<br /> 
            "engvoc_tax"."rus_word", "engvoc_tax"."slug", "engvoc_tax"."parent_id",<br />
            COUNT("engvoc_eng_taxonomies"."eng_id") AS "foo"<br />
            FROM "engvoc_tax" LEFT OUTER JOIN "engvoc_eng_taxonomies"<br />
            ON ("engvoc_tax"."id" = "engvoc_eng_taxonomies"."taxonomy_id")<br />
            GROUP BY "engvoc_tax"."id"''',
            'result': tax_count
        }
    }
    return render(request, 'djbook/aggregation.html', data)


class Node:
    def __init__(self, obj, parent):
        self.id = obj.id
        self.obj = obj
        self.parent = parent
        self.kids = []


def get_kids(tax_set, node):
    nodes = []
    # kids = Taxonomy.objects.filter(parent_id=node.id).order_by('eng_word')
    for tax in tax_set:
        if tax.parent_id == node.id:
            child = Node(tax, node)
            node.kids.append(child)
            nodes.append(child)
    return nodes


def build_tree(tax_set, tax_id):
    tree = None
    root = None
    for tax in tax_set:
        if tax.id == tax_id:
            root = tax
            break

    if root:
        tree = Node(root, None)
        nodes = [tree]
        while nodes:
            node = nodes.pop(0)
            nodes.extend(get_kids(tax_set, node))
    return tree


def build_html_by_tree(tree):
    html = ''
    if tree and tree.kids:
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

    cursor = None
    parts = []
    try:
        cursor = connection.cursor()
        query = 'select parts.rus_word as name, count(engs.id) as qty'
        query += ' from engvoc_part parts left join engvoc_eng engs'
        query += ' on parts.id = engs.part_id'
        query += ' group by name, parts.id'
        query += ' order by parts.id'
        cursor.execute(query)
        result = cursor.fetchall()
        if result:
            for row in result:
                parts.append({'name': row[0], 'qty': row[1]})
    except Exception as ex:
        logger.error(ex)
    finally:
        if cursor:
            cursor.close()

    # Получить все англ. существительные.
    # nouns = Eng.objects.filter(part=1).order_by('word')

    tax_most_tree_html = ''
    tax_theme_tree_html = ''

    tax_set = Taxonomy.objects.all().order_by('eng_word')
    tree = build_tree(tax_set, 15)
    if tree:
        elem = '<h6 class="mt-3 list-group-head">'
        elem += '<b>' + tree.obj.eng_word + '</b> &ndash;&nbsp;'
        elem += tree.obj.rus_word + '</h6>\n'
        tax_most_tree_html = elem
        tax_most_tree_html += build_html_by_tree(tree)
        tree = build_tree(tax_set, 17)
        elem = '<h6 class="mt-3 list-group-head">'
        elem += '<b>' + tree.obj.eng_word + '</b> &ndash;&nbsp;'
        elem += tree.obj.rus_word + '</h6>\n'
        tax_theme_tree_html = elem
        tax_theme_tree_html += build_html_by_tree(tree)

    data = {
        'parts': parts,
        'tax_most_tree_html': tax_most_tree_html,
        'tax_theme_tree_html': tax_theme_tree_html
    }
    return render(request, 'djbook/home.html', data)


def theme(request, slug):
    tax = Taxonomy.objects.get(slug=slug)
    words = {}
    # PostgreSQL имеет функцию ArrayAgg(). В поле trans - кортеж.
    # words = Eng.objects.filter(taxonomies__slug=slug).annotate(trans=ArrayAgg('translations__word')).order_by('word')
    cursor = None
    try:
        cursor = connection.cursor()
        query = 'select engs.word eng, russ.word rus'
        query += ''' from engvoc_eng engs, 
        engvoc_eng_translations engs_russ, 
        engvoc_rus russ, 
        engvoc_tax tax,
        engvoc_eng_taxonomies engs_taxs'''
        query += ' where engs.id = engs_russ.eng_id'
        query += ' and engs_russ.rus_id = russ.id'
        query += ' and engs.id = engs_taxs.eng_id'
        query += ' and engs_taxs.taxonomy_id = tax.id'
        query += ' and tax.slug = %s'
        query += ' order by eng, rus'
        cursor.execute(query, [slug])
        result = cursor.fetchall()
        if result:
            for row in result:
                if row[0] in words:
                    words[row[0]] += ', ' + row[1]
                else:
                    words[row[0]] = row[1]
    except Exception as ex:
        logger.error(ex)
    finally:
        if cursor:
            cursor.close()

    data = {
        'count': len(words),
        'tax': tax,
        'words': words
    }
    return render(request, 'djbook/theme.html', data)


def http400(request, exception):
    data = {
        'code': 400,
        'text': 'Плохой запрос'
    }
    return render(request, 'djbook/http-error.html', data, status=400)


def http403(request, exception):
    data = {
        'code': 403,
        'text': 'Доступ запрещён'
    }
    return render(request, 'djbook/http-error.html', data,  status=403)


def http404(request, exception):
    data = {
        'code': 404,
        'text': 'Страница не&nbsp;найдена'
    }
    return render(request, 'djbook/http-error.html', data,  status=404)


def http500(request):
    data = {
        'code': 500,
        'text': 'Ошибка сервера'
    }
    return render(request, 'djbook/http-error.html', data, status=500)
