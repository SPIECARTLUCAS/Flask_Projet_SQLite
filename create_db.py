import sqlite3

# Connexion à la base de données SQLite (elle sera créée si elle n'existe pas)
connection = sqlite3.connect('database.db')

# Création du curseur
cursor = connection.cursor()

# Création de la table livres
cursor.execute('''
    CREATE TABLE IF NOT EXISTS livres (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        titre TEXT NOT NULL,
        auteur TEXT NOT NULL
    );
''')

# Création de la table utilisateurs
cursor.execute('''
    CREATE TABLE IF NOT EXISTS utilisateurs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nom TEXT NOT NULL,
        prenom TEXT NOT NULL,
        email TEXT NOT NULL UNIQUE,
        role TEXT NOT NULL
    );
''')

# Création de la table stock (pour gérer les exemplaires des livres)
cursor.execute('''
    CREATE TABLE IF NOT EXISTS stock (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        livre_id INTEGER NOT NULL,
        exemplaire_id INTEGER NOT NULL,
        FOREIGN KEY (livre_id) REFERENCES livres(id)
    );
''')

# Création de la table emprunts
cursor.execute('''
    CREATE TABLE IF NOT EXISTS emprunts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        utilisateur_id INTEGER NOT NULL,
        livre_id INTEGER NOT NULL,
        date_emprunt TEXT NOT NULL,
        date_retour_prevue TEXT NOT NULL,
        FOREIGN KEY (utilisateur_id) REFERENCES utilisateurs(id),
        FOREIGN KEY (livre_id) REFERENCES livres(id)
    );
''')

# Insertion de quelques livres dans la table livres
cursor.execute("INSERT INTO livres (titre, auteur) VALUES (?, ?)", ('Les Misérables', 'Victor Hugo'))
cursor.execute("INSERT INTO livres (titre, auteur) VALUES (?, ?)", ('1984', 'George Orwell'))
cursor.execute("INSERT INTO livres (titre, auteur) VALUES (?, ?)", ('Le Petit Prince', 'Antoine de Saint-Exupéry'))

# Insertion de quelques utilisateurs dans la table utilisateurs
cursor.execute("INSERT INTO utilisateurs (nom, prenom, email, role) VALUES (?, ?, ?, ?)", 
               ('DUPONT', 'Emilie', 'emilie.dupont@example.com', 'administrateur'))
cursor.execute("INSERT INTO utilisateurs (nom, prenom, email, role) VALUES (?, ?, ?, ?)", 
               ('LEROUX', 'Lucas', 'lucas.leroux@example.com', 'utilisateur'))
cursor.execute("INSERT INTO utilisateurs (nom, prenom, email, role) VALUES (?, ?, ?, ?)", 
               ('MARTIN', 'Amandine', 'amandine.martin@example.com', 'utilisateur'))

# Insertion de quelques exemplaires dans la table stock
cursor.execute("INSERT INTO stock (livre_id, exemplaire_id) VALUES (?, ?)", (1, 1))
cursor.execute("INSERT INTO stock (livre_id, exemplaire_id) VALUES (?, ?)", (1, 2))
cursor.execute("INSERT INTO stock (livre_id, exemplaire_id) VALUES (?, ?)", (2, 1))
cursor.execute("INSERT INTO stock (livre_id, exemplaire_id) VALUES (?, ?)", (3, 1))
cursor.execute("INSERT INTO stock (livre_id, exemplaire_id) VALUES (?, ?)", (3, 2))

# Insertion de quelques emprunts dans la table emprunts
cursor.execute("INSERT INTO emprunts (utilisateur_id, livre_id, date_emprunt, date_retour_prevue) VALUES (?, ?, ?, ?)", 
               (2, 1, '2025-01-20 10:00:00', '2025-02-01 12:00:00'))
cursor.execute("INSERT INTO emprunts (utilisateur_id, livre_id, date_emprunt, date_retour_prevue) VALUES (?, ?, ?, ?)", 
               (3, 3, '2025-01-22 09:00:00', '2025-02-15 12:00:00'))

# Validation des modifications
connection.commit()

# Fermeture de la connexion
connection.close()

print("Les tables et les données ont été créées et insérées avec succès.")
