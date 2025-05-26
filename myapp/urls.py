# myapp/urls.py
from django.urls import path
from . import views
from django.contrib.auth.decorators import login_required
app_name = "myapp"
urlpatterns = [

    path('', views.index, name='index'),  #Home page
    path('login/', views.user_login, name='login'),  #Login page

    path('radar/',views.radar,name="radar"), #Radar_test

    path('darkmode/',views.darkMode,name="darkMode"), #Dark and light mode page

    path('register/',views.register,name="register"), #Register

    path('logout/', views.user_logout, name='logout'), #Logout

    path('profile/', views.profile, name='profile'), #User Profile

    path('settings/', login_required(views.settings), name='settings'), # User Settings
    path('settings/change_email/', login_required(views.change_email), name='change_email'),    #User Email Change
    path('settings/change_password/', login_required(views.change_password), name='change_password'), #User Password change

    path('admin_adm/', views.admin_dashboard, name='admin_dashboard'),
    path('admin_adm/user/<int:user_id>/edit/', views.admin_edit_user, name='admin_edit_user'),
    path('admin_adm/user/<int:user_id>/delete/', views.admin_delete_user, name='admin_delete_user'),

]
