from django.urls import path
from . import views

app_name = 'party'

urlpatterns = [
    path('', views.index, name='index'),
    path('capture/', views.capture_pokemon, name='capture'),
    path('optimize/', views.optimize_party, name='optimize'),
    path('sort/', views.sort_party, name='sort'),
    path('move-to-party/<int:pk>/', views.move_to_party, name='move_to_party'),
    path('move-to-pc/<int:pk>/', views.move_to_pc, name='move_to_pc'),
    path('release/<int:pk>/', views.release_pokemon, name='release'),
    path('api/stats/<int:pk>/', views.pokemon_stats_api, name='stats_api'),
]
