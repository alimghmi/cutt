from django.db import router
from django.urls import path
from rest_framework import routers

from core import views

router = routers.SimpleRouter()
router.register('links', views.LinkViewSet, basename='link')
router.register('users', views.UserViewSet, basename='user')

urlpatterns = router.urls
urlpatterns += [
                    path('signup/', views.SignupAPI.as_view(), name='singup-api'),
                    path('stats/<slug:slug>/', views.StatsAPI.as_view(), name='stats-api'),
                    path('<slug:slug>/', views.RedirectAPI.as_view(), name='redirect-api'),
                ]
