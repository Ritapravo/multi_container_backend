from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home),
    path('createLab/', views.createLab.as_view()),
    path('labs/', views.getlabs.as_view()),
    path('labs/<str:pk>/',  views.getlabs.as_view( )),

    # Student part

    path('attemptLab/<str:pk>/', views.attemptLab.as_view()),
    path('endLab/<str:pk>/', views.exitLab.as_view()),

    path('evaluateLab/<str:pk>/', views.evaluateLab.as_view()),

    # path('admin/', admin.site.urls)
]