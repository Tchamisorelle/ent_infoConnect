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
from ent_infoConnect.views import user_login, rmail, agenda, dashboard, document,DownloadDocumentView, annonce, annonce_ens, deleteAnnonce, editAnnonce, addAnnonce_ens, addAnnonce, req_note, list_note, requete, notes, list_docu, stock_docu, register, reset_password_request, connexion, new_utilisateur, go, register_ensei, new_utilisateur_ensei, preinscri, reset_password_done, reset_password_complete,CustomPasswordResetConfirmView, user_logout, notes_ens, import_notes, dashboard_ens
from django.contrib.auth import views as auth_views
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('user_login/', user_login, name='user_login'),
    path('renit_pwd/', rmail, name='mail'),
    path('register/', register, name='register'),
    path('register_ensei/', register_ensei, name='register_ensei'),
    path('mail_reini/', reset_password_request, name='reinitial'),
    path('connexion/', connexion, name='connexion'),
    path('notes/', notes, name='notes'),
    path('notes_ens/', notes_ens, name='notes_ens'),
    path('import-notes/', import_notes, name='import_notes'),
    path('requete/', requete, name='requete'),
    path('agenda/', agenda, name='agenda'),
    path('document/', document, name='document'),
    path('dashboard/', dashboard, name='dashboard'),
    path('dashboard_ens/', dashboard_ens, name = 'dashboard_ens'),
    path('annonce/', annonce, name='annonce'),
    path('annonce/addAnnonce', addAnnonce, name='addAnnonce'),
    path('annonce_ens/addAnnonce_ens', addAnnonce_ens, name='addAnnonce_ens'),
    path('annonce_ens/', annonce_ens, name='annonce_ens'),
    path('annonce/deleteAnnonce/<int:annonce_id>/', deleteAnnonce, name='deleteAnnonce'),
    path('annonce/editAnnonce/<int:annonce_id>/', editAnnonce, name='editAnnonce'),
    path('sign_up/', new_utilisateur, name='sign-up'),
    path('sign_up_en/', new_utilisateur_ensei, name='sign-up-ensei'),
    path('req_note/', req_note, name='req_note'),
    path('list_note/', list_note, name='list_note'), #il s'agit des note du module requete qui recupere la liste de note dispo dans la bd
    path('list_docu/', list_docu, name='list_docu'),
    path('stock_docu/', stock_docu, name='stock_docu'),
    path('download_document/<int:id_doc>/', DownloadDocumentView.as_view(), name='download_document'),

    path('document/', document, name='document'),
    path('go/', go, name='go'),
    path('preinscription/', preinscri, name='preinscri'),
    path('user_logout/', user_logout, name='user_logout'),
    path('reset_password_done/', reset_password_done, name='reset_password_done'),
    # path("reset-password/", reset_password_request, name="reset_password"),
    path("rest_password/<str:token>/<str:uidb64>/", CustomPasswordResetConfirmView.as_view(), name="password_reset_confirm"),
    path('reset_password_complete/', reset_password_complete, name='reset_password_complete'),
    path('', connexion),

]
# Ajouter ceci pour servir les fichiers médias pendant le développement
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)