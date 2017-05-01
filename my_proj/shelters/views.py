# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.http import HttpResponse, Http404, JsonResponse, HttpResponseRedirect
from shelters.models import Shelter, Pet, Rating, Volunteer_work
from shelters.forms import ShelterForm, PetForm, PetFilterForm, CommentForm
from django.contrib.auth.forms import UserCreationForm
from django.template.context_processors import csrf
from django.core.urlresolvers import reverse
from django.db.models import Avg, Count
from datetime import datetime

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
        shelter = Shelter.objects.filter(id=shelter_id, rating__content_type__model='User').annotate(aver = Avg('rating__rating'), cnt = Count('rating__rating'))[0]
    except Shelter.DoesNotExist:
        raise Http404('No such shelter')
    filter_form = PetFilterForm()
    comments = Rating.objects.filter(content_type__model='User', shelter=shelter.id)
    if request.method=='GET':
        com_form = CommentForm()
    elif request.method=='POST':
        com_form = CommentForm(request.POST)
        if com_form.is_valid():
            new_rat = Rating(
                rating=com_form.data['rating'],
                comment=com_form.data['comment'],
                author=request.user,
                shelter=shelter,
                content_object=request.user,
            )
            new_rat.save()
            com_form = CommentForm()
    return render(
        request, 'shelters/shelter_detail.html',
        {'shelter': shelter, 'filter_form': filter_form,
        'comments': comments, 'com_form': com_form}
    )

def shelter_admin(request, shelter_id):
    try:
        shelter = Shelter.objects.filter(id=shelter_id, rating__content_type__model='User').annotate(aver=Avg('rating__rating'),cnt=Count('rating__rating'))[0]
    except Shelter.DoesNotExist:
        raise Http404('No such shelter')
    if request.user in shelter.administrators.all():
        filter_form = PetFilterForm()
        if request.method=='GET':
            shel_form = ShelterForm(instance=shelter)
            pet_form = PetForm()
        elif request.method=='POST':
            shel_form = ShelterForm(request.POST)
            pet_form = PetForm(request.POST, request.FILES)
            if 'shelbtn' in request.POST:
                if shel_form.is_valid():
                    shelter.name = shel_form.data['name']
                    shelter.location = shel_form.data['location']
                    shelter.email = shel_form.data['email']
                    shelter.save()
            elif 'addpet' in request.POST:
                if pet_form.is_valid():
                    new_pet = Pet(
                        name=pet_form.data['name'],
                        ptype=pet_form.data['ptype'],
                        sex=pet_form.data['sex'],
                        photo=request.FILES['photo'],#pet_form.data['photo'],
                        in_date=datetime.strptime(pet_form.data['in_date'], "%d.%m.%Y"),
                        shelter_id=shelter
                    )
                    new_pet.save()
                    pet_form = PetForm()
        return render(
            request, 'shelters/shelter_admin.html',
            {'shelter': shelter, 'filter_form': filter_form,
             'pet_form': pet_form, 'shel_form': shel_form}
        )
    else:
        raise Http404('No such page')

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
    admins = Shelter.objects.filter(administrators=request.user.id)
    print(len(work))
    return render(
        request, 'shelters/account.html',
        {'work': work, 'admins': admins}
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
