# -*- coding: utf-8 -*-
from django.conf import settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns, static

import app.views as views
from django.conf.urls import url

from datetime import datetime
from app.forms import CustomAuthenticationForm, CustomPasswordChangeForm
# from app.views import *
# from app.models import *
from django.contrib.auth.views import login, logout,\
    password_change, password_change_done


urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^contact$', views.contact, name='contact'),
    url(r'^about$', views.about, name='about'),
    url(r'^login', login,
        {
            'template_name': 'app/login.html',
            'authentication_form': CustomAuthenticationForm,
            'extra_context':
                {
                    'title': 'Залогуйтеся, будь ласка',
                    'year': datetime.now().year,
                }
        }, name='login'),
    url(r'^logout$', logout,
        {
            'next_page': '/'
        }, name='logout'),
    url(r'^password_change/$', password_change,
        {
            'template_name': 'app/password_change.html',
            'password_change_form': CustomPasswordChangeForm,
            'extra_context':
                {
                    'title': 'Ви можете змінити Ваш пароль'
                }
        }, name='password_change'),
    url(r'^password_change/done/$', password_change_done,
        {
            'template_name': 'app/password_change_done.html',
        }, name='password_change_done'),
    url(r'^profile/$', views.profile, name='profile'),
    url(r'^apps$', views.apps, name='apps'),
    url(r'^clients$', views.clients, name='clients'),
    url(r'^search', views.search, name='search'),
    url(r'^statistic/$', views.statistic, name='statistic'),
    url(r'^archive/$', views.archive, name='archive'),
    url(r'^reviews/$', views.reviews, name='reviews'),
    url(r'^addreview/$', views.add_review, name='add_review'),
    url(r'^addapp/$', views.add_app, name='add_app'),
    # url(r'^result/$', views.render_result, name='result'),
    url(r'^sync_clients$', views.sync_clients, name='sync_clients'),
    url(r'^update_client_balance', views.update_client_balance),
    url(r'^clients/(?P<client_id>[0-9]+)/$', views.client_profile,
        name='client_profile'),
    url(r'^filter_clients$', views.filter_clients,
        name='filter_clients'),
    url(r'^clients_next_page$', views.clients_next_page,
        name='clients_next_page'),
]

urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
