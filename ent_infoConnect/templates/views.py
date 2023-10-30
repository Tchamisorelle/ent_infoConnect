from django.shortcuts import render, redirect
from .models import Enseignant, Etudiant
from django.contrib.auth.hashers import make_password
from django.contrib.auth.hashers import check_password

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
        elif etudiant is not None and check_password(mot_de_passe, etudiant.mot_de_passe_etudiant):
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
def rmail(request):
    return render(request, 'renit_pwd.html')
