from django.conf.urls import url
from django.views.generic import RedirectView
from shelters.views import shelter_list, shelter_detail, ajax_shelters, shelter_pets
from shelters.views import pet_list, pet_detail, ajax_pets
from shelters.views import account, signup, main_page
from shelters.views import ajax_shel_admin, ajax_comment
from django.contrib.auth.views import login, logout

urlpatterns = [
    url(r'^$', main_page, name='main_page'),
    url(r'^login/$', login, name='login'),
    url(r'^logout/$', logout, name='logout'),
    url(r'^registration/$', signup, name='signup'),
    url(r'^shelters/list/$', shelter_list, name='shelter_list'),
    url(r'^shelters/(?P<shelter_id>\d+)/$', shelter_detail, name='shelter_detail'),
    url(r'^shelters/(?P<shelter_id>\d+)/pets/$', shelter_pets, name='shelter_pets'),
    url(r'^pets/list/$', pet_list, name = 'pet_list'),
    url(r'^pets/(?P<pet_id>\d+)/$', pet_detail, name='pet_detail'),
    url(r'^account/$', account, name='account'),
    url(r'^ajax/shelters/$', ajax_shelters, name='ajax_shelters'),
    url(r'^ajax/pets/$', ajax_pets, name='ajax_pets'),
    url(r'^ajax/shel_admin/$', ajax_shel_admin, name='ajax_shel_admin'),
    url(r'^ajax/comment/$', ajax_comment, name='ajax_comment'),
]
