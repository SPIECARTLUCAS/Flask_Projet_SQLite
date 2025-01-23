from flask import Flask, render_template, request, redirect
import sqlite3

# Initialiser l'application Flask
app = Flask(__name__)

# Définir la route pour la page /welcome
@app.route('/index')
def index():
    return render_template('index.html')  # Rend le fichier HTML dans le dossier templates


# Définir la route pour afficher le formulaire d'enregistrement/suppression des livres
@app.route('/formulaire_livre', methods=['GET'])
def formulaire_livre():
    return render_template('formulaire_livre.html')  # afficher le formulaire

# Définir la route pour enregistrer un livre
@app.route('/formulaire_livre', methods=['POST'])
def enregistrer_livre():
    titre = request.form['titre']
    auteur = request.form['auteur']

@app.route('/recherche_livre/')
def ReadBDD():
    conn = sqlite3.connect('database.db')  # Corrigé : sqlite3
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM livres') # Exécution de la requête SQL pour récupérer les données
    data = cursor.fetchall()
    conn.close()  # Fermeture de la connexion à la base de données
    return render_template('data.html', data=data) # Rendu de la page HTML avec les données extraites


# Démarrer l'application Flask
if __name__ == "__main__":
    app.run(debug=True)
