"""Modulo en donde se desarrolla el servidor."""

import json
import logging

from bson import json_util
from datetime import datetime
from flask import Flask, request, Response, render_template
from flask_weasyprint import HTML, render_pdf


from app.code.get_status import FAILED, OK
from app.db.users import User
from app.db.guys import Guy


app = Flask(__name__)
userManager = User()
guys_manager = Guy()
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


@app.route('/')
def index():
    """Ruta que devuelve el index."""
    return render_template('index.html')


@app.route('/login')
def login():
    """Ruta que devuelve el index."""
    return render_template('login.html')


@app.route('/sign_up')
def sign_up():
    """Ruta que devuelve el index."""
    return render_template('sign_up.html')


@app.route('/search')
def search():
    return render_template('busqueda.html')


@app.route('/folio')
def folio():
    return render_template('folio.html')


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
            grade = request.form['grade']
            email = request.form['email']
            addrees = request.form['dir']
            tel = request.form['tel']
            tel2 = request.form['tel2']
            if name and guardian and birthday and gender and age and curp and grade and email and addrees and tel:
                dt = datetime.now()
                identifier = f"{dt.strftime('%Y%m')}{curp[4:10]}{curp[0:4]}"
                guy = json_util.loads(json_util.dumps(guys_manager.get_guy(identifier)))
                guys = json_util.loads(json_util.dumps(guys_manager.get_guys()))
                print(len(guys))
                print(len(guy))
                if len(guys) <= 50:
                    if len(guy) == 0:
                        html = render_template(
                            'folio.html',
                            folio=identifier,
                            name=name,
                            tutor=guardian,
                            date=birthday,
                            genere=gender,
                            age=age,
                            curp=curp,
                            grade=grade,
                            email=email,
                            addrees=addrees,
                            tel=tel,
                            tel2=tel2,
                            alert="Registro exitoso con folio:"
                        )
                        if guys_manager.set_guy(
                            folio=identifier,
                            name=name,
                            guardian=guardian,
                            birthday=birthday,
                            gender=gender,
                            age=age,
                            curp=curp,
                            grade=grade,
                            email=email,
                            addrees=addrees,
                            tel=tel,
                            tel2=tel2,
                        ):
                            return render_pdf(HTML(string=html))
                    else:
                        return render_template('register.html', alert='El niño ya se encuentra registrado')
                else:
                    return render_template('register.html', alert='Cupo lleno')
    except Exception as e:
        logger.exception(e)
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


@app.route('/update_guy', methods=['POST'])
def update_guy():
    if request.method == 'POST':
        folio = request.form['folio']
        name = request.form['nomb']
        guardian = request.form['nombTutor']
        birthday = request.form['trip-start']
        gender = request.form['hm']
        age = request.form['edad']
        curp = request.form['curp']
        grade = request.form['grade']
        email = request.form['email']
        addrees = request.form['dir']
        tel = request.form['tel']
        tel2 = request.form['tel2']
        if folio and name and guardian and birthday and gender and age and curp and grade and email and addrees and tel:
            html = render_template(
                        'folio.html',
                        folio=folio,
                        name=name,
                        tutor=guardian,
                        date=birthday,
                        genere=gender,
                        age=age,
                        curp=curp,
                        grade=grade,
                        email=email,
                        addrees=addrees,
                        tel=tel,
                        tel2=tel2,
                        alert="Datos actualizados correctamente")
            if guys_manager.update_guy(
                folio=folio,
                name=name,
                guardian=guardian,
                birthday=birthday,
                gender=gender,
                age=age, curp=curp,
                grade=grade,
                email=email,
                addrees=addrees,
                tel=tel,
                tel2=tel2):
                return render_pdf(HTML(string=html))
        return Response(
            json.dumps(
                {
                    'message': 'No created, incorrect data body',
                },
            ),
                status=FAILED,
                mimetype='application/json',
            )
