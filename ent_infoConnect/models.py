from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission, UserManager
from django.utils import timezone
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.urls import reverse

class Agenda(models.Model):
    id_ag = models.AutoField(primary_key=True)
    titre = models.CharField(max_length=255, blank=True, null=True)
    date_deb_ag = models.DateField(blank=True, null=True)
    date_fin = models.DateField(blank=True, null=True)
    note = models.CharField(max_length=255, blank=True, null=True)
    matricule = models.ForeignKey('Etudiant', db_column='matricule', blank=True, null=True, on_delete=models.CASCADE)
    matricule_en = models.ForeignKey('Enseignant',  db_column='matricule_en', blank=True, null=True, on_delete=models.CASCADE)

    class Meta:
        managed = True
        db_table = 'agenda'

class Annonce(models.Model):
    id_ann = models.AutoField(primary_key=True)
    texte = models.TextField(blank=True, null=True)
    date_pub = models.DateTimeField(auto_now=True, null=True)
    categorie = models.CharField(max_length=255, blank=True, null=True)
    titre = models.CharField(max_length=255, blank=True, null=True)
    matricule = models.ForeignKey('Etudiant', db_column='matricule', blank=True, null=True, on_delete=models.CASCADE)
    matricule_en = models.ForeignKey('Enseignant',  db_column='matricule_en', blank=True, null=True, on_delete=models.CASCADE)
    class Meta:
        managed = True
        db_table = 'annonce'


class Document(models.Model):
    id_doc = models.AutoField(primary_key=True)
    titre = models.CharField(max_length=255, blank=True, null=True)
    file = models.FileField(null=True, blank=True)
    date_doc = models.DateField(blank=True, null=True)
    description = models.CharField(max_length=255, blank=True, null=True)
    #matricule = models.ForeignKey('Etudiant',db_column='matricule', blank=True, null=True, on_delete=models.CASCADE)
    matricule_en = models.ForeignKey('Enseignant', db_column='matricule_en', blank=True, null=True, on_delete=models.CASCADE)

    class Meta:
        managed = True
        db_table = 'document'
    @property
    def url(self):
        return reverse('download_document', args=[str(self.id)])
    

class EnseignantManager(BaseUserManager):
    def create_user(self, matricule_en, email, mot_de_passe_ensei=None, **extra_fields):
        if not email:
            raise ValueError("L'adresse e-mail est obligatoire.")
        email = self.normalize_email(email)
        user = self.model(matricule_en=matricule_en, email=email, **extra_fields)
        user.set_password(mot_de_passe_ensei)
        user.save(using=self._db)
        return user

    def create_superuser(self, matricule_en, email, mot_de_passe_ensei=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        return self.create_user(matricule_en, email, mot_de_passe_ensei, **extra_fields)
    
class Enseignant(AbstractBaseUser):
    matricule_en = models.CharField(primary_key=True, max_length=20)
    nom = models.CharField(max_length=255, blank=True, null=True)
    prenom = models.CharField(max_length=255, blank=True, null=True)
    email = models.CharField(max_length=255, blank=True, null=True)
    sexe = models.CharField(max_length=1, blank=True, null=True)
    mot_de_passe_ensei = models.CharField(max_length=255, blank=True, null=True)
    # Attributs requis pour AbstractBaseUser
    last_login = models.DateTimeField(auto_now=True, null=True)
    objects = EnseignantManager()
    USERNAME_FIELD = 'email'    
    password = None
    def __str__(self):
        return self.email
    class Meta:
        managed = True
        db_table = 'enseignant'


class EtudiantManager(BaseUserManager):
    def create_user(self, matricule, email, mot_de_passe=None, **extra_fields):
        if not email:
            raise ValueError("L'adresse e-mail est obligatoire.")
        email = self.normalize_email(email)
        user = self.model(matricule=matricule, email=email, **extra_fields)
        user.set_password(mot_de_passe)
        user.save(using=self._db)
        return user

    def create_superuser(self, matricule, email, mot_de_passe=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        return self.create_user(matricule, email, mot_de_passe, **extra_fields)

class Etudiant(AbstractBaseUser):
    # user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    matricule = models.CharField(primary_key=True, max_length=10)
    nom = models.CharField(max_length=255, blank=True, null=True)
    prenom = models.CharField(max_length=255, blank=True, null=True)
    email = models.CharField(max_length=255, unique=True)
    mot_de_passe = models.CharField(max_length=255, blank=True, null=True)
    sexe = models.CharField(max_length=1, blank=True, null=True)
    filiere = models.CharField(max_length=255, blank=True, null=True)
    niveau = models.CharField(max_length=2, blank=True, null=True)
    statut = models.CharField(max_length=255, blank=True, null=True)

    # Attributs requis pour AbstractBaseUser
    last_login = models.DateTimeField(auto_now=True, null=True)
    
    objects = EtudiantManager()
    USERNAME_FIELD = 'email'
    password = None
    def __str__(self):
        return self.email
    class Meta:
        managed = True
        db_table = 'etudiant'


class Note(models.Model):
    id_note = models.AutoField(primary_key=True)
    examen = models.CharField(max_length=255, blank=True, null=True)
    valeur = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    date_fin = models.DateField(blank=True, null=True)
    date_deb = models.DateField(blank=True, null=True)
    matricule = models.ForeignKey('Etudiant', db_column='matricule', blank=True, null=True, on_delete=models.CASCADE)
    matricule_en = models.ForeignKey('Enseignant', db_column='matricule_en', blank=True, null=True, on_delete=models.CASCADE)
    code_ue = models.ForeignKey('Ue', db_column='code_ue', blank=True, null=True, on_delete=models.CASCADE)

    class Meta:
        managed = True
        db_table = 'note'


class ProfilEns(models.Model):
    id_pr_en = models.AutoField(primary_key=True)
    matricule_en = models.ForeignKey('Enseignant', db_column='matricule_en', blank=True, null=True, on_delete=models.CASCADE)

    class Meta:
        managed = True
        db_table = 'profil_ens'


class ProfilEtu(models.Model):
    id_prof = models.AutoField(primary_key=True)
    mgp = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    matricule = models.ForeignKey('Etudiant', db_column='matricule', blank=True, null=True, on_delete=models.CASCADE )

    class Meta:
        managed = True
        db_table = 'profil_etu'


class Ue(models.Model):
    code_ue = models.CharField(primary_key=True, max_length=10)
    nom = models.CharField(max_length=255, blank=True, null=True)
    credit = models.IntegerField(blank=True, null=True)
    matricule_en = models.ForeignKey('Enseignant', db_column='matricule_en', blank=True, null=True, on_delete=models.CASCADE)
    TYPE_CHOICES = [
        ('F', 'Fondamentale'),
        ('O', 'Optionnelle'),
    ]
    type_ue = models.CharField(max_length=1, choices=TYPE_CHOICES, default='O')

    class Meta:
        managed = True
        db_table = 'ue'



class ResetLink(models.Model):
    ETUDIANT = 'ETUDIANT'
    ENSEIGNANT = 'ENSEIGNANT'

    USER_TYPE_CHOICES = (
        (ETUDIANT, 'Etudiant'),
        (ENSEIGNANT, 'Enseignant'),
    )

    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.CharField(max_length=255)  # Utilisez CharField pour stocker une chaîne unique
    user = GenericForeignKey('content_type', 'object_id')
    token = models.CharField(max_length=100)
    expiration_time = models.DateTimeField()

    def __str__(self):
        return f"ResetLink for {self.get_user_type_display()}"

    def is_valid(self):
        return timezone.now() <= self.expiration_time
