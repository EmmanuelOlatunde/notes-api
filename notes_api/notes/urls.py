from . import views
from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path('notes/',views.note_list, name="notes-view-create" ),
    path('notes/<int:pk>',views.note_detail, name="notes-detail" ),
    #path('register',views.register, name="register" ),
    #path('login',views.login, name="login" ),
    path('auth/', obtain_auth_token),  # Token login
    #path('notes-ui/', views.notes_frontend, name='notes-frontend'),

]
urlpatterns = format_suffix_patterns(urlpatterns)