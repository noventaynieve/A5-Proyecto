from dotenv import load_dotenv
load_dotenv()

from flask import Flask, render_template, redirect, url_for
from flask_wtf import CSRFProtect

from config import Config
from models.user import db
from routes.user_routes import user_bp

app = Flask(__name__)
app.config.from_object(Config)

# Seguridad en cookies
app.config['SESSION_COOKIE_SECURE'] = False
app.config['SESSION_COOKIE_HTTPONLY'] = True

# Inicializar extensiones
csrf = CSRFProtect(app)
db.init_app(app)

# Registrar Blueprint
app.register_blueprint(user_bp)

# Redirección raíz
@app.route('/')
def index():
    return redirect(url_for('users.login'))

# Manejadores de errores HTTP
@app.errorhandler(401)
def unauthorized(e):
    return render_template('401.html'), 401

@app.errorhandler(403)
def forbidden(e):
    return render_template('403.html'), 403

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

# Crear tablas si no existen
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True, port=8000)
