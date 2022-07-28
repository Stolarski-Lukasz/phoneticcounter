from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('count_consonants_a/', views.count_consonants_a, name='count_consonants_a'),
    path('count_consonants_b/', views.count_consonants_b, name='count_consonants_b'),
    path('count_vowels_a/', views.count_vowels_a, name='count_vowels_a'),
    path('count_vowels_b/', views.count_vowels_b, name='count_vowels_b'),
    path('count_phonemes_a/', views.count_phonemes_a, name='count_phonemes_a'),
    path('count_phonemes_b/', views.count_phonemes_b, name='count_phonemes_b'),
    path('count_syllables/', views.count_syllables, name='count_syllables')
]
