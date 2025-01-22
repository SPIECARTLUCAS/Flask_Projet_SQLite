from flask import Flask, render_template_string, render_template, jsonify, request, redirect, url_for, session
from flask import render_template
from flask import json
from urllib.request import urlopen
from werkzeug.utils import secure_filename
import sqlite3

app = Flask(__name__)                                                                                                                  
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'  # Clé secrète pour les sessions

# Fonction pour créer une clé "authentifie" dans la session utilisateur
def est_authentifie():
    return session.get('authentifie')

@app.route('/')
def hello_world():
    return render_template('hello.html') #comm2
@app.route('/biblio')
def page_bibliotheque():
    return render_template('bibliotheque.html')


@app.route('/lecture')
def lecture():
    if not est_authentifie():
        # Rediriger vers la page d'authentification si l'utilisateur n'est pas authentifié
        return redirect(url_for('authentification'))

  # Si l'utilisateur est authentifié
    return "<h2>Bravo, vous êtes authentifié</h2>"

@app.route('/authentification', methods=['GET', 'POST'])
def authentification():
    if request.method == 'POST':
        # Vérifier les identifiants
        if request.form['username'] == 'admin' and request.form['password'] == 'password': # password à cacher par la suite
            session['authentifie'] = True
            # Rediriger vers la route lecture après une authentification réussie
            return redirect(url_for('lecture'))
        else:
            # Afficher un message d'erreur si les identifiants sont incorrects
            return render_template('formulaire_authentification.html', error=True)

    return render_template('formulaire_authentification.html', error=False)

@app.route('/fiche_client/<int:post_id>')
def Readfiche(post_id):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM clients WHERE id = ?', (post_id,))
    data = cursor.fetchall()
    conn.close()
    # Rendre le template HTML et transmettre les données
    return render_template('read_data.html', data=data)

@app.route('/consultation/')
def ReadBDD():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM clients;')
    data = cursor.fetchall()
    conn.close()
    return render_template('read_data.html', data=data)

@app.route('/enregistrer_client', methods=['GET'])
def formulaire_client():
    return render_template('formulaire.html')  # afficher le formulaire*


@app.route('/fiche_nom/', methods=['GET', 'POST'])
def ReadBDD_2():
    nom = request.args.get('nom', '')  # Récupérer le nom passé en paramètre GET ou POST
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    if nom:
        # Recherche spécifique par nom
        cursor.execute('SELECT * FROM clients WHERE nom = ?', (nom,))
    else:
        # Si aucun nom fourni, afficher tous les clients
        cursor.execute('SELECT * FROM clients;')

    data = cursor.fetchall()
    conn.close()

    # Renvoyer les données au template HTML
    return render_template('search_data.html', data=data, nom=nom)


@app.route('/enregistrer_client', methods=['POST'])
def enregistrer_client():
    nom = request.form['nom']
    prenom = request.form['prenom']

    # Connexion à la base de données
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    # Exécution de la requête SQL pour insérer un nouveau client
    cursor.execute('INSERT INTO clients (created, nom, prenom, adresse) VALUES (?, ?, ?, ?)', (1002938, nom, prenom, "ICI"))
    conn.commit()
    conn.close()
    return redirect('/consultation/')  # Rediriger vers la page d'accueil après l'enregistrement
                                                                                                                                       
if __name__ == "__main__":
  app.run(debug=True)

DATABASE = 'bibliotheque.db'

def get_db():
    """Obtenir une connexion à la base de données."""
    if 'db' not in g:
        g.db = sqlite3.connect(DATABASE)
        g.db.row_factory = sqlite3.Row
    return g.db

def close_db(e=None):
    """Fermer la connexion à la base de données."""
    db = g.pop('db', None)
    if db is not None:
        db.close()

def init_db():
    """Initialiser la base de données avec les tables nécessaires."""
    with sqlite3.connect(DATABASE) as conn:
        conn.execute('''
            CREATE TABLE IF NOT EXISTS Livre (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                titre TEXT NOT NULL,
                auteur TEXT NOT NULL,
                genre TEXT,
                disponible INTEGER DEFAULT 1
            )
        ''')
        conn.commit()

def create_app():
    """Créer et configurer l'application Flask."""
    app = Flask(__name__)

    # Initialiser la base de données
    with app.app_context():
        init_db()

    # Route principale : gestion de la bibliothèque
    @app.route('/bibliotheque', methods=['GET', 'POST'])
    def bibliotheque():
        db = get_db()

        # Gérer l'ajout de livres (POST)
        if request.method == 'POST' and 'ajouter_livre' in request.form:
            titre = request.form['titre']
            auteur = request.form['auteur']
            genre = request.form['genre']
            db.execute(
                "INSERT INTO Livre (titre, auteur, genre) VALUES (?, ?, ?)",
                (titre, auteur, genre)
            )
            db.commit()
            return redirect(url_for('bibliotheque'))

        # Gérer la recherche de livres (GET ou POST)
        query = request.form.get('query', '') if request.method == 'POST' else request.args.get('query', '')
        livres = db.execute(
            "SELECT * FROM Livre WHERE titre LIKE ? OR auteur LIKE ?",
            (f'%{query}%', f'%{query}%')
        ).fetchall()

        return render_template('bibliotheque.html', livres=livres, query=query)

    # Enregistrer les gestionnaires de cycle de vie de la base de données
    app.teardown_appcontext(close_db)

    return app
