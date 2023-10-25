-- Création de la table "etudiant"
CREATE TABLE public.etudiant (
    matricule VARCHAR(10) PRIMARY KEY,
    nom VARCHAR(255),
    prenom VARCHAR(255),
    email VARCHAR(255),
    sexe CHAR(1),
    mot_de_passe VARCHAR(255),
    filiere VARCHAR(255),
    niveau CHAR(2),
    statut VARCHAR(255)
);

-- Création de la table "enseignant"
CREATE TABLE public.enseignant (
    matricule_en VARCHAR(20) PRIMARY KEY,
    nom VARCHAR(255),
    prenom VARCHAR(255),
    email VARCHAR(255),
    sexe CHAR(1),
    mot_de_passe_ensei VARCHAR(255)
);

-- Création de la table "document"
CREATE TABLE public.document (
    id_doc INT AUTO_INCREMENT PRIMARY KEY,
    titre VARCHAR(255),
    date_doc DATE,
    type_doc VARCHAR(255),
    matricule VARCHAR(10),
    matricule_en VARCHAR(20),
    FOREIGN KEY (matricule) REFERENCES etudiant(matricule),
    FOREIGN KEY (matricule_en) REFERENCES enseignant(matricule_en)
);

-- Création de la table "annonce"
CREATE TABLE public.annonce (
    id_ann INT AUTO_INCREMENT PRIMARY KEY,
    texte TEXT,
    date_pub DATE,
    categorie VARCHAR(255),
    titre VARCHAR(255),
    matricule VARCHAR(10),
    matricule_en VARCHAR(20),
    FOREIGN KEY (matricule) REFERENCES etudiant(matricule),
    FOREIGN KEY (matricule_en) REFERENCES enseignant(matricule_en)
);

-- Création de la table "note"
CREATE TABLE public.note (
    id_note INT AUTO_INCREMENT PRIMARY KEY,
    examen VARCHAR(255),
    valeur DECIMAL(5, 2),
    date_fin DATE,
    date_deb DATE,
    matricule VARCHAR(10),
    matricule_en VARCHAR(20),
    code_ue VARCHAR(10),
    FOREIGN KEY (matricule) REFERENCES etudiant(matricule),
    FOREIGN KEY (matricule_en) REFERENCES enseignant(matricule_en),
    FOREIGN KEY (code_ue) REFERENCES ue(code_ue)
);

-- Création de la table "ue"
CREATE TABLE public.ue (
    code_ue VARCHAR(10) PRIMARY KEY,
    nom VARCHAR(255),
    credit INT,
    matricule_en VARCHAR(20),
    FOREIGN KEY (matricule_en) REFERENCES enseignant(matricule_en)
);

-- Création de la table "agenda"
CREATE TABLE public.agenda (
    id_ag INT AUTO_INCREMENT PRIMARY KEY,
    titre VARCHAR(255),
    date_deb_ag DATETIME,
    date_fin DATETIME,
    note VARCHAR(255),
    matricule VARCHAR(10),
    matricule_en VARCHAR(20),
    FOREIGN KEY (matricule) REFERENCES etudiant(matricule),
    FOREIGN KEY (matricule_en) REFERENCES enseignant(matricule_en)
);

-- Création de la table "profil_etu"
CREATE TABLE public.profil_etu (
    id_prof INT AUTO_INCREMENT PRIMARY KEY,
    mgp DECIMAL(5, 2),
    matricule VARCHAR(10),
    FOREIGN KEY (matricule) REFERENCES etudiant(matricule)
);

-- Création de la table "profil_ens"
CREATE TABLE public.profil_ens (
    id_pr_en INT AUTO_INCREMENT PRIMARY KEY,
    matricule_en VARCHAR(20),
    FOREIGN KEY (matricule_en) REFERENCES enseignant(matricule_en)
);
