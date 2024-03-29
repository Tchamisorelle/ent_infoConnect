from django.shortcuts import render, redirect
from .models import Enseignant, Etudiant, ResetLink, Note, Ue, Document, Requete
from .utils import MGP, normalisationNotes, calculate_stats, stat, selection
from django.db.models import F
from django.contrib.auth.hashers import make_password
from django.contrib.auth.hashers import check_password
import re
import os
from django.http import HttpResponseServerError
from django.views.decorators.csrf import csrf_exempt
import pandas as pd
from datetime import datetime, timedelta
from django.db import IntegrityError
from django.db.models import Count
from django.core.serializers.json import DjangoJSONEncoder
from django.forms.models import model_to_dict
from django import forms
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
# from django.utils.html import strip_tags
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
from django.http import JsonResponse
from django.db import connection
# document
import json
from datetime import datetime
from django.http import FileResponse
import mimetypes
from django.shortcuts import get_object_or_404
# Create your views here.

def user_login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        mot_de_passe = request.POST.get('password')
        enseignant = None
        etudiant = None
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
                'matricule_en': enseignant.matricule_en,
            }
            request.session['user_info'] = user_info
            return redirect('dashboard_ens')
        elif etudiant is not None and check_password(mot_de_passe, etudiant.mot_de_passe):
            user_info = {
                'first_name': etudiant.nom,
                'last_name': etudiant.prenom,
                'email': email,
                'matricule': etudiant.matricule
            }
            request.session['user_info'] = user_info
            return redirect('dashboard')
        else:
            # Affichez un message d'erreur si l'authentification échoue
            error_message = "Adresse e-mail ou mot de passe incorrect"
    else:
        error_message = None

    return render(request, 'connexion.html', {'error_message': error_message})

def register(request):
    return render(request, 'inscription.html')
# def interface(request):
#     return render(request, 'interface.html')
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

def requete_ens(request):
    user_info = request.session.get('user_info', {})
    matricule_ens = user_info.get('matricule_en', None)
    form = ImportRequetForm(user_info=user_info)
    if matricule_ens:
        requetes = Requete.objects.filter(matricule_en=matricule_ens)
        requet_data = []
        for requete in requetes:
            code_ue = requete.code_ue.code_ue
            statut = requete.statut
            requet_data.append({'code_ue': code_ue, 'statut': statut})
        return render(request, 'requete_ens.html', {'form': form, 'requete_data': requet_data, 'user_info': user_info})
    else:
        messages.error(request, 'Matricule enseignant non trouvé.')
        return render(request, 'requete_ens.html', {'form': form, 'user_info': user_info})



def notes(request):
    user_info = request.session.get('user_info', {})
    exams = ['cc', 'tps', 'examen']
    matricule = user_info.get('matricule', None)
    Unites_en = Ue.objects.all()
    notes_etudiant = {}

    for unite in Ue.objects.all():
        nom_ue = unite.nom
        notes_ue = Note.objects.filter(matricule=matricule, code_ue=unite.code_ue)
        total = sum(note.valeur for note in notes_ue)
        notes_etudiant[unite.code_ue] = {'notes': notes_ue, 'total': total, 'nom': nom_ue}

    return render(request, 'notes.html', {'notes_data': notes_etudiant, 'user_info': user_info, 'exams': exams})
        
class ImportNotesForm(forms.Form):
    ue_code = forms.ModelChoiceField(queryset=Ue.objects.none())
    file = forms.FileField()

    def __init__(self, *args, user_info=None, **kwargs):
        super(ImportNotesForm, self).__init__(*args, **kwargs)

        if user_info:
            self.fields['ue_code'].queryset = Ue.objects.filter(matricule_en=user_info.get('matricule_en'))


def import_notes_logic(request, form):
    try:
        ue_code = form.cleaned_data['ue_code']
        enseignant = Enseignant.objects.get(matricule_en=request.session['user_info']['matricule_en'])
        ue = Ue.objects.get(matricule_en=enseignant.matricule_en)
        df = pd.read_excel(request.FILES['file'])
        notes_data = df.values
        matricule_et = None
        nom = None
        prenoms = None
        cc = None
        tps = None
        examen = None     
        #print(notes_data)               
        for note_data in notes_data:
            matricule_et, nom, prenoms, cc, tps, examen = note_data
            
            matricule_et = matricule_et.lower()
            try:
                etudiant = Etudiant.objects.get(matricule=matricule_et)
                
            except Etudiant.DoesNotExist:
                email = f"{nom.lower()}.{prenoms.lower()}@facsciences-uy1.cm"
                password = make_password('Gsuite@uy1')
                etudiant = Etudiant.objects.create(matricule=matricule_et, nom=nom, prenom=prenoms, mot_de_passe=password, email=email)
                message = "<html><body>&nbsp; &nbsp; <strong> Etudiant: </strong>" + nom + "&nbsp;" + prenoms + "<br/>" + "<br/> &nbsp; &nbsp; <strong> Matricule </strong>" + matricule_et+ "<br/> <br/> Notes(s): <br/>" + "<strong>" + ", cc" + cc +",Tp" + tps + ", examen" + examen + "</strong>" + "<p>Cordialement,<br>L\'équipe infoConnect</p><footer><center>&copy; 2023 infoConnect</center></footer></body></html>"  # Convertir la liste en une chaîne
                

            date_deb = datetime.now().date()
            date_fin = date_deb + timedelta(days=7)
            try:
                existing_note_cc = Note.objects.get(examen='cc', matricule=etudiant, matricule_en=enseignant, code_ue=ue_code)
                existing_note_tps = Note.objects.get(examen='tps', matricule=etudiant, matricule_en=enseignant, code_ue=ue_code)
                existing_note_examen = Note.objects.get(examen='examen', matricule=etudiant, matricule_en=enseignant, code_ue=ue_code)
                existing_note_cc.valeur = cc
                existing_note_tps.valeur = tps
                existing_note_examen.valeur = examen
                existing_note_cc.save()
                existing_note_tps.save()
                existing_note_examen.save()
            except Note.DoesNotExist:
                Note.objects.create(examen='cc', valeur=cc, date_deb=date_deb, date_fin=date_fin, matricule=etudiant, matricule_en=enseignant, code_ue=ue_code)
                Note.objects.create(examen='tps', valeur=tps, date_deb=date_deb, date_fin=date_fin, matricule=etudiant, matricule_en=enseignant, code_ue=ue_code)
                Note.objects.create(examen='examen', valeur=examen, date_deb=date_deb, date_fin=date_fin, matricule=etudiant, matricule_en=enseignant, code_ue=ue_code)
            try:
                message = "<html><body>&nbsp; &nbsp; <strong> Etudiant: </strong>" + nom + "&nbsp;" + prenoms + "<br/>" + "<br/> &nbsp; &nbsp; <strong> Matricule </strong>" + matricule_et+ "<br/> <br/> Notes(s): <br/>" + "<strong>" + " cc: " + str(cc) + ",<br/>Tp: " + str(tps) + ",  <br/> examen: " + str(examen) + "</strong>" + "<p>Cordialement,<br>L\'équipe infoConnect</p><footer><center>&copy; 2023 infoConnect</center></footer></body></html>"  # Convertir la liste en une chaîne
                objet = f"Note de l'UE {ue_code}"
                mail = Etudiant.objects.filter(matricule=matricule_et).values_list('email', flat=True).first()
                # print(mail)
                send_mail(
                    objet,
                    message,
                    "infoConnect <pharma.prjt.yde@gmail.com>", #expediteur
                    [mail], #destinataire
                    fail_silently=False,
                    html_message=message
                    )
            except Exception as e:
                print(f"Erreur lors de l'envoi d'e-mail : {e}")

        messages.success(request, 'Les notes ont été importées avec succès.')
        return redirect('notes_ens')
    except Enseignant.DoesNotExist:
        messages.error(request, 'Enseignant non trouvé.')
    except Ue.DoesNotExist:
        messages.error(request, 'UE non trouvée.')
    except Exception as e:
        messages.error(request, f'Une erreur s\'est produite : {str(e)}')
        return HttpResponseServerError('Internal Server Error')

    return None

def import_notes(request):
    if 'user_info' in request.session:
        form = ImportNotesForm(request.POST, request.FILES, user_info=request.session['user_info'])
        if request.method == 'POST':
            if form.is_valid():
                result = import_notes_logic(request, form)
                if result is not None:
                    return result
            else:
                messages.error(request, 'Le formulaire n\'est pas valide. Veuillez corriger les erreurs.')
    else:
        form = ImportNotesForm(user_info=request.session['user_info'])

    return render(request, 'notes_ens.html', {'form': form})

def notes_ens(request):
    user_info = request.session.get('user_info', {})
    form = ImportNotesForm(request.POST or None, request.FILES or None)

    if user_info:
        form.fields['ue_code'].queryset = Ue.objects.filter(matricule_en=user_info.get('matricule_en'))
           
    stats = {}

    if request.method == 'POST':
        if form.is_valid():
            ue_code = form.cleaned_data['ue_code']

    for ue in Ue.objects.filter(matricule_en=user_info.get('matricule_en')):
        ue_stats = calculate_stats(ue.code_ue)
        stats[ue.code_ue] = ue_stats


    return render(request, 'notes_ens.html', {'form': form, 'user_info': user_info, 'stats': stats})

class ImportRequetForm(forms.Form):
    ue_code = forms.ModelChoiceField(queryset=Ue.objects.none())
    file = forms.FileField()
    statut = forms.ChoiceField(choices=[('traiter', 'Traiter'), ('non_traiter', 'Non Traiter')])

    def __init__(self, *args, user_info=None, **kwargs):
        super(ImportRequetForm, self).__init__(*args, **kwargs)

        if user_info:
            self.fields['ue_code'].queryset = Ue.objects.filter(matricule_en=user_info.get('matricule_en'))

def correct_requet(request):
    
    form = ImportRequetForm(request.POST, request.FILES, user_info=request.session.get('user_info'))

    if form.is_valid():
        code_ue = form.cleaned_data['ue_code']
        statut = form.cleaned_data['statut']

        try:
            requete = Requete.objects.filter(code_ue=code_ue)
            for requet in requete:
                requet.statut = statut
                requet.save()
                
                result = import_notes_logic(request, form)

            if result is not None:
                return result
        except Requete.DoesNotExist:
            messages.error(request, 'L\'objet Requete avec le code UE spécifié n\'existe pas.')
    else:
        messages.error(request, 'Le formulaire n\'est pas valide. Veuillez corriger les erreurs.')
    
    return render(request, 'requete_ens.html', {'form': form})

def requete(request):
    user_info = request.session.get('user_info', {})
    return render(request, 'requete.html', {'user_info': user_info})

def agenda(request):
    return render(request, 'connexion.html')
def document(request):
    user_info = request.session.get('user_info', {})

    return render(request, 'document.html', {'user_info': user_info})
def document_ens(request):
    return render(request, 'document_ens.html')

def dashboard(request):
    user_info = request.session.get('user_info', {})
    return render(request, 'dashboard.html', {'user_info': user_info})


def dashboard_ens(request):
    return render(request, 'dashboard_ens.html')

def reset_password_done(request):
    return render(request, 'succes.html')

def list_note(request):
    # Récupérer toutes les valeurs uniques de code_ue
    code_ue_list = Note.objects.values_list('code_ue', flat=True).distinct()

    # Créer une liste pour stocker les données finales
    notes_data = []

    # Pour chaque code_ue, récupérer toutes les valeurs uniques de date_deb, date_fin et examen
    for code_ue in code_ue_list:
        # Récupérer les valeurs uniques de date_deb, date_fin et examen pour le code_ue actuel
        notes_for_ue = Note.objects.filter(code_ue=code_ue).values(
            'date_deb',
            'date_fin',
            'examen'
        ).distinct()
        
        aggregated_data = {
            'examen': code_ue,
            'dates': [{'date_deb': note['date_deb'], 'date_fin': note['date_fin'], 'typ_exam': note['examen']} for note in notes_for_ue],
        }
        

        # Ajout les données agrégées au dictionnaire final
        notes_data.append(aggregated_data)
        
    return JsonResponse(notes_data, safe=False)

def req_note(request):
    if request.method == 'POST':
        examens = request.POST.get('examens')
        if examens is None:
            # Champ 'examens' non présent dans la requête, faites quelque chose en conséquence
            messages.error(request, 'Veuillez sélectionner un examen.')
            return redirect('requete')

        ue = Ue.objects.get(code_ue=examens)
        user_info = request.session.get('user_info', {})
        email = user_info['email']
        if ue:
            statut = 'Non Traiter'
            matricule_en = ue.matricule_en

            # Création d'une instance de Requete dans la base de données
            inst_re = Requete.objects.create(
                code_ue=ue,
                statut=statut,
                matricule_en=matricule_en
            )
            inst_re.save()
            requete_ens(request)
            qualifications = request.POST.getlist('qualification')
            # Reste du code ici
            examens.lower() 
            objet = f"Requete sur les notes {examens}"
            message = "<html><body>&nbsp; &nbsp; <strong> Etudiant: </strong>" + user_info['first_name'] + "&nbsp;" + user_info['last_name'] + "<br/>" + "<br/> &nbsp; &nbsp; <strong> Matricule </strong>" + user_info['matricule']+ "<br/> <br/> Probleme(s): <br/>" + "<strong>" + ", ".join(qualifications) +"</strong>" + "<p>Cordialement,<br>L\'équipe infoConnect</p><footer><center>&copy; 2023 infoConnect</center></footer></body></html>"  # Convertir la liste en une chaîne
            email_enseignant = Enseignant.objects.filter(ue__code_ue=ue).values_list('email', flat=True).first()
            
            if qualifications and objet and message:

                try:
                    send_mail(
                        objet,
                        message,
                        f"infoConnect <{email}>", #expediteur
                        [email_enseignant], #destinataire
                        fail_silently=False,
                        html_message=message
                        )
                    send_mail(
                        objet,
                        message,
                        "infoConnect <pharma.prjt.yde@gmail.com>",  
                        [email],
                        fail_silently=False,
                        html_message='<html><body style="background-color:  #f0f8f9;"> <p style="padding: 10px;"> Merci,<br/> Nous vous remercions pour l\'interet que vous portez a cette plateforme!</p> <p style="padding-left: 10px;">Votre requete a été transmise. <br> A bientot!! </p><p style="padding: 10px;">Cordialement,<br>L\'équipe infoConnect</p><footer><center>&copy; 2023 infoConnect</center></footer></body></html>'
                        )
                    messages.success(
                    request, 'Votre requete a été envoyée avec succès.')
                except Exception as e:
                        messages.error(
                            request, 'Une erreur s\'est produite lors de l\'envoi de la suggestion.')
        else:
            messages.error(
                request, 'erreur.')

    return redirect('requete')

def list_docu(request):
    documents = Document.objects.values('id_doc','titre', 'file', 'date_doc', 'description')
    document_data = []
    for doc in documents:
        doc_data = {
            'id_doc': doc['id_doc'],
            'titre': doc['titre'],
            'file': doc['file'],
            'date_doc': doc['date_doc'],
            'description': doc['description'],
        }
        document_data.append(doc_data)

    return JsonResponse(document_data, safe=False)

def list_docu_ens(request):
    user_info = request.session.get('user_info', {})
    documents = Document.objects.filter(matricule_en=user_info['matricule_en'])
    documents = documents.values('id_doc', 'titre', 'file', 'date_doc', 'description')
    document_data = []
    for doc in documents:
        doc_data = {
            'id_doc': doc['id_doc'],
            'titre': doc['titre'],
            'file': doc['file'],
            'date_doc': doc['date_doc'],
            'description': doc['description'],
        }
        document_data.append(doc_data)

    return JsonResponse(document_data,encoder=DjangoJSONEncoder, safe=False)


@require_POST
def stock_docu(request):
    if request.method == 'POST':
        # Récupérer les informations de l'utilisateur connecté à partir de la session
        user_info = request.session.get('user_info', {})
        matricule_en = user_info.get('matricule_en', None)

        # Vérifier si l'utilisateur est un enseignant
        if matricule_en:
            try:
                # Récupérer l'enseignant à partir de la table Enseignant
                enseignant = Enseignant.objects.get(matricule_en=matricule_en)

                # Récupérer les données du corps de la requête
                titre = request.POST.get('titre', '')
                description = request.POST.get('description', '')
                date_str = request.POST.get('date_doc', '')

                # Validation de la date
                date = datetime.strptime(date_str, '%Y-%m-%d').date() if date_str else None

                # Récupération du fichier
                file = request.FILES.get('file')

                # Enregistrement dans la base de données
                new_document = Document(titre=titre, description=description, date_doc=date, file=file, matricule_en=enseignant)
                new_document.save()

                response_data = {"success": True, "message": "Document stocké avec succès."}
                return redirect('document_ens')
            except Exception as e:
                return JsonResponse({'success': False, 'message': 'Erreur lors de l\'enregistrement du document.', 'error': str(e)})
        else:
            # L'utilisateur n'est pas un enseignant, renvoyer un message d'erreur
            error_message = "Vous n'êtes pas autorisé à effectuer cette action."
            return redirect('document_ens')
    else:
      
        return redirect('connexion')
class DownloadDocumentView(View):
    def get(self, request, id_doc):
        document = get_object_or_404(Document, pk=id_doc)
        file_path = document.file.path
        response = FileResponse(open(file_path, 'rb'))
        response['Content-Disposition'] = f'attachment; filename="{document.file}"'
        return response


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
            # print("Reset URL:", reset_url)
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
            excel_file = os.path.join(os.path.dirname(__file__), "bd_etudiant.xlsx")            
            email_exists = False

            try:
                sheet = "Feuil1"
                workbook = pd.read_excel(excel_file, sheet_name=sheet)
                
                for index, row in workbook.iterrows():
                    mail = row["mail"].lower()
                    matricul = row["matricule"].lower()
                    if  mail == email.lower() and  matricul == matricule.lower():
                        email_exists = True
                        # print("Adresse e-mail trouvée dans le fichier Excel")
                        break
            except Exception as e:
                error_message = 'Une erreur s\'est produite lors de la vérification de l\'e-mail.'
                # print("Erreur lors de l'ouverture du fichier Excel:", str(e))

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
            excel_file = os.path.join(os.path.dirname(__file__), "bd_professeur.xlsx")            
            email_exists = False
            try:
                    sheet = "Feuil1"
                    workbook = pd.read_excel(excel_file, sheet_name=sheet)
                    for index, row in workbook.iterrows():
                        mail = row["mail"].lower()
                        matricule = row["matricule"].lower()
                        
                        if mail == email.lower() and matricule == matricule_en.lower():
                            email_exists = True
                            # print("Adresse e-mail trouvée dans le fichier Excel")
                            break
            except Exception as e:
                error_message = 'Une erreur s\'est produite lors de la vérification de l\'e-mail.'
                # print("Erreur lors de l'ouverture du fichier Excel:", str(e))

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
