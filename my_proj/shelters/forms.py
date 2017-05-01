# -*- coding: utf-8 -*-
from django import forms
from shelters.models import Shelter, Pet


class ShelterForm(forms.ModelForm):

    class Meta:
        fields = ('name', 'location', 'email')
        model = Shelter

class PetForm(forms.ModelForm):

    class Meta:
        fields = ('name','ptype','sex','photo','in_date')
        model = Pet

class PetFilterForm(forms.Form):
    types =((-1, 'Любой'), (0, 'Кот'), (1, 'Собака'), (2, 'Грызун'), (3, 'Птица'))
    ptype = forms.ChoiceField(choices=types, widget=forms.Select, label='Тип')
    sexes = ((-1, 'Любой'), (0,'Девочка'), (1,'Мальчик'))
    sex = forms.ChoiceField(choices=sexes, widget=forms.Select, label='Пол')
    avail = forms.BooleanField(required=False, initial='True', label='Находится в приюте')

class CommentForm(forms.Form):
    rating = forms.IntegerField(min_value=0, max_value=10)
    comment = forms.CharField(max_length=300)

#class ShelFilterForm(forms.Form):
    #forms.FloatField()
