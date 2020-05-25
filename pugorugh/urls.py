from django.urls import path, register_converter
from django.views.generic import TemplateView
from django.views.generic.base import RedirectView

from rest_framework.authtoken.views import obtain_auth_token
from rest_framework.urlpatterns import format_suffix_patterns

from pugorugh import converters, views

register_converter(converters.SignedIntConverter, 'sint')
register_converter(converters.StatusConverter, 'status')

# API endpoints
urlpatterns = [
    path('', TemplateView.as_view(template_name='index.html')),

    path('api/user/', views.UserRegisterView.as_view(), name='register-user'),
    path('api/user/login/', obtain_auth_token, name='login-user'),
    path('api/user/preferences/', views.SetPrefView.as_view()),

    # TODO: Create status converter
    path('api/dog/new/', views.CreateDogView.as_view()),
    path('api/dog/<int:pk>/delete/', views.DeleteDogView.as_view()),
    path('api/dog/<int:pk>/hide/', views.HideDogView.as_view()),
    path('api/dog/<int:pk>/<status:status>/', views.SetStatusView.as_view()),
    path('api/dog/<int:pk>/<status:status>/prev/', views.PrevStatusView.as_view()),
    path('api/dog/<sint:pk>/<status:status>/next/', views.NextStatusView.as_view()),

    # TODO: fix this
    # path('/favicon.ico', RedirectView.as_view(url='/static/icons/favicon.ico', permanent=True)),
]

# TODO: Read about format_suffix_patterns and add necessary stuff to views
urlpatterns = format_suffix_patterns(urlpatterns)