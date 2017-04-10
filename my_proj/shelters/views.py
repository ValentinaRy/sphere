# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.http import HttpResponse, Http404, JsonResponse, HttpResponseRedirect
from shelters.models import Shelter, Pet, Rating, Volunteer_work
from shelters.forms import ShelterForm, PetForm, PetFilterForm
from django.contrib.auth.forms import UserCreationForm
from django.template.context_processors import csrf
from django.core.urlresolvers import reverse
from django.db.models import Avg, Count
from django.core import serializers

def main_page(request):
    return render(
        request, 'shelters/main.html'
    )

def ajax_shelters(request):
    page = int(request.GET['page']);
    shelters = Shelter.objects.filter(rating__content_type__model='User')[(int(page)-1)*20:int(page)*20].annotate(aver = Avg('rating__rating'), cnt = Count('rating__rating'))
    names = []
    rates = []
    cnts = []
    ids = []
    for i in range(0, 20):
        names.append(shelters[i].name)
        rates.append(shelters[i].aver)
        cnts.append(shelters[i].cnt)
        ids.append(shelters[i].id)
    return JsonResponse({'names': names, 'rates': rates, 'cnts': cnts, 'ids': ids})

def shelter_list(request):
    shelters = Shelter.objects.filter(rating__content_type__model='User')[0:20].annotate(aver = Avg('rating__rating'), cnt = Count('rating__rating'))
    return render(
        request, 'shelters/shelter_list.html',
        {'shelters': shelters}
    )

def shelter_detail(request, shelter_id):
    try:
        shelter = Shelter.objects.get(id=shelter_id) 
    except Shelter.DoesNotExist:
        raise Http404('No such shelter')
    pet_list = Pet.objects.filter(shelter_id=shelter_id)
    return render(
        request, 'shelters/shelter_detail.html',
        {'shelter': shelter, 'pet_list': pet_list}
    )

def ajax_pets(request):
    page = int(request.GET['page'])
    ptype = int(request.GET['ptype'])
    sex = int(request.GET['sex'])
    avail = request.GET['avail'] == 'on'
    pets = []
    if ptype != -1:
        if sex != -1:
            if avail:
                pets = Pet.objects.filter(ptype=ptype, sex=sex, owner_id__isnull=True)[(int(page)-1)*20:int(page)*20]
            else:
                pets = Pet.objects.filter(ptype=ptype, sex=sex)[(int(page)-1)*20:int(page)*20]
        else:
            if avail:
                pets = Pet.objects.filter(ptype=ptype, owner_id__isnull=True)[(int(page)-1)*20:int(page)*20]
            else:
                pets = Pet.objects.filter(ptype=ptype)[(int(page)-1)*20:int(page)*20]
    else:
        if sex != -1:
            if avail:
                pets = Pet.objects.filter(sex=sex, owner_id__isnull=True)[(int(page)-1)*20:int(page)*20]
            else:
                pets = Pet.objects.filter(sex=sex)[(int(page)-1)*20:int(page)*20]
        else:
            if avail:
                pets = Pet.objects.filter(owner_id__isnull=True)[(int(page)-1)*20:int(page)*20]
            else:
                pets = Pet.objects.all()[(int(page)-1)*20:int(page)*20]
    names = []
    photos = []
    ids = []
    for i in range(0, 20):
        names.append(pets[i].name)
        photos.append(pets[i].photo.url)
        ids.append(pets[i].id)
    return JsonResponse({'names': names, 'photos': photos, 'ids': ids})

def pet_list(request):
    page = 1
    if request.method == 'POST':
        filter_form = PetFilterForm(request.POST)
    else:
        filter_form = PetFilterForm(request.GET)
    ptype = -1
    sex = -1
    avail = False
    if filter_form.is_valid():
        ptype = int(filter_form.cleaned_data['ptype'])
        sex = int(filter_form.cleaned_data['sex'])
        avail = filter_form.cleaned_data['avail']
    pets = []
    if ptype != -1:
        if sex != -1:
            if avail:
                pets = Pet.objects.filter(ptype=ptype, sex=sex, owner_id__isnull=True)[(int(page)-1)*20:int(page)*20]
            else:
                pets = Pet.objects.filter(ptype=ptype, sex=sex)[(int(page)-1)*20:int(page)*20]
        else:
            if avail:
                pets = Pet.objects.filter(ptype=ptype, owner_id__isnull=True)[(int(page)-1)*20:int(page)*20]
            else:
                pets = Pet.objects.filter(ptype=ptype)[(int(page)-1)*20:int(page)*20]
    else:
        if sex != -1:
            if avail:
                pets = Pet.objects.filter(sex=sex, owner_id__isnull=True)[(int(page)-1)*20:int(page)*20]
            else:
                pets = Pet.objects.filter(sex=sex)[(int(page)-1)*20:int(page)*20]
        else:
            if avail:
                pets = Pet.objects.filter(owner_id__isnull=True)[(int(page)-1)*20:int(page)*20]
            else:
                pets = Pet.objects.all()[(int(page)-1)*20:int(page)*20]
    return render(
        request, 'shelters/pet_list.html',
        {'pets': pets, 'filter_form': filter_form}
    )

def pet_detail(request, pet_id):
    try:
        pet = Pet.objects.get(id=pet_id) 
    except Pet.DoesNotExist:
        raise Http404('No such pet')
    avail = pet.owner_id is None
    return render(
        request, 'shelters/pet_detail.html',
        {'pet': pet, 'ptype': pet.types[pet.ptype][1],
        'psex': pet.sexes[pet.sex][1], 'avail': avail}
    )


def account(request):
    work = Volunteer_work.objects.filter(volunteer=request.user.id)
    print(len(work))
    return render(
        request, 'shelters/account.html',
        {'work': work}
    )

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('account'))
    else:
        form = UserCreationForm()
    token = {}
    token.update(csrf(request))
    token['form'] = form
    return render(
        request, 'registration/registration.html', token
    )
