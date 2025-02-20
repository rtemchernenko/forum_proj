from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from graphene_django.views import GraphQLView
from .schema import schema
from .views import profile_view, RegisterView
from . import views

app_name = 'forum_app'

urlpatterns = [
    path('profile/', profile_view, name='profile'),
    path('register/', RegisterView.as_view(), name='register'),
    path('logout/', views.logout, name='logout'),
    path('graphql/', GraphQLView.as_view(graphiql=True, schema=schema)),  # GraphQL API
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
