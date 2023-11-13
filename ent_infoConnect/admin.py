from django.contrib import admin


from .models import Agenda, Annonce, Document, Enseignant, Etudiant, Note, ProfilEns, ProfilEtu, Ue, ResetLink

# Enregistrez chaque modèle ici
admin.site.register(Agenda)
admin.site.register(Annonce)
admin.site.register(Document)
admin.site.register(Enseignant)
admin.site.register(Etudiant)
admin.site.register(Note)
admin.site.register(ProfilEns)
admin.site.register(ProfilEtu)
admin.site.register(Ue)
admin.site.register(ResetLink)
