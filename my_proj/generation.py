import random
from shelters.models import Shelter, Volunteer_work, Rating, Pet
from django.db import connection
from django.contrib.auth.models import User
import time
from datetime import date

times = []
times.append(time.time())

#execfile('generation.py')
alphabet = "abcdefghijklmnopqrstuvwxyz0123456789"

men_names = ()
women_names = ()
surnames = ()

with open('lists/men_names.txt') as f:
    men_names = f.read().splitlines()
with open('lists/women_names.txt') as f:
    women_names = f.read().splitlines()
with open('lists/surnames.txt') as f:
    surnames = f.read().splitlines()

cnt_men_names = len(men_names)
cnt_women_names = len(women_names)
cnt_surnames = len(surnames)
times.append(time.time())
bulk_users = []
for i in range(0,100000):
    name = ""
    pas = ""
    if random.randint(0,1) == 1:
        name = women_names[random.randint(0,cnt_women_names-1)]
    else:
        name = men_names[random.randint(0,cnt_men_names-1)]
    surname = surnames[random.randint(0,cnt_surnames-1)]
    for j in range(1,10):
        pas += str(alphabet[random.randint(0,35)])
    username = name+surname+str(random.randint(10000,99999))
    email = username+"@mail.com"
    bulk_users.append(User(username=username, first_name=name, last_name=surname, email=email, password=pas))
User.objects.bulk_create(bulk_users)
times.append(time.time())
adjectives = ()
nouns = ()
cities = ()
streets = ()
with open('lists/adjectives.txt') as f:
    adjectives = f.read().splitlines()
with open('lists/nouns.txt') as f:
    nouns = f.read().splitlines()
with open('lists/cities.txt') as f:
    cities = f.read().splitlines()
with open('lists/streets.txt') as f:
    streets = f.read().splitlines()
cnt_adjectives = len(adjectives)
cnt_nouns = len(nouns)
cnt_cities = len(cities)
cnt_streets = len(streets)
times.append(time.time())
bulk_shelters = []
for i in range(0,2000):
    name = ""
    if random.randint(1,5) > 1:
        if random.randint(0,1) == 1:
            name = women_names[random.randint(0,cnt_women_names-1)]
        else:
            name = men_names[random.randint(0,cnt_men_names-1)]
        name += "'s "
        if random.randint(1,100) == 1:
            name += "shelter"
        else:
            if random.randint(1,20) > 1:
                name += adjectives[random.randint(0,cnt_adjectives-1)]
            name += " " + nouns[random.randint(0,cnt_nouns-1)]
    else:
        if random.randint(1,5) > 1:
            name = "Shelter of name "
            if random.randint(0,1) == 1:
                name += women_names[random.randint(0,cnt_women_names-1)]
            else:
                name += men_names[random.randint(0,cnt_men_names-1)]
            name += " " + surnames[random.randint(0,cnt_surnames-1)]
        else:
            name += adjectives[random.randint(0,cnt_adjectives-1)]
            name += " " + nouns[random.randint(0,cnt_nouns-1)]
    location = cities[random.randint(0,cnt_cities-1)] + ", "
    location += streets[random.randint(0,cnt_streets-1)] + ", "
    location += str(random.randint(1,300))
    email = name.replace(" ", "").replace("'", "") + "@mail.com"
    bulk_shelters.append(Shelter(name=name, location=location, email=email))
Shelter.objects.bulk_create(bulk_shelters)
times.append(time.time())
del men_names
del women_names
del surnames
del adjectives
del nouns
del cities
del streets

pet_names = ()
with open('lists/pet_names.txt') as f:
    pet_names = f.read().splitlines()
cnt_pet_names = len(pet_names)

shelters = Shelter.objects.all()
users = User.objects.all()
cnt_shel = len(shelters)
cnt_user = len(users)
times.append(time.time())
bulk_pets = []
for i in range(0,200000):
    name = pet_names[random.randint(0, cnt_pet_names-1)]
    ptype = random.randint(0,3)
    sex = random.randint(0,1)
    photo = str(random.randint(ptype*10+1,(ptype+1)*10)) + ".jpg"
    in_date = date(random.randint(2010,2016), random.randint(1,12), random.randint(1,28))
    shelter_id = shelters[random.randint(0, cnt_shel-1)]
    if random.randint(1,25) == 1:
        out_date = date(2017, random.randint(1,12), random.randint(1,28))
        owner_id = users[random.randint(0, cnt_user-1)]
        bulk_pets.append(Pet(name=name, ptype=ptype, sex=sex, photo=photo, in_date=in_date, 
                out_date=out_date, shelter_id=shelter_id, owner_id=owner_id))
    else:
        bulk_pets.append(Pet(name=name, ptype=ptype, sex=sex, photo=photo, in_date=in_date, shelter_id=shelter_id))
Pet.objects.bulk_create(bulk_pets)
times.append(time.time())
del pet_names
times.append(time.time())
bulk_works = []
for i in range(0,100000):
    volunteer = users[random.randint(0, cnt_user-1)]
    shelter = shelters[random.randint(0, cnt_shel-1)]
    work_date = date(random.randint(2010,2017), random.randint(1,12), random.randint(1,28))
    work_time = random.randint(1,12)
    reward = work_time*100
    bulk_works.append(Volunteer_work(volunteer=volunteer, shelter=shelter, date=work_date,
                            work_time=work_time, reward=reward))
Volunteer_work.objects.bulk_create(bulk_works)
times.append(time.time())
works = Volunteer_work.objects.all()
cnt_work = len(works)
times.append(time.time())
bulk_ratings = []
for i in range(0,100000):
    rating = random.randint(1,10)
    comment = ""
    lng = random.randint(0,20)
    for j in range(0,lng):
        comment += str(alphabet[random.randint(0,25)])
    shelter = shelters[random.randint(0, cnt_shel-1)]
    if random.randint(0,1) == 0:
        user = users[random.randint(0, cnt_user-1)]
        #comment = "user to shelter"
        bulk_ratings.append(Rating(rating=rating, comment=comment, shelter=shelter, 
                content_object=user))
    else:
        work = works[random.randint(0, cnt_work-1)]
        #comment = "shelter to work"
        bulk_ratings.append(Rating(rating=rating, comment=comment, shelter=shelter, 
                content_object=work))
Rating.objects.bulk_create(bulk_ratings)
times.append(time.time())

for shel in shelters:
    adm = users[random.randint(0, cnt_user-1)]
    shel.administrators.add(adm)
times.append(time.time())
print(times)
