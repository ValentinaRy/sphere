# -*- coding: utf-8 -*-
from django import forms
from shelters.models import Shelter, Pet
import datetime


class ShelterForm(forms.Form):
    shel_name = forms.CharField(max_length=200, label='Название приюта')
    shel_location = forms.CharField(max_length=200, label='Адрес')
    shel_email = forms.EmailField(max_length=200, label='E-mail')

class PetForm(forms.Form):
    pet_name = forms.CharField(max_length=200, label='Имя питомца')
    types = ((-1, 'Любой'), (0, 'Кот'), (1, 'Собака'), (2, 'Грызун'), (3, 'Птица'))
    pet_ptype = forms.ChoiceField(choices=types, widget=forms.Select, label='Тип')
    sexes = ((-1, 'Любой'), (0, 'Девочка'), (1, 'Мальчик'))
    pet_sex = forms.ChoiceField(choices=sexes, widget=forms.Select, label='Пол')
    pet_photo = forms.ImageField(label='Фото', required=False)
    pet_in_date = forms.DateField(label='Дата поступления', initial=datetime.date.today())


class PetFilterForm(forms.Form):
    types =((-1, 'Любой'), (0, 'Кот'), (1, 'Собака'), (2, 'Грызун'), (3, 'Птица'))
    ptype = forms.ChoiceField(choices=types, widget=forms.Select, label='Тип')
    sexes = ((-1, 'Любой'), (0,'Девочка'), (1,'Мальчик'))
    sex = forms.ChoiceField(choices=sexes, widget=forms.Select, label='Пол')
    avail = forms.BooleanField(required=False, initial='True', label='Находится в приюте')

class CommentForm(forms.Form):
    rating = forms.IntegerField(min_value=0, max_value=10, label='Оценка')
    comment = forms.CharField(max_length=300, widget=forms.Textarea, label='Комментарий')

#class ShelFilterForm(forms.Form):
    #forms.FloatField()
