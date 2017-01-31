# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-11-08 06:40
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='applicationstatus',
            name='type',
            field=models.CharField(choices=[('initial', '\u041f\u043e\u0447\u0430\u0442\u043a\u043e\u0432\u0438\u0439'), ('interim', '\u041f\u0440\u043e\u043c\u0456\u0436\u043d\u0438\u0439'), ('quits', '\u0417\u0430\u0432\u0435\u0440\u0448\u0430\u043b\u044c\u043d\u0438\u0439'), ('denied', '\u0412\u0456\u0434\u0445\u0438\u043b\u0435\u043d\u043e')], default='interim', help_text='\u0412\u043a\u0430\u0436\u0456\u0442\u044c \u0445\u0430\u0440\u0430\u043a\u0442\u0435\u0440 \u0441\u0442\u0430\u0442\u0443\u0441\u0443. \u041f\u0440\u0438\u043c\u0456\u0442\u043a\u0430: \u0434\u043b\u044f \u043a\u043e\u0440\u0435\u043a\u0442\u043d\u043e\u0441\u0442\u0456 \u0440\u043e\u0431\u043e\u0442\u0438 \u043f\u043e\u0447\u0430\u0442\u043a\u043e\u0432\u0438\u0439 \u0441\u0442\u0430\u0442\u0443\u0441 \u043f\u043e\u0432\u0438\u043d\u0435\u043d \u0431\u0443\u0442\u0438 \u043b\u0438\u0448\u0435 \u043e\u0434\u0438\u043d. \u0412\u0456\u043d \u0431\u0443\u0434\u0435 \u0430\u0432\u0442\u043e\u043c\u0430\u0442\u0438\u0447\u043d\u043e \u043f\u0440\u0438\u0437\u043d\u0430\u0447\u0430\u0442\u0438\u0441\u044f \u043d\u0430 \u0437\u0432\u0435\u0440\u043d\u0435\u043d\u043d\u044f, \u0449\u043e \u043e\u0442\u0440\u0438\u043c\u0430\u043b\u0438 \u0440\u0435\u0437\u043e\u043b\u044e\u0446\u0456\u044e.', max_length=7, verbose_name='* \u0422\u0438\u043f \u0441\u0442\u0430\u0442\u0443\u0441\u0443'),
        ),
        migrations.AlterField(
            model_name='applicationtype',
            name='form_template',
            field=models.CharField(choices=[('price_inquiry.html', 'price_inquiry'), ('source_sertificate.html', 'source_sertificate')], help_text='\u041e\u0431\u0435\u0440\u0456\u0442\u044c \u0448\u0430\u0431\u043b\u043e\u043d \u0437\u0430\u044f\u0432\u043a\u0438 \u0437 \u043d\u0430\u044f\u0432\u043d\u0438\u0445 (\u043f\u0456\u0434\u0433\u043e\u0442\u043e\u0432\u043b\u0435\u043d\u0438\u0439 html \u0444\u0430\u0439\u043b)', max_length=50, verbose_name='* \u0424\u043e\u0440\u043c\u0430 \u0448\u0430\u0431\u043b\u043e\u043d\u0443'),
        ),
        migrations.AlterField(
            model_name='responsetype',
            name='form_template',
            field=models.CharField(choices=[('price_inquiry.html', 'price_inquiry'), ('source_sertificate.html', 'source_sertificate')], help_text='\u041e\u0431\u0435\u0440\u0456\u0442\u044c \u0448\u0430\u0431\u043b\u043e\u043d \u0432\u0456\u0434\u043f\u043e\u0432\u0456\u0434\u0456 \u0437 \u043d\u0430\u044f\u0432\u043d\u0438\u0445(\u043f\u0456\u0434\u0433\u043e\u0442\u043e\u0432\u043b\u0435\u043d\u0438\u0439 html \u0444\u0430\u0439\u043b)', max_length=50, verbose_name='* \u0424\u043e\u0440\u043c\u0430 \u0448\u0430\u0431\u043b\u043e\u043d\u0443'),
        ),
    ]