from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, Length, EqualTo

class RegisterForm(FlaskForm):
    username = StringField('Nombre de Usuario', validators=[
        DataRequired(message="El usuario es requerido"),
        Length(min=3, max=20, message="Debe tener entre 3 y 20 caracteres")
    ])
    email = StringField('Correo Electrónico', validators=[
        DataRequired(message="El email es requerido"),
        Email(message="Ingresa un correo válido")
    ])
    password = PasswordField('Contraseña', validators=[
        DataRequired(message="La contraseña es requerida"),
        Length(min=6, message="La contraseña debe tener al menos 6 caracteres")
    ])
    confirm_password = PasswordField('Confirmar Contraseña', validators=[
        DataRequired(),
        EqualTo('password', message="Las contraseñas deben coincidir")
    ])
    submit = SubmitField('Registrarse')

class LoginForm(FlaskForm):
    email = StringField('Correo Electrónico', validators=[DataRequired(), Email()])
    password = PasswordField('Contraseña', validators=[DataRequired()])
    submit = SubmitField('Iniciar Sesión')

class EditProfileForm(FlaskForm):
    username = StringField('Nombre de Usuario', validators=[DataRequired(), Length(min=3, max=20)])
    email = StringField('Correo Electrónico', validators=[DataRequired(), Email()])
    submit = SubmitField('Guardar Cambios')
