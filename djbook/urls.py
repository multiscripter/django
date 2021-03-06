"""djbook URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import url
from django.contrib import admin
from django.urls import include, path
from django.views.generic import RedirectView
from djbook.controllers import forms
from djbook import views

urlpatterns = [
    # Страница с формами.
    path('forms-response/', forms.common, name='forms'),
    path('forms/', forms.common, name='forms'),
    # Тестирование методов агрегации моделей.
    path('aggregation/', views.aggregation, name='aggregation'),
    # Голосовалка.
    path('polls/', include('polls.urls')),
    # Админка.
    path('admin/', admin.site.urls),
    # Страница категории. ex: /theme/animals/
    path('theme/<slug:slug>/', views.theme, name='theme'),
    # Главная страница сайта.
    path('', views.home, name='home'),
    # Инструкция на случай если favicon.ico не прописан в тэге head страницы
    # и не настроена отдача favicon.ico в Nginx.
    url(r'^favicon\.ico$', RedirectView.as_view(url='/static/favicon.ico'), name='favicon'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

handler400 = 'djbook.views.http400'
handler403 = 'djbook.views.http403'
handler404 = 'djbook.views.http404'
handler500 = 'djbook.views.http500'
