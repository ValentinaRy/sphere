# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.http import HttpResponse, Http404, JsonResponse, HttpResponseRedirect
from shelters.models import Shelter, Pet, Rating, Volunteer_work
from shelters.forms import ShelterForm, PetForm, PetFilterForm, CommentForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.template.context_processors import csrf
from django.core.urlresolvers import reverse
from django.db.models import Avg, Count
from datetime import datetime, date
from django.conf import settings
from django.core import serializers
import random


def main_page(request):
    return render(
        request, 'shelters/main.html'
    )


def ajax_shelters(request):
    if 'page' in request.GET:
        page = int(request.GET['page'])
    else:
        page = 0
    shelters = Shelter.objects.filter(rating__content_type__model='User').annotate(aver=Avg('rating__rating'),
                                                                                   cnt=Count('rating__rating'))[
               (int(page) - 1) * 20:int(page) * 20]
    return JsonResponse({'data': list(shelters.values('id', 'name', 'aver', 'cnt'))})


def shelter_list(request):
    return render(
        request, 'shelters/shelter_list.html',
    )


def shelter_detail(request, shelter_id):
    try:
        shelter = Shelter.objects.filter(id=shelter_id,
                rating__content_type__model='User').annotate(aver=Avg('rating__rating'),
                                                            cnt=Count('rating__rating'))[0]
    except Shelter.DoesNotExist:
        raise Http404('No such shelter')
    com_form = CommentForm()
    resp_dict = {'shelter': shelter, 'com_form': com_form}
    if request.user in shelter.administrators.all():
        shel_form = ShelterForm(initial={
            'shel_name': shelter.name,
            'shel_location': shelter.location,
            'shel_email': shelter.email}
        )
        resp_dict.update({'shel_form': shel_form})
    return render(
        request, 'shelters/shelter_detail.html', resp_dict
    )


def shelter_pets(request, shelter_id):
    try:
        shelter = Shelter.objects.filter(id=shelter_id,
                rating__content_type__model='User').annotate(aver=Avg('rating__rating'),
                                                            cnt=Count('rating__rating'))[0]
    except Shelter.DoesNotExist:
        raise Http404('No such shelter')
    filter_form = PetFilterForm()
    resp_dict = {'shelter': shelter, 'filter_form': filter_form}
    if request.user in shelter.administrators.all():
        shel_form = ShelterForm(initial={
            'shel_name': shelter.name,
            'shel_location': shelter.location,
            'shel_email': shelter.email})
        pet_form = PetForm()
        resp_dict.update({'shel_form': shel_form, 'pet_form': pet_form})
    return render(
        request, 'shelters/shelter_pets.html', resp_dict
    )

def ajax_shel_admin(request):
    if 'shel_id' in request.POST:
        shel_id = int(request.POST['shel_id'])
        try:
            shelter = Shelter.objects.get(id=shel_id)
        except Shelter.DoesNotExist:
            return JsonResponse({'status': 0, 'message': 'No such shelter'})
        if not (request.user in shelter.administrators.all()):
            return JsonResponse({'status': 0, 'message': 'You have not permissions'})
        if 'ch_shel' in request.POST:
            shelform = ShelterForm(request.POST)
            if shelform.is_valid():
                shelter.name = shelform.cleaned_data['shel_name']
                shelter.location = shelform.cleaned_data['shel_location']
                shelter.email = shelform.cleaned_data['shel_email']
                shelter.save()
                return JsonResponse({'status': 1})
            else:
                return JsonResponse({'status': 0, 'message': 'There are errors',
                                     'errors': shelform.errors})
        elif 'add_pet' in request.POST:
            petform = PetForm(request.POST, request.FILES)
            if not ('pet_photo' in request.FILES):
                return JsonResponse({'status': 0, 'message': 'No pet photo'})
            if petform.is_valid():
                if petform.cleaned_data['pet_ptype'] == '-1':
                    return JsonResponse({'status': 0, 'message': 'Type can\'t be Any'})
                if petform.cleaned_data['pet_sex'] == '-1':
                    return JsonResponse({'status': 0, 'message': 'Sex can\'t be Any'})
                f = request.FILES['pet_photo']
                randstr = ""
                for i in range (1,20):
                    randstr += chr(ord('a')+random.randint(0,25))
                filename = randstr + f.name
                with open(settings.MEDIA_ROOT + "/" + filename, 'wb+') as destination:
                    for chunk in f.chunks():
                        destination.write(chunk)
                new_pet = Pet(
                    name=petform.cleaned_data['pet_name'],
                    ptype=petform.cleaned_data['pet_ptype'],
                    sex=petform.cleaned_data['pet_sex'],
                    photo=filename,
                    in_date=petform.cleaned_data['pet_in_date'],
                    shelter_id=shelter
                )
                new_pet.save()
                return JsonResponse({'status':1})
            else:
                return JsonResponse({'status': 0, 'message': 'There are errors in form',
                                     'errors': petform.errors})
        elif 'ch_pet' in request.POST:
            petform = PetForm(request.POST, request.FILES)
            if not ('pet_id' in request.POST):
                petform.add_error(None, "No pet id")
            else:
                try:
                    pet_id = int(request.POST['pet_id'])
                    pet = Pet.objects.get(id=pet_id)
                except Pet.DoesNotExist:
                    return JsonResponse({'status': 0, 'message': 'No such pet'})
            if petform.is_valid():
                if petform.cleaned_data['pet_ptype'] == '-1':
                    return JsonResponse({'status': 0, 'message': 'Type can\'t be Any'})
                if petform.cleaned_data['pet_sex'] == '-1':
                    return JsonResponse({'status': 0, 'message': 'Sex can\'t be Any'})
                pet.name=petform.cleaned_data['pet_name']
                pet.ptype=int(petform.cleaned_data['pet_ptype'])
                pet.sex=int(petform.cleaned_data['pet_sex'])
                if 'pet_photo' in request.FILES:
                    pet.photo=petform.cleaned_data['pet_photo']
                pet.in_date=petform.cleaned_data['pet_in_date']
                pet.save()
                return JsonResponse({'status': 1, 'photo_url': pet.photo.url})
            else:
                return JsonResponse({'status': 0, 'message': 'There are errors in form',
                                     'errors': petform.errors})
        elif 'del_pet' in request.POST:
            if not ('pet_id' in request.POST):
                return JsonResponse({'status': 0, 'message': 'No pet id'})
            else:
                try:
                    pet_id = int(request.POST['pet_id'])
                    pet = Pet.objects.get(id=pet_id)
                except Pet.DoesNotExist:
                    return JsonResponse({'status': 0, 'message': 'No such pet'})
                pet.delete()
                return JsonResponse({'status': 1})
        elif 'get_username' in request.POST:
            if not('owner_id' in request.POST and request.POST['owner_id']!=''):
                return JsonResponse({'status': 0})
            user_id = int(request.POST['owner_id'])
            try:
                user = User.objects.get(id=user_id)
            except User.DoesNotExist:
                return JsonResponse({'status': 0})
            return JsonResponse({'status': 1, 'username': user.username})
        elif 'set_owner' in request.POST:
            if not('owner_id' in request.POST):
                return JsonResponse({'status': 0, 'message': 'No user id'})
            if not ('pet_id' in request.POST):
                return JsonResponse({'status': 0, 'message': 'No pet id'})
            user_id = int(request.POST['owner_id'])
            pet_id = int(request.POST['pet_id'])
            try:
                user = User.objects.get(id=user_id)
                pet = Pet.objects.get(id=pet_id)
            except User.DoesNotExist:
                return JsonResponse({'status': 0, 'message': 'No such user'})
            except Pet.DoesNotExist:
                return JsonResponse({'status': 0, 'message': 'No such pet'})
            pet.owner_id = user
            pet.save()
            return JsonResponse({'status': 1, 'username': user.username})

    return JsonResponse({'status':0, 'message': 'Something wrong'})

def ajax_comment(request):
    if request.method == 'POST':
        if not ('shel_id' in request.POST):
            return JsonResponse({'status': 0, 'message': 'No shelter id'})
        shel_id = int(request.POST['shel_id'])
        try:
            shelter = Shelter.objects.get(id=shel_id)
        except Shelter.DoesNotExist:
            return JsonResponse({'status':0, 'message': 'No such shelter'})
        comm_form = CommentForm(request.POST)
        if comm_form.is_valid():
            comment = Rating(
                rating = comm_form.cleaned_data['rating'],
                comment = comm_form.cleaned_data['comment'],
                author = request.user,
                shelter = shelter,
                content_object = request.user,
            )
            comment.save()
            return JsonResponse({'status': 1})
        else:
            return JsonResponse({'status': 0, 'message': 'There are errors',
                                         'errors': comm_form.errors})
    else:
        if not ('shel_id' in request.GET):
            return JsonResponse({'status': 0, 'message': 'No shelter id'})
        shel_id = int(request.GET['shel_id'])
        try:
            shelter = Shelter.objects.filter(id=shel_id,
                        rating__content_type__model='User').annotate(aver=Avg('rating__rating'),
                            cnt=Count('rating__rating'))[0]
        except Shelter.DoesNotExist:
            return JsonResponse({'status':0, 'message': 'No such shelter'})
        comments = Rating.objects.filter(content_type__model='User', shelter=shelter.id)
        authors = []
        for c in comments:
            authors.append(c.content_object.username)
        return JsonResponse({'status':1,'comments': list(comments.values('rating', 'comment')),
                             'aver': shelter.aver, 'cnt': shelter.cnt, 'authors': authors})

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
        pets = pets[(int(page) - 1) * 20:int(page) * 20]
    else:
        pets = pets[0:20]
    return JsonResponse({'data': list(pets.values('id', 'name', 'photo'))})


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
    resp_dict = {'pet': pet, 'ptype': pet.types[pet.ptype][1],
         'psex': pet.sexes[pet.sex][1], 'avail': avail}
    if request.user in pet.shelter_id.administrators.all():
        petform = PetForm(initial = {
            'pet_name': pet.name,
            'pet_ptype': pet.ptype,
            'pet_sex': pet.sex,
            'pet_photo': pet.photo,
            'pet_in_date': pet.in_date
        })
        print(petform.is_valid(), petform.errors)
        resp_dict.update({'pet_form': petform})
    return render(
        request, 'shelters/pet_detail.html', resp_dict
    )


def account(request):
    work = Volunteer_work.objects.filter(volunteer=request.user.id)
    admins = Shelter.objects.filter(administrators=request.user.id)
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
