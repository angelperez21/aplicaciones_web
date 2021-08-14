"""Modulo en donde se desarrolla el servidor."""

import json

from bson import json_util
from datetime import datetime
from flask import Flask, request, Response, render_template

from app.code.get_status import FAILED, OK
from app.db.users import User
from app.db.guys import Guy


app = Flask(__name__)
userManager = User()
guys_manager = Guy()


@app.route('/')
def index():
    """Ruta que devuelve el index."""
    return render_template('index.html')



@app.route('/sign_up')
def sign_up():
    """Ruta que devuelve el index."""
    return render_template('sign_up.html')


@app.route('/search')
def search():
   return render_template('busqueda.html')

@app.route('/validation', methods=['POST'])
def validation():
    try:
        if request.method == 'POST':
            user_page = request.form['email']
            passwd_page = request.form['passwd']
            email_db = json_util.loads(
                json_util.dumps(
                    userManager.find_user(user_page),
                ),
            )
        if len(email_db):
            email_dict = email_db[0]
            return (
                render_template('register.html')
                if email_dict['passwd'] == passwd_page
                else render_template('index.html', alert='Contraseña incorrecta')
            )
        else:
            return render_template('index.html', alert='Correo no encontrado')
    except Exception:
        return Response(
                json.dumps(
                    {
                        'message': 'Not found',
                    },
                ),
                status=FAILED,
                mimetype='application/json',
            )


@app.route('/insert_user', methods=['POST'])
def insert_user():
    if request.method == 'POST':
        user = request.form['user']
        email = request.form['email']
        passwd = request.form['passwd']
        passwd1 = request.form['passwd1']
        if passwd == passwd1:
            # Almacenamos al usuario en nuestra DB
            responseDB = userManager.insert_user(user, email, passwd)
            if responseDB:
                return render_template(
                    'index.html',
                    successful='Registro exitoso, por favor incie sesión',
                )
            else:
                return render_template(
                    'index.html',
                    alert='Error al registrar el usuario, revise su información',
                )
        else:
            return render_template('sign_up.html', alert='Contraseñas distintas')


@app.route('/save_guy', methods=['POST'])
def save_guy():
    """Ruta para realizar el registro en la DB de MongoDB
    Returns:
    return a dict
    """
    try:
        if request.method == 'POST':
            name = request.form['nomb']
            guardian = request.form['nombTutor']
            birthday = request.form['trip-start']
            gender = request.form['hm']
            age = request.form['edad']
            curp = request.form['curp']
            if name and guardian and birthday and gender and age and curp:
                dt = datetime.now()
                identifier = f"{dt.strftime('%d%m%Y%')}{curp[0:10]}"
                guy = guys_manager.get_guy(identifier)
                guys = guys_manager.get_guys()
                if len(guys) < 50:
                    if guy == 0:
                        if guys_manager.set_guy(folio=identifier, name=name, guardian=guardian, birthday=birthday, gender=gender, age=age, curp=curp):
                            return render_template('busqueda.html', folio=identifier)
                return render_template('register.html', alert='Cupo lleno')
    except Exception:
        return Response(
                json.dumps(
                    {
                        'message': 'No created, incorrect data body',
                    },
                ),
                status=FAILED,
                mimetype='application/json',
            )


@app.route('/search_guy', methods=['POST'])
def search_guy():
    """Ruta para realizar el registro en la DB de MongoDB
    Returns:
    return a dict
    """
    if request.method == 'POST':
        folio = request.json.get('folio')
        guy = json_util.loads(json_util.dumps(guys_manager.get_guy(folio)))
        if guy:
            return Response(
                json.dumps(
                    {
                        'guy': guy,
                    },
                ),
                status=OK,
                mimetype='application/json',
            )
        return Response(
                    json.dumps(
                        {
                            'guy': [],
                        },
                    ),
                    status=FAILED,
                    mimetype='application/json',
                )