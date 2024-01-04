from .models import Note

def MGP(notes_normalisees, Credits):
    
    somme = 0
    for note, credit in zip(notes_normalisees, Credits):
        somme = somme + note*credit
    n =  sum(Credits)
    return somme / n





def normalisationNotes(totaux_notes):
    note_pondere = []
    for total in totaux_notes:
        if 0 <= total < 35:
            note_pondere.append(0)
            continue
        elif 35 <= total < 40:
            note_pondere.append(1)
            continue
        elif 40 <= total < 45:
            note_pondere.append(1.3)
            continue
        elif 45 <= total < 50:
            note_pondere.append(1.7)
            continue
        elif 50 <= total < 55:
            note_pondere.append(2)
            continue
        elif 55 <= total < 60:
            note_pondere.append(2.3)
            continue
        elif 60 <= total < 65:
            note_pondere.append(2.7)
            continue
        elif 65 <= total < 70:
            note_pondere.append(3)
            continue
        elif 70 <= total < 75:
            note_pondere.append(3.3)
            continue
        elif 75 <= total < 80:
            note_pondere.append(3.7)
            continue
        elif 80 <= total <= 100:
            note_pondere.append(4)
            continue
        
    return note_pondere

def calculate_stats(ue):
    stats = {}
    type_exams = ['cc', 'tps', 'examen']

    for exam in type_exams:
        stats[exam] = stat(ue, exam)

    return stats

def stat(ue, type_exam):
    eleves = Note.objects.filter(examen=type_exam, code_ue=ue)
    nbr_eleves = eleves.count()
    
    eleves_0_25 = selection(0, 25, eleves, type_exam)
    eleves_25_50 = selection(25, 50, eleves, type_exam)
    eleves_50_75 = selection(50, 75, eleves, type_exam)
    eleves_75_100 = selection(75, 100.01, eleves, type_exam)


    # Pourcentages
    pourcentage_0_25 = "{:.2f}".format((eleves_0_25 / nbr_eleves) * 100) if nbr_eleves > 0 else 'Nan'
    pourcentage_25_50 = "{:.2f}".format((eleves_25_50 / nbr_eleves) * 100) if nbr_eleves > 0 else 'Nan'
    pourcentage_50_75 = "{:.2f}".format((eleves_50_75 / nbr_eleves) * 100) if nbr_eleves > 0 else 'Nan'
    pourcentage_75_100 = "{:.2f}".format((eleves_75_100 / nbr_eleves) * 100) if nbr_eleves > 0 else 'Nan'

    eff = {
        'effectif_0_25': eleves_0_25,
        'effectif_25_50': eleves_25_50,
        'effectif_50_75': eleves_50_75,
        'effectif_75_100': eleves_75_100,
    }
    freq = {
        'range_0_25': pourcentage_0_25,
        'range_25_50': pourcentage_25_50,
        'range_50_75': pourcentage_50_75,
        'range_75_100': pourcentage_75_100,
    }

    return eff, freq



def selection(notemin, notemax, eleves, type_exam):
    compteur = 0
    for eleve in eleves:
        if type_exam == 'cc' and notemin <= (eleve.valeur / 20) * 100 < notemax:
            compteur += 1
        elif type_exam == 'tps' and notemin <= (eleve.valeur / 30) * 100 < notemax:
            compteur += 1
        elif type_exam == 'examen' and notemin <= (eleve.valeur / 50) * 100 < notemax:
            compteur += 1
    
    return compteur