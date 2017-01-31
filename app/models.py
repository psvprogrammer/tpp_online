# -*- coding: utf-8 -*-
"""
Definition of models.
"""
from datetime import datetime
from django.contrib.auth.models import User
from django.db import models
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.utils.html import format_html

from os import listdir, path
from os.path import isfile, join

SHORT_NAME_LEN = 20


def generate_filename(instance, filename):
    return '{:%m-%d-%Y_%H:%M:%S}_{}'.format(datetime.now(), filename)


def get_client_avatar_upload_path(instance, filename):
    return 'uploads/client/avatar/' +\
           generate_filename(instance, filename)


def get_employee_avatar_upload_path(instance, filename):
    return 'uploads/employee/avatar/' +\
           generate_filename(instance, filename)


def get_app_scan_upload_path(instance, filename):
    return 'uploads/client/app/scan/' +\
           generate_filename(instance, filename)


def get_app_attach_upload_path(instance, filename):
    return 'uploads/client/app/attach/' +\
           generate_filename(instance, filename)


def get_resp_scan_upload_path(instance, filename):
    return 'uploads/employee/resp/scan/' +\
           generate_filename(instance, filename)


def get_resp_attach_upload_path(instance, filename):
    return 'uploads/employee/resp/attach/' +\
           generate_filename(instance, filename)


def get_resp_bill_upload_path(instance, filename):
    return 'uploads/employee/resp/bill/' +\
           generate_filename(instance, filename)


def get_mark_upload_path(instance, filename):
    return 'marks/' + \
           generate_filename(instance, filename)


def get_forms_choices(forms_directory=''):
    template_dir = join(settings.PROJECT_ROOT,
                        'app', 'templates', 'app', forms_directory)
    if path.isdir(template_dir) and path.exists(template_dir):
        template_files = [f for f in listdir(template_dir)
                          if isfile(join(template_dir, f))]
        template_names = [f.replace('.html', '') for f in template_files]
        return tuple(zip(template_files, template_names))
    else:
        return (
            ('', 'ПОМИЛКА пошуку шаблонів форм'),
        )


class Label(models.Model):
    """Model that represents possible color labels"""
    class Meta:
        verbose_name = 'Кольорова мітка'
        verbose_name_plural = 'Кольорові мітки'

    name = models.CharField('* Назва мітки',
                            help_text='Вкажіть назву кольорової мітки',
                            max_length=50)
    # color will be stored as text in HEX format. Default is ffffff (white)
    color = models.CharField('* Колір',
                             help_text='Вкажіть колір, що буде '
                                       'використовуватися для цієї мітки'
                                       'Код кольору у HEX форматі (6 цифр)',
                             max_length=6, default='ffffff')

    def get_full_label_name(self):
        # return '{}'.format(self.name)
        return format_html(
            '<span style="color:#{};">{}</span>',
            self.color, self.name
        )

    def __str__(self):
        return self.get_full_label_name()


class ClientCategory(models.Model):
    """Model for client category"""
    class Meta:
        verbose_name = 'Категорія клієнта'
        verbose_name_plural = 'Категорії клієнтів'

    name = models.CharField('* Назва категорії',
                            help_text='Вкажіть назву категорії',
                            max_length=50, default='')
    description = models.CharField('Опис', help_text='Опис категорії',
                                   max_length=100,
                                   blank=True, default='')
    discount = models.IntegerField('Знижка', help_text='Відсоток знижки',
                                   blank=True, default=0)
    label = models.ForeignKey(Label, verbose_name='Кольорова мітка',
                              help_text='Вкажіть кольорову мітку для групи.',
                              null=True, blank=True,
                              on_delete=models.SET_NULL)

    def get_full_instance_name(self):
        if self.discount != 0:
            name = '{} (знижка {}%)'.format(self.name, self.discount)
        else:
            name = '{}'.format(self.name)
        return name

    def __str__(self):
        return self.get_full_instance_name()

    def get_client_num(self):
        return len(Client.objects.filter(category_id=self.id))


class Mark(models.Model):
    """Model that represents possible marks in the system"""
    class Meta:
        verbose_name = 'Оцінка'
        verbose_name_plural = 'Оцінки'

    name = models.CharField('* Назва',
                            help_text='Вкажіть назву оцінки',
                            max_length=30)
    absolute = models.IntegerField('* Абсолютне значення',
                                   help_text='Абсолютне числове значення, '
                                             'що буде використовуватися'
                                             'для порівняння. Чим більше '
                                             'абсолютне значення - тим '
                                             'краща оцінка',
                                   default=0)
    picture = models.ImageField('* Картинка',
                                help_text='Вкажіть картинку, що буде '
                                          'асоційована з цією оцінкою',
                                null=True, blank=True,
                                upload_to=get_mark_upload_path)

    def get_full_instance_name(self):
        return '{} (оцінка - {})'.format(self.absolute, self.name)

    def __str__(self):
        return self.get_full_instance_name()


class Client(models.Model):
    """Model for client"""
    class Meta:
        verbose_name = 'Клієнт'
        verbose_name_plural = 'Клієнти'
        permissions = (
            ('client_role', 'User has client rights'),
        )

    default_avatar_url = settings.MEDIA_URL + 'default-profile.jpg'

    name = models.CharField('* Назва', help_text='Назва клієнта',
                            max_length=250, default='')
    full_name = models.CharField('Повна назва',
                                 help_text='Повна назва клієнта',
                                 max_length=250, blank=True, default='')
    user = models.ForeignKey(User,
                             verbose_name='* Користувач',
                             help_text='Відповідний користувач',
                             on_delete=models.PROTECT)
    category = models.ForeignKey(ClientCategory,
                                 verbose_name='Категорія клієнтів',
                                 help_text='Вкажіть категорію клієнта',
                                 blank=True, null=True,
                                 on_delete=models.SET_NULL)
    balance = models.IntegerField('Баланс',
                                  help_text='Поточний сальдовий баланс',
                                  blank=True, default=0)
    avatar = models.ImageField('Аватар',
                               help_text='Завантажте Ваше фото',
                               default=default_avatar_url, blank=True,
                               upload_to=get_client_avatar_upload_path)
    address = models.CharField('Адреса',
                               help_text='Фактична адреса клієнта',
                               max_length=100, blank=True, default='')
    phone = models.CharField('Телефон',
                             help_text='Контактний телефон. Максимум 20 цифр',
                             max_length=20, blank=True, default='')
    fop = models.BooleanField('ФОП',
                              help_text='Відмітьте, якщо '
                                        'це фізична особа підприємець',
                              default=False)
    code_ipn = models.CharField('ЄДРПОУ/ДРФО',
                                help_text='Код ЄДРПОУ/ДРФО. Максимум 12 цифр',
                                max_length=12, blank=True, default='')
    code_1c = models.CharField('Код 1с',
                               help_text='Введіть внутрішній код 1с. '
                                         'Максимум 9 цифр',
                               max_length=9, blank=True, default='')
    overall_mark = models.ForeignKey(Mark,
                                     verbose_name='Загальна оцінка',
                                     help_text='Загальна оцінка діяльності '
                                               'організації',
                                     null=True, blank=True,
                                     on_delete=models.SET_NULL)
    # readonly field
    email_verified = models.BooleanField('Email підтверджено',
                                         help_text='Чи верифікаваний email',
                                         default=False)
    init_date = models.DateField('* Дата',
                                 help_text='Дата створення',
                                 auto_now_add=True, editable=False, null=True)
    deprecated = models.BooleanField('Неактуальний',
                                     help_text='Відмітьте, щоб '
                                               'деактивувати клієнта',
                                     default=False)

    def get_full_instance_name(self):
        try:
            user = User.objects.get(id=self.user_id)
        except ObjectDoesNotExist:
            user = 'Користувача не вибрано'

        try:
            category = ClientCategory.objects.get(id=self.category_id)
        except ObjectDoesNotExist:
            category = 'Без категорії'

        if self.code_ipn != '':
            if self.fop:
                code_ipn = ', ДРФО: ' + self.code_ipn
            else:
                code_ipn = ', ЄДРПОУ: ' + self.code_ipn
        else:
            code_ipn = self.code_ipn

        return '{} (user: {}) /{}/'.format(self.name + code_ipn,
                                            user.username, category)

    def get_title_name(self):
        if len(self.full_name) >= len(self.name) and self.full_name != '':
            return self.full_name
        elif self.name != '':
            return self.name
        else:
            try:
                user = User.objects.get(id=self.user_id)
                full_name = user.get_full_name()
                short_name = user.get_short_name()
                if len(full_name) >= len(short_name)\
                        and full_name != '':
                    user = full_name
                elif short_name != '':
                    user = short_name
                else:
                    user = user.username
            except ObjectDoesNotExist:
                user = 'Користувача клієнта видалено або не вибрано!'
            return user

    def get_short_name(self):
        if len(self.name) > SHORT_NAME_LEN:
            return self.name[:SHORT_NAME_LEN] + '...'
        else:
            return self.name

    def get_short_phone(self):
        if len(self.phone) > SHORT_NAME_LEN:
            return self.phone[:SHORT_NAME_LEN] + '...'
        else:
            return self.phone

    def __str__(self):
        return self.get_full_instance_name()


class ApplicationStatus(models.Model):
    """Model that represents possible status of the application"""
    class Meta:
        verbose_name = 'Статус звернення'
        verbose_name_plural = 'Статуси звернення'

    INITIAL = 'initial'
    INTERIM = 'interim'
    QUITS = 'quits'
    DENIED = 'denied'

    TYPE_CHOICES = (
        (INITIAL, 'Початковий'),
        (INTERIM, 'Проміжний'),
        (QUITS, 'Завершальний'),
        (DENIED, 'Відхилено'),
    )

    name = models.CharField('* Назва',
                            help_text='Назва статусу заявки',
                            max_length=50)
    type = models.CharField('* Тип статусу',
                            help_text='Вкажіть характер статусу. Примітка: '
                                      'для коректності роботи початковий '
                                      'статус повинен бути лише один. Він '
                                      'буде автоматично призначатися на '
                                      'звернення, що отримали резолюцію.',
                            choices=TYPE_CHOICES, default=INTERIM,
                            max_length=7)
    label = models.ForeignKey(Label, verbose_name='Кольорова мітка',
                              help_text='Вкажіть кольорову мітку,'
                                        'що буде асоціюватися з цим статусом',
                              null=True, blank=True,
                              on_delete=models.SET_NULL)

    def get_full_instance_name(self):
        type_choices = dict(self.TYPE_CHOICES)
        return '{} ({})'.format(self.name, type_choices[self.type])

    def __str__(self):
        return self.get_full_instance_name()


class ApplicationType(models.Model):
    """Model that describes application type"""
    class Meta:
        verbose_name = 'Тип звернення'
        verbose_name_plural = 'Типи звернення'

    FORM_CHOICES = get_forms_choices('application_forms')
    name = models.CharField('* Назва',
                            help_text='Вкажіть назву форми заявки',
                            max_length=50)
    form_template = models.CharField('* Форма шаблону',
                                     help_text='Оберіть шаблон заявки '
                                     'з наявних (підготовлений html файл)',
                                     max_length=50,
                                     choices=FORM_CHOICES)
    deprecated = models.BooleanField('Застаріла',
                                     help_text='Відмітьте, якщо форма '
                                               'неактуальна',
                                     default=False)

    def get_short_instance_name(self):
        if len(self.name) > SHORT_NAME_LEN:
            return self.name[:SHORT_NAME_LEN] + '...'
        else:
            return self.name

    def get_full_instance_name(self):
        return '{} (форма: {}){}'.format(
            self.name, self.form_template,
            '' if not self.deprecated else ' --застаріла'
        )

    def __str__(self):
        return self.get_full_instance_name()


class Resolution(models.Model):
    """Model that describes possible resolutions of the application"""
    class Meta:
        verbose_name = 'Резолюція'
        verbose_name_plural = 'Види резолюцій'

    name = models.CharField('* Назва', max_length=50,
                            help_text='Вкажіть текст резолюції')
    # defines whether this resolution should choose
    # initial quit set of status
    quits = models.BooleanField('Ознака відхилення', default=False,
                                help_text='Відмітьте, якщо дана резолюція '
                                          'означає відхилення / '
                                          'закриття звернення')

    def get_full_instance_name(self):
        if self.quits:
            name = '{} (ознака відхилення)'.format(self.name)
        else:
            name = '{}'.format(self.name)
        return name

    def __str__(self):
        return self.get_full_instance_name()


class Application(models.Model):
    """Main class of the client application"""
    class Meta:
        verbose_name = 'Звернення'
        verbose_name_plural = 'Звернення клієнтів'

    client = models.ForeignKey(Client, verbose_name='* Клієнт',
                               help_text='Вкажіть відповідного користувача',
                               on_delete=models.PROTECT)
    # application can be registered by secretary (not by client itself)
    # in that case 'author' and 'client' will be different
    author = models.ForeignKey(User, verbose_name='Автор звернення',
                               help_text='Вкажіть автора, якщо він '
                                         'відрізняється від клієнта',
                               on_delete=models.SET_NULL,
                               blank=True, null=True)
    # output number of the application of the client
    number = models.CharField('Номер',
                              help_text='Вихідний номер заявника (без дати)',
                              max_length=20, default='', blank=True)
    contact = models.TextField('* Контакти',
                               help_text='Вкажіть Ваші ПІБ та телефон '
                                         'для зворотнього звязку')
    text = models.TextField('Звернення',
                            help_text='Опишіть суть Вашого звернення',
                            blank=True, default='')
    date = models.DateField('* Дата',
                            help_text='Дата подання заявки',
                            auto_now_add=True, editable=False, null=True)
    status = models.ForeignKey(ApplicationStatus, verbose_name='Статус',
                               help_text='Вкажіть поточний статус звернення',
                               on_delete=models.SET_NULL,
                               null=True, blank=True)
    type = models.ForeignKey(ApplicationType, verbose_name='* Тип звернення',
                             help_text='Оберіть можливу причину звернення',
                             on_delete=models.PROTECT)
    resolution = models.ForeignKey(Resolution, verbose_name='Резолюція',
                                   help_text='Вкажіть резолюцію на звернення',
                                   null=True, blank=True,
                                   on_delete=models.SET_NULL)
    resolution_comment = models.CharField('Коментар до резолюції',
                                          help_text='Вкажіть додаткову '
                                                    'інформацію до резолюції',
                                          max_length=250,
                                          blank=True, default='')
    # defines whether user want's to cancel the application
    # it doesn't mean that application will be closed!
    # it's up to employee's decision (close this app or not)
    canceled = models.BooleanField('Скасоване',
                                   help_text='Відмітьте, якщо звернення '
                                             'отримало запит на скасування',
                                   default=False)
    done = models.BooleanField('Виконане',
                               help_text='Відмітьте, якщо звернення '
                                         'виконане виконавцем',
                               default=False)
    closed = models.BooleanField('Закрите',
                                 help_text='Відмітьте, щоб закрити '
                                           'звернення',
                                 default=False)

    def get_full_instance_name(self):
        try:
            client = Client.objects.get(id=self.client_id)
            if self.number != '':
                name = '№ ' + self.number + \
                       ' від ' + '{:%d-%m-%Y}, {}'\
                    .format(self.date, client.name)
            else:
                name = 'Від ' + '{:%d-%m-%Y}, {}'\
                    .format(self.date, client.name)
        except ObjectDoesNotExist:
            name = 'Клієнта цього звернення видалено'

        return name

    def __str__(self):
        return self.get_full_instance_name()


class ApplicationScan(models.Model):
    """Model that response for handling the
    scan of the application form"""
    class Meta:
        verbose_name = 'Скан копія звернення'
        verbose_name_plural = 'Скановані копії звернень'

    app = models.ForeignKey(Application,
                            verbose_name='* Звернення',
                            help_text='Вкажіть звернення, до якого '
                                      'відноситься ця скан копія',
                            null=True, default=None,
                            on_delete=models.SET_NULL)
    scan = models.ImageField('* Скан',
                             help_text='Вкажіть скан копію Вашого '
                                       'звернення',
                             upload_to=get_app_scan_upload_path)

    def get_full_instance_name(self):
        try:
            app = Application.objects.get(id=self.app_id)
            name = 'Скан до звернення: ' + app.get_full_instance_name()
        except ObjectDoesNotExist:
            name = 'Скан до звернення, що було видалене'
        return name

    def __str__(self):
        return self.get_full_instance_name()


class ApplicationAttachment(models.Model):
    """Model that response for handling
    scans of the attachments to the application"""
    class Meta:
        verbose_name = 'Додаток до звернення'
        verbose_name_plural = 'Додатки до звернень'

    app = models.ForeignKey(Application,
                            verbose_name='* Звернення',
                            help_text='Вкажіть звернення, до якого '
                                      'відноситься цей додаток',
                            null=True, on_delete=models.SET_NULL)
    attach = models.ImageField('* Додаток',
                               help_text='Вкажіть додаток до'
                                         'Вашого звернення',
                               upload_to=get_app_attach_upload_path)

    def get_full_instance_name(self):
        try:
            app = Application.objects.get(id=self.app_id)
            name = 'Додаток до звернення: ' + app.get_full_instance_name()
        except ObjectDoesNotExist:
            name = 'Додаток до звернення, що було видалене'
        return name

    def __str__(self):
        return self.get_full_instance_name()


class Department(models.Model):
    """Model that represents the departments of the organization"""
    class Meta:
        verbose_name = 'Відділ'
        verbose_name_plural = 'Відділи'

    name = models.CharField('* Назва',
                            help_text='Вкажіть назву відділу',
                            max_length=30)

    def get_full_instance_name(self):
        return '{}'.format(self.name)

    def __str__(self):
        return self.get_full_instance_name()


class Submission(models.Model):
    """Model that let us to know the submission of the departments"""
    class Meta:
        verbose_name = 'Підпорядкування відділу'
        verbose_name_plural = 'Підпорядкування відділів'

    parent_department = models.ForeignKey(Department,
                                          verbose_name='* Головний відділ',
                                          help_text='Вкажіть відділ, '
                                                    'що є головним',
                                          related_name='parent_department',
                                          null=True, on_delete=models.SET_NULL)
    child_department = models.ForeignKey(Department,
                                         verbose_name='* Підпорядкування',
                                         help_text='Вкажіть відділ, '
                                                   'що підпорядковується',
                                         related_name='child_department',
                                         null=True, on_delete=models.SET_NULL)

    def get_full_instance_name(self):
        try:
            parent = Department.objects.get(id=self.parent_department_id)
            parent = parent.name
        except ObjectDoesNotExist:
            parent = 'Батьківський відділ видалено'

        try:
            child = Department.objects.get(id=self.child_department_id)
            child = child.name
        except ObjectDoesNotExist:
            child = 'Підпорядкований відділ видалено'

        return 'Підпорядкування: {} -> {}'.format(parent, child)

    def __str__(self):
        return self.get_full_instance_name()


class Employee(models.Model):
    """Main Model of worker"""
    class Meta:
        verbose_name = 'Працівник'
        verbose_name_plural = 'Працівники'
        permissions = (
            ('employee_role', 'User has employee rights'),
            ('moderator_role', 'User has moderator rights'),
            ('department_head_role', 'User has rights of department head'),
            ('secretary_role', 'User has secretary rights'),
            ('manager_role', 'User has rights of manager'),
        )

    user = models.ForeignKey(User,
                             verbose_name='* Користувач',
                             help_text='Вкажіть відповідного користувача',
                             on_delete=models.PROTECT)
    avatar = models.ImageField('Аватар',
                               help_text='Завантажте своє фото',
                               blank=True,
                               default=settings.MEDIA_URL +
                               'default-profile.jpg',
                               max_length=250,
                               upload_to=get_employee_avatar_upload_path)
    # readonly field
    email_verified = models.BooleanField('Email підтверджено',
                                         help_text='Чи верифікаваний email',
                                         default=False)
    deprecated = models.BooleanField('Неактуальний',
                                     help_text='Відмітьте, щоб '
                                               'деактивувати працівника',
                                     default=False)

    def get_short_instance_name(self):
        try:
            user = User.objects.get(id=self.user_id)
            if user.first_name != '' or user.last_name != '':
                user = u'{} (логін: {})'\
                    .format(user.first_name + ' ' + user.last_name,
                            user.username)
            else:
                user = u'логін: {}'.format(user.username)
        except ObjectDoesNotExist:
            user = u'Користувача працівника видалено'

        deprecated = u'(деактивовано) ' if self.deprecated else ''

        return u'{}{}'.format(deprecated, user)

    def get_full_instance_name(self):
        try:
            user = User.objects.get(id=self.user_id)
            if user.first_name != '' or user.last_name != '':
                user = '{} (користувач: {}), ' \
                       'останній логін: {:%d-%m-%Y %H:%M:%S}'\
                    .format(user.first_name + ' ' + user.last_name,
                            user.username, user.last_login)
            else:
                user = 'користувач: {}, ' \
                       'останній логін: {:%d-%m-%Y %H:%M:%S}' \
                    .format(user.username, user.last_login)
        except ObjectDoesNotExist:
            user = 'Користувача працівника видалено'

        try:
            department = Department.objects.get(id=self.department_id)
            department = ', ({})'.format(department.name)
        except ObjectDoesNotExist:
            department = ', (відділ працівника видалено)'

        deprecated = '(деактивовано) ' if self.deprecated else ''

        return '{}{}{}'.format(deprecated, user, department)

    def __str__(self):
        return self.get_short_instance_name()


# class Role(models.Model):
#     """Model that represent possible roles of the employee"""
#     class Meta:
#         verbose_name = 'Роль'
#         verbose_name_plural = 'Ролі'
#
#     name = models.CharField('* Назва',
#                             help_text='Вкажіть назву ролі працівника',
#                             max_length=30)
#
#     def get_full_instance_name(self):
#         return '{}'.format(self.name)
#
#     def __str__(self):
#         return self.get_full_instance_name()
#
#
# class EmployeeRole(models.Model):
#     """Model that represents roles for the employees"""
#     class Meta:
#         verbose_name = 'Роль працівника'
#         verbose_name_plural = 'Ролі працівника'
#
#     employee = models.ForeignKey(Employee,
#                                  verbose_name='* Працівник',
#                                  help_text='Вкажіть відповідного працівника',
#                                  on_delete=models.SET_NULL, null=True)
#     role = models.ForeignKey(Role, verbose_name='* Роль',
#                              help_text='Вкажіть роль працівника',
#                              null=True, on_delete=models.SET_NULL)
#
#     def get_full_instance_name(self):
#         try:
#             employee = Employee.objects.get(id=self.employee_id)
#             user = User.objects.get(id=employee.id)
#             name = 'Користувач {}'.format(user.username)
#         except ObjectDoesNotExist:
#             name = 'Працівника або користувача видалено'
#
#         try:
#             role = Role.objects.get(id=self.role_id)
#             role = 'роль {}'.format(role.name)
#         except ObjectDoesNotExist:
#             role = 'роль було видалено'
#
#         return '{} -> {}'.format(name, role)
#
#     def __str__(self):
#         return self.get_full_instance_name()


class DepartmentHead(models.Model):
    """Model that represents the table of the heads for each department"""
    class Meta:
        verbose_name = 'Начальник відділу'
        verbose_name_plural = 'Начальники відділів'

    department = models.ForeignKey(Department,
                                   verbose_name='* Відділ',
                                   help_text='Вкажіть відділ, якому буде '
                                             'призначено керівника',
                                   on_delete=models.SET_NULL, null=True)
    employee = models.ForeignKey(Employee,
                                 verbose_name='* Керівник',
                                 help_text='Вкажіть керівника відділу',
                                 on_delete=models.SET_NULL, null=True)

    def get_full_instance_name(self):
        try:
            department = Department.objects.get(id=self.department_id)
            department = 'Начальник відділу {}'.format(department.name)
        except ObjectDoesNotExist:
            department = '(відділ було видалено)'

        try:
            employee = Employee.objects.get(id=self.employee_id)
            user = User.objects.get(id=employee.user_id)
            employee = user.get_short_name()
        except ObjectDoesNotExist:
            employee = '(працівника або користувача видалено)'

        return '{}: {}'.format(department, employee)

    def __str__(self):
        return self.get_full_instance_name()


class ResponseType(models.Model):
    """Model that represents all possible types of response"""
    class Meta:
        verbose_name = 'Тип відповіді'
        verbose_name_plural = 'Типи відповіді'

    FORM_CHOICES = get_forms_choices('response_forms')
    name = models.CharField('* Назва',
                            help_text='Вкажіть назву форми відповіді',
                            max_length=50)
    form_template = models.CharField('* Форма шаблону',
                                     help_text='Оберіть шаблон відповіді '
                                               'з наявних'
                                               '(підготовлений html файл)',
                                     max_length=50,
                                     choices=FORM_CHOICES)
    deprecated = models.BooleanField('Застаріла',
                                     help_text='Відмітьте, якщо форма '
                                               'неактуальна',
                                     default=False)

    def get_full_instance_name(self):
        return '{} (форма: {}){}'.format(
            self.name, self.form_template,
            '' if not self.deprecated else ' --застаріла'
        )

    def __str__(self):
        return self.get_full_instance_name()


class Response(models.Model):
    """Model that represents the response on the application"""
    class Meta:
        verbose_name = 'Відповідь'
        verbose_name_plural = 'Відповіді'

    application = models.ForeignKey(Application,
                                    verbose_name='* Звернення',
                                    help_text='Вкажіть звернення, до якого'
                                              'відносить ця відповідь',
                                    null=True, on_delete=models.SET_NULL)
    number = models.CharField('Номер',
                              help_text='Вихідний внутрішній'
                                        'номер (без дати)',
                              max_length=20, default='', blank=True)
    title = models.CharField('Шапка',
                             help_text='Текст шапки відповіді (кому)',
                             blank=True, default='', max_length=100)
    text = models.TextField('Відповідь', help_text='Текст відповіді',
                            blank=True, default='')
    # read only field
    date = models.DateField('Дата',
                            help_text='Вкажіть дату надання відповіді',
                            blank=True, auto_now_add=True, editable=True)
    type = models.ForeignKey(ResponseType,
                             verbose_name='* Тип',
                             help_text='Вкажіть тип відповіді',
                             on_delete=models.SET_NULL, null=True)
    cost = models.DecimalField('Вартість',
                               help_text='Вкажіть вартість наданих послуг',
                               max_digits=6, decimal_places=2,
                               blank=True, default=0)
    # read only
    client_review = models.TextField('Відгук',
                                     help_text='Відгук клієнта',
                                     blank=True, default='', max_length=254)
    # read only
    client_mark = models.ForeignKey(Mark,
                                    verbose_name='Оцінка',
                                    help_text='Оцінка клієнта',
                                    null=True, on_delete=models.SET_NULL)

    def get_full_instance_name(self):
        try:
            application = Application.objects.get(id=self.app)
            client = Client.objects.get(id=application.client_id)
            if self.number != '':
                name = '№ ' + self.number + \
                       ' від ' + '{:%d-%m-%Y}, {}'\
                    .format(self.date, client.name)
            else:
                name = 'Від ' + '{:%d-%m-%Y}, {}'\
                    .format(self.date, client.name)
        except ObjectDoesNotExist:
            name = 'Клієнта цього звернення видалено'

        return name

    def __str__(self):
        return self.get_full_instance_name()


class ResponseScan(models.Model):
    """Model that response for handling the
    scan of the response form"""
    class Meta:
        verbose_name = 'Скан копія відповіді'
        verbose_name_plural = 'Скан копії відповідей'

    response = models.ForeignKey(Response,
                                 verbose_name='* Відповідь',
                                 help_text='Відповідь, до якої відноситься '
                                           'цей скан',
                                 on_delete=models.SET_NULL, null=True)
    scan = models.ImageField('* Скан',
                             help_text='Вкажіть електронну копію відповіді',
                             upload_to=get_resp_scan_upload_path)

    def get_full_instance_name(self):
        try:
            response = Response.objects.get(id=self.response_id)
            name = 'Скан до відповіді: ' + response.get_full_instance_name()
        except ObjectDoesNotExist:
            name = 'Скан до відповіді, що була видалена'
        return name

    def __str__(self):
        return self.get_full_instance_name()


class ResponseAttachment(models.Model):
    """Model that response for handling
    scans of the attachments to the response"""
    class Meta:
        verbose_name = 'Скан копія додатку до відповіді'
        verbose_name_plural = 'Скан копії додатків до відповіді'

    response = models.ForeignKey(Response,
                                 verbose_name='* Відповідь',
                                 help_text='Відповідь, до якої відноситься '
                                           'цей додаток',
                                 on_delete=models.SET_NULL, null=True)
    attach = models.ImageField('* Додаток',
                               help_text='Вкажіть електронну копію додатку',
                               upload_to=get_resp_attach_upload_path)

    def get_full_instance_name(self):
        try:
            response = Response.objects.get(id=self.response_id)
            name = 'Додаток до відповіді: ' +\
                   response.get_full_instance_name()
        except ObjectDoesNotExist:
            name = 'Додаток до відповіді, що була видалена'
        return name

    def __str__(self):
        return self.get_full_instance_name()


class ResponseBill(models.Model):
    """Model that response for handling the
    scan of the bill for response"""
    class Meta:
        verbose_name = 'Електронний рахунок'
        verbose_name_plural = 'Електронні рахунки'

    response = models.ForeignKey(Response,
                                 verbose_name='* Відповідь',
                                 help_text='Відповідь, до якої відноситься '
                                           'цей рахунок',
                                 on_delete=models.SET_NULL, null=True)
    bill = models.ImageField('* Рахунок',
                             help_text='Вкажіть електронну копію рахунку',
                             upload_to=get_resp_bill_upload_path)

    def get_full_instance_name(self):
        try:
            response = Response.objects.get(id=self.response_id)
            name = 'Рахунок до відповіді: ' +\
                   response.get_full_instance_name()
        except ObjectDoesNotExist:
            name = 'Рахунок до відповіді, що була видалена'
        return name

    def __str__(self):
        return self.get_full_instance_name()


class ResponsePerformer(models.Model):
    """Model that represent the employees that responsible
    for the response"""
    class Meta:
        verbose_name = 'Виконавець замовлення'
        verbose_name_plural = 'Виконавці замовлення'

    response = models.ForeignKey(Response,
                                 verbose_name='',
                                 help_text='',
                                 on_delete=models.SET_NULL, null=True)
    employee = models.ForeignKey(Employee,
                                 verbose_name='',
                                 help_text='',
                                 on_delete=models.SET_NULL, null=True)

    def get_full_instance_name(self):
        try:
            response = Response.objects.get(id=self.response_id)
            employee = Employee.objects.get(id=self.employee_id)
            name = 'Виконавець: {} на відповідь: {}'\
                .format(employee.get_full_instance_name(),
                        response.get_full_instance_name())
        except ObjectDoesNotExist:
            name = 'Відповідь або виконавеця було видалено'
        return name

    def __str__(self):
        return self.get_full_instance_name()


class Review(models.Model):
    """Model that represents customer feedback
    about the organization"""
    class Meta:
        verbose_name = 'Відгук'
        verbose_name_plural = 'Відгуки'

    client = models.ForeignKey(Client,
                               verbose_name='* Клієнт',
                               help_text='Клієнт, що залишив відгук',
                               null=True, on_delete=models.SET_NULL)
    # readonly
    text = models.TextField('* Відгук',
                            help_text='Текст відгуку',
                            max_length=1000)
    # readonly
    date = models.DateTimeField('* Дата',
                                help_text='Дата написання відгуку',
                                auto_now_add=True,
                                editable=False)
    # readonly
    anonymously = models.BooleanField('Анонімно',
                                      help_text='Чи опубліковано анонімно',
                                      default=False)
    approved = models.BooleanField('Погоджено',
                                   help_text='Відмітьте, якщо відгук '
                                             'пройшов модерацію',
                                   default=False)

    def get_full_instance_name(self):
        try:
            client = Client.objects.get(id=self.client_id)
            client = 'Відгук від: {}'.format(client.get_full_instance_name())
        except ObjectDoesNotExist:
            client = 'Відгук від клієнта, що був видалений'
        approved = ' (погоджений)' if self.approved else ' (не погоджений)'

        return '{}{}'.format(client, approved)

    def __str__(self):
        return self.get_full_instance_name()


class ApplicationMessage(models.Model):
    """Model that represents messages between
    clients and employees about some application"""
    class Meta:
        verbose_name = 'Повідомлення до звернення'
        verbose_name_plural = 'Переписка по зверненню'

    user = models.ForeignKey(User,
                             verbose_name='* Користувач',
                             help_text='Вкажіть користувача - автора '
                                       'повідомлення',
                             null=True, on_delete=models.SET_NULL)
    application = models.ForeignKey(Application,
                                    verbose_name='* Звернення',
                                    help_text='Вкажіть звернення, що якого '
                                              'буде відноситись це '
                                              'повідомлення',
                                    null=True, on_delete=models.SET_NULL)
    message = models.TextField('* Повідомлення',
                               help_text='Введіть текст Вашого повідомлення',
                               default='')
    date = models.DateTimeField(auto_now_add=True, editable=False)

    def get_full_instance_name(self):
        try:
            app = Application.objects.get(id=self.application_id)
            app = 'Повідомлення до заявки {} від {:%d-%m-%Y ' \
                  '%H:%M:%S}'.format(app.get_full_instance_name(), self.date)
        except ObjectDoesNotExist:
            app = 'Повідомлення від {:%d-%m-%Y %H:%M:%S} (заявку ' \
                  'видалено)'.format(app.get_full_instance_name(), self.date)

        return app

    def __str__(self):
        return self.get_full_instance_name()


class ApplicationControl(models.Model):
    """Model that allows the system store the controls
    from employees. So they should approve before the application
    can be closed"""
    class Meta:
        verbose_name = 'Контроль'
        verbose_name_plural = 'Контролі'

    application = models.ForeignKey(Application,
                                    verbose_name='* Звернення',
                                    help_text='Вкажіть звернення, на яке '
                                              'потрібно додати контроль',
                                    null=True, on_delete=models.SET_NULL)
    employee = models.ForeignKey(Employee,
                                 verbose_name='* Працівник',
                                 help_text='Працівник, що бажає '
                                           'контролювати закриття довідки',
                                 null=True, on_delete=models.SET_NULL)
    approved = models.BooleanField('Підтверджено',
                                   help_text='Вкажіть, щоб підтвердити '
                                             'закриття довідки',
                                   default=False)
    date = models.DateTimeField('Контрольна дата',
                                help_text='Вкажіть контрольну дату виконання',
                                null=True, blank=True, auto_now=True)

    def get_full_instance_name(self):
        try:
            app = Application.objects.get(id=self.application_id)
            app = 'Контроль за зверненням {}'\
                .format(app.get_full_instance_name())
        except ObjectDoesNotExist:
            app = '(звернення видалено)'

        try:
            employee = Employee.objects.get(id=self.employee_id)
            employee = 'користувач: {}'\
                .format(employee.get_short_instance_name())
        except ObjectDoesNotExist:
            employee = '(користувача видалено)'

        return '{}, {}'.format(app, employee)

    def __str__(self):
        return self.get_full_instance_name()


class ApplicationHistory(models.Model):
    """Model that represents the history of the application"""
    class Meta:
        verbose_name = 'Зміна над зверненням'
        verbose_name_plural = 'Історія змін над зверненнями'

    application = models.ForeignKey(Application,
                                    verbose_name='* Звернення',
                                    help_text='Вкажіть звернення, до якого '
                                              'відноситься ця дія',
                                    null=True, on_delete=models.SET_NULL)
    user = models.ForeignKey(User,
                             verbose_name='* Користувач',
                             help_text='Вкажіть користувача, яким внесені '
                                       'зміни',
                             null=True, on_delete=models.SET_NULL)
    # readonly
    date = models.DateTimeField('* Дата',
                                help_text='Дата внесення змін до звернення',
                                auto_now_add=True)
    action = models.TextField('* Дія',
                              help_text='Опис вчиненої дії над зверненням',
                              default='')

    def get_full_instance_name(self):
        try:
            user = User.objects.get(id=self.user_id)
            user = 'Дія користувачем: {} від {}'\
                .format(user.get_username(), self.date)
        except ObjectDoesNotExist:
            user = 'Дія від {} (користувача видалено)'.format(self.date)

        return user

    def __str__(self):
        return self.get_full_instance_name()


class DepartmentEmployee(models.Model):
    """Model that represents the table of the heads for each department"""
    class Meta:
        verbose_name = 'Працівник відділу'
        verbose_name_plural = 'Працівники по відділам'

    department = models.ForeignKey(Department,
                                   verbose_name='* Відділ',
                                   help_text='Вкажіть відділ до якого '
                                             'відносить цей працівник',
                                   on_delete=models.SET_NULL, null=True)
    employee = models.ForeignKey(Employee,
                                 verbose_name='* Працівник',
                                 help_text='Вкажіть працівника відділу',
                                 on_delete=models.SET_NULL, null=True)

    def get_full_instance_name(self):
        try:
            department = Department.objects.get(id=self.department_id)
            department = 'Відділ {}'.format(department.name)
        except ObjectDoesNotExist:
            department = '(відділ було видалено)'

        try:
            employee = Employee.objects.get(id=self.employee_id)
            user = User.objects.get(id=employee.user_id)
            employee = user.get_short_name()
        except ObjectDoesNotExist:
            employee = '(працівника або користувача видалено)'

        return '{}: {}'.format(department, employee)

    def __str__(self):
        return self.get_full_instance_name()
