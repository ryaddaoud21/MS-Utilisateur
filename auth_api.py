from flask import Flask
from API.auth import auth_blueprint
from API.models import db
from API.config import Config

# Initialisation de l'application Flask
app = Flask(__name__)
app.config.from_object(Config)

# Initialisation de la base de données
db.init_app(app)

# Enregistrement du blueprint pour l'authentification
app.register_blueprint(auth_blueprint)

# Route d'accueil
@app.route('/')
def home():
    return {"message": "Bienvenue dans le service d'authentification !"}

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5004)