from .models import Ue, Note
from .utils import MGP, normalisationNotes

def mgp(request):
    user_info = request.session.get('user_info', {})
    matricule = user_info.get('matricule', None)

    if matricule:
        Unites_en = Ue.objects.all()
        totaux_notes = []
        Credits = []

        for unite in Ue.objects.all():
            credit = unite.credit
            notes_ue = Note.objects.filter(matricule=matricule, code_ue=unite.code_ue)
            total = sum(note.valeur for note in notes_ue)
            totaux_notes.append(total)
            Credits.append(credit)

        notes_normalisees = normalisationNotes(totaux_notes)
        mgp = round(MGP(notes_normalisees, Credits), 2)
    else:
        mgp = 0

    return {'mgp': mgp}

