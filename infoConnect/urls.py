"""
URL configuration for infoConnect project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from ent_infoConnect.views import user_login, rmail, agenda, dashboard, document, annonce, requete, note, register, reset_password_request, connexion, new_utilisateur, go, register_ensei, new_utilisateur_ensei, preinscri, reset_password_done, reset_password_complete,CustomPasswordResetConfirmView, user_logout
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('user_login/', user_login, name='user_login'),
    path('renit_pwd/', rmail, name='mail'),
    path('register/', register, name='register'),
    path('register_ensei/', register_ensei, name='register_ensei'),
    path('mail_reini/', reset_password_request, name='reinitial'),
    path('connexion/', connexion, name='connexion'),
    # path('interface/', interface, name='interface'),
    path('note/', note, name='note'),
    path('requete/', requete, name='requete'),
    path('agenda/', agenda, name='agenda'),
    path('document/', document, name='document'),
    path('dashboard/', dashboard, name='dashboard'),
    path('annonce/', annonce, name='annonce'),
    path('sign_up/', new_utilisateur, name='sign-up'),
    path('sign_up_en/', new_utilisateur_ensei, name='sign-up-ensei'),
    path('go/', go, name='go'),
    path('preinscription/', preinscri, name='preinscri'),
    path('user_logout/', user_logout, name='user_logout'),
    
    path('reset_password_done/', reset_password_done, name='reset_password_done'),
    # path("reset-password/", reset_password_request, name="reset_password"),
    path("rest_password/<str:token>/<str:uidb64>/", CustomPasswordResetConfirmView.as_view(), name="password_reset_confirm"),
    path('reset_password_complete/', reset_password_complete, name='reset_password_complete'),
    

]
