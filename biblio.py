import sqlite3

# Connexion à la base de données SQLite
connection = sqlite3.connect('bibliotheque.db')

# Création des tables à partir du fichier schema.sql
with open('schema.sql') as f:
    connection.executescript(f.read())

# Initialisation des données de la table Livre
cur = connection.cursor()

cur.execute("INSERT INTO Livre (titre, auteur, genre) VALUES (?, ?, ?)",
            ('Le Petit Prince', 'Antoine de Saint-Exupéry', 'Fiction'))
cur.execute("INSERT INTO Livre (titre, auteur, genre) VALUES (?, ?, ?)",
            ('1984', 'George Orwell', 'Dystopie'))
cur.execute("INSERT INTO Livre (titre, auteur, genre) VALUES (?, ?, ?)",
            ('Les Misérables', 'Victor Hugo', 'Classique'))
cur.execute("INSERT INTO Livre (titre, auteur, genre) VALUES (?, ?, ?)",
            ('L\'Étranger', 'Albert Camus', 'Philosophie'))
cur.execute("INSERT INTO Livre (titre, auteur, genre) VALUES (?, ?, ?)",
            ('Harry Potter à l\'école des sorciers', 'J.K. Rowling', 'Fantasy'))
cur.execute("INSERT INTO Livre (titre, auteur, genre) VALUES (?, ?, ?)",
            ('Le Seigneur des Anneaux', 'J.R.R. Tolkien', 'Fantasy'))

# Sauvegarder les changements et fermer la connexion
connection.commit()
connection.close()

print("Base de données initialisée avec succès.")
