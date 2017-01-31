# -*- coding: utf-8 -*-
"""
Definition of views.
"""

import os
import codecs
import copy

from django.shortcuts import render
from django.http import HttpRequest, HttpResponseRedirect
from datetime import datetime
from django.contrib.auth.decorators import login_required, permission_required
from django.conf import settings

from django.contrib.auth.models import Group
from django.contrib.auth.models import User
from app.forms import ClientProfileForm, UserProfileForm, EmployeeProfileForm,\
    GeneralAppForm
from app.models import Client, ClientCategory, Mark, Employee, ApplicationType

from django.core.exceptions import ObjectDoesNotExist
# from django.template import RequestContext
from django_ajax.decorators import ajax
from django.db.models import Q


CLIENTS_PER_PAGE = 20


def get_global_context(request):
    context = {
        'request': request,
        # 'year': datetime.now().year,
    }
    return context


def home(request):
    """Renders the home page."""
    assert isinstance(request, HttpRequest)
    context = get_global_context(request)
    return render(request, 'app/index.html', context)


def contact(request):
    """Renders the contact page."""
    assert isinstance(request, HttpRequest)
    context = get_global_context(request)
    context.update({
        'title': 'Contact',
        'message': 'Your contact page.',
    })
    return render(request, 'app/contact.html', context)


def about(request):
    """Renders the about page."""
    assert isinstance(request, HttpRequest)
    context = get_global_context(request)
    context.update({
        'title': 'About',
        'message': 'Your application description page.',
    })
    return render(request, 'app/about.html', context)


@login_required
def profile(request):
    """User profile page"""
    context = get_global_context(request)

    if request.method == 'POST':
        user = request.user
        if user.has_perm('app.employee_role'):
            employee = Employee.objects.get(user_id=user.id)
            employee_form = EmployeeProfileForm(request.POST, request.FILES,
                                                instance=employee)
            user_form = UserProfileForm(request.POST, instance=request.user)

            if user_form.is_valid() and employee_form.is_valid():
                if user_form.has_changed():
                    user.username = user_form.cleaned_data['username']
                    user.email = user_form.cleaned_data['email']
                    user.first_name = user_form.cleaned_data['first_name']
                    user.last_name = user_form.cleaned_data['last_name']
                    user.save()

                if employee_form.has_changed():
                    # saving data
                    if employee_form.cleaned_data['avatar'] and\
                            employee.avatar !=\
                                    employee_form.cleaned_data['avatar']:
                        cur_avatar = employee.avatar
                        employee.avatar = employee_form.cleaned_data['avatar']
                        delete_current_avatar_file(cur_avatar.path)
                    employee.save()
            else:
                user_data = dict(
                    (key, user_form.data[key]) for key in
                    list(set(user_form.data) & set(user_form.fields))
                )
                current_data_user = User(**user_data)

                employee_data = dict(
                    (key, employee_form.data[key]) for key in
                    list(set(employee_form.data) & set(employee_form.fields))
                    if key != 'avatar'
                )
                current_data_employee = Employee(**employee_data)
                current_data_employee.avatar = employee.avatar

                context.update({
                    'title': employee.get_short_instance_name(),
                    'cur_user': current_data_user,
                    'employee': current_data_employee,
                    'employee_form': employee_form,
                    'user_form': user_form,
                })

            return render_profile(request, context)

        elif user.has_perm('app.client_role'):
            client = Client.objects.get(user_id=request.user.id)
            client_form = ClientProfileForm(request.POST, request.FILES,
                                            instance=client)
            user_form = UserProfileForm(request.POST, instance=request.user)

            if user_form.is_valid() and client_form.is_valid():
                if user_form.has_changed():
                    user.username = user_form.cleaned_data['username']
                    user.email = user_form.cleaned_data['email']
                    user.first_name = user_form.cleaned_data['first_name']
                    user.last_name = user_form.cleaned_data['last_name']
                    user.save()

                if client_form.has_changed():
                    # saving data
                    client = Client.objects.get(user_id=user.id)
                    client.name = client_form.cleaned_data['name']
                    client.full_name = client_form.cleaned_data['full_name']
                    client.code_ipn = client_form.cleaned_data['code_ipn']
                    client.address = client_form.cleaned_data['address']
                    client.phone = client_form.cleaned_data['phone']
                    client.overall_mark_id =\
                        client_form.data['overall_mark']
                    if client_form.cleaned_data['avatar'] and\
                            client.avatar != client_form.cleaned_data['avatar']:
                        cur_avatar = client.avatar
                        client.avatar = client_form.cleaned_data['avatar']
                        delete_current_avatar_file(cur_avatar.path)
                    client.save()
            else:
                user_data = dict(
                    (key, user_form.data[key]) for key in
                    list(set(user_form.data) & set(user_form.fields))
                )
                current_data_user = User(**user_data)

                client_data = dict(
                    (key, client_form.data[key]) for key in
                    list(set(client_form.data) & set(client_form.fields))
                    if key != 'avatar'
                )
                client_data.update({
                    'overall_mark': Mark.objects.get(
                        id=client_form.data['overall_mark']),
                })
                current_data_client = Client(**client_data)
                current_data_client.balance = client.balance
                current_data_client.avatar = client.avatar

                context.update({
                    'title': client.get_title_name(),
                    'cur_user': current_data_user,
                    'client': current_data_client,
                    'client_form': client_form,
                    'user_form': user_form,
                })

            return render_profile(request, context)

    else:
        return render_profile(request, context)


def delete_current_avatar_file(file_path):
    try:
        os.remove(file_path)
    except OSError:
        pass


def render_profile(request, context):
    # define the role of current user
    user = request.user

    if user.has_perm('app.employee_role'):
        if 'role' not in context:
            context.update({
                'role': get_top_employee_role(user)
            })
        if 'cur_user' not in context or 'user_form' not in context:
            form = UserProfileForm(instance=user)
            context.update({
                'cur_user': user,
                'user_form': form,
            })
        if 'employee' not in context or 'employee_form' not in context:
            employee = Employee.objects.get(user_id=user.id)
            form = EmployeeProfileForm(instance=employee)
            context.update({
                'employee': employee,
                'title': employee.get_short_instance_name(),
                'employee_form': form,
            })
        return render(request, 'app/profile.html', context)

    elif user.has_perm('app.client_role'):
        # current user is a client
        try:
            marks = Mark.objects.all()
            context.update({
                'marks': marks,
            })
            if 'cur_user' not in context or 'user_form' not in context:
                form = UserProfileForm(instance=user)
                context.update({
                    'cur_user': user,
                    'user_form': form,
                })
            if 'client' not in context or 'client_form' not in context:
                client = Client.objects.get(user_id=request.user.id)
                form = ClientProfileForm(instance=client)
                context.update({
                    'title': client.get_title_name(),
                    'client': client,
                    'client_form': form,
                })
            return render(request, 'app/profile_client.html', context)
        except ObjectDoesNotExist as ex:
            context.update({
                'error': ex.message,
            })
            return render(request, 'app/error.html', context)

    else:
        # user doesn't have employee or client role
        return render(request, 'app/access_denied.html', context)


def get_top_employee_role(user):
    role = '--не призначено--'
    if user.has_perm('app.manager_role'):
        role = 'керівник'
    elif user.has_perm('app.secretary_role'):
        role = 'діловод'
    elif user.has_perm('app.department_head_role'):
        role = 'керівник відділу'
    elif user.has_perm('app.moderator_role'):
        role = 'модератор'
    elif user.has_perm('app.employee_role'):
        role = 'працівник'

    return role


@login_required
def apps(request):
    """Main view for page with all applications"""
    context = get_global_context(request)
    return render(request, 'app/apps.html', context)


@login_required
@permission_required('app.employee_role')
def clients(request):
    """Main view for page with all clients"""
    context = get_global_context(request)

    all_clients = Client.objects.all()
    clients_package = build_clients_package(all_clients)

    context.update({
        'clients': clients_package['clients'],
        'categories': clients_package['categories'],
        'nocategory_clients': clients_package['nocategory_clients'],
    })

    return render(request, 'app/clients.html', context)


@ajax
@login_required
@permission_required('app.employee_role')
def filter_clients(request):
    context = get_global_context(request)

    filtered_clients = get_filtered_clients(request)
    clients_package = build_clients_package(filtered_clients)

    context.update({
        'clients': clients_package['clients'],
        'categories': clients_package['categories'],
        'nocategory_clients': clients_package['nocategory_clients'],
    })

    return render(request, 'app/clients_content.html', context)


@ajax
@login_required
@permission_required('app.employee_role')
def clients_next_page(request):
    filtered_clients = get_filtered_clients(request)

    if request.POST['exclude']:
        exclude = request.POST['exclude']
        exclude = str(exclude).split(',')
        filtered_clients = filtered_clients.exclude(id__in=exclude)

    clients_package = build_clients_package(filtered_clients)

    rows_to_append = []
    append_fragments = {}
    for category in clients_package['categories']:
        for client in clients_package['clients']:
            if client.category == category:
                try:
                    new_str = str(render(request, 'app/client_table_row.html',
                                         {'client': client}).content, 'utf-8')
                except:
                    new_str = str(render(request, 'app/client_table_row.html',
                                         {'client': client}).content)
                rows_to_append.append(new_str)

        if len(rows_to_append) > 0:
            append_fragments.update({
                '#category_'+str(category.id): ''.join(rows_to_append),
            })
            rows_to_append = []

    no_category_rows_to_append = []
    for client in clients_package['clients']:
        if not client.category:
            try:
                # no_category_rows_to_append.append(get_client_row_html(client))
                new_str = str(render(request, 'app/client_table_row.html',
                                     {'client': client}).content, 'utf-8')
            except:
                new_str = str(render(request, 'app/client_table_row.html',
                                     {'client': client}).content)
            no_category_rows_to_append.append(new_str)

    if len(no_category_rows_to_append) > 0:
        append_fragments.update({
            '#category_none': ''.join(no_category_rows_to_append),
        })

    data = {
        'append-fragments': append_fragments,
    }
    return data


def get_filtered_clients(request):
    filter_str = ''
    if request.POST['filter']:
        filter_str = request.POST['filter']

    if filter_str != '':
        filtered_clients = Client.objects.filter(
            Q(name__icontains=filter_str) | Q(
                full_name__icontains=filter_str) |
            Q(user__username__icontains=filter_str) |
            Q(user__first_name__icontains=filter_str) |
            Q(user__last_name__icontains=filter_str) |
            Q(category__name__icontains=filter_str) |
            Q(address__icontains=filter_str) | Q(phone__icontains=filter_str) |
            Q(code_ipn__icontains=filter_str) | Q(
                code_1c__icontains=filter_str) |
            Q(overall_mark__name__icontains=filter_str) |
            Q(balance__icontains=filter_str)
        )
    else:
        filtered_clients = Client.objects.all()

    return filtered_clients


def build_clients_package(filtered_clients):
    clients_package = []

    all_categories = ClientCategory.objects.all()

    for category in all_categories:
        for client in filtered_clients:
            if client.category == category \
                    and len(clients_package) < CLIENTS_PER_PAGE:
                clients_package.append(client)
            elif len(clients_package) >= CLIENTS_PER_PAGE:
                break

    # add clients with no category
    if len(clients_package) < CLIENTS_PER_PAGE:
        for client in filtered_clients:
            if not client.category:
                if len(clients_package) < CLIENTS_PER_PAGE:
                    clients_package.append(client)
                else:
                    break

    not_empty_categories = []
    no_category_clients = []
    for client in clients_package:
        if client.category and client.category not in not_empty_categories:
            not_empty_categories.append(client.category)
        elif not client.category:
            no_category_clients.append(client)

    return {
        'clients': clients_package,
        'categories': all_categories,
        'nocategory_clients': no_category_clients,
    }


# def get_client_row_html(client):
#     if client.balance < 0:
#         balance_label_class = 'label-danger'
#     elif client.balance == 0:
#         balance_label_class = 'label-warning'
#     else:
#         balance_label_class = 'label-success'
#
#     if client.overall_mark:
#         overall_mark = u'<img src="{picture}" class="img-circle" ' \
#                        u'style="width: 35px; height: 35px">'\
#             .format(picture=client.overall_mark.picture)
#     else:
#         overall_mark = '---'
#     return u'<tr class="client_row" id="{id}">' \
#            u'<td><a href="client_profile/{id}"> {short_name}</a></td>' \
#            u'<td>{code_ipn}</td>' \
#            u'<td>{short_phone}</td>' \
#            u'<td><h5>' \
#            u'<span class="label {label_class}">{balance}</span>' \
#            u'</h5></td>' \
#            u'<td class="hidden-sm hidden-xs">{overall_mark}</td>' \
#            u'</tr>'.format(id=client.id, short_name=client.get_short_name(),
#                            code_ipn=client.code_ipn,
#                            short_phone=client.get_short_phone(),
#                            label_class=balance_label_class,
#                            balance=client.balance,
#                            overall_mark=overall_mark)


@login_required
def search(request):
    """Main view for search page"""
    context = get_global_context(request)
    return render(request, 'app/search.html', context)


@login_required
def statistic(request):
    """Main view for statistic page"""
    context = get_global_context(request)
    return render(request, 'app/statistic.html', context)


@login_required
def archive(request):
    """Main view for archive page"""
    context = get_global_context(request)
    return render(request, 'app/archive.html', context)


def reviews(request):
    """Main view for reviews page"""
    context = get_global_context(request)
    return render(request, 'app/reviews.html', context)


def add_review(request):
    """Main view for add review page"""
    context = get_global_context(request)
    return render(request, 'app/add_review.html', context)


@login_required
@permission_required('app.client_role')
def add_app(request):
    """Main view for creating new app page"""
    context = get_global_context(request)

    if request.POST:
        # contact_data, text_data
        app_data = parse_app_data(request.POST.dict())
        # define_app_images(request)
        app_type_id = request.POST['app_type']
        try:
            app_type = ApplicationType.objects.get(id=app_type_id)
        except ObjectDoesNotExist:
            context.update({
                'error': 'Сталася помилка при реєстрації нової заявки: '
                         'обраний тип заявки не знайдено в базі даних, '
                         'або він був видалений...'
            })
            return render(request, 'app/error.html', context)

        if app_type.form_template == 'general.html':
            return render_general_form(request, context)

    try:
        client = Client.objects.get(user_id=request.user.id)
        context.update({
            'client': client,
        })
    except ObjectDoesNotExist:
        pass

    # template_directory
    template_dir = os.path.join(settings.PROJECT_ROOT,
                                'app', 'templates', 'app',
                                'application_forms')
    # template_directory
    requirements_dir = os.path.join(settings.PROJECT_ROOT,
                                    'app', 'templates', 'app',
                                    'application_forms', 'requirements')
    app_types = ApplicationType.objects.all()
    for app_type in app_types:
        app_type.template_form = os.path.join(template_dir,
                                              app_type.form_template)

        if os.path.isfile(os.path.join(requirements_dir,
                                       app_type.form_template)):
            app_type.requirements_form = os.path.join(requirements_dir,
                                                      app_type.form_template)

        if app_type.form_template == 'general.html':
            form = GeneralAppForm({
                'contact_person': request.user.get_full_name(),
                'contact_phone': client.phone,
                'text_text': '',
            })
            app_type.form = form

    context.update({
        'app_types': app_types,
    })

    return render(request, 'app/add_app.html', context)


def render_general_form(request, context):
    form = GeneralAppForm(request.POST, request.FILES)
    if len(request.FILES.getlist('app_scan')) > 0:
        form.fields['contact_person'].required = False
        form.fields['contact_phone'].required = False
        form.fields['text_text'].required = False

    if form.is_valid():
        # add new app
        pass
    else:
        context.update({
            'form': form,
        })
        return render(request, 'app/add_app.html', context)


def define_app_images(request):
    app_type_id = request.POST['app_type']
    if 'app-scan_' + app_type_id in request.FILES.keys():
        request.FILES.update({
            'app_scan': request.FILES.getlist('app-scan_' + app_type_id)
        })

    if 'app-attach_' + app_type_id in request.FILES.keys():
        request.FILES.update({
            'app_attach': request.FILES.getlist('app-attach_' + app_type_id)
        })


def parse_app_data(post_dict):
    contact_data, text_data = {}, {}
    for key, value in post_dict.items():
        if 'text_' in key:
            # new_key = str(key).replace('text_', '')
            text_data.update({
                key: value
            })
        if 'contact_' in key:
            # new_key = str(key).replace('contact_', '')
            contact_data.update({
                key: value
            })
    return {
        'contact_data': contact_data,
        'text_data': text_data,
    }


@login_required
def sync_clients(request):
    """View to sync clients with csv file, exported from 1c"""
    context = get_global_context(request)

    errors, logs = [], []
    if request.user.is_authenticated() and request.user.is_superuser:
        csvfile = codecs.open(os.path.join(settings.MEDIA_ROOT,
                                           'uploads', '1c', 'clients.csv'),
                              'r', 'cp1251')

        rows = csvfile.read().split('\n')
        fields = [
            'code_1c',
            'code_ipn',
            'name',
            'full_name',
            'address',
            'phone',
            'email',
            'balance',
            'first_name',
            'last_name'
        ]
        all_clients = [dict(zip(fields, row.split(';'))) for row in rows]
        all_clients = all_clients[1:]
        counter = -1
        for client in all_clients:
            # if client['code_1c'] == '000000148':
            counter += 1
            progress = float(counter/len(all_clients)*100)
            if client['code_1c'] != '' and client['name'] != ''\
                    and client['code_ipn'] != '':
                try:
                    db_client = Client.objects.get(code_1c=client['code_1c'])
                    db_user = User.objects.get(id=db_client.user_id)
                except ObjectDoesNotExist:
                    # creating new client
                    try:
                        new_user = User.objects.create_user(
                            username=client['code_ipn'],
                            email=client['email'],
                            password=client['code_ipn'],
                        )
                    except Exception as e:
                        errors.append(e.message)
                        continue
                    new_user.first_name = client['first_name']
                    new_user.last_name = client['last_name']
                    try:
                        new_user.save()
                        g = Group.objects.get(name='Clients')
                        g.user_set.add(new_user)
                    except Exception as e:
                        errors.append(e.message)
                        continue
                    else:
                        try:
                            balance = float(
                                str(client['balance']).replace(',', '.')
                            )
                        except Exception as e:
                            errors.append(e.message)
                            continue
                        new_client = Client.objects.create(**{
                            'user_id': new_user.id,
                            'code_1c': client['code_1c'],
                            'code_ipn': client['code_ipn'],
                            'name': client['name'],
                            'full_name': client['full_name'],
                            'address': client['address'],
                            'phone': client['phone'],
                            'balance': balance,
                        })
                        try:
                            new_client.save()
                            logs.append('new client added: ' +
                                        new_client.get_full_instance_name())
                        except Exception as e:
                            new_user.delete()
                            errors.append(e.message)
                            continue
                else:
                    # updating existing client
                    has_changes = None
                    if db_user.first_name == '' and client['first_name'] != '':
                        db_user.first_name = client['first_name']
                        has_changes = True

                    if db_user.last_name == '' and client['last_name'] != '':
                        db_user.last_name = client['last_name']
                        has_changes = True

                    if db_user.email == '' and client['email'] != '':
                        db_user.email = client['email']
                        has_changes = True

                    if has_changes:
                        db_user.save()
                        has_changes = None

                    if db_client.code_ipn == '' and client['code_ipn'] != '':
                        db_client.code_ipn = client['code_ipn']
                        has_changes = True

                    if db_client.name == '' and client['name'] != '':
                        db_client.name = client['name']
                        has_changes = True

                    if db_client.full_name == '' and client['full_name'] != '':
                        db_client.full_name = client['full_name']
                        has_changes = True

                    if db_client.address == '' and client['address'] != '':
                        db_client.address = client['address']
                        has_changes = True

                    if db_client.phone == '' and client['phone'] != '':
                        db_client.phone = client['phone']
                        has_changes = True

                    try:
                        balance = float(
                            str(client['balance']).replace(',', '.')
                        )
                    except Exception as e:
                        errors.append(e.message)
                        continue
                    if db_client.balance != balance:
                        db_client.balance = balance
                        has_changes = True

                    if has_changes:
                        db_client.save()
                    logs.append('client: ' +
                                db_client.get_full_instance_name() +
                                ' updated')

            else:
                errors.append('client with empty required fields: ' +
                              str(client))

        if len(errors) != 0:
            context.update({
                'errors': errors,
                'message': 'Під час синхронізації виникли помилки...',
            })
        else:
            context.update({
                'message': 'Синхронізація клієнтів відбулася успішно',
            })

        if len(logs) != 0:
            context.update({
                'logs': logs,
            })
        return render(request, 'app/result.html', context)

    else:
        # this is not a superuser. He can't sync clients!
        errors.append('У Вас, нажаль, немає доступу до цієї сторінки :(')
        context.update({
            'errors': errors,
        })
        return render(request, 'app/result.html', context)


def update_client_balance(request):
    context = get_global_context(request)
    errors, logs = [], []
    client, balance = 'none', '0'
    if request.GET['key'] and request.GET['key'] == 'abracadabra':
        if request.method == 'GET':
            if request.GET['client'] and request.GET['balance']:
                try:
                    balance = float(
                        str(request.GET['balance']).replace(',', '.')
                    )
                except Exception as e:
                    errors.append(e.message)
                else:
                    kod = request.GET['client']
                    try:
                        client = Client.objects.get(code_1c=kod)
                    except ObjectDoesNotExist:
                        errors.append('client with code: [' + kod +
                                      '] doesn\'t exist in DB')
                    else:
                        # if we found the client - updating his balance
                        if client.balance != int(balance):
                            client.balance = balance
                            client.save()
                            logs.append('client balance [code: ' + kod +
                                        '] successfully updated! ' +
                                        'new balance: ' + str(client.balance))
                        else:
                            logs.append('client balance doesn\'t changed: '
                                        + str(balance) + ' grn.')
            else:
                errors.append('Field client or balance doesn\'t exist!')
        else:
            errors.append('Not a GET request')
    else:
        errors.append('invalid key!')

    if len(errors) != 0:
        context.update({
            'errors': errors,
            'message': 'Some errors occurred while updating client...',
        })
    else:
        message = 'Success!'
        context.update({
            'message': message,
        })
        if len(logs) != 0:
            context.update({
                'logs': logs,
            })

    return render(request, 'app/api_result.html', context)


@login_required
@permission_required('app.employee_role')
def client_profile(request, client_id):
    context = get_global_context(request)
    errors = []
    try:
        client = Client.objects.get(id=client_id)
        user = User.objects.get(id=client.user_id)
        context.update({
            'title': client.get_title_name(),
            'client': client,
            'cur_user': user,
        })
    except ObjectDoesNotExist:
        errors.append('Сторінка профілю клієнта, що Ви намагаєтеся знайти, '
                      'не знайдена в базі даних...')

    if len(errors) > 0:
        context.update({
            'errors': errors,
        })

    return render(request, 'app/client_profile.html', context)
