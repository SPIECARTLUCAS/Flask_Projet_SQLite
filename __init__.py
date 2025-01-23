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
    
@app.route('/biblio')
def page_bibliotheque():
    return render_template('bibliotheque.html')
    
@app.route('/')
def index():
    livres = Livre.query.all()
    return render_template('index.html', livres=livres)



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

@app.route('/inscription', methods=['GET', 'POST'])
def inscription():
    if request.method == 'POST':
        nom_utilisateur = request.form['nom_utilisateur']
        mot_de_passe = request.form['mot_de_passe']
        
        if Utilisateur.query.filter_by(nom_utilisateur=nom_utilisateur).first():
            flash('Nom d\'utilisateur déjà pris.', 'danger')
            return redirect(url_for('inscription'))

        hash_mdp = generate_password_hash(mot_de_passe)
        nouvel_utilisateur = Utilisateur(nom_utilisateur=nom_utilisateur, mot_de_passe=hash_mdp)
        db.session.add(nouvel_utilisateur)
        db.session.commit()
        flash('Inscription réussie ! Connectez-vous.', 'success')
        return redirect(url_for('connexion'))

    return render_template('inscription.html')

@app.route('/connexion', methods=['GET', 'POST'])
def connexion():
    if request.method == 'POST':
        nom_utilisateur = request.form['nom_utilisateur']
        mot_de_passe = request.form['mot_de_passe']

        utilisateur = Utilisateur.query.filter_by(nom_utilisateur=nom_utilisateur).first()
        if utilisateur and check_password_hash(utilisateur.mot_de_passe, mot_de_passe):
            session['utilisateur_id'] = utilisateur.id
            session['nom_utilisateur'] = utilisateur.nom_utilisateur
            flash('Connexion réussie !', 'success')
            return redirect(url_for('index'))
        else:
            flash('Nom d\'utilisateur ou mot de passe incorrect.', 'danger')

    return render_template('connexion.html')

@app.route('/deconnexion')
def deconnexion():
    session.pop('utilisateur_id', None)
    session.pop('nom_utilisateur', None)
    flash('Vous êtes déconnecté.', 'info')
    return redirect(url_for('index'))

@app.route('/emprunter/<int:livre_id>')
def emprunter_livre(livre_id):
    if 'utilisateur_id' not in session:
        flash('Veuillez vous connecter pour emprunter un livre.', 'warning')
        return redirect(url_for('connexion'))

    livre = Livre.query.get_or_404(livre_id)
    if not livre.disponible:
        flash('Ce livre est déjà emprunté.', 'danger')
    else:
        livre.disponible = False
        db.session.commit()
        flash(f'Vous avez emprunté "{livre.titre}".', 'success')

    return redirect(url_for('index'))

@app.route('/rendre/<int:livre_id>')
def rendre_livre(livre_id):
    if 'utilisateur_id' not in session:
        flash('Veuillez vous connecter pour rendre un livre.', 'warning')
        return redirect(url_for('connexion'))

    livre = Livre.query.get_or_404(livre_id)
    if livre.disponible:
        flash('Ce livre n\'est pas emprunté.', 'danger')
    else:
        livre.disponible = True
        db.session.commit()
        flash(f'Vous avez rendu "{livre.titre}".', 'success')

    return redirect(url_for('index'))
