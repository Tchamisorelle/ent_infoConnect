from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission, UserManager
from django.utils import timezone

class Agenda(models.Model):
    id_ag = models.AutoField(primary_key=True)
    titre = models.CharField(max_length=255, blank=True, null=True)
    date_deb_ag = models.DateField(blank=True, null=True)
    date_fin = models.DateField(blank=True, null=True)
    note = models.CharField(max_length=255, blank=True, null=True)
    matricule = models.ForeignKey('Etudiant', db_column='matricule', blank=True, null=True, on_delete=models.CASCADE)
    matricule_en = models.ForeignKey('Enseignant',  db_column='matricule_en', blank=True, null=True, on_delete=models.CASCADE)

    class Meta:
        managed = False
        db_table = 'agenda'


class Annonce(models.Model):
    id_ann = models.AutoField(primary_key=True)
    texte = models.TextField(blank=True, null=True)
    date_pub = models.DateField(blank=True, null=True)
    categorie = models.CharField(max_length=255, blank=True, null=True)
    titre = models.CharField(max_length=255, blank=True, null=True)
    matricule = models.ForeignKey('Etudiant', db_column='matricule', blank=True, null=True, on_delete=models.CASCADE)
    matricule_en = models.ForeignKey('Enseignant',  db_column='matricule_en', blank=True, null=True, on_delete=models.CASCADE)

    class Meta:
        managed = False
        db_table = 'annonce'


class Document(models.Model):
    id_doc = models.AutoField(primary_key=True)
    titre = models.CharField(max_length=255, blank=True, null=True)
    date_doc = models.DateField(blank=True, null=True)
    type_doc = models.CharField(max_length=255, blank=True, null=True)
    matricule = models.ForeignKey('Etudiant',db_column='matricule', blank=True, null=True, on_delete=models.CASCADE)
    matricule_en = models.ForeignKey('Enseignant', db_column='matricule_en', blank=True, null=True, on_delete=models.CASCADE)

    class Meta:
        managed = False
        db_table = 'document'

class EnseignantManager(UserManager):
    pass
class Enseignant(AbstractUser):
    objects = EnseignantManager()
    matricule_en = models.CharField(primary_key=True, max_length=20)
    nom = models.CharField(max_length=255, blank=True, null=True)
    prenom = models.CharField(max_length=255, blank=True, null=True)
    email = models.CharField(max_length=255, blank=True, null=True)
    sexe = models.CharField(max_length=1, blank=True, null=True)
    mot_de_passe_ensei = models.CharField(max_length=255, blank=True, null=True)

    groups = models.ManyToManyField(Group, related_name='enseignant_groups')

    # Définir un related_name unique pour les autorisations d'utilisateur
    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name=('user permissions'),
        blank=True,
        related_name='enseignant_user_permissions',
    )
    class Meta:
        managed = False
        db_table = 'enseignant'

class EtudiantManager(UserManager):
    pass

class Etudiant(AbstractUser):
    objects = EtudiantManager()
    matricule = models.CharField(primary_key=True, max_length=10)
    nom = models.CharField(max_length=255, blank=True, null=True)
    prenom = models.CharField(max_length=255, blank=True, null=True)
    email = models.CharField(max_length=255, blank=True, null=True)
    sexe = models.CharField(max_length=1, blank=True, null=True)
    mot_de_passe = models.CharField(max_length=255, blank=True, null=True)
    filiere = models.CharField(max_length=255, blank=True, null=True)
    niveau = models.CharField(max_length=2, blank=True, null=True)
    statut = models.CharField(max_length=255, blank=True, null=True)

    groups = models.ManyToManyField(Group, related_name='etudiant_groups')
 
    # Définir un related_name unique pour les autorisations d'utilisateur
    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name=('user permissions'),
        blank=True,
        related_name='etudiant_user_permissions',
    )
    class Meta:
        managed = False
        db_table = 'etudiant'


class Note(models.Model):
    id_note = models.AutoField(primary_key=True)
    examen = models.CharField(max_length=255, blank=True, null=True)
    valeur = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    date_fin = models.DateField(blank=True, null=True)
    date_deb = models.DateField(blank=True, null=True)
    matricule = models.ForeignKey(Etudiant, db_column='matricule', blank=True, null=True, on_delete=models.CASCADE)
    matricule_en = models.ForeignKey(Enseignant, db_column='matricule_en', blank=True, null=True, on_delete=models.CASCADE)
    code_ue = models.ForeignKey('Ue', db_column='code_ue', blank=True, null=True, on_delete=models.CASCADE)

    class Meta:
        managed = False
        db_table = 'note'


class ProfilEns(models.Model):
    id_pr_en = models.AutoField(primary_key=True)
    matricule_en = models.ForeignKey(Enseignant, db_column='matricule_en', blank=True, null=True, on_delete=models.CASCADE)

    class Meta:
        managed = False
        db_table = 'profil_ens'


class ProfilEtu(models.Model):
    id_prof = models.AutoField(primary_key=True)
    mgp = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    matricule = models.ForeignKey(Etudiant, db_column='matricule', blank=True, null=True, on_delete=models.CASCADE )

    class Meta:
        managed = False
        db_table = 'profil_etu'


class Ue(models.Model):
    code_ue = models.CharField(primary_key=True, max_length=10)
    nom = models.CharField(max_length=255, blank=True, null=True)
    credit = models.IntegerField(blank=True, null=True)
    matricule_en = models.ForeignKey(Enseignant, db_column='matricule_en', blank=True, null=True, on_delete=models.CASCADE)

    class Meta:
        managed = False
        db_table = 'ue'

class ResetLink(models.Model):
    ETUDIANT = 'ETUDIANT'
    ENSEIGNANT = 'ENSEIGNANT'

    USER_TYPE_CHOICES = (
        (ETUDIANT, 'Étudiant'),
        (ENSEIGNANT, 'Enseignant'),
    )

    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES)
    token = models.CharField(max_length=100)
    expiration_time = models.DateTimeField()

    def __str__(self):
        return f"ResetLink for {self.get_user_type_display()}"
        # Utilisez get_user_type_display() pour obtenir la représentation conviviale

    def is_valid(self):
        return timezone.now() <= self.expiration_time