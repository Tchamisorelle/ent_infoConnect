from django.shortcuts import render, redirect
from .models import Enseignant, Etudiant, ResetLink
from django.contrib.auth.hashers import make_password
from django.contrib.auth.hashers import check_password
import re
from .until import send_notification_email
from decouple import config
from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.contrib.auth import get_user_model
from django.contrib.auth.views import PasswordResetConfirmView
from django.core.mail import send_mail
from datetime import timedelta
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_decode
# from django.utils.text import force_bytes, force_text
from django.urls import reverse_lazy
from django.utils import timezone
from django.shortcuts import render
from django.views.generic import View
from django.utils.encoding import force_bytes
from django.core.mail import EmailMultiAlternatives
from django.utils.html import strip_tags
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
# from django.contrib.auth import authenticate, login
from django.http import JsonResponse
from django.contrib.auth import logout
import openpyxl
from django.views.decorators.http import require_POST
from django.contrib.contenttypes.models import ContentType  # Ajoutez cette ligne
import pandas as pd
# Create your views here.

def user_login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        mot_de_passe = request.POST.get('password')

        try:
            enseignant = Enseignant.objects.get(email=email)
        except Enseignant.DoesNotExist:
            enseignant = None

        # Si l'utilisateur n'est pas trouvé dans la table Enseignant, chercher dans la table Etudiant
        if enseignant is None:
            try:
                etudiant = Etudiant.objects.get(email=email)
            except Etudiant.DoesNotExist:
                etudiant = None

        if enseignant is not None and check_password(mot_de_passe, enseignant.mot_de_passe_ensei):
            user_info = {
                'first_name': enseignant.nom,
                'last_name': enseignant.prenom,
                'email': email,
            }
            request.session['user_info'] = user_info
            return redirect('interface')
        elif etudiant is not None and check_password(mot_de_passe, etudiant.mot_de_passe):
            user_info = {
                'first_name': etudiant.nom,
                'last_name': etudiant.prenom,
                'email': email,
            }
            request.session['user_info'] = user_info
            return redirect('interface')
        else:
            # Affichez un message d'erreur si l'authentification échoue
            error_message = "Adresse e-mail ou mot de passe incorrect"
    else:
        error_message = None

    return render(request, 'connexion.html', {'error_message': error_message})

def register(request):
    return render(request, 'inscription.html')
def interface(request):
    return render(request, 'interface.html')
def register_ensei(request):
    return render(request, 'inscription_ensei.html')
def rmail(request):
    return render(request, 'renit_pwd.html')
def connexion(request):
    return render(request, 'connexion.html')
def preinscri(request):
    return render(request, 'preinscription.html')
def annonce(request):
    return render(request, 'connexion.html')
def note(request):
    return render(request, 'connexion.html')
def requete(request):
    return render(request, 'requete.html')
def agenda(request):
    return render(request, 'connexion.html')
def document(request):
    return render(request, 'connexion.html')

def reset_password_done(request):
    return render(request, 'succes.html')

# def requete(request):
#     return render(request, 'requete.html')

def reset_password_request(request):
    if request.method == "POST":
        email = request.POST.get("email")
        try: 
            user = Enseignant.objects.get(email=email)
        except Enseignant.DoesNotExist:
            user = None

        # Si l'utilisateur n'est pas trouvé dans la table Enseignant, chercher dans la table Etudiant
        if user is None:
            try:
                user = Etudiant.objects.get(email=email)
            except Etudiant.DoesNotExist:
                return render(request, "email.html", {"error_messages": "Cet email est invalide."})
        
        if user is not None:
            token = default_token_generator.make_token(user)
            # Définir la durée de validité du lien de réinitialisation (par exemple, 1 heure)
            link_expiration_time = timezone.now() + timedelta(hours=2)

            # Enregistrez le lien de réinitialisation avec sa durée de validité
            reset_link = ResetLink(
                user=user,
                token=token,
                expiration_time=link_expiration_time,
                content_type=ContentType.objects.get_for_model(user),
                object_id=str(user.pk),
                
            )
            reset_link.save()

            current_site = get_current_site(request)
            # Générer l'URL de réinitialisation
            reset_url = reverse("password_reset_confirm", kwargs={
                # Décodez l'uidb64
                "uidb64": urlsafe_base64_encode(force_bytes(reset_link.pk)),
                "token": token,
            })

            # Afficher les valeurs pour vérification
            print("Reset URL:", reset_url)
            mail_subject = "Réinitialisation de mot de passe"
            html_content = render_to_string(
                "reset_password_email.html",
                {
                    "user": user,
                    "domaine": current_site.domain,
                    # Utilisez uidb64 ici
                    "uid": urlsafe_base64_encode(force_bytes(reset_link.pk)),
                    "jeton": token,
                    # "protocol": 'http',
                    # "reset_url": reset_url_full,
                    "reset_url": reset_url,
                },
            )

            text_content = strip_tags(html_content)
            email = EmailMultiAlternatives(
                subject=mail_subject,
                body=text_content,
                from_email="infoConnect <'pharma.prjt.yde@gmail.com'>",
                to=[email],
            )
            email.attach_alternative(html_content, "text/html")
            email.send(fail_silently=False)
        else:
            return render(request, "email.html", {"error_messages": "Cet email est invalide."})

        return redirect("reset_password_done")
    return render(request, "email.html")

class CustomPasswordResetConfirmView(View):
    # Le template contenant le formulaire de réinitialisation
    template_name = "modifier_pwd.html"

    def get_user(self, token):
        try:
            reset_link = ResetLink.objects.get(token=token)
            return reset_link.user
        except ResetLink.DoesNotExist:
            return None

    def get(self, request, uidb64, token, *args, **kwargs):
        user = self.get_user(token)

        if user is not None and default_token_generator.check_token(user, token):
            reset_link = self.get_reset_link_data(token)
            context = {
                "valid_reset_link": True,
                "uidb64": uidb64,
                "token": token,
            }

            if reset_link["token"] is not None:
                if reset_link["expiration_time"] <= timezone.now():
                    context["expired_reset_link"] = True
                    messages.error(
                        self.request, "Le lien de réinitialisation a expiré.")
                    return redirect(reverse_lazy("index"))

            return render(request, self.template_name, context)
        else:
            return redirect(reverse_lazy("index"))

    def get_reset_link_data(self, token):
        try:
            reset_link = ResetLink.objects.get(token=token)
            return {
                "token": reset_link.token,
                "expiration_time": reset_link.expiration_time,
            }
        except ResetLink.DoesNotExist:
            return None

    def post(self, request, uidb64, token, *args, **kwargs):
        user = self.get_user(token)
        new_password = request.POST.get("new_password1")
        new_password2 = request.POST.get("new_password2")
        error_messages = []

        if user is not None and default_token_generator.check_token(user, token):
            # Vérification du mot de passe
            if new_password != new_password2:
                error_messages.append("Les mots de passe ne correspondent pas")
            if len(new_password) < 8:
                error_messages.append(
                    "Le mot de passe doit contenir au moins 8 caractères")
            if not re.search(r'\d', new_password):
                error_messages.append(
                    "Le mot de passe doit contenir au moins un chiffre")
            if not re.search(r'[!@#$%^&*(),.?":{}|<>]', new_password):
                error_messages.append(
                    "Le mot de passe doit contenir au moins un caractère spécial $ & % £")

            if error_messages:
                error_message = ". ".join(error_messages)
                # Ajouter le message d'erreur
                messages.error(request, error_message)
                redirect_url = reverse("password_reset_confirm", kwargs={
                                       "token": token, "uidb64": uidb64, })
                return redirect(redirect_url)
            else:
                user.set_password(new_password)
                user.save()
                messages.success(
                    request, "Le mot de passe a été réinitialisé avec succès.")
                return redirect(reverse_lazy("reset_password_complete"))
        else:
            context = {"invalid_reset_link": True}
            return render(request, self.template_name, context)

def user_logout(request):
    # Déconnectez l'utilisateur
    logout(request)

    # Supprimez les données de session associées
    if 'user_info' in request.session:
        del request.session['user_info']

    # Redirigez l'utilisateur vers la page de déconnexion ou une autre page de votre choix
    return redirect('connexion')

def reset_password_complete(request):
    return render(request, 'reset_password_complete.html')

def new_utilisateur(request):
    error_message = None

    if request.method == 'POST':
        nom = request.POST.get('nom')
        prenom = request.POST.get('prenom')
        sexe = request.POST.get('sexe')
        email = request.POST.get('mail')
        mot_de_passe = request.POST.get('mot_de_passe')
        matricule = request.POST.get('matricule')
        statut = request.POST.get("qualification")
        filiere = request.POST.get('filiere')
        niveau = request.POST.get('niveau')

        # Validation du formulaire
        if not nom or not prenom or not email or not mot_de_passe:
            error_message = 'Tous les champs du formulaire sont obligatoires.'
        else:
            # Hachage du mot de passe
            hashed_password = make_password(mot_de_passe)

            # Vérification de l'existence de l'e-mail dans le fichier Excel
            excel_file = r"D:\projets\projet_inf331\infoConnect\ent_infoConnect\bd_etudiant.xlsx"
            email_exists = False

            try:
                sheet = "Feuil1"
                workbook = pd.read_excel(excel_file, sheet_name=sheet)
                
                print("Fichier Excel ouvert avec succès")

                for index, row in workbook.iterrows():
                    mail = row["mail"].lower()
                    matricul = row["matricule"].lower()
                    if  mail == email.lower() and  matricul == matricule.lower():
                        email_exists = True
                        print("Adresse e-mail trouvée dans le fichier Excel")
                        break
            except Exception as e:
                error_message = 'Une erreur s\'est produite lors de la vérification de l\'e-mail.'
                print("Erreur lors de l'ouverture du fichier Excel:", str(e))

            if not email_exists:
                error_message = 'Cet e-mail ne correspond pas à un étudiant de l\'université.'
            else:
                # Création d'un nouvel objet Utilisateur et enregistrement dans la base de données
                
                nouvel_utilisateur = Etudiant.objects.create(
                    matricule=matricule.lower(), nom=nom.lower(), prenom=prenom.lower(), email=email.lower(), sexe=sexe.lower(), mot_de_passe=hashed_password,
                    filiere=filiere, niveau=niveau.lower(), statut=statut.lower()
                )
                nouvel_utilisateur.save()

                # Envoi du mail
                subject = 'Bienvenue sur infoConnect'
                message = f"Bienvenue {prenom}!"
                recipient_list = [email]
                send_notification_email(subject=subject, message=message, recipient_list=recipient_list)

                # Redirection vers une page de confirmation ou toute autre page souhaitée
                return redirect('connexion')

    context = {'error_message': error_message}
    return render(request, 'inscription.html', context)

def new_utilisateur_ensei(request):
    error_message = None

    if request.method == 'POST':
        nom = request.POST.get('nom')
        prenom = request.POST.get('prenom')
        sexe = request.POST.get('sexe')
        email = request.POST.get('mail')
        mot_de_passe_ensei = request.POST.get('mot_de_passe')
        matricule_en = request.POST.get('matricule')
        
        if not nom or not prenom or not email or not mot_de_passe_ensei:
            error_message = 'Tous les champs du formulaire sont obligatoires.'
        else:
            # Hachage du mot de passe
            hashed_password = make_password(mot_de_passe_ensei)

            # Vérification de l'existence de l'e-mail dans le fichier Excel
            excel_file = r"D:\projets\projet_inf331\infoConnect\ent_infoConnect\bd_professeur.xlsx"
            email_exists = False
            try:
                    sheet = "Feuil1"
                    workbook = pd.read_excel(excel_file, sheet_name=sheet)
                    print("Fichier Excel ouvert avec succès")

                    for index, row in workbook.iterrows():
                        mail = row["mail"].lower()
                        matricule = row["matricule"].lower()
                        
                        if mail == email.lower() and matricule == matricule_en.lower():
                            email_exists = True
                            print("Adresse e-mail trouvée dans le fichier Excel")
                            break
            except Exception as e:
                error_message = 'Une erreur s\'est produite lors de la vérification de l\'e-mail.'
                print("Erreur lors de l'ouverture du fichier Excel:", str(e))

            if not email_exists:
                    error_message = 'Cet e-mail ne correspond pas à un enseignant de l\'université.'
            else:
                    # Création d'un nouvel objet Utilisateur et enregistrement dans la base de données
                    
                    nouvel_utilisateur = Enseignant.objects.create(
                        matricule_en=matricule_en.lower(), nom=nom.lower(), prenom=prenom.lower(), email=email.lower(), sexe=sexe.lower(), mot_de_passe_ensei=hashed_password,
                        
                    )
                    nouvel_utilisateur.save()

                    # Envoi du mail
                    subject = 'Bienvenue sur infoConnect'
                    message = f"Bienvenue {prenom}!"
                    recipient_list = [email]
                    send_notification_email(subject=subject, message=message, recipient_list=recipient_list)

                    # Redirection vers une page de confirmation ou toute autre page souhaitée
                    return redirect('connexion')

        
    context = {'error_message': error_message}
    return render(request, 'inscription_ensei.html', context)

@require_POST
def go(request):
    if request.method == 'POST':
        qualification = request.POST.get('qualification')
        
        if qualification == 'etudiant':
            # L'utilisateur a choisi "Étudiant"
            # Redirigez l'utilisateur vers une autre page HTML
            return redirect('register')
        elif qualification == 'enseignant':
            # L'utilisateur a choisi "Enseignant"
            # Vous pouvez effectuer des actions spécifiques ici
            return redirect('register_ensei')
        else:
            # La qualification est différente de "etudiant" et "enseignant"
            # Vous pouvez gérer ce cas si nécessaire
            return redirect('preinscri')
