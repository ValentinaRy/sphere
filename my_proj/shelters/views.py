# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.http import HttpResponse, Http404, JsonResponse, HttpResponseRedirect
from shelters.models import Shelter, Pet, Rating, Volunteer_work
from shelters.forms import ShelterForm, PetForm, PetFilterForm
from django.contrib.auth.forms import UserCreationForm
from django.template.context_processors import csrf
from django.core.urlresolvers import reverse
from django.db.models import Avg, Count

def main_page(request):
    return render(
        request, 'shelters/main.html'
    )

def ajax_shelters(request):
    if 'page' in request.GET:
        page = int(request.GET['page'])
    else:
        page = 0
    shelters = Shelter.objects.filter(rating__content_type__model='User').annotate(aver = Avg('rating__rating'), cnt = Count('rating__rating'))[(int(page)-1)*20:int(page)*20]
    return JsonResponse({'data':list(shelters.values('id','name', 'aver', 'cnt'))})

def shelter_list(request):
    return render(
        request, 'shelters/shelter_list.html',
    )

def shelter_detail(request, shelter_id):
    try:
        shelter = Shelter.objects.get(id=shelter_id) 
    except Shelter.DoesNotExist:
        raise Http404('No such shelter')
    filter_form = PetFilterForm()
    return render(
        request, 'shelters/shelter_detail.html',
        {'shelter': shelter, 'filter_form': filter_form}
    )

def ajax_pets(request):
    pets = Pet.objects.all();
    if 'ptype' in request.GET:
        ptype = int(request.GET['ptype'])
        if ptype != -1:
            pets = pets.filter(ptype=ptype)
    if 'sex' in request.GET:
        sex = int(request.GET['sex'])
        if sex != -1:
            pets = pets.filter(sex=sex)
    if 'avail' in request.GET:
        avail = request.GET['avail'] == 'on'
        if avail:
            pets = pets.filter(owner_id__isnull=True)
    if 'shel_id' in request.GET:
        shel_id = int(request.GET['shel_id'])
        if shel_id != -1:
            pets = pets.filter(shelter_id__id=shel_id)
    if 'page' in request.GET:
        page = int(request.GET['page'])
        pets = pets[(int(page)-1)*20:int(page)*20]
    else:
        pets = pets[0:20]
    return JsonResponse({'data':list(pets.values('id','name','photo'))})

def pet_list(request):
    filter_form = PetFilterForm()
    return render(
        request, 'shelters/pet_list.html',
        {'filter_form': filter_form}
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
