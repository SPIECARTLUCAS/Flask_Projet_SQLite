-- Table des utilisateurs
DROP TABLE IF EXISTS utilisateurs;
CREATE TABLE utilisateurs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nom TEXT NOT NULL,
    prenom TEXT NOT NULL,
    email TEXT NOT NULL,
    role TEXT NOT NULL CHECK(role IN ('utilisateur', 'administrateur')) -- Rôle de l'utilisateur
);

-- Table des livres
DROP TABLE IF EXISTS livres;
CREATE TABLE livres (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    titre TEXT NOT NULL,
    auteur TEXT NOT NULL
);

-- Table du stock (gestion centralisée du stock des livres)
DROP TABLE IF EXISTS stock;
CREATE TABLE stock (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    livre_id INTEGER NOT NULL,
    quantite INTEGER NOT NULL DEFAULT 0, -- Quantité de livres disponibles
    date_modification TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP, -- Date de modification du stock
    FOREIGN KEY (livre_id) REFERENCES livres(id)
);

-- Table des emprunts
DROP TABLE IF EXISTS emprunts;
CREATE TABLE emprunts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    utilisateur_id INTEGER NOT NULL,
    livre_id INTEGER NOT NULL,
    date_emprunt TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    date_retour_prevue TIMESTAMP NOT NULL, -- Date prévue de retour du livre
    FOREIGN KEY (utilisateur_id) REFERENCES utilisateurs(id),
    FOREIGN KEY (livre_id) REFERENCES livres(id)
);
