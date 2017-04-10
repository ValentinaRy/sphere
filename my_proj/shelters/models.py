# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey

class Shelter(models.Model):
    name = models.CharField(max_length=200, verbose_name='Название приюта', db_index=True)
    location = models.CharField(max_length=200, verbose_name='Адрес')
    email = models.CharField(max_length=200, verbose_name='E-mail')
    volunteers = models.ManyToManyField(to=User, through='Volunteer_work')
    
    def __unicode__(self):
        return unicode(self.name)
    
    class Meta:
        verbose_name = 'Приют'
        verbose_name_plural = 'Приюты'

class Volunteer_work(models.Model):
    volunteer = models.ForeignKey(to=User, verbose_name='Волонтер', db_index=True)
    shelter = models.ForeignKey(to=Shelter, verbose_name='Приют')
    date = models.DateField(verbose_name='Дата')
    work_time = models.PositiveIntegerField(verbose_name='Время работы в часах')
    reward = models.PositiveIntegerField(verbose_name='Вознаграждение')
    
    def __unicode__(self):
        return unicode('%s-%s:%s,%d' % (self.shelter,self.volunteer,self.date,self.work_time))
        
    class Meta:
        verbose_name = 'Волонтерство'
        verbose_name_plural = 'Волонтерство'

class Rating(models.Model):
    rating = models.PositiveSmallIntegerField(verbose_name='Оценка')
    comment = models.CharField(max_length=300, verbose_name='Комментарий')
    author = models.ForeignKey(to=User)
    shelter = models.ForeignKey(to=Shelter)
    content_type = models.ForeignKey(to=ContentType)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    def __unicode__(self):
        return unicode('%d-%s,%s-%s' % (self.rating,self.shelter,self.content_object,self.comment))
    
    class Meta:
        verbose_name = 'Оценка'
        verbose_name_plural = 'Оценки'

class Pet(models.Model):
    name = models.CharField(max_length=200, verbose_name='Имя питомца')
    types =((0, 'Кот'), (1, 'Собака'), (2, 'Грызун'), (3, 'Птица'))
    ptype = models.SmallIntegerField(choices=types, verbose_name='Тип', db_index=True)
    sexes = ((0,'Девочка'), (1,'Мальчик'))
    sex = models.SmallIntegerField(choices=sexes, verbose_name='Пол', db_index=True)
    photo = models.ImageField(upload_to='images/')
    in_date = models.DateField(verbose_name='Дата поступления в приют')
    out_date = models.DateField(null=True, blank=True, verbose_name='Дата взятия из приюта')
    shelter_id = models.ForeignKey(to=Shelter, verbose_name='Приют', db_index=True)
    owner_id = models.ForeignKey(to=User, null=True, blank=True, on_delete=models.DO_NOTHING, verbose_name='Хозяин')
    
    def __unicode__(self):
        return unicode(self.name)
    
    class Meta:
        verbose_name = 'Питомец'
        verbose_name_plural = 'Питомцы'
